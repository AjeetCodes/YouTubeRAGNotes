import os
from django.shortcuts import render
from django.http import HttpResponse
import json
from django.conf import settings
from markdown import markdown
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

# # Gemini API
# # Free, double-check pricing https://ai.google.dev/pricing
import google.generativeai as genai

# # ChromaDB
import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv
# Create your views here.
class YouTubeNotes:
    def getYouTubeNotes(self, request):
        if request.method == "GET":
            return render(request, 'youtube_notes/index.html')
        else:
            body = request.POST
            youtube_id = body.get('youtube_id')
            if not youtube_id:
                return render(request, 'youtube_notes/index.html', {"error" : "Field is required.", "youtube_id" :  youtube_id})
            load_dotenv()
            # Set up resources

            GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
            genai.configure(api_key=GEMINI_API_KEY)
            # Instantiate Gemini model
            # Model choices: https://ai.google.dev/gemini-api/docs/models/gemini
            genai_model = genai.GenerativeModel('models/gemini-1.5-flash')
            # Load the vector database, if it exists, otherwise create new on first run
            chroma_client = chromadb.PersistentClient(path="my_chromadb")
            # Select an embedding function.
            # Embedding Function choices:https://docs.trychroma.com/guides/embeddings#custom-embedding-functions
            gemini_ef  = embedding_functions.GoogleGenerativeAiEmbeddingFunction(api_key=GEMINI_API_KEY)
            # Load collection, if it exists, otherwise create new on first run. Specify the model that we want to use to do the embedding.
            chroma_collection = chroma_client.get_or_create_collection(name='youtube_notes', embedding_function=gemini_ef)

            # INPUTS:

            # Adjust prompt as needed
            prompt = "Extract key notes from video transcript: "

            # Extract Transcript

            # Reference: https://github.com/jdepoix/youtube-transcript-api
            transcript = YouTubeTranscriptApi.get_transcript(youtube_id, languages=['en','en-US','en-GB'])
            transcript = TextFormatter().format_transcript(transcript)

            public_folder_path = os.path.join(settings.BASE_DIR, 'public')
            if not os.path.exists(public_folder_path):
                os.makedirs(public_folder_path)
            temp_ts_file_path = os.path.join(public_folder_path, 'temp_ts.txt')
            with open(temp_ts_file_path, "w") as file:
                file.write(transcript)
            # https://ai.google.dev/api/generate-content

            # Generate Notes
            response = genai_model.generate_content(prompt + transcript, stream=False)
            temp_notes_file_path = os.path.join(public_folder_path, 'temp_notes.txt')
            with open(temp_notes_file_path, "w") as file:
                file.write(response.text)

            # save notes 
            with open(temp_notes_file_path, "r") as file:
                notes = file.read()
            # Insert, if record doesn't exist, otherwise update existing record
            # https://docs.trychroma.com/reference/py-collection#upsert
            chroma_collection.upsert(
                documents=[notes],
                ids=[youtube_id]
            )

            # Validation
            result = chroma_collection.get(youtube_id, include=['documents'])
            # print(result)
            content = result['documents'][0]
            html = self.convertMarkdownToHtml(content)
            # print(html)
            return render(request, 'youtube_notes/index.html', {"notes" : html, "youtube_id" :  youtube_id})
    
    def convertMarkdownToHtml(self, content):
        html = markdown(content)
        return html
    def searchQuery(self, request):
        if request.method == "GET":
            return render(request, 'youtube_notes/query.html')
        else:
            query = request.POST.get('query') 
            if not query:
                return render(request, 'youtube_notes/query.html', {"error" : "Field is required."})
            
            load_dotenv()
            # Set up resources

            GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
            genai.configure(api_key=GEMINI_API_KEY)
            # Instantiate Gemini model
            # Model choices: https://ai.google.dev/gemini-api/docs/models/gemini
            genai_model = genai.GenerativeModel('models/gemini-1.5-flash')
            # Load the vector database, if it exists, otherwise create new on first run
            chroma_client = chromadb.PersistentClient(path="my_chromadb")
            # Select an embedding function.
            # Embedding Function choices:https://docs.trychroma.com/guides/embeddings#custom-embedding-functions
            gemini_ef  = embedding_functions.GoogleGenerativeAiEmbeddingFunction(api_key=GEMINI_API_KEY)
            # Load collection, if it exists, otherwise create new on first run. Specify the model that we want to use to do the embedding.
            chroma_collection = chroma_client.get_or_create_collection(name='youtube_notes', embedding_function=gemini_ef)

            try:
                # Validation
                result = chroma_collection.query(
                    query_texts=query,
                    n_results=3,
                    include=["documents"]
                )
                documents = result['documents']
                # print(documents)
                for content in documents:
                    content = content[0]
                # print(content)
                prompt = "Answer the following QUESTION using DOCUMENT as context."
                prompt += f"QUESTION: {query}"
                prompt += f"DOCUMENT: {content}"
                genai_model = genai.GenerativeModel('models/gemini-1.5-flash')
                response = genai_model.generate_content(prompt, stream=False)
                # Extract and format the answer
                answer = response.text
            except (AttributeError, IndexError):
                answer = "No valid response received from the AI model."
            return render(request, 'youtube_notes/query.html', {"query_results": answer})
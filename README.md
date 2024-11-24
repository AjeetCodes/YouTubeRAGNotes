# YouTube RAG Chat App

Welcome to the YouTube RAG Chat App! This application is designed to create detailed notes from YouTube videos and allow you to query them using a powerful vector database like ChromaDB. It's a great tool for extracting key insights and having intelligent conversations based on video content.

## Features

- **YouTube Video Note Creation:**  
  Extracts and generates notes from any YouTube video based on its content.
  
- **Vector Database (ChromaDB):**  
  Stores the notes in ChromaDB, which allows for efficient and fast retrieval of relevant information based on your queries.

- **Query-Based Information Retrieval:**  
  Provides a chat-based interface where you can query the notes, and it fetches relevant answers from the database.

## Tech Stack

- **Django:** For building the backend and serving the application.
- **ChromaDB:** A vector database used for storing and querying notes.
- **YouTube API:** For retrieving video data and generating notes.
- **Python Libraries:** NumPy, Pandas for data processing.

## Installation

To set up the project locally, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/AjeetCodes/YouTubeRAGNotes.git
    ```

2. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up environment variables:
    - Make sure to create a `.env` file and set any necessary environment variables, such as YouTube API keys and database configurations.

4. Run the Django server:
    ```bash
    python manage.py runserver
    ```

Your app should now be running locally.

## How It Works

1. **Input a YouTube Video ID:**  
   You provide the ID of a YouTube video, and the app extracts the video content, processes it, and generates notes.

2. **Store Notes in ChromaDB:**  
   The generated notes are stored in a vector database (ChromaDB), which indexes them for fast retrieval.

3. **Query for Answers:**  
   You can query the stored notes, and the system will return the most relevant information based on your question.

## Example Usage

- **Create Notes:**  
  Enter a YouTube video ID, and the app will generate and store notes from the video.

- **Query Notes:**  
  Ask questions related to the content of the video, and the app will provide accurate answers based on the stored notes.

## Contributing

Feel free to fork this repository, make changes, and create pull requests. Contributions are always welcome!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

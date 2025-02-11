# Cricket Web Bot

## Overview
The **Cricket Web Bot** is a Flask-based chatbot that can answer cricket-related queries by generating and executing SQL queries on an SQLite database. It integrates with Hugging Face's Inference API and a Gradio-hosted SQL query generator to process user queries efficiently.

## Features
- Retrieves cricket team rankings based on user queries.
- Fetches all-rounder statistics from the database.
- Processes match and innings-related queries.
- Uses LLMs (Hugging Face Inference API) for query interpretation and response generation.
- Implements a Flask API for interaction.

## Technologies Used
- **Python** (Flask, SQLAlchemy, Hugging Face Inference API)
- **SQLite** (Database for storing cricket stats)
- **Gradio Client** (For SQL query generation)
- **Flask-CORS** (For enabling cross-origin requests)

## Installation
### Prerequisites
Ensure you have the following installed:
- Python 3.x
- SQLite

### Setup
1. Clone this repository:
   ```sh
   git clone https://github.com/your-repo/cricket-web-bot.git
   cd cricket-web-bot
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Set environment variables for Hugging Face API:
   ```sh
   export HF_API_KEY='your_huggingface_api_key'
   export HF_MODEL_NAME='your_huggingface_model_name'
   ```
4. Run the application:
   ```sh
   python app.py
   ```

## API Endpoints
### `POST /ask-question`
Handles chat queries and returns relevant cricket-related information.

#### Request Body:
```json
{
  "question": "Show ODI rankings"
}
```

#### Response:
```json
{
  "answer": "India is ranked #1 in ODI rankings."
}
```

## Usage
### Interactive Mode
You can interact with the bot using the command-line interface:
```sh
python app.py
```
Example Queries:
- "Show ODI rankings"
- "Show stats of Kohli"
- "Show all-rounder stats"

## Contributing
1. Fork the repository.
2. Create a new branch: `git checkout -b feature-branch`
3. Commit your changes: `git commit -m "Add new feature"`
4. Push to the branch: `git push origin feature-branch`
5. Open a pull request.

## License
This project is licensed under the MIT License.


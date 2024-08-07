
# Project Name
This FastAPI project integrates language models and image processing to provide customer support in selecting website templates.

## Technologies Used
- **FastAPI**: A modern, fast (high-performance) web framework for building APIs with Python 3.11+ based on standard Python type hints.
- **Langchain**: A framework for chaining language models and other components to create complex conversational applications.
- **OpenAI GPT-4**: Utilized for natural language understanding and generation, offering sophisticated conversational capabilities.

## Installation

### Prerequisites
- Python 3.11+ installed on your machine. You can download it from [python.org](https://www.python.org/downloads/).
- Pip: Python's package installer. It comes installed with Python if you're using Python 3.4 or later.

### Steps to Install
1. **Clone the Repository**:
   - First, clone the repository to your local machine using the command:
     ```bash
     git clone https://github.com/hungson175/PageTemplateRecommendation.git
     cd project
     ```

2. **Create a Virtual Environment** (Recommended):
   - It's a good practice to create a virtual environment to manage dependencies for the project separately. You can create one using:
     ```bash
     python -m venv env
     ```
   - Activate the virtual environment:
     - On Windows:
       ```bash
       .\env\Scripts\activate
       ```
     - On macOS and Linux:
       ```bash
       source env/bin/activate
       ```

3. **Install Dependencies**:
   - Install all the required packages using `pip` from the `requirements.txt` file:
     ```bash
     pip install -r requirements.txt
     ```

### Environment Variables
- You need to set up environment variables before running the application:
  - File`.env` contains the variable `OPENAI_API_KEY`.
  - Ensure the `.env` file is in the root directory of your project.

### Running the Server
- Once all dependencies are installed and the environment variables are set, you can start the server by running:
  ```bash
  uvicorn main:app --reload
  ```
  This command will start the FastAPI server with live reloading enabled, making it easy to develop and test your application.

## Next Steps
- With your environment set up and running, you're ready to explore the API functionalities as detailed in the API Usage section above using Postman or any other API client.

## API Usage with Postman
### Setup
1. Install Postman on your device.
2. Start your FastAPI server locally by running `uvicorn main:app --reload` in your terminal.
3. Open Postman and set up your environment:
   - Create a new environment and add the variable `base_url` with the value `http://127.0.0.1:8000`.

### Interacting with the APIs
#### Start a Conversation
- **Endpoint**: `GET /start-conversation`
- **Method**: GET
- **Description**: Initiates a new conversation, clearing any existing chat history.

**Example Request**:
```plaintext
{{base_url}}/start-conversation
```
**Example Response**:
```json
{
  "response_code": 0,
  "message": "Initial greeting from the bot..."
}
```

#### Send a Customer Message
- **Endpoint**: `POST /customer-message`
- **Method**: POST
- **Body**: `{"content": "Your message here"}`
- **Description**: Sends a customer message to the server and receives a basic acknowledgment.

**Example Request**:
```plaintext
{{base_url}}/customer-message
```
**Body**:
```json
{
  "content": "Hi, I need help choosing a template."
}
```
**Example Response**:
```json
{
  "response_code": 0,
  "message": "Received: Your message here"
}
```

#### Chat with the Bot
- **Endpoint**: `POST /chat-with-bot`
- **Method**: POST
- **Body**: `{"content": "Your conversation input here"}`
- **Description**: Sends user input to the bot and gets a response based on the conversation context.

**Example Request**:
```plaintext
{{base_url}}/chat-with-bot
```
**Body**:
```json
{
  "content": "Can you show me some professional templates?"
}
```
**Example Response**:
```json
{
  "response_code": 0,
  "message": "Bot's response based on the conversation logic..."
}
```

#### Extract Information from Uploaded Image
- **Endpoint**: `POST /extract-image-info`
- **Method**: POST
- **Body**: `{"url": "URL of the image to analyze"}`
- **Description**: Analyzes the image at the provided URL and extracts relevant template information.

**Example Request**:
```plaintext
{{base_url}}/extract-image-info
```
**Body**:
```json
{
  "url": "http://example.com/image.jpg"
}
```
**Example Response**:
```json
{
  "response_code": 0,
  "message": "Extracted information from the image..."
}
```

### Retrieving Chat History
- **Endpoint**: `GET /history`
- **Method**: GET
- **Description**: Retrieves the entire chat history from the current session.

**Example Request**:
```plaintext
{{base_url}}/history
```
**Example Response**:
```json
{
  "response_code": 0,
  "message": "List of all messages in the chat..."
}
```

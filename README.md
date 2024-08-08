
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
- Should always be called first, or to reset the conversation

**Example Request**:
```plaintext
{{base_url}}/start-conversation
```
**Example Response**:
```json
{
    "response_code": 0,
    "message": {
        "question": "Hi",
        "chat_history": [
            {
                "content": "Hi",
                "additional_kwargs": {},
                "response_metadata": {},
                "type": "human",
                "name": null,
                "id": null,
                "example": false
            },
            {
                "content": "Hey there! What do you have in mind for your website?",
                "additional_kwargs": {},
                "response_metadata": {},
                "type": "ai",
                "name": null,
                "id": null,
                "example": false,
                "tool_calls": [],
                "invalid_tool_calls": [],
                "usage_metadata": null
            }
        ],
        "text": "Hey there! What do you have in mind for your website?"
    }
}
```
Note: you only have to pay attention the last line "text". It is the response of the bot
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
	"content": "I want to sell online clothing"
}
```
**Example Response**:
```json
{
    "response_code": 0,
    "message": "That sounds great! Are you looking for a specific type of page, like a Home page, Product page, or Collection page?"
}
```

#### Extract Information from Uploaded Image
- **Endpoint**: `POST /extract-image-info`
- **Method**: POST
- **Body**: `{"url": "Local file path of the image - only support local file right now"}`
- **Description**: Analyzes the image at the provided URL and extracts relevant template information.

**Example Request**:
```plaintext
{{base_url}}/extract-image-info
```
**Body**:
```json
{
    "url": "/user/some_user/assets/template_hiut_denim.png"
}
```
**Example Response**:
```json
{
    "response_code": 0,
    "message": {
        "summary": "This website template is designed for a denim clothing brand, showcasing a blend of lifestyle imagery and product displays. It emphasizes a clean and modern aesthetic, making it suitable for brands focused on quality and craftsmanship in apparel. The layout encourages easy navigation and highlights key product offerings.",
        "page-type": [
            "Home page",
            "Product page"
        ],
        "style": [
            "Minimalist",
            "Professional"
        ],
        "industry": [
            "Clothing"
        ]
    }
}
```

#### Extracting Information from Chat History

- **Endpoint**: `/extract-chat-info`
- **Method**: POST
- **Description**: Analyzes the accumulated chat history to extract key information about the user's preferences regarding page type, style, and industry, which are crucial for template selection.

#### Request
This endpoint does not require any parameters or data to be sent in the body of the request, as it operates directly on the stored chat history.

**Usage with Postman**:
1. Ensure your API is up and running as instructed in the "Running the Server" section.
2. Open Postman and select the "POST" method from the dropdown menu.
3. Enter the endpoint URL:
   ```plaintext
   {{base_url}}/extract-chat-info
   ```
4. Since this endpoint does not require a body, you can directly send the request.

**Example Response**:
Upon success, the server responds with extracted information categorized by page type, style, and industry, which assists in selecting the appropriate website template. Here's what the response might look like:

```json
{
  "response_code": 0,
  "message": {
    "summary": "The customer is looking for a professional and minimalistic design for their new clothing brand.",
    "page-type": ["Home page", "Product page"],
    "style": ["Professional", "Minimalist"],
    "industry": ["Clothing"]
  }
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

## Chat flow example:
1. **Start a conversation:**
   - `GET /start-conversation`
2. **Chat with the bot:**
   - `POST /chat-with-bot` with content: "I want to sell online clothing"
3. **Extract information from an uploaded image:**
   - `POST /extract-image-info`
4. **Chat with the bot:**
   - `POST /chat-with-bot` with content: "Summarize the uploaded website image so I can be sure you understand it correctly"
   - `POST /chat-with-bot` with content: "Any more suggestions ?"
5. **Extract information from chat history:**
   - `POST /extract-chat-info`


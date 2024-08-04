import os

from fastapi import FastAPI
from langchain.chains.conversation.base import ConversationChain
from langchain.memory import ConversationBufferWindowMemory
from pydantic import BaseModel
import openai
from dotenv import load_dotenv
import datetime
from langchain_openai import ChatOpenAI

# Get the current date
current_date = datetime.datetime.now().date()
# Define the date after which the model should be set to "gpt-3.5-turbo"
target_date = datetime.date(2024, 7, 31)

# Set the model variable based on the current date
if current_date > target_date:
    llm_model = "gpt-3.5-turbo"
else:
    llm_model = "gpt-3.5-turbo-0301"
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
# create a chat with memory
memory = ConversationBufferWindowMemory(k=10)
llm = ChatOpenAI(temperature=0.1, model=llm_model,)
conversation = ConversationChain(llm=llm, memory=memory, verbose=True)

app = FastAPI()


class Message(BaseModel):
    content: str


@app.get("/start-conversation")
async def start_conversation():
    # reset the memory
    memory.clear()
    print(f"Memory after clear: \n```{memory.buffer}```")

    return {"response_code": 0,
            "message": "Hello ! I will help you to make a great shopify page. What do you need help with?"}


@app.post("/customer-message")
async def customer_message(user_input: Message):
    response_message = "Received: " + user_input.content
    recommended_templates = ["template1", "template2", "template3"]
    return {
        "response_code": 0,
        "message": response_message,
        "templates": recommended_templates
    }


@app.post("/chat-with-bot")
async def chat_with_bot(user_input: Message):
    rep = conversation.invoke(user_input.content)

    return {
        "response_code": 0,
        "message": rep["response"],
    }
@app.get("/history")
async def get_history():
    return {
        "response_code": 0,
        "message": memory.buffer,
    }
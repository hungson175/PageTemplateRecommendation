import os

import dotenv

from fastapi import FastAPI
from langchain.chains.conversation.base import ConversationChain
from langchain.chains.llm import LLMChain
from langchain.memory import ConversationBufferWindowMemory, ConversationBufferMemory
from langchain_core.messages import AIMessage
from langchain_core.prompts import (
    ChatPromptTemplate, SystemMessagePromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate)
from pydantic import BaseModel
import openai
from dotenv import load_dotenv
import datetime
from langchain_openai import ChatOpenAI
from tools.open_ai_tools import get_image_response
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
# create a chat with memory
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)  # Chat model , not completion
system_message = """
As an online customer service representative at ShopifyCreator, your role is to assist customers in selecting the right template from our templates store. During interactions, you should gather the following details:

- Page Type: Identify the needed page types, which could include 'About Us', 'Landing', 'Contact', 'Home', 'Product', 'Collection', 'Blog Post', 'Password', and 'Advertorial' pages.
- Style: Determine the desired template style(s), such as 'Cheerful', 'Elegant', 'Energetic', 'Luxury', 'Minimalist', 'Professional', or 'Spooky'.
- Industry: Clarify the industry category applicable to the template. Options include 'Art & Crafts', 'Books, Music & Videos', 'Clothing', 'Electronics', 'Food & Drink', 'Hardware & Automotive', 'Health & Beauty', 'Home & Decor', 'Jewelry & Accessories', 'Pet Supplies', 'Service', 'Sports & Recreation', 'Baby & Kids', 'Outdoors & Gardening', or 'Other'.
- Additional Information: Extract any other relevant information from the conversation that might aid in selecting the appropriate template.
The first one or 2 questions should not too formal, it should be something like "What do you have in mind ?" or "What are you looking for ?" - and then you can ask more specific questions to get more details
"""
system_prompt = ChatPromptTemplate(
    messages=[
        SystemMessagePromptTemplate.from_template(
            system_message
        ),
        # The `variable_name` here is what must align with memory
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{question}")
    ]
)

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
conversation = LLMChain(
    llm=llm,
    prompt=system_prompt,
    verbose=True,
    memory=memory,
)
memory.clear()
app = FastAPI()


class Message(BaseModel):
    content: str


class Image(BaseModel):
    url: str


def extract_categories_from_content(extractor_message_template: str, func):
    summary_schema = ResponseSchema(
        name="summary",
        type="str",
        description="""Summary of the content (image/text...), 
        focus on helping to choose a website template base on the content""",
    )
    type_schema = ResponseSchema(
        name="page-type",
        type="list[str]",
        description="""One or more of the following Page Types: About us page, Landing page,
        Contact page, Home page, Product page, Collection page, Blog post page, Password page, 
        Advertorial page""",
    )
    style_schema = ResponseSchema(
        name="style",
        type="list[str]",
        description="""One or more of following Style categories: Cheerful, Elegant, Energetic, 
        Luxury, Minimalist, Professional, Spooky""",
    )
    industry_schema = ResponseSchema(
        name="industry",
        type="list[str]",
        description="""One or more of following Industry categories: Art & crafts, Books, 
        music & videos, Clothing, Electronics, Food & drink, Hardware & automotive, 
        Health & beauty, Home & decor, Jewelry & accessories, Pet supplies, Service, 
        Sports & recreation, Baby & kids, Outdoors & gardening, Other""",
    )
    response_schema = [summary_schema, type_schema, style_schema, industry_schema]

    output_parser = StructuredOutputParser.from_response_schemas(response_schema)

    format_instruction = output_parser.get_format_instructions()
    extractor_prompt = ChatPromptTemplate.from_template(extractor_message_template)

    input_message = extractor_prompt.format_messages(
        format_instruction=format_instruction
    )
    print("Input message: ", input_message)
    response_message = func(input_message[0].content)
    print("Response message: ", response_message)
    formated_response = output_parser.parse(response_message)
    return {
        "response_code": 0,
        "message": formated_response,
    }


@app.get("/start-conversation")
async def start_conversation():
    # reset the memory
    memory.clear()
    print(f"Memory after clear: \n```{memory.buffer}```")
    greeting_message = conversation({"question": "Hi"})
    return {"response_code": 0,
            "message": greeting_message}


@app.post("/customer-message")
async def customer_message(user_input: Message):
    response_message = "Received: " + user_input.content
    return {
        "response_code": 0,
        "message": response_message,
    }


@app.post("/chat-with-bot")
async def chat_with_bot(user_input: Message):
    rep = conversation({"question": user_input.content})

    return {
        "response_code": 0,
        "message": rep["text"],
    }


@app.get("/history")
async def get_history():
    return {
        "response_code": 0,
        "message": memory.buffer,
    }


@app.post("/extract-image-info")
async def extract_image_info(image: Image):
    message_template_str = """\
    Act as e-commerce expert extract the following information from the image:
    - summary
    - page-type
    - style
    - industry
    {format_instruction}
    """
    formatted_response_message = extract_categories_from_content(message_template_str,
                                                                 lambda extractor_input_message: get_image_response(
                                                                     image_path=image.url,
                                                                     message=extractor_input_message))
    conversation({"question": f""" This is the information extracted from the uploaded image by user: 
    >>>> EXTRACTED INFORMATION FROM UPLOADED IMAGE <<<<
    ```
    {formatted_response_message.__str__().replace("{", "{{").replace("}", "}}")}
    ```
    """})
    return formatted_response_message


@app.post("/extract-chat-info")
async def extract_chat_info():
    message_template_str = """\
    Act as e-commerce expert and extract the following information from the chat history:
    - summary
    - page-type
    - style
    - industry

    >>>> FORMAT INSTRUCTION <<<<
    format_instruction

    >>>> CHAT HISTORY <<<<
    {chat_history}
    """
    message_template = ChatPromptTemplate.from_template(message_template_str)
    extractor_message = message_template.format_messages(
        chat_history=memory.buffer
    )
    extractor_template_str = extractor_message[0].content.replace("format_instruction", "{format_instruction}")
    print("Extractor template: ", extractor_template_str)
    formatted_response_message = extract_categories_from_content(extractor_template_str,
                                                                 lambda extractor_input_message: conversation(
                                                                     {"question": extractor_input_message})["text"])
    return formatted_response_message

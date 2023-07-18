import os
from dotenv import load_dotenv, find_dotenv
from langchain.chat_models import AzureChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage



ENV_FILE = find_dotenv()
load_dotenv(ENV_FILE) # find_dotenv is called automatically


llm = AzureChatOpenAI(
    openai_api_key=os.environ["OPENAI_API_KEY"],
    openai_api_base=os.environ["OPENAI_API_BASE"],
    deployment_name=os.environ["CHAT_ENGINE"]
    ) # type: ignore

llm.temperature = 0

messages = [
    SystemMessage(
        content="You are a helpful assistant."
    ),
    HumanMessage(
        content="Hi Jarvis, how are you today?"
    ),
    AIMessage(content="My name is Jarvis, how may I assist you today?"),
]


def ai_response(message: str):
    messages.append(HumanMessage(content=message))
    return llm(messages=messages).content

if __name__ == "__main__":
    # print(llm("Tell me a joke"))
    ai_response("Who was Donald Trump")

"""
If necessary adjust the model parameters
llm.temperature = 0.8
llm.top_p = 1
"""
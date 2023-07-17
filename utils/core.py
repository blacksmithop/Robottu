import os
# Import Azure OpenAI
from langchain.llms import AzureOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv, find_dotenv


ENV_FILE = find_dotenv()
load_dotenv(ENV_FILE) # find_dotenv is called automatically


llm = AzureOpenAI(
    openai_api_key=os.environ["OPENAI_API_KEY"],
    openai_api_base=os.environ["OPENAI_API_BASE"],
    openai_api_version=os.environ["OPENAI_API_VERSION"],
    deployment_name=os.environ["COMPLETION_ENGINE"]
    ) # type: ignore

llm.temperature = 0.2

openai_template = """
Message: ```{input}```
You are a conversational partner. Respond to the message in triple backticks
"""

prompt = PromptTemplate(input_variables=["input"], template=openai_template)
OpenAiLLM = LLMChain(llm=llm, prompt=prompt, output_key="output")  


def ai_response(message: str):
    return OpenAiLLM.run(message)

# if __name__ == "__main__":
#     print(llm("Tell me a joke"))

"""
If necessary adjust the model parameters
llm.temperature = 0.8
llm.top_p = 1
"""
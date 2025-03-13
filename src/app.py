from dotenv import load_dotenv

load_dotenv()

from interface import AudioInterface
from agents import AssistantAgent
from tools import get_free_slots_tool, get_price_tool, create_event_tool
from langchain_anthropic import ChatAnthropic


SYSTEM_PROMPT = """Today's date is Monday, February 26, 2025. 
You are Sofia, from AwesomeHairdresser and you're a helpful hairdresser. Your job is to book and cancel customer appointments.
First ask the customer's name. After he introduces him self, ask what is he looking for.
Use the provided tools to search for price services, checking existing appointment and booking new ones.
When asking a question, dont provide explainations on why you're asking that. Be kind, polite and provide short and concice answers.
Answer the customer with the date and time of the appointment, and after that, provide duration the service.
Provide the price of the service in euros only at the end of the conversation, before customer confirmation.
If he agrees, them book it.
Responses must be in english, not another language.
"""

# Define the llm
model = ChatAnthropic(model="claude-3-7-sonnet-latest", temperature=0)


# Define the tools to be used by the model
tools = [get_free_slots_tool(), get_price_tool, create_event_tool()]

# The hairdresser agent needs a model, a set of tools and a prompt
hairdresser_agent = AssistantAgent(llm=model, tools=tools, system_prompt=SYSTEM_PROMPT)

# Audio interface to capture microphone voice, extract transcripts, and syntetize speech from text
interface = AudioInterface()

while True:
    text = interface.listen()
    response = hairdresser_agent.run(text)
    interface.speak(response)


from langgraph.graph import  StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_anthropic import ChatAnthropic
from typing import Annotated 
from typing_extensions import TypedDict 
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.checkpoint.memory import MemorySaver

class State(TypedDict):
    messages: Annotated[list, add_messages]

class ChatbotAgent:

    def __init__(self) -> None:
                
        # Initialize llm 
        self.llm = ChatAnthropic(model="claude-3-7-sonnet-latest", temperature=0)

        # Initialize the (state) graph
        graph_builder = StateGraph(State)
        
        # Add the chatbot node
        graph_builder.add_node("chatbot", self.chatbot)

        # Set entry and finish points
        graph_builder.add_edge(START, "chatbot")
        graph_builder.add_edge("chatbot", END)

        # Adding memory
        memory = MemorySaver()

        self.config = {"configurable": {"thread_id": "1"}}

        # Compile the graph
        self.graph = graph_builder.compile(checkpointer=memory)



    # Define the chatbot function
    def chatbot(self, state: State):
        return {"messages": [self.llm.invoke(state["messages"])]}

    # Run the graph with human input
    def run(self, user_input):
        messages = [HumanMessage(content=user_input)]
        result = self.graph.invoke({"messages": messages}, self.config)
        return result['messages'][-1].content
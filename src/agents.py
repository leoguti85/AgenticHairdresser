from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator
from langchain_core.messages import (
    AnyMessage,
    SystemMessage,
    HumanMessage,
    ToolMessage,
)
from langgraph.checkpoint.memory import MemorySaver


class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]


class AssistantAgent:
    def __init__(self, llm, tools, system_prompt) -> None:
        self.system = system_prompt

        # Initialize the state graph
        graph = StateGraph(AgentState)

        graph.add_node("llm", self.call_antrophic)
        graph.add_node("action", self.take_action)

        graph.add_edge("action", "llm")
        graph.add_conditional_edges(
            "llm", self.exists_action, {True: "action", False: END}
        )

        # Adding memory
        memory = MemorySaver()
        self.config = {"configurable": {"thread_id": "1"}}

        # Adding entrypoint
        graph.set_entry_point("llm")
        self.graph = graph.compile(checkpointer=memory)

        # Making aware the model has tools

        self.tools = {t.name: t for t in tools}
        self.llm = llm.bind_tools(tools)

    def call_antrophic(self, state: AgentState):
        messages = state["messages"]
        if self.system:
            messages = [SystemMessage(content=self.system)] + messages

        message = self.llm.invoke(messages)
        print(f"{message.content}\n")
        return {"messages": [message]}

    def take_action(self, state: AgentState):
        tool_calls = state["messages"][-1].tool_calls
        results = []
        for t in tool_calls:
            print(f"Calling: {t}")

            result = self.tools[t["name"]].invoke(t["args"])
            results.append(
                ToolMessage(tool_call_id=t["id"], name=t["name"], content=str(result))
            )
        print("Back to the llm!")
        return {"messages": results}

    def exists_action(self, state: AgentState):
        result = state["messages"][-1]
        return len(result.tool_calls) > 0

    # Run the graph with human input
    def run(self, user_input):
        messages = [HumanMessage(content=user_input)]
        result = self.graph.invoke({"messages": messages}, self.config)
        return result["messages"][-1].content

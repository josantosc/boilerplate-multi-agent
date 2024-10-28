from typing import Annotated, Sequence
from typing_extensions import TypedDict

from langgraph.prebuilt import tools_condition
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END, START
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage
from langgraph.prebuilt import ToolNode

from app.generator.medical_generator import generate_response, validate_questions
from app.retriever.medical_retriver import retriever_tool, rewrite_query


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]


def agent(state, tools):
    messages = state["messages"]
    model = ChatOpenAI(temperature=0, streaming=True, model="gpt-4-turbo")
    model = model.bind_tools(tools)
    response = model.invoke(messages)
    return {"messages": [response]}


def create_workflow(llm):
    tools = [retriever_tool]
    workflow = StateGraph(AgentState)
    workflow.add_node("agent", lambda state: {"messages": llm.bind_tools(tools).invoke(state['messages'])})
    retrieve = ToolNode([retriever_tool])
    workflow.add_node("retrieve", retrieve)
    workflow.add_node("rewrite", rewrite_query)
    workflow.add_node("generate", generate_response)

    workflow.add_edge(START, "agent")
    workflow.add_conditional_edges("agent", tools_condition, {"tools": "retrieve", END: END})
    workflow.add_conditional_edges("retrieve", validate_questions)
    workflow.add_edge("generate", END)
    workflow.add_edge("rewrite", "agent")

    return workflow.compile()


def agent_rag(message, thread_id, llm):
    graph = create_workflow(llm)
    inputs = {"messages": [("user", message)]}
    config = {"configurable": {"thread_id": thread_id}}
    response = graph.invoke(input=inputs, config=config)
    data = response['messages'][-1].content
    return data

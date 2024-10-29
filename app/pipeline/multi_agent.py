import uuid
from typing import Annotated, Sequence
from typing_extensions import TypedDict

from langgraph.prebuilt import tools_condition
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END, START, MessagesState
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode

from app.generator.medical_generator import generate_response, validate_questions
from app.retriever.medical_retriver import retriever_tool, rewrite_query, feedback_user


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]


llm = ChatOpenAI(temperature=0, streaming=True, model="gpt-4-turbo")

tools = [retriever_tool]


def agent(state):
    messages = state["messages"]
    last_massage = messages[-1].content
    model = llm.bind_tools(tools)
    response = model.invoke(last_massage)
    return {"messages": [response]}


def is_iamessage(state):
    messages = state["messages"]
    last_message = messages[-1].content
    if not last_message:
        return "retrieve"
    return "feedback_user"


def create_workflow():
    workflow = StateGraph(MessagesState)
    workflow.add_node("agent", agent)
    retrieve = ToolNode([retriever_tool])
    workflow.add_node("retrieve", retrieve)
    workflow.add_node("rewrite", rewrite_query)
    workflow.add_node("generate", generate_response)
    workflow.add_node("feedback_user", feedback_user)

    workflow.add_edge(START, "agent")
    workflow.add_conditional_edges("agent", tools_condition, {"tools": "retrieve", END: END})
    workflow.add_conditional_edges("agent", is_iamessage,
                                   {"retrieve": "retrieve", "feedback_user": "feedback_user", END: END})
    workflow.add_conditional_edges("retrieve", validate_questions)
    workflow.add_edge("generate", "feedback_user")
    workflow.add_edge("feedback_user", END)
    workflow.add_edge("rewrite", "agent")

    memory = MemorySaver()

    return workflow.compile(checkpointer=memory, debug=True)


def agent_rag(message, thread_id: str):
    graph = create_workflow()

    if not thread_id:
        thread_id = uuid.UUID
    config = {"configurable": {"thread_id": thread_id}}
    inputs = {"messages": [HumanMessage(content=message)]}
    data = ''
    for event in graph.stream(input=inputs, config=config, stream_mode="values"):
        data = event["messages"][-1].content
    return data

from langchain.tools.retriever import create_retriever_tool
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

from app.data_preparation.medical_data import retriever

retriever_tool = create_retriever_tool(
    retriever,
    "retrieve",
    "Search and return relevant information about the healthcare field",
)


def rewrite_query(state):
    messages = state["messages"]
    if len(state["messages"]) >= 6:
        return state

    question = messages[0].content
    msg = [
        HumanMessage(content=f"""
        \n Look at the input and try to reason about the underlying semantic intent / meaning.
        \n Here is the initial question:
        \n -------
        \n {question}
        \n -------
        \n Formulate an improved question:
        """)
    ]

    model = ChatOpenAI(temperature=0, model="gpt-4-0125-preview", streaming=True)
    response = model.invoke(msg)
    return {"messages": [response]}


def feedback_user(state):
    messages = state["messages"]
    question = messages[0].content
    answer = messages[-1].content

    msg = [
        HumanMessage(content=f"""
          \nObserve a pergunta e o contexto, tente raciocinar sobre a intenção/significado semântico subjacente.
          \n Aqui está o contexto: {answer}
          \n Aqui está a pergunta do usuário: {question}
          \n Formule uma resposta melhorada sem alucinação, entre 10 a 50 tokens, reposta concisa e sempre traduza para português do brasil:
           """)
    ]

    model = ChatOpenAI(temperature=0, model="gpt-4-0125-preview", streaming=True)
    response = model.invoke(msg)
    return {"messages": [response]}

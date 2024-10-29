from typing import Literal

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from pydantic import BaseModel, Field

from app.data_preparation.medical_data import manager


def validate_questions(state) -> Literal["generate", "rewrite", "__end__"]:
    class Score(BaseModel):
        binary_score: str = Field(description="A pergunta do usuário é relevante 'sim' ou 'não'")

    model = ChatOpenAI(temperature=0, model="gpt-4-0125-preview", streaming=True)
    llm_with_tool = model.with_structured_output(Score)
    prompt = PromptTemplate(
        template="""Você é um avaliador avaliando a relevância da pergunta de um usuário.
        \n Aqui está o documento recuperado: \n\n {context} \n\n 
        Aqui está a pergunta do usuário: {question}
        \n Se o documento contiver palavra(s)-chave ou significado semântico relacionado à pergunta do usuário, classifique a pergunta como relevante.
        \n Dê uma pontuação binária 'sim' ou 'não' para indicar se a pergunta é relevante.""",
        input_variables=["context", "question"]
    )

    chain = prompt | llm_with_tool
    messages = state["messages"]
    last_message = messages[-1]
    question = messages[0].content
    docs = last_message.content
    scored_result = chain.invoke({"question": question, "context": docs})
    score = scored_result.binary_score

    if score == "sim":
        manager.add_texts([question, docs])
        return "generate"
    else:
        return "rewrite"


def generate_response(state):
    messages = state["messages"]
    question = messages[0].content
    last_message = messages[-1]
    docs = last_message.content

    prompt = PromptTemplate(
        template="""Você é um assistente para tarefas de resposta a perguntas.
                    Use os seguintes partes de contexto recuperado para responder à pergunta.
                    Se você não sabe a resposta, apenas diga que não sabe.
                    Use no máximo três frases e mantenha a resposta concisa.""",
        input_variables=["context", "question"]
    )

    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, streaming=True)

    rag_chain = prompt | llm | StrOutputParser()
    response = rag_chain.invoke({"context": docs, "question": question})
    return {"messages": [response]}

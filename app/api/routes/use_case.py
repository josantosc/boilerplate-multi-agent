import json
import logging
from typing import Optional, Annotated

from fastapi import APIRouter, Path, Query
from app.pipeline.multi_agent import agent_rag


router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/medical_agent", summary="MedQuAD com RAG (Retrieval-Augmented Generation)",
             description="Este endpoint permite testes rápidos de um sistema multiagente projetado para responder a questões sobre "
                         "doenças e tratamentos médicos. Ele utiliza o dataset MedQuAD-MedicalQnADataset como base de conhecimento "
                         "para aprimorar as capacidades do modelo de linguagem (LLM) por meio da técnica RAG (Retrieval-Augmented Generation).",

             )
async def medical_agent(*,
                        message: str = Query(description="O texto da consulta médica enviado pelo usuário. Este campo é obrigatório e serve como entrada."),
                        thread: Annotated[str | None, Query(description="Um identificador opcional para a conversa ou sessão. Este campo é usado para manter o contexto de interações anteriores")] = None):
    response = agent_rag(message, thread)
    return {"message": response}

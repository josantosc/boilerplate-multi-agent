import json
import logging
from typing import Optional

from fastapi import APIRouter, HTTPException, Request, Response
from app.pipeline.multi_agent import agent_rag
from app.utils.agent.worflow_function import extract_message_data, get_thread_info, update_thread_info
from app.utils.whatsapp import WhatsApp
from app.core.config import settings
from app.utils.whatsapp.process_message import process_message

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/",summary="Verificação de Webhook",
            description="Endpoint para verificação do webhook utilizando token")
def verify(request: Request):
    try:
        if request.query_params['hub.mode'] and request.query_params['hub.verify_token']:
            if request.query_params['hub.mode'] == 'subscribe' and request.query_params[
                'hub.verify_token'] == settings.VERYFY_TOKEN:
                print('WEBHOOK_VERIFIED')
                return Response(content=request.query_params['hub.challenge'], status_code=200)
            else:
                return Response(content='verify token requerido ', status_code=403)
    except:
        print('NO VERIFY')
        return Response(content='verify token requerido', status_code=403)


@router.post("/",  summary="Webhook para processamento de mensagens",
             description="Recebe mensagens da API do WhatsApp, processa e envia respostas.",

             )
async def webhook(request: Request):
    try:
        body = await request.json()
        message_data, status = await extract_message_data(body)

        if status:
            return {"status": status}
        if not message_data:
            raise HTTPException(status_code=400, detail="Invalid or missing message data")

        sender_id, phone_number_id, text = message_data["sender_id"], message_data["phone_number_id"], message_data[
            "text"]
        logger.info(f"MESSAGE USER: {text}")

        whatsapp = WhatsApp(token=settings.WHATSAPP_TOKEN, phone_number_id=phone_number_id)
        thread_info = get_thread_info(sender_id)

        response = process_message(thread_info, text, sender_id, whatsapp)

        return {"message": response, "status": 200}

    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Malformed JSON or empty body")
    except Exception as e:
        logger.error(f"Failed to send notification: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to send notification: {str(e)}")


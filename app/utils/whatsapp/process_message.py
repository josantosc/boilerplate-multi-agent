from app.adapters.openai_api.openai_services import handle_response
from app.pipeline.multi_agent import agent_rag
from app.utils.agent.worflow_function import update_thread_info


def process_message(thread_info, text, sender_id, whatsapp):
    if not thread_info:
        thread_id = update_thread_info(sender_id=sender_id)
        response = agent_rag(text, thread_id)
    else:
        response = agent_rag(text, thread_info['thread_id'])
    data_response = {"type": "text", "content": response}
    handle_response(whatsapp, sender_id, data_response)
    return response

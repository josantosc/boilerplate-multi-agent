import logging
from json import dumps
from datetime import datetime

import redis

from app.core.config import settings

logger = logging.getLogger(__name__)


def open_connection():
    redis_url = "redis://"
    if settings.REDIS_PASSWORD:
        redis_url += f":{settings.REDIS_PASSWORD}@"

    redis_url += f"{settings.REDIS_HOST}:{settings.REDIS_PORT}/0"
    return redis.Redis.from_url(redis_url, decode_responses=True, encoding="utf8")


redis_pool = open_connection()


def set_event(sender_id, thread_info):
    with open_connection() as pool:
        try:
            expiration_delta = datetime.fromisoformat(thread_info['expiration_time']) - datetime.utcnow()
            expiration_seconds = int(expiration_delta.total_seconds())
            key = f"thread:{sender_id}"
            event_data = pool.setex(key, expiration_seconds, dumps(thread_info))
            return event_data
        except redis.RedisError as e:
            print(f"Erro ao setar o evento: {e}")
            return None


def delete_event(sender_id):
    with open_connection() as pool:
        try:
            key = f"thread:{sender_id}"
            event_data = pool.delete(key)
            return event_data
        except redis.RedisError as e:
            print(f"Erro ao deletar o evento: {e}")
            return None


def get_event(sender_id):
    with open_connection() as pool:
        try:
            key = f"thread:{sender_id}"
            open_connection().info()
            event_data = pool.getex(key)
            return event_data
        except redis.RedisError as e:
            print(f"Erro ao obter o evento: {e}")
            return None


def purge_queue(queue: str) -> bool:
    return redis_pool.delete(f"{settings.APPLICATION_NAME}-{queue}")


def stop_task(task_id):
    with open_connection() as pool:
        try:
            key = f'task:{task_id}:stopped, true'
            return pool.set(key, '1')
        except redis.RedisError as e:
            print(f"Error when pausing task: {e}")
            return None


def resume_task(task_id):
    with open_connection() as pool:
        try:
            key = f'task:{task_id}:stopped, true'
            return pool.delete(key)
        except redis.RedisError as e:
            print(f"Error resuming task: {e}")
            return None

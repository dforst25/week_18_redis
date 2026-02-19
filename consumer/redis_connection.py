import os
import redis

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB = int(os.getenv("REDIS_DB", "0"))


class RedisManager:
    def __init__(self):
        self.config = {
            "host": os.getenv("REDIS_HOST", "localhost"),
            "port": int(os.getenv("REDIS_PORT", "6379")),
            "db": int(os.getenv("REDIS_DB", "0")),
            "decode_responses": True
        }
        self.client = None

    def check_connection(self):
        if self.client:
            self.client.ping()

    def get_client(self):
        if self.client:
            self.check_connection()
            return self.client
        try:
            self.client = redis.Redis(**self.config)
            self.check_connection()
            return self.client
        except Exception as e:
            raise ConnectionError(f"Failed to create a redis connection: {str(e)}")

    def pop_alert(self, queue: str):
        client = self.get_client()
        alert_data = client.rpop(queue)
        return alert_data



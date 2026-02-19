from datetime import datetime
from redis_connection import RedisManager
from mongo_connection import MongoConnection
import json


def main():
    redis_cnx = RedisManager()
    mongo_cnx = MongoConnection()
    print("waiting for alerts...")
    while True:
        alert = redis_cnx.pop_alert('urgent_queue')
        if alert is None:
            alert = redis_cnx.pop_alert('normal_queue')
        if alert is None:
            continue
        alert_json_format = json.loads(alert)
        print(f"Got an {alert_json_format['priority']} alert:")
        alert_json_format["insertion_time"] = datetime.now()
        alert_json_format["timestamp"] = datetime.strptime(alert_json_format["timestamp"], "%Y-%m-%dT%H:%M:%S.%f")
        print(f"insertion_time: {alert_json_format['insertion_time']}")
        mongo_cnx.insert_alert(alert_json_format)


if __name__ == "__main__":
    main()

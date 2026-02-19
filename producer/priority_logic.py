import json
from redis_connection import RedisManager


def load_json_to_list(json_path: json) -> list[json]:
    with open(json_path, 'r') as file:
        json_list = json.load(file)
    return json_list


def get_priority(alert):
    people_count = alert.get('people_count', 2)
    distance_from_fence_m = alert.get('distance_from_fence_m', 151)
    vehicle_type = alert.get('vehicle_type')
    if alert.get('weapons_count', 0) > 0 \
            or distance_from_fence_m <= 50 \
            or people_count >= 8 \
            or vehicle_type == 'truck' \
            or (people_count >= 4 and distance_from_fence_m <= 150) \
            or (people_count >= 3 and vehicle_type == "jeep"):
        return 'URGENT'
    else:
        return 'NORMAL'


def process_alert(alert, redis: RedisManager):
    priority = get_priority(alert)
    alert['priority'] = priority
    redis.push_alert(alert_data=alert, queue=f"{priority.lower()}_queue")

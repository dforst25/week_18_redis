from priority_logic import *


def main():
    redis_cnx = RedisManager()
    alerts_list = load_json_to_list('../data/border_alerts.json')
    for alert in alerts_list:
        process_alert(alert, redis_cnx)


if __name__ == "__main__":
    main()

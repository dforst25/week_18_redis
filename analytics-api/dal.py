from redis_connection import RedisManager
from mongo_connection import MongoConnection


def get_border_and_priority_analytics():
    redis_cnx = RedisManager()
    route_data = redis_cnx.get_data(route_num='2')
    if route_data:
        return route_data
    else:
        mongo_cnx = MongoConnection()
        collection = mongo_cnx.get_collection()
        route_data = collection.aggregate([
            {
                "$group": {'border': "$border", 'priority': '$priority', 'count_events': {'$count': '$_id'}}
            },
            {
                "$sort": {"priority": -1, "count_events": -1}
            }
        ]).to_list()
        route = {
            'data': route_data
        }
        redis_cnx.insert_route_data(route, '2')
        if route_data:
            return route
        else:
            return None


def get_5_top_urgent_zones():
    redis_cnx = RedisManager()
    route_data = redis_cnx.get_data(route_num='1')
    if route_data:
        return route_data
    else:
        mongo_cnx = MongoConnection()
        collection = mongo_cnx.get_collection()
        route_data = collection.aggregate([
            {
                "$match": {'$priority': 'URGENT'}
            },
            {
                "$group": {'border': "$border", 'count_events': {'$count': '$_id'}}
            },
            {
                "$sort": {"count_events": -1}
            },
            {
                "$limit": 5
            }
        ]).to_list()
        route = {
            "data": route_data
        }
        redis_cnx.insert_route_data(route, '1')
        if route_data:
            return route
        else:
            return None


def get_distance_distribution_analytics():
    redis_cnx = RedisManager()
    route_data = redis_cnx.get_data(route_num='3')
    if route_data:
        return route_data
    else:
        mongo_cnx = MongoConnection()
        collection = mongo_cnx.get_collection()
        route_data = collection.aggregate([
            {
                "$addFields": {
                    '1-300': {'$distance_from_fence_m': {"$le": 300, "$ge": 0}},
                    '301-800': {'$distance_from_fence_m': {"$le": 800, "$ge": 301}},
                    '801-1500': {'$distance_from_fence_m': {"$le": 1500, "$ge": 801}}
                }
            },
            {
                "$project": {'1-300': "$1-300", '301-800': "$301-800", '801-1500': "$801-1500",
                             'count_events': {'$count': '$_id'}}
            },
        ]).to_list()
        route = {
            "data": route_data
        }
        redis_cnx.insert_route_data(route, '3')
        if route_data:
            return route
        else:
            return None


def get_low_visibility_high_activity_analytics():
    return None


def get_hot_zones_analytics():
    return None

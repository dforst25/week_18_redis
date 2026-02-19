from fastapi import APIRouter, HTTPException
import dal

router = APIRouter()


@router.get('/analytics/alerts-by-border-and-priority')
def get_border_and_priority_analytics():
    try:
        return dal.get_border_and_priority_analytics()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get the border and priority analytics:\n{str(e)}")


@router.get('/analytics/top-urgent-zones')
def get_5_top_urgent_zones():
    try:
        return dal.get_5_top_urgent_zones()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get the top urgent zones:\n{str(e)}")


@router.get('/analytics/distance-distribution')
def get_distance_distribution():
    try:
        return dal.get_distance_distribution_analytics()
    except Exception as e:
        raise HTTPException(status_code=409, detail=f"Failed to get distance distribution:\n{str(e)}")


@router.get('/analytics/low-visibility-high-activity')
def get_low_visibility_high_activity_analytics():
    try:
        return dal.get_low_visibility_high_activity_analytics()
    except Exception as e:
        raise HTTPException(status_code=409, detail=f"Failed to get low visibility high activity:\n{str(e)}")


@router.get('/analytics/hot-zones')
def get_hot_zones_analytics():
    try:
        return dal.get_hot_zones_analytics()
    except Exception as e:
        raise HTTPException(status_code=409, detail=f"Failed to get hot zones:\n{str(e)}")
from fastapi import APIRouter

from src.History.History import History
from src.ws.RestApi import RestApi

app = RestApi.get_app()
router = APIRouter(prefix="/history", tags=["history"])

@router.get("/{code}")
def get_history(code: str):
    histories = History.fetch(code)
    if len(histories) == 0:
        return {
            "detail": []
        }

    return {
        "detail": [h.get_json() for h in histories]
    }


RestApi.add_router(router)
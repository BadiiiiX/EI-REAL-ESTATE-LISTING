import uvicorn
from fastapi import FastAPI, APIRouter

class RestApi:
    _instance: "RestApi" = None

    def __init__(self):
        self.app = FastAPI()
        self._routers = []

    @classmethod
    def get_instance(cls) -> "RestApi":
        if cls._instance is None:
            cls._instance = RestApi()
        return cls._instance

    @classmethod
    def get_app(cls) -> FastAPI:
        return cls.get_instance().app

    @classmethod
    def add_router(cls, router: APIRouter):
        print("adding router {}".format(router))
        instance = cls.get_instance()
        instance._routers.append(router)
        instance.get_app().include_router(router)

    @classmethod
    def run(cls, host="127.0.0.1", port=8080, reload=False):
        uvicorn.run(cls.get_app(), host=host, port=port, reload=reload)

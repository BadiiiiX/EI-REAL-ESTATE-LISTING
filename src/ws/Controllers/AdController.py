from glob import glob
import os
from pathlib import Path
from fastapi import APIRouter, HTTPException, UploadFile, File

from src.ws.RestApi import RestApi
from src.Ad.Ad import Ad

app = RestApi.get_app()
router = APIRouter(prefix="/ad", tags=["ad"])

data_path = "src/ws/Controllers/cache"
list_ad = set()

BASE_DIR = Path(__file__).parent
UPLOAD_DIR = BASE_DIR / "cache"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

def __retrieve_add(file_path: str):
    def __is_file_exists(path, file_name):
        path = glob(f"{path}\\*.html")
        for file_path in path:
            if file_name in file_path:
                return True, file_path

        return False, None

    if file_path.endswith(".html"):
        file = file_path.replace(".html", "")

    (result, data) = __is_file_exists(path=data_path, file_name=file_path)
    print(result)
    if result:
        ad = Ad(data)
        list_ad.add(ad)
        print(list_ad)
        return {
            "detail": ad.get_json()
        }
    else :
        raise HTTPException(status_code=404, detail="File not found")

@router.get("/files")
def get_existant_files():

    def __list_files(path):
        files = os.scandir(path)
        print(files)
        parsed_files = []
        for file in files:
            if file.is_file() and file.name.endswith(".html"):
                parsed_files.append(file.name.split(".html")[0])

        return parsed_files

    return {
        "detail": __list_files(path=data_path)
    }

@router.get("/list")
def get_ad_list():
    print(list_ad)
    return {
        "detail": list_ad
    }

@router.get("/{file_id}")
def get_ad_by_id(file_id: str):
    for ad in list_ad:
        if ad.id == file_id:
            return {"detail": ad}

    raise HTTPException(status_code=404, detail="Not Found")

@router.post("/addfile")
def add_file(file: UploadFile = File(...)):
    try:
        contents = file.file.read()
        save_path = UPLOAD_DIR / file.filename
        with open(save_path, 'wb') as f:
            f.write(contents)
    except Exception:
        raise HTTPException(status_code=500, detail='Something went wrong')
    finally:
        file.file.close()

    return __retrieve_add(file_path=save_path.name)


@router.put("/add")
def add_ad(ad):
    print("add {}".format(ad))



RestApi.add_router(router)
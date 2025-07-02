from datetime import date
import requests
from pydantic import BaseModel, constr, confloat, conint, Field, field_validator

from src.History.HistoryParser import HistoryParser
from src.History.Lot import Lot

BASE_URL = "https://dvf-api.data.gouv.fr/dvf"


class History(BaseModel):
    id: constr(min_length=1, strip_whitespace=True)
    date: date
    transaction: constr(strip_whitespace=True, min_length=1)
    price: confloat(ge=0)
    code: conint(ge=10000, le=99999)
    commune: conint(ge=10000, le=99999)
    nom: constr(min_length=1)
    departement: conint(ge=1, le=99)
    lot: list[Lot]
    nature: constr(min_length=1, strip_whitespace=True) = Field(default=None)
    area: confloat(gt=0) = Field(default=None)
    natureCode: constr(min_length=1, max_length=2, strip_whitespace=True) = Field(default=None)
    rooms: conint(ge=0) = Field(default=None)
    houseArea: confloat(gt=0) = Field(default=None)

    def __init__(self, *args, **keywords):
        if args:
            data = args[0]
            super().__init__(**data)
            
    @field_validator("transaction", mode="before")
    def validate_transaction(cls, value):
        value_clean = value.strip().upper().replace(" ", "")
        return value_clean

    @classmethod
    def from_json(cls, data: dict) -> "History":
        return cls.model_construct(**data)

    def get_json(self):
        return {
            "id": self.id,
            "date": self.date.isoformat(),
            "transaction": self.transaction,
            "nom": self.nom,
            "code": self.code,
            "price": self.price,
            "commune": self.commune,
            "departement": self.departement,
            "houseArea": self.houseArea or "N/A",
            "area": self.area or "N/A",
            "rooms": self.rooms or "N/A",
            "nature": self.nature or "N/A",
            "natureCode": self.natureCode or "N/A",
            "lot": [l.get_json() for l in self.lot],
        }

    def __str__(self) -> str:

        def format_lots() -> str:
            if not self.lot:
                return ""
            return "\n" + "\n".join(f"    - {str(lot)}" for lot in self.lot)

        return (
            f"[[{self.id}]] \n"
            f"[{self.date}] {self.transaction} à {self.nom} "
            f"(commune {self.commune}, département {self.departement})\n"
            f"  - Prix : {self.price:.2f} €\n"
            f"  - Surface : {self.area if self.area else 'n/a'} m² "
            f"| Type : {self.nature or 'n/a'} ({self.natureCode or 'n/a'})\n"
            f"  - Bâti : {self.houseArea if self.houseArea else 'n/a'} m² "
            f"| Pièces : {self.rooms if self.rooms else 'n/a'}\n"
            f"  - Lots : {len(self.lot)}"
            f"{format_lots()}"
        )

    @staticmethod
    def retrieve(postal_code: str) -> list[dict]:
        base_url = BASE_URL
        params = {
            "com": postal_code
        }

        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json().get("data")

            return data

        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la requête : {e}")
            return list()

    @staticmethod
    def fetch(postal_code: str | int) -> list | None:
        data = History.retrieve(postal_code)
        if not data:
            return list()

        histories = list()

        for item in data:
            history_data = HistoryParser(item).get_data()
            histories.append(History(history_data))

        return histories

from pathlib import Path
from pydantic import BaseModel, confloat, conint, constr

from src.Ad.Parser import Parser

class Ad(BaseModel):
    id: constr(min_length=1)
    price: confloat(ge=0)
    area: confloat(gt=0)
    code: conint(ge=10000, le=99999)
    region: constr(min_length=1, strip_whitespace=True)
    type: constr(min_length=1, strip_whitespace=True)

    def __init__(self, *args, **keywords):
        if args:
            content = ''
            with open(args[0], encoding="utf-8") as f:
                content = f.read()

            file_name = path = Path(args[0])

            parser = Parser(content, file_name.stem)
            data = parser.get_parsed()

            super().__init__(**data)

    @classmethod
    def from_json(cls, data: dict) -> "Ad":
        return cls.model_construct(**data)


    def get_json(self):
        return {
                "id": self.id,
                "type": self.type,
                "price": f"{self.price:.2f}€",
                "area": f"{self.area:.2f}m²",
                "region": f"{self.region}",
                "code": f"{self.code}",
            }

    def __str__(self):
        return f"{self.type} en {self.region} ({self.code}) de {self.area}m² à {self.price}€"

    def __eq__(self, other):
        return isinstance(other, Ad) and self.id == other.id

    def __hash__(self):
        return hash(self.id)
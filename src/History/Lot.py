from pydantic import BaseModel, constr, confloat

class Lot(BaseModel):
    area: confloat(gt=0)
    number: constr(min_length=1, strip_whitespace=True)

    def get_json(self):
        return {
            "area": self.area,
            "number": self.number,
        }

    def __init__(self, *args, **keywords):
        if args:
            super().__init__(**args[0])

    def __str__(self) -> str:
        return f"Lot {self.number} – {self.area} m²"
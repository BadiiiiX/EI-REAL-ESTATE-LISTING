from src.History.Lot import Lot

class HistoryParser:

    def __init__(self, json_value: dict):

        self.actions = [
            {
                "json_name": "id_mutation",
                "dict_name": "id",
                "load_fn": None
            },
            {
                "json_name": "code_postal",
                "dict_name": "code",
                "load_fn": None
            },
            {
                "json_name": "date_mutation",
                "dict_name": "date",
                "load_fn": None
            },
            {
                "json_name": "nature_mutation",
                "dict_name": "transaction",
                "load_fn": "_upper"
            },
            {
                "json_name": "valeur_fonciere",
                "dict_name": "price",
                "load_fn": None
            },
            {
                "json_name": "code_commune",
                "dict_name": "commune",
                "load_fn": None
            },
            {
                "json_name": "nom_commune",
                "dict_name": "nom",
                "load_fn": None
            },
            {
                "json_name": "code_departement",
                "dict_name": "departement",
                "load_fn": None
            },
            {
                "json_name": "nature_culture",
                "dict_name": "nature",
                "load_fn": "_optional"
            },
            {
                "json_name": "surface_terrain",
                "dict_name": "area",
                "load_fn": "_optional"
            },
            {
                "json_name": "code_nature_culture",
                "dict_name": "natureCode",
                "load_fn": "_optional"
            },
            {
                "json_name": "nombre_pieces_principales",
                "dict_name": "rooms",
                "load_fn": "_optional"
            },
            {
                "json_name": "surface_reelle_bati",
                "dict_name": "houseArea",
                "load_fn": "_optional"
            },
            {
                "json_name": "lot",
                "dict_name": "lot",
                "load_fn": "_parse_lot"
            }
        ]

        self.data = {}
        self.content = json_value

        for action in self.actions:
            if action["load_fn"] is not None:
                self.load_function(action)
            else:
                self.parse_action(action)

    def get_data(self):
        return self.data

    def parse_action(self, action):
        self.data[action["dict_name"]] = self.content.get(action["json_name"])

    def load_function(self, action):
        json_name, dict_name, load_fn = action.values()

        method = getattr(self, load_fn, None)
        if not method:
            raise AttributeError

        method(action)
        return None


    def _upper(self, action: dict) -> None:
        json_data: str = self.content.get(action["json_name"])

        self.data[action["dict_name"]] = json_data.upper()


    def _parse_lot(self, action: dict) -> None:
        def get_lot(number: int) -> Lot | None:
            NUMBER_TAG = f"lot{number}_numero"
            AREA_TAG = f"lot{number}_surface_carrez"

            data_number = self.content.get(NUMBER_TAG)
            data_area = self.content.get(AREA_TAG)

            if data_number is None or data_area is None:
                return None

            lot_data = {
                "number": self.content.get(NUMBER_TAG),
                "area": self.content.get(AREA_TAG),
            }

            return Lot(lot_data)

        def define_lots(lots: list[Lot]):
            self.data[action["dict_name"]] = lots

        LOT_COUNT = self.content.get("nombre_lots")

        list_lot = list()

        if LOT_COUNT == 0:
            define_lots(list_lot)

        for i in range(1, 4):
            lot = get_lot(i)
            if lot:
                list_lot.append(lot)

        define_lots(list_lot)

    def _optional(self, action):
        data = self.content.get(action["json_name"])

        if data is not None:
            self.parse_action(action)
import json
from json import JSONEncoder

class Preference:

    # region: 台北市
    # kind: 分租套房
    # pattern: 3房
    # space: 坪數
    def __init__(self, user_id: str, region: str, kind: str, rent_price: int, pattern: str, space: str):
        self.user_id = user_id
        self.region = region
        self.kind = kind
        self.rent_price = rent_price
        self.pattern = pattern
        self.space = space

    def __str__(self):
        return ("user_id: " + str(self.user_id) + "\n" +
        "region: " + str(self.region) + "\n" +
        "kind: " + str(self.kind) + "\n" +
        "rent_price: " + str(self.rent_price) + "\n" +
        "pattern: " + str(self.pattern) + "\n" +
        "space: " + str(self.space))

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

    def sql_insert_field_string(self):
        result_list = ["id"]
        self.region is not None and result_list.append("region")
        self.kind is not None and result_list.append("kind")
        self.rent_price is not None and result_list.append("rent_price")
        self.pattern is not None and result_list.append("pattern")
        self.space is not None and result_list.append("space")
        return ",".join(result_list)


    def sql_insert_value_string(self):
        result_list = [f"{self.user_id}"]
        self.region is not None and result_list.append(f"'{self.region}'")
        self.kind is not None and result_list.append(f"'{self.kind}'")
        self.rent_price is not None and result_list.append(str(self.rent_price))
        self.pattern is not None and result_list.append(f"'{self.pattern}'")
        self.space is not None and result_list.append(f"'{self.space}'")
        return ",".join(result_list)
    
    def on_duplicate_key_update_string(self):
        result_list = []
        self.region is not None and result_list.append(f"region=VALUES(region)")
        self.kind is not None and result_list.append(f"kind=VALUES(kind)")
        self.rent_price is not None and result_list.append(f"rent_price=VALUES(rent_price)")
        self.pattern is not None and result_list.append(f"pattern=VALUES(pattern)")
        self.space is not None and result_list.append(f"space=VALUES(space)")
        return ",".join(result_list)

class PreferenceEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
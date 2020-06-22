import base64

class Subject:

    def __init__(
        self, 
        subject_id: str, 
        name: bytes, 
        region: str, 
        section: str, 
        kind: str, 
        price: str, 
        location: str, 
        sub_type: str, 
        pattern: str, 
        size: str, 
        floor: str, 
        contact_person: str, 
        url: str):
        self.subject_id = subject_id
        self.name = name
        self.region = region
        self.section = section
        self.kind = kind
        self.price = price
        self.location = location
        self.sub_type = sub_type
        self.pattern = pattern      
        self.size = size   
        self.floor = floor 
        self.contact_person = contact_person
        self.url = url

    def __str__(self):
        return ("id: " + str(self.subject_id) + "\n" +
        "name: " + str(self.name) + "\n" + 
        "region: " + str(self.region) + "\n" + 
        "section: " + str(self.section) + "\n" + 
        "kind: " + str(self.kind) + "\n" + 
        "price: " + str(self.price) + "\n" + 
        "location: " + str(self.location) + "\n" + 
        "sub_type: " + str(self.sub_type) + "\n" +
        "pattern: " + str(self.pattern) + "\n" +
        "size: " + str(self.size) + "\n" +
        "floor: " + str(self.floor) + "\n" +
        "contact_person: " + str(self.contact_person) + "\n" +
        "url: " + str(self.url))

    def sql_inset_field_string(self):
        result_list = []
        self.subject_id is not None and result_list.append("subject_id")
        self.name is not None and result_list.append("name")
        self.region is not None and result_list.append("region")
        self.section is not None and result_list.append("section")
        self.kind is not None and result_list.append("kind")
        self.price is not None and result_list.append("price")
        self.location is not None and result_list.append("location")
        self.sub_type is not None and result_list.append("sub_type")
        self.pattern is not None and result_list.append("pattern")
        self.size is not None and result_list.append("size")
        self.floor is not None and result_list.append("floor")
        self.contact_person is not None and result_list.append("contact_person")
        self.url is not None and result_list.append("url")
        return ", ".join(result_list)

    def sql_insert_value_string(self):
        result_list = []
        self.subject_id is not None and result_list.append(f"'{self.subject_id}'")
        # encodedName = base64.b64encode(self.name.encode("UTF-8"))
        self.name is not None and result_list.append(f"'{self.name}''")
        self.region is not None and result_list.append(f"'{self.region}'")
        self.section is not None and result_list.append(f"'{self.section}'")
        self.kind is not None and result_list.append(f"'{self.kind}'")
        self.price is not None and result_list.append(str(self.price))
        self.location is not None and result_list.append(f"'{self.location}'")
        self.sub_type is not None and result_list.append(f"'{self.sub_type}'")
        self.pattern is not None and result_list.append(f"'{self.pattern}'")
        self.size is not None and result_list.append(f"'{self.size}'")
        self.floor is not None and result_list.append(f"'{self.floor}'")
        self.contact_person is not None and result_list.append(f"'{self.contact_person}'")
        self.url is not None and result_list.append(f"'{self.url}'")
        return ",".join(result_list)

    def on_duplicate_key_update_string(self):
        result_list = []
        self.subject_id is not None and result_list.append("subject_id=VALUES(subject_id)")
        self.name is not None and result_list.append("name=VALUES(name)")
        self.region is not None and result_list.append("region=VALUES(region)")
        self.section is not None and result_list.append("section=VALUES(section)")
        self.kind is not None and result_list.append("kind=VALUES(kind)")
        self.price is not None and result_list.append("price=VALUES(price)")
        self.location is not None and result_list.append("location=VALUES(location)")
        self.sub_type is not None and result_list.append("sub_type=VALUES(sub_type)")
        self.pattern is not None and result_list.append("pattern=VALUES(pattern)")
        self.size is not None and result_list.append("size=VALUES(size)")
        self.floor is not None and result_list.append("floor=VALUES(floor)")
        self.contact_person is not None and result_list.append("contact_person=VALUES(contact_person)")
        self.url is not None and result_list.append("url=VALUES(url)")
        return ",".join(result_list)

    def query_condition_string(self):
        result_list = []
        self.region is not '' and result_list.append(f"AND region = '{self.region}'")
        self.section is not '' and result_list.append(f"AND section = '{self.section}'")
        self.kind is not '' and result_list.append(f"AND kind = '{self.kind}'")
        self.price is not '' and result_list.append(f"AND rent_price > {self.price}")
        # self.sub_type is not None and result_list.append(f"AND sub_type LIKE '%{self.kind}%'")
        self.pattern is not '' and result_list.append(f"AND pattern LIKE '%{self.pattern}%'")
        # self.size is not '' and result_list.append(f"AND space = '{self.size}'")
        # self.floor is not None and result_list.append(f"AND floor < {self.floor}")
        return "\n".join(result_list)
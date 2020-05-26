class Subject:

    def __init__(self, subject_id: str, name: str, price: str, location: str, sub_type: str, size: str, floor: str, contact_person: str, url: str):
        self.subject_id = subject_id
        self.name = name
        self.price = price
        self.location = location
        self.sub_type = sub_type           
        self.size = size   
        self.floor = floor 
        self.contact_person = contact_person
        self.url = url

    def __str__(self):
        return ("id: " + str(self.subject_id) + "\n" +
        "name: " + str(self.name) + "\n" + 
        "price: " + str(self.price) + "\n" + 
        "location: " + self.location + "\n" + 
        "sub_type: " + self.sub_type + "\n" +
        "size: " + self.size + "\n" +
        "floor: " + self.floor + "\n" +
        "contact_person: " + self.contact_person + "\n" +
        "url: " + self.url)
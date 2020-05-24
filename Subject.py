class Subject:

    def __init__(self, id, name, price, location, sub_type, size, floor, contact_person, url):
        self.id = id
        self.name = name
        self.price = price
        self.location = location
        self.sub_type = sub_type           
        self.size = size   
        self.floor = floor 
        self.contact_person = contact_person
        self.url = url

    def __str__(self):
        return ("id: " + str(self.id) + "\n" +
        "name: " + str(self.name) + "\n" + 
        "price: " + str(self.price) + "\n" + 
        "location: " + self.location + "\n" + 
        "sub_type: " + self.sub_type + "\n" +
        "size: " + self.size + "\n" +
        "floor: " + self.floor + "\n" +
        "contact_person: " + self.contact_person + "\n" +
        "url: " + self.url)
import urllib.request as req
import bs4

# debug
import pprint

from Subject import Subject

def data_from_url_string(url_string: str):
    with req.urlopen(url_string) as response:
        return response.read().decode("utf-8")

def replace_all(text, dic):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text

def fetchSubject(root):
    # subject means rental house
    subjects_tree = root.find_all("ul", class_="listInfo clearfix")

    subjects = []
    for subject_tree in subjects_tree:
        # id
        result = subject_tree.find("span", class_="shoucang")
        id = result.a["data-text"]
        # pprint.pprint(id)

        # name
        result = subject_tree.find("a", target="_blank")
        name = result.string
        # pprint.pprint(name)

        # price
        result = subject_tree.find("div", class_="price")
        price = result.i.string
        # pprint.pprint(price)
        
        # location
        result = subject_tree.find("em")
        location = result.string
        # pprint.pprint(location)

        # info
        result = subject_tree.find("p", class_="lightBox")
        replaced_dic = {
            " ": "",
            "\xa0\xa0": ",",
            "\n": "",
            "|,": ""
        }
        info = replace_all(str(result.text), replaced_dic)
        split_info = info.split(",")
        sub_type = split_info[0]
        size = split_info[1]
        floor = split_info[2]
        # info = str(result.text).replace("\xa0\xa0", ", ").replace(" ", "").replace("\n", "").replace(",|", "")
        # pprint.pprint(split_info)

        # contact_person
        result = subject_tree.find_all("em")[1]
        contact_person = result.string
        # pprint.pprint(contact_person)

        # url
        result = subject_tree.find("li", class_="pull-left infoContent")
        url = "https:" + result.h3.a["href"]
        # pprint.pprint(url)

        subject = Subject(id, name, price, location, sub_type, size, floor, contact_person, url)
        subjects.append(subject)

    return subjects

data = data_from_url_string("https://rent.591.com.tw/?kind=0&region=1")
subjects = fetchSubject(bs4.BeautifulSoup(data, "html.parser"))

for sub in subjects:
    print(sub)

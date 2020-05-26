import urllib.request as req
import bs4
import re

# debug
import pprint

from Subject import Subject

def __data_from_url_string(url_string: str):
    with req.urlopen(url_string) as response:
        return response.read().decode("utf-8")

def __replace_all(text, dic):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text

def __fetchSubject(root):
    # subject means rental house
    subjects_tree = root.find_all("ul", class_="listInfo clearfix")

    subjects = []
    for subject_tree in subjects_tree:
        # subject_id
        result = subject_tree.find("span", class_="shoucang")
        subject_id = str(result.a["data-text"])
        # pprint.pprint(subject_id)

        # name
        result = subject_tree.find("a", target="_blank")
        name = re.sub('\W+',' ',result.string).strip()
        # pprint.pprint(name)

        # price
        result = subject_tree.find("div", class_="price")
        price = str(result.i.string)
        # pprint.pprint(price)
        
        # location
        result = subject_tree.find("em")
        location = str(result.string)
        # pprint.pprint(location)

        # info
        result = subject_tree.find("p", class_="lightBox")
        replaced_dic = {
            " ": "",
            "\xa0\xa0": ",",
            "\n": "",
            "|,": ""
        }
        info = __replace_all(str(result.text), replaced_dic)
        split_info = info.split(",")
        sub_type = str(split_info[0])
        size = str(split_info[1])
        floor = str(split_info[2])
        # info = str(result.text).replace("\xa0\xa0", ", ").replace(" ", "").replace("\n", "").replace(",|", "")
        # pprint.pprint(split_info)

        # contact_person
        result = subject_tree.find_all("em")[1]
        contact_person = str(result.string)
        # pprint.pprint(contact_person)

        # url
        result = subject_tree.find("li", class_="pull-left infoContent")
        url = "https:" + str(result.h3.a["href"])
        # pprint.pprint(url)

        subject = Subject(subject_id, name, price, location, sub_type, size, floor, contact_person, url)
        subjects.append(subject)

    return subjects

def get_subjects_from_url(url: str):
    data = __data_from_url_string(url)
    subjects = __fetchSubject(bs4.BeautifulSoup(data, "html.parser"))
    for sub in subjects:
        # print('')
        print(sub.name)
    return subjects

import urllib.request as req
import bs4
import base64
import json
import socket
import urllib.error as urlError

# debug
import pprint

from subject import Subject


def __data_from_url_string(url_string: str):
    try:
        with req.urlopen(url_string) as response:
            return response.read().decode("utf-8")
    except socket.gaierror as error:
        # raise AssertionError
        raise Exception(f"socket error: {error}")
    except urlError.URLError as error:
        raise Exception(f"URLError error: {error}")


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
        temp = str(result.string).encode("UTF-8")
        name = base64.b64encode(temp)

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

        subject = Subject(subject_id, name, price, location,
                          sub_type, size, floor, contact_person, url)
        subjects.append(subject)

    return subjects


def get_subjects_from_url(url: str):
    try:
        data = __data_from_url_string(url)
        subjects = __fetchSubject(bs4.BeautifulSoup(data, "html.parser"))
        for sub in subjects:
            encoded_name = base64.b64decode(sub.name)
            print(encoded_name.decode("UTF-8"))
        return subjects
    except:
        raise Exception("data from url response error.")

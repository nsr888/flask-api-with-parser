from bs4 import BeautifulSoup
import os


def parse_friends_html(html, limit):
    soup = BeautifulSoup(html, "html.parser")
    data_arr = []
    for div in soup.find_all("div", class_="ugrid_i"):
        if len(data_arr) == limit:
            break
        if div:
            person_dict = {}
            img = div.find("img")
            o_class = div.find("a", class_="o")
            if o_class:
                person_dict["id"] = (
                    o_class["hrefattrs"].split("friendId=")[-1].split("&")[0]
                )
                person_dict["alias"] = o_class["href"].split("/")[-1]
                person_dict["name"] = o_class.text
            person_dict["image"] = ""
            if img:
                person_dict["image"] = "http:" + img["src"]
            data_arr.append(person_dict)
    return data_arr


if __name__ == "__main__":
    HTML_FILE = "../tests/raw.html"
    if os.path.exists(HTML_FILE):
        with open(HTML_FILE, "r") as f:
            html = f.read()
        arr = parse_friends_html(html, 3)
        print(arr)

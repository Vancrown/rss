import re
import json
import requests
from bs4 import BeautifulSoup


def load_db(path):
    with open(path, "r+", encoding="utf-8") as f:
        d = json.load(f)

    return d["items"]


def init_soup(path):
    with open(path, "r+", encoding="utf-8") as f:
        s = f.read()
    soup = BeautifulSoup(s, "xml")
    return soup


def preprocess_cdata(soup):
    # for desc in [x.find("description") for x in soup.find("channel").findAll("item")]:
    #     new_s = f"<![CDATA[ {desc.text.strip()} ]]>"
    #     desc.string = new_s
    for item in soup.find("channel").findAll("item"):
        item.decompose()

    return soup


def get_cur_idx(soup):
    eps_l = [int(x.find("itunes:episode").text) for x in soup.findAll("item")]
    cur_idx = max(eps_l) + 1
    return cur_idx


def build_item(soup, cur):
    new_item = soup.new_tag("item")

    title = soup.new_tag("title")
    title.string = cur["title"]
    new_item.append(title)

    eps = soup.new_tag("itunes:episode")
    eps.string = str(cur["episode"])
    new_item.append(eps)

    title = soup.new_tag("itunes:title")
    title.string = cur["title"]
    new_item.append(title)

    des = soup.new_tag("description")
    des.string = cur["description"]
    new_item.append(des)

    wasabi_link = soup.new_tag("link")
    wasabi_link.string = cur["link"]
    new_item.append(wasabi_link)

    wasabi_link = soup.new_tag("guid")
    wasabi_link.string = cur["link"]
    wasabi_link.attrs = {"isPermaLink": "false"}
    new_item.append(wasabi_link)

    author = soup.new_tag("author")
    author.string = cur["author"]
    new_item.append(author)

    pub_date = soup.new_tag("pubDate")
    pub_date.string = cur["pubDate"]
    new_item.append(pub_date)

    enclosure = soup.new_tag("enclosure")
    enclosure.attrs = {
        "type": "audio/mpeg",
        "length": cur["length"],
        "url": cur["link"],
    }
    new_item.append(enclosure)

    duration = soup.new_tag("itunes:duration")
    duration.string = str(cur["duration"])
    new_item.append(duration)

    return new_item


def db_to_rss(soup, db_d):
    for k, v in db_d.items():
        new_item = build_item(soup, v)
        soup.find("channel").append(new_item)

    ret_s = soup.prettify().replace("&lt;", "<").replace("&gt;", ">")
    return ret_s


def write_rss(path, s):
    with open(path, "w", encoding="utf-8") as f:
        f.write(s)


if __name__ == "__main__":
    soup = init_soup("./feed/cfa_1.xml")
    preprocess_cdata(soup)
    # cur_id = 1
    # cur_idx = get_cur_idx(soup)
    db_d = load_db("./scrap_wasabi/backend/cfa_db.json")
    # db_d = {k: v for k, v in db_d.items() if int(k) >= cur_idx}

    s = db_to_rss(soup, db_d)
    write_rss("./scrap_wasabi/backend/test.xml", s)
    # write_rss("./feed/cfa_1.xml", s)

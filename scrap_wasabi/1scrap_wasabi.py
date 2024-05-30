import re
import json
import requests
from bs4 import BeautifulSoup


def load_maps(file_path):
    with open(file_path, "r+", encoding="utf-8") as f:
        s = json.load(f)
    return s["rssTitles"]


def init_db(file_path):
    with open(file_path, "r+", encoding="utf-8") as f:
        s = json.load(f)
    key_l = s["items"].keys()
    if len(key_l) == 0:
        max_exist_idx = 0
    else:
        max_exist_idx = int(max(key_l))
    cur_idx = max_exist_idx + 1
    return s, cur_idx


def get_attr_l(url):
    response = requests.get(url)
    result = response.content
    soup = BeautifulSoup(result, "xml")

    link_l = [x.find("guid").contents[0] for x in soup.find_all("item")]
    # link_l = [x.replace("&", "&amp;") for x in link_l]
    title_l = [x.find("title").contents[0] for x in soup.find_all("item")]
    pubDate_l = [x.find("pubDate").contents[0] for x in soup.find_all("item")]
    duration_l = [x.find("itunes:duration").contents[0] for x in soup.find_all("item")]
    length_l = [x.find("enclosure").get("length") for x in soup.find_all("item")]

    return link_l, title_l, pubDate_l, duration_l, length_l


def update_db(
    db_d,
    cur_idx,
    rss_map_d,
    link_l,
    title_l,
    pubDate_l,
    duration_l,
    length_l,
):
    for i in range(len(link_l)):
        cur_url = link_l[i]
        cur_title = title_l[i]
        cur_pubDate = pubDate_l[i]
        cur_duration = duration_l[i]
        cur_length = length_l[i]

        if cur_title in rss_map_d.keys():
            cur_val = {
                "rssTitle": cur_title,
                "episode": int(cur_idx),
                "title": rss_map_d[cur_title]["title"],
                "description": rss_map_d[cur_title]["description"],
                "link": cur_url,
                "author": "羊小凡",
                "pubDate": cur_pubDate,
                "length": cur_length,
                "duration": cur_duration,
            }

            db_d["items"][str(cur_idx)] = cur_val

            cur_idx += 1
    return db_d


def build_db(
    rss_map_d,
    link_l,
    title_l,
    # pubDate_l,
    duration_l,
    length_l,
):
    new_db_d = {"items": {}}
    for i in range(len(link_l)):
        cur_url = link_l[i]
        cur_title = title_l[i]
        # cur_pubDate = pubDate_l[i]
        cur_duration = duration_l[i]
        cur_length = length_l[i]

        if cur_title in rss_map_d.keys():
            cur_val = {
                "rssTitle": cur_title,
                "episode": int(i + 1),
                "title": rss_map_d[cur_title]["title"],
                "description": rss_map_d[cur_title]["description"],
                "link": cur_url,
                "author": "羊小凡",
                "pubDate": rss_map_d[cur_title]["pubDate"],
                # "pubDate": cur_pubDate,
                "length": cur_length,
                "duration": cur_duration,
            }

            new_db_d["items"][str(i + 1)] = cur_val

    return new_db_d


def write_to_db(path, db_d):
    with open(path, "w+", encoding="utf-8") as f:
        json.dump(db_d, f, indent=4, ensure_ascii=False)


def refresh_db(url, map_file_path, db_file_path):
    link_l, title_l, pubDate_l, duration_l, length_l = get_attr_l(url)
    rss_map_d = load_maps(map_file_path)
    # db_d, cur_idx = init_db(db_file_path)
    # db_d = update_db(
    #     db_d,
    #     cur_idx,
    #     rss_map_d,
    #     link_l,
    #     title_l,
    #     pubDate_l,
    #     duration_l,
    #     length_l,
    # )
    new_db_d = build_db(
        rss_map_d,
        link_l,
        title_l,
        # pubDate_l,
        duration_l,
        length_l,
    )
    # [wip] change test to db.json
    # write_to_db("./scrap_wasabi/backend/test.json", db_d)
    write_to_db(db_file_path, new_db_d)


if __name__ == "__main__":
    url = "https://audio.com/rss/collection/1786941485940961"
    map_file_path = "./scrap_wasabi/cfa_maps.json"
    db_file_path = "./scrap_wasabi/backend/cfa_db.json"
    # db_file_path = "./scrap_wasabi/backend/test.json"
    refresh_db(url, map_file_path, db_file_path)

import a_db_to_rss, a_scrap_wasabi


if __name__ == "__main__":
    new_db_d = a_scrap_wasabi.run()
    a_db_to_rss.run(new_db_d["items"])

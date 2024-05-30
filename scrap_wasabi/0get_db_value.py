import datetime as dt


def get_pubDate(yyyy, mm, dd, h=17, m=17, s=17):
    return (
        dt.datetime(year=yyyy, month=mm, day=dd, hour=h, minute=m, second=s).strftime(
            "%a, %d %b %Y %H:%M:%S"
        )
        + " +0000"
    )


if __name__ == "__main__":
    # every Friday
    yyyy = 2024
    mm = 5
    dd = 25

    print(get_pubDate(yyyy=yyyy, mm=mm, dd=dd))

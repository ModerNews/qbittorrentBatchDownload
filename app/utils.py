import datetime

import pydantic
import requests

from rss_parser import Parser
from pydantic import BaseModel


class NyaaEntry(BaseModel):
    title: str
    simplified_title: str
    torrent_link: str
    upstream_link: str
    upload_date: datetime.datetime


def get_xml_tree(url: str):
    data = requests.get(url)
    parsed = Parser.parse(data.text)
    return parsed


def get_nyaa_entries(series_title: str, team: str = "[SubsPlease]", *, base_url="https://nyaa.si/?page=rss&", color=0x0085fe):
    url = base_url + f"q={team}+{series_title.replace(' ', '+')}"
    feed = get_xml_tree(url)
    data = []
    for item in feed.channel.items:
        data.append(NyaaEntry(title=str(item.title),
                              torrent_link=str(item.link),
                              upstream_link=str(item.guid),
                              upload_date=datetime.datetime.strptime(str(item.pub_date), "%a, %d %b %Y %H:%M:%S -0000"),
                              simplified_title=sorted((s.split(']')[-1] for s in str(item.title).split('[')), key=lambda x: len(x))[-1].strip()))

    return data
import requests


class Client:
    def __init__(self, host, port, username="admin", password="adminadmin", headers={}):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.headers = headers
        self.cookies = self.get_session_cookies()

    def get_session_cookies(self):
        url = f"http://{self.host}:{self.port}/api/v2/auth/login"
        data = {"username": self.username, "password": self.password}
        headers = {"Referer": f"http://{self.host}:{self.port}/"}
        response = requests.post(url, data=data, headers=headers)
        return response.cookies

    def get_torrents(self):
        url = f"http://{self.host}:{self.port}/api/v2/torrents/info"
        response = requests.get(url, cookies=self.cookies)
        return response.json()

    def add_torrent(self, target, savepath, *,
                    category="movies",
                    skip_checking=False,
                    paused=False,
                    root_folder=True):
        url = f"http://{self.host}:{self.port}/api/v2/torrents/add"
        # headers = self.headers | {"Content-Type": "multipart/form-data; boundary=------------------------6688794727912"}
        data = {
            "urls": target if isinstance(target, str) else "\n".join(target),
            "savepath": savepath,
            "category": category,
            "skip_checking": skip_checking,
            "paused": paused,
            "root_folder": root_folder,
        }
        response = requests.post(url, data=data, cookies=self.cookies, headers=self.headers)
        try:
            return response.json()
        except:
            return response
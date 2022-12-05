import requests

class Downloader:

    def __init__(self, url, params, method):
        self.__url = url
        self.__params = {
            "index": params.get("index"),
            "value": params.get("value"),
            "tz": params.get("tz"),
            "start": params.get("start"),
            "fin": params.get("fin"),
            "x": params.get("x"),
            "y": params.get("y")
        }
        self.__method = method

    def get_html(self):
        response = requests.get(self.__url)
        self.__html = response
        return response

    def save(self, file_path):
        with open(file_path, "wb+") as f:
            f.write(self.__html.content)


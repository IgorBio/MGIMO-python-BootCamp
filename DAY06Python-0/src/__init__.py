from download import Downloader
from parser import Parser
from data import some_logic


def process(url, web_page_path=None, data_path=None):
    PARAMS = {}
    downloader = Downloader(url=url, params=PARAMS, method="GET")
    downloader.get_html()
    downloader.save(web_page_path)
    parser = Parser(source=web_page_path)
    parser.parser()
    parser.save(data_path)
    return some_logic(data_path)


if __name__ == "__main__":
    FILE_PATH = "index.html"
    URL = "https://i-fakt.ru/"
    output = process(url=URL, web_page_path=FILE_PATH, data_path="sample.json")
    print(output)


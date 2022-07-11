from bs4 import BeautifulSoup
from urllib.request import urlopen
import json


def scrap_bird_list():
    url = "https://en.wikipedia.org/wiki/List_of_birds_by_common_name"
    page = urlopen(url)
    html_bytes = page.read()
    html_data = html_bytes.decode("utf-8")
    soup = BeautifulSoup(html_data, "html.parser")
    page_elements = soup.find_all('li')
    print("No. of Birds: "+str(len(page_elements)))
    count = 0
    data = {'birds': []}
    with open("birds.json", "w") as outfile:
        index = 0
        for i in page_elements:
            count = count + 1
            if 27 < count < 11002:
                print(i.text)
                data['birds'].insert(index, i.text)
                index = index + 1
        print(data)
        outfile.write(json.dumps(data, indent=4))


if __name__ == '__main__':
    scrap_bird_list()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

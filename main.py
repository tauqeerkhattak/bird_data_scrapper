import requests
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


def scrap_bird_image():
    bird_name = "Yellow-scarfed tanager"
    bird_name = bird_name.replace(" ", "_")
    bird_name = bird_name.lower()
    print(bird_name)
    wiki_page_url = "https://en.wikipedia.org/wiki/"+bird_name
    image_url = "https://en.wikipedia.org"
    page = requests.get(wiki_page_url)
    soup = BeautifulSoup(page.content, "html.parser")
    image = soup.find('a', class_="image")
    print(image_url+image.attrs["href"])


if __name__ == '__main__':
    scrap_bird_image()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

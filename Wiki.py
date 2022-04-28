import requests
from bs4 import BeautifulSoup
import json

def create_api_data():
    url ="https://type.fit/api/quotes"
    response = requests.get(url)
    return response.json()

def create_quotes_dict(api_data):
    quotes ={}
    for data in api_data:
        if data["author"]:
            if not data["author"]  in quotes :
                quotes[data["author"] ] = []
            quotes[data["author"] ].append(data["text"])
    return  quotes
def get_image(author):
    url = f"https://en.wikipedia.org/wiki/{author}"
    page = requests.get(url)
    html = page.content
    soup = BeautifulSoup(html,'html.parser')
    try:
        td = soup.find("td",class_ ="infobox-image")
        image = td.find("img")
        return "https:"+ image['src']
    except Exception as e:
        print (e)
        return None
def get_image_dict(authors):
    images = {}
    num_authors = len(authors)
    for author_num,author in enumerate(authors,start = 1):
        images[author]  = get_image(author)
        print (f"processing{author_num}/{num_authors}author")
    return images
def create_json(filename , data):
    with open(filename ,'w') as f:
        json.dump(data,f)
if __name__ == '__main__':
    api_data = create_api_data()
    quotes = create_quotes_dict(api_data)
    authors = list( quotes.keys() )
    images = get_image_dict(authors)
    create_json("quotes.json",quotes)
    create_json("images.json",images)

import requests 
from bs4 import BeautifulSoup
from dataclasses import dataclass, asdict


@dataclass
class Card():
    id:int
    title:str
    price:str
    

url = "https://neman.kg"

def get_html(url, category):
    response = requests.get(url +"/" + category).text
    return response

# print(get_html(url, "lekarstvennye-sredstva/"))    
def get_cards_from_html(html):
    soup = BeautifulSoup(html,"html.parser")
    cards = soup.find_all("div",class_="ty-column3")
    return (cards)
# html =(get_html(url, "lekarstvennye-sredstva/")) 
# print(get_cards_from_html(html))
def get_data_from_cards(cards):
    result = []
    id_counter = 1
    for card in cards:
        try:
            title = card.find("div",class_ ="ut2-gl__name").text.strip()
        except AttributeError:
            continue

        try:
            price = card.find("span",class_="ty-price").text.strip()
        except AttributeError:
            continue
        
        obj =asdict(Card(id_counter,title, price))
        id_counter += 1
        result.append(obj)
    return result        



html =(get_html(url, "lekarstvennye-sredstva/")) 
cards = (get_cards_from_html(html))

result = get_data_from_cards(cards)
# print(result)




    
    



with open('bosses.txt', 'r') as f:
    bosses = f.readlines()
import requests
from bs4 import BeautifulSoup

url = "https://eldenring.wiki.fextralife.com/"
boss_data = open('boss_data.csv', 'w')
categories = ['NAME', 'HP', 'DEFENSE', 'STANCE',
                'RUNES', 'DROPS', 'LOCATION', 'DUO',
                'NEG_STANDARD', 'NEG_SLASH', 'NEG_STRIKE', 'NEG_PIERCE', 'NEG_MAGIC', 'NEG_FIRE', 'NEG_LIGHTNING', 'NEG_HOLY',
                'RES_POISON', 'RES_ROT', 'RES_BLEED', 'RES_FROST', 'RES_SLEEP', 'RES_MADNESS']


def has_specific_child(tag):
    return tag.find('ul', class_='searchable') is not None

def get_attribute(heading, atribute):
    atributes = []
    next_element = heading.find_next_sibling('ul')
    lis = next_element.find_all('li')
    for li in lis:
        text = li.text.strip()
        if atribute in text:
                # print(text)
            text = text.split(' ')
            # print(text)
            if atribute == "Health":
                text = clean_health(text[1])
    # print(atributes)
    set_atributes = set(atributes)
    return set_atributes

def clean_health(text): 
    text = text.replace(u'\xa0', u' ')
    text = text.split(' ')
    print(text[0])
    return text[0]

boss_data.write(','.join(categories)+'\n')
for boss in bosses[:1]:
    healths = []
    defenses = []
    stances = []
    drops = []
    response = requests.get(url+boss.strip())
    boss_name = boss.strip().split('/')[-1].replace('+', ' ')
    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, "html.parser")
        bonfire_headings = soup.find_all('h3', class_='bonfire')
        for heading in bonfire_headings:
            health = get_attribute(heading, "Health")
            if health:
                healths.append(health)
            defense = get_attribute(heading, "Defense")
            if defense:
                defenses.append(defense)
            stance = get_attribute(heading, "Stance")
            if stance:
                stances.append(stance)
            drop = get_attribute(heading, "Drops")
            if drop:
                drops.append(drop)
    print(healths)

                        

    boss_data.write('\n')       
    

boss_data.close()

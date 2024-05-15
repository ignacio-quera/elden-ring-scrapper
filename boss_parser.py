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
negations_categories = ["Standard", "Slash", "Strike", "Pierce", "Magic", "Fire", "Lightning", "Holy"]
resistances_categories = ["Poison", "Rot", "Bleed", "Frost", "Sleep", "Madness"]

def has_specific_child(tag):
    return tag.find('ul', class_='searchable') is not None

def get_attribute(heading, atribute):
    atributes = []
    next_element = heading.find_next_sibling()
    lis = next_element.find_all('li')
    for li in lis:
        text = li.text.strip()
        if atribute in text:
            if atribute == "Drops":
                clean_drops(text)
            else:
                text = text.replace(u'\xa0', u' ')
                text = text.split(' ')
            if atribute == "Health":
                text = clean_health(text[1])
                atributes.append(text)
            else:
                atributes.append(text[1])
            # if atribute == "Defense":
                # text = text[1]
    return atributes

def clean_health(text): 
    text = text.replace(u'\xa0', u' ')
    text = text.replace(',', '') 
    text = text.split(' ')
    return text[0]

def clean_drops(text):
    # text = text.split(',')
    # text = text.replace(u'\xa0', u' ')

    return text

def get_negations(negations_soup):
    negations = []
    for negation_tag in negations_soup:
        if "Negation" in negation_tag.text:
            print(negation_tag.text)
            negation = negation_tag.text.strip()
            negation = negation.split('\n')
            for n in negation:
                for cat in negations_categories:
                    if cat in n:
                        n = n.replace(u'\xa0', u' ')
                        negations.append(n.split(' ')[1])
    return [negations]

def get_resistances(resistances_soup):
    resistances = []
    for resistance_tag in resistances_soup:
        if "Resistance" in resistance_tag.text:
            resistance = resistance_tag.text.strip()
            resistance = resistance.split('\n')
            for r in resistance:
                for cat in resistances_categories:
                    if cat in r:
                        resistances.append(r.split(':')[1])
        else:
            resistances.append('None')
    return [resistances]

boss_data.write(','.join(categories)+'\n')
for boss in bosses[16:19]:
    healths = []
    defenses = []
    stances = []
    drops = []
    response = requests.get(url+boss.strip())
    boss_name = boss.strip().split('/')[-1].replace('+', ' ')
    boss_name = boss_name.replace(',', '')
    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, "html.parser")
        # Find the elements containing boss information
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

        # Find negations and resistances
        negations_soup = soup.find_all('div', class_='col-sm-6')
        negations = get_negations(negations_soup)

        resistances_soup = soup.find_all('div', class_='col-sm-6')
        resistances = get_resistances(resistances_soup)
        
    print(boss_name)
    for health, defense, stance, drop, negation, resistance in zip(healths, defenses, stances, drops, negations, resistances):
        boss_data.write(
            boss_name + ',' + health[0] + ',' + defense[0] + ',' + stance[0] + ',' + 'drops' + ',' 'runes' + ',' + 'location' + ',' 
            + 'duo' + ',' + ','.join(negation)+ ',' + ','.join(resistance) + '\n')

                        

    boss_data.write('\n')       
    

boss_data.close()

import requests
from bs4 import BeautifulSoup

url = "https://eldenring.wiki.fextralife.com/"
response = requests.get(url+'/Locations')
locations_url = []

def has_specific_child(tag):
    return tag.find('ul', class_='searchable') is not None

if response.status_code == 200:
    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")

    # Find the elements containing boss information
    boss_elements = soup.find_all(has_specific_child, class_ = "col-sm-4")
    for boss_element in boss_elements:
        area = boss_element.find("a", class_="wiki_link").text.strip()
        bosses = boss_element.find_all("a", class_="wiki_link")
        for boss in bosses[1:]:
            locations_url.append(boss.get('href'))
    with open('bosses.txt', 'w') as f:
        for item in bossess_url:
            f.write("%s\n" % item)
else:
    print("Failed to fetch the page.")

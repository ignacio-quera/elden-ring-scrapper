import requests
from bs4 import BeautifulSoup
import json
import re

def remove_text_in_parentheses(input_string):
    # Define the regular expression pattern to match text within parentheses
    pattern = r'\([^)]*\)'
    
    # Use re.sub() to substitute the matched pattern with an empty string
    result = re.sub(pattern, '', input_string)
    
    return result

def remove_text_in_brackets(input_string):
    # Define the regular expression pattern to match text within parentheses
    pattern = r'\[[^)]*\]'
    
    # Use re.sub() to substitute the matched pattern with an empty string
    result = re.sub(pattern, '', input_string)
    
    return result

url = "https://eldenring.wiki.fextralife.com/"
response = requests.get(url+'/Sites+of+Grace')
dic = {}

if response.status_code == 200:
    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")

    h4_elements = soup.find_all('h4')

    for h4_element in h4_elements:
        location = remove_text_in_parentheses(h4_element.text)
        ul_element = h4_element.find_next_sibling('ul')
        if ul_element:
            li_elements = ul_element.find_all('li')
            for element in li_elements:
                grace = remove_text_in_brackets(element.text)
                dic[grace]  = location
    
    with open("locations.json", "w") as outfile:
        json.dump(dic, outfile)
else:
    print("Failed to fetch the page.")

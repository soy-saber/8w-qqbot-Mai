import requests
from bs4 import BeautifulSoup
import re

url = 'https://www.random.org/integers/?num=100&min=1&max=100&col=5&base=10&format=html&rnd=new'
response = requests.get(url)
html = response.content.decode('utf-8')
soup = BeautifulSoup(html, 'html.parser')
fake_list = soup.select('#invisible > pre')
numbers = []
for item in fake_list:
    numbers = item.get_text()
str_numbers_list = re.findall("\\d+", numbers)
numbers_list = map(int, str_numbers_list)
final_number = sum(numbers_list)/100

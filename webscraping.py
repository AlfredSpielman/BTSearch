import pandas as pd
from bs4 import BeautifulSoup
import requests
from tqdm import trange

column_names = ['Sieć', 'Województwo', 'Miejscowość', 'Adres', 'Technologie', 'ID stacji', 'Ostatnia aktualizacja']
full_df = pd.DataFrame(columns=column_names)

res = requests.get(f"http://beta.btsearch.pl/bts/?page=1")
soup = BeautifulSoup(res.content)
pages = int(soup.find('li', {'class': 'active'}).text[12:][:4]) + 1

for page in trange(1, pages):
    res = requests.get(f"http://beta.btsearch.pl/bts/?page={page}")
    soup = BeautifulSoup(res.content, "lxml")
    rows = soup.find('tbody').find_all('tr')
    df = pd.DataFrame(columns=column_names)
    for row in rows:
        text = row.text.split('\n')[1:-1]
        techs = [t.strip() for t in text[4:-3][2::2]]
        data = {
            'Sieć': text[0],
            'Województwo': text[1],
            'Miejscowość': text[2],
            'Adres': text[3],
            'Technologie': techs,
            'ID stacji': text[-2:-1][0],
            'Ostatnia aktualizacja': text[-1]}
        df = df.append(data, ignore_index=True)
    full_df = full_df.append(df)

full_df.to_csv('baza_bts.csv', index=False)

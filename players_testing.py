from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd

driver = webdriver.Firefox()
driver.implicitly_wait(2)

url = 'https://www.basketball-reference.com/leagues/NBA_2021_per_game.html'
driver.get(url)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

table = soup.find('table', attrs={'id': 'per_game_stats'})

cols = table.thead.find_all('th')
cols = [h.text.strip() for h in cols]
cols = cols[1:]

rows = table.find_all('tr')


player_stats = [[td.getText().strip() for td in rows[i].find_all('td')] for i in range(len(rows))]
player_stats = player_stats[1:]

players_df = pd.DataFrame(player_stats, columns=cols)
players_df.set_index('Player', inplace=True)

player = 'Trae Young'
print(f'{player} hits {players_df.loc[player][9]} 3s per game')
print(f'{player} scores {players_df.loc[player][27]} points per game')
print(f'{player} grabs {players_df.loc[player][21]} rebounds per game')
print(f'{player} dishes {players_df.loc[player][22]} assists per game')
driver.quit()
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd

player_list = []
def compare_player_stats(): # TODO: input player_list when you transfer this?
    timeout = 25
    url = 'https://www.basketball-reference.com/leagues/NBA_2021_per_game.html'
    driver = webdriver.Firefox()
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    table = soup.find('table', attrs={'id': 'per_game_stats'})

    cols = table.thead.find_all('th')
    cols = [h.text.strip() for h in cols]
    cols = cols[1:]

    rows = table.find_all('tr')
    rows = rows[1:]
    player_stats = [[td.getText().strip() for td in rows[i].find_all('td')] for i in range(len(rows))]

    for i in range(len(player_stats)):
        if len(player_stats[i]) > 1:
            player_list.append(player_stats[i][0])
    print(player_list)

    df = pd.DataFrame(player_stats, columns=cols)
    df.set_index('Player', inplace=True)

    driver.quit()
    return df


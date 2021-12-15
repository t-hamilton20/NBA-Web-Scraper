from bs4 import BeautifulSoup
import pandas as pd
import requests
import re

player = input("Enter an NBA Player: ")
player = player.lower()
firstLetter = player.find(" ")
url = "https://www.basketball-reference.com/players/" + player[firstLetter + 1] + "/" + player[firstLetter + 1:] + player[0:2] + "01.html"
page = requests.get(url)

soup = BeautifulSoup(page.content, "html.parser")

meta = soup.find('h1')
start = str(meta).find("<span>")
end = str(meta).find("</span>")
name = str(meta)[start + 6 : end]
print("Career Averages For", name + ":")

seasons = set([])
for year in soup.find_all('th', {'data-stat': "season"}):
    s = str(year).find("</a>")
    if s > 0:
        seasons.add(str(year)[s - 7 : s])
seasons = sorted(list(seasons))

teams = []
tradedFlag = False
tradedCount = 0

for year in soup.find_all('td', {'data-stat': "team_id"}):
    s = str(year).find("</a>")
    tot = str(year).find("TOT")

    if (len(teams) < len(seasons)):
        if tot > 0:
            teams.append("TOT")
            tradedFlag = True;

        if tradedCount == 0 and not tradedFlag:
            if s > 0:
                teams.append(str(year)[s - 3: s])

        if tradedFlag:
            tradedCount = tradedCount + 1

        if tradedCount > 2:
            tradedFlag = False;
            tradedCount = 0

pts = []
for year in soup.find_all('td', {'data-stat': "pts_per_g"}):
    s = re.search(r"\d", str(year))

    if (len(pts) < len(seasons)):
        if(str(year)[s.start() + 3].isdigit()):
            pts.append(str(year)[s.start() : s.start() + 4])
        else:
            pts.append(str(year)[s.start(): s.start() + 3])

ast = []
for year in soup.find_all('td', {'data-stat': "ast_per_g"}):
    s = re.search(r"\d", str(year))

    if (len(ast) < len(seasons)):
        if(str(year)[s.start() + 3].isdigit()):
            ast.append(str(year)[s.start() : s.start() + 4])
        else:
            ast.append(str(year)[s.start(): s.start() + 3])

reb = []
for year in soup.find_all('td', {'data-stat': "trb_per_g"}):
    s = re.search(r"\d", str(year))

    if (len(reb) < len(seasons)):
        if(str(year)[s.start() + 3].isdigit()):
            reb.append(str(year)[s.start() : s.start() + 4])
        else:
            reb.append(str(year)[s.start(): s.start() + 3])

ts = []
fga = []
fta = []
for year in soup.find_all('td', {'data-stat': "fga_per_g"}):
    s = re.search(r"\d", str(year))

    if (len(fga) < len(seasons)):
        if(str(year)[s.start() + 3].isdigit()):
            fga.append(str(year)[s.start() : s.start() + 4])
        else:
            fga.append(str(year)[s.start(): s.start() + 3])

for year in soup.find_all('td', {'data-stat': "fta_per_g"}):
    s = re.search(r"\d", str(year))

    if (len(fta) < len(seasons)):
        if(str(year)[s.start() + 3].isdigit()):
            fta.append(str(year)[s.start() : s.start() + 4])
        else:
            fta.append(str(year)[s.start(): s.start() + 3])

for i in range(len(fta)):
    ts.append(round(float(pts[i]) / (2 * (float(fga[i]) + 0.44 * float(fta[i]))), 3))

player = {'Season': seasons, 'Team' : teams, 'Points' : pts, 'Assists' : ast, 'Total Rebounds' : reb, 'True Shooting %' : ts}

df = pd.DataFrame(player, columns = ['Season', 'Team', 'Points', 'Assists', 'Total Rebounds', 'True Shooting %'])
print(df)

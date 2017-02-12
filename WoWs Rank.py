import json
import requests

# Player ID
playerID = '2011774448'
server = 'asia'

# Get Current Rank, Batlles and winRate for last season
playerRankAPI = 'https://api.worldofwarships.' + server + '/wows/seasons/accountinfo/?application_id=demo&account_id=' + playerID + '&fields=seasons.rank_solo.battles%2C+seasons.rank_solo.wins%2C+seasons.rank_info.rank%2c+seasons.rank_info.max_rank'

data = requests.get(playerRankAPI)
dataJson = json.loads(data.text)

print(playerID)
# Get the length of dataJson
allSeason = dataJson['data'][playerID]['seasons']
seasonCount = len(allSeason)

lastSeason = list(allSeason.keys())[seasonCount - 1]
print('Season ' + lastSeason)
seasonJson = allSeason[lastSeason]

rank = seasonJson['rank_info']['rank']
maxRank = seasonJson['rank_info']['max_rank']
if not seasonJson['rank_solo'] is None:
    battles = seasonJson['rank_solo']['battles']
    wins = seasonJson['rank_solo']['wins']

if not battles is 0:
    winRate = wins / battles * 100
else:
    winRate = 0

print('Rank ' + str(rank) + ' (Best: ' + str(rank) + ')\n' + str(battles) + ' battle(s)\n' + 'Win rate: {:.2f}%'.format(winRate))

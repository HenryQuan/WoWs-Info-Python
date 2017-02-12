import json
import requests

# setup server string
server = 'asia'
serverAPI = 'https://api.worldoftanks.' + server + '/wgn/servers/info/?application_id=demo&language=en'

# get data from API
dataText = requests.get(serverAPI)
dataJson = json.loads(dataText.text)

# get online number for world of warships
online = dataJson['data']['wows'][0]['players_online']
print('There are ' + str(online) + ' players online')

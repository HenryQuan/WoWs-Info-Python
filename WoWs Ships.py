# This is used to get player's ships
import json
import requests

# Calculate general information for the ships
def calPlayerShipsStat(battles, damage_dealt, frags, xp, survived_battles, hits, shots, wins):
    if battles > 0:
        winRate = '{:.2f}%'.format(wins / battles * 100)
        averageDamage = '{:.0f}'.format(damage_dealt / battles)
        averageXp = '{:.0f}'.format(xp / battles)
        death = (battles - survived_battles)
        if death == 0: death = 1
        killDeathRatio = '{:.2f}'.format(frags / death)
        hitRatio = '0'
        if shots > 0:
            hitRatio = '{:.2f}%'.format(hits / shots * 100)

        return (battles, winRate, averageDamage, averageXp, killDeathRatio, hitRatio)
    else:
        # There is nothing to Calculate if this ship is never played
        return (0,0,0,0,0,0)


playerID = '2008682384'
server = 'asia'
playerShipsAPI = 'https://api.worldofwarships.' + server + '/wows/ships/stats/?application_id=demo&account_id=' + playerID + '&fields=ship_id%2Cpvp.battles%2Cpvp.damage_dealt%2Cpvp.wins%2Cpvp.xp%2Cpvp.frags%2Cpvp.survived_battles%2Cpvp.main_battery.hits%2Cpvp.main_battery.shots'
shipInfoAPI = 'https://api.worldofwarships.' + server + '/wows/encyclopedia/ships/?application_id=demo&fields=name%2Cship_id%2Ctype%2Ctier%2Cnation'

# Get ship information first
ships = requests.get(shipInfoAPI)
shipsJson = json.loads(ships.text)
shipsDataJson = shipsJson['data']

""" Print out all ships with their ID, name, nation, type and tier
for key in shipsDataJson.keys():
    print(key)
    print('Tier ' + str(shipsDataJson[key]['tier']) + ' ' + shipsDataJson[key]['nation'] + ' ' + shipsDataJson[key]['type'] + ' ' + shipsDataJson[key]['name'] + '\n')
"""

# Get player information
playerShips = requests.get(playerShipsAPI)
playerShipsJson = json.loads(playerShips.text)
if playerID in playerShipsJson['data']:
    playerShipsDataJson = playerShipsJson['data'][playerID]
    playerShipsCount = len(playerShipsDataJson)

    tier = 0
    mostPlay = 0
    mostPlayShipName = ''
    totalShip = 0
    totalBattles = 0

    for i in range(0, playerShipsCount):
        shipID = str(playerShipsDataJson[i]['ship_id'])
        currentShip = playerShipsDataJson[i]['pvp']

        if shipID in shipsDataJson.keys():
            tier += shipsDataJson[shipID]['tier'] * currentShip['battles']
            if currentShip['battles'] > mostPlay:
                mostPlay = currentShip['battles']
                mostPlayShipName = shipsDataJson[shipID]['name']
            totalShip += 1
            totalBattles += currentShip['battles']
            print('Tier ' + str(shipsDataJson[shipID]['tier'])+ ' ' + shipsDataJson[shipID]['nation'] + ' ' + shipsDataJson[shipID]['type'] + ' ' + shipsDataJson[shipID]['name'])
        else:
            print(shipID + '\n')

        data = calPlayerShipsStat(currentShip['battles'], currentShip['damage_dealt'], currentShip['frags'], currentShip['xp'], currentShip['survived_battles'], currentShip['main_battery']['hits'], currentShip['main_battery']['shots'], currentShip['wins'])
        print('WinRate: ' + str(data[1]) + '\n' + 'Battles: ' + str(data[0]))
        print('Xp: ' + str(data[2]) + '\n' + 'Damage: ' + str(data[2]))
        print('KillDeathRatio: ' + str(data[4]) + '\n' + 'HitRatio: ' + str(data[5]) + '\n')



    print('This player has ' + str(playerShipsCount) + ' ships')
    print('Average tier : ' + '{:0.2f}'.format(tier / totalBattles))
    print('Most play ship: ' + mostPlayShipName)
else:
    print('No information')

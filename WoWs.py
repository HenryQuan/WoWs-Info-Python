import requests
import json
import datetime

class WoWsClass:
    # There are four servers available
    Russia = 0
    Europe = 1
    US = 2
    Asia = 3
    allServer = ['ru', 'eu', 'com', 'asia']
    server = ''

    # Your own application ID
    application_id = ''

    # World of Warship Asia official API
    playerAPI = ''
    playerDataAPI = ''

    # Set server type and application_id
    def __init__(self, serverID, application_id):
        self.server = self.getServerDomain(serverID)
        self.application_id = application_id
        self.setAPI()

    # Get server domain
    def getServerDomain(self, name):
        return self.allServer[name]

    # Setup API url string
    def setAPI(self):
        self.playerAPI = 'https://api.worldofwarships.' + str(self.server) + \
            '/wows/account/list/?application_id=' + str(self.application_id)
        self.playerDataAPI = 'https://api.worldofwarships.' + str(self.server) + \
            '/wows/account/info/?application_id=' + str(self.application_id)

    # Search for username
    def getUsername(self, name):

        postdata = dict(search = name, language = 'en')
        username = requests.post(self.playerAPI, data = postdata)
        return username.text

    # Print out all possible names and ids
    def printAllNameAndId(self, jsonString):

        if jsonString is None or '"error"' in jsonString:
            print('Input String is not valid')
            # Quit this app
            exit(1)
        else:
            nameAndIdJson = json.loads(jsonString)
            element = len(nameAndIdJson['data'])

            if element == 0:
                print('\nThere is no such player')
            elif element == 1:
                print('\nThere is only one match')
            else:
                print('\nThere are ' + str(element) + ' matches')

            i = 0
            while(i < element):
                print('{:3d}'.format(i + 1) + ': ' +
                    str(nameAndIdJson['data'][i]['nickname']))
                i += 1

            # Return raw data
            return nameAndIdJson

    def enterUsername(self):

        # User input
        name = input('Please enter your user name: ')

        # Loop untill valid input
        while name.isspace() or len(name) < 3:
            print('Input string cannot be empty and should be more than 3 character')
            name = input('Please enter your user name: ')

        # Get and print out all names (100 results at most)
        dataText = self.getUsername(name)
        dataJson = self.printAllNameAndId(dataText)
        return dataJson

    def chooseUsername(self, count):

        numberChosen = input('> ')
        while numberChosen.isdigit() == False or int(numberChosen) < 1 or int(numberChosen) > int(count):
            print('Number out of range or invalid input')
            numberChosen = input('> ')

        # Data Index starts from 0!
        return int(numberChosen) - 1

    def getElementFromData(self, data):
        return len(data['data'])

    # Convert timestamps to Date Time
    def numberToDate(self, integer):
        return datetime.datetime.fromtimestamp(integer)

    # Get some information about that account id
    def getInformationFromId(self, account_id):

        postdata = dict(account_id = account_id, language = 'en')
        playerData = requests.post(self.playerDataAPI, data = postdata)
        if playerData is None or '"error"' in playerData:
            print('Input String is not valid')
            # Quit this app
            exit(1)
        else:
            playerDataJson = json.loads(playerData.text)
            return playerDataJson

    # print out useful for this player
    def printInformation(self, data, account_id):

        # Date created
        usefulData = data['data'][str(account_id)];
        dateCreated = self.numberToDate((usefulData['created_at']))
        currentData = datetime.datetime.utcnow()
        dateDiff = (currentData - dateCreated).days

        serviceLevel = usefulData['leveling_tier']

        # Hit ratio, average exp, average damage, win rate
        pvp = usefulData['statistics']['pvp']
        hits = pvp['main_battery']['hits']
        shots = pvp['main_battery']['shots']

        win = pvp['wins']
        totalDamage = pvp['damage_dealt']
        xp = pvp['xp']

        totalFrags = pvp['frags']
        survivedBattles = pvp['survived_battles']
        totalBattles = pvp['battles']

        # Calculate data and print it out
        if int(shots) == 0:
            hitRatio = 0
        else:
            hitRatio = hits / shots * 100

        if int(totalBattles) == 0:
            winRate = 0
            averageDamage = 0
            averageXp = 0
            killdeathRatio = 0
        else:
            winRate = win / totalBattles * 100
            averageDamage = totalDamage / totalBattles
            averageXp = xp / totalBattles
            killdeathRatio = totalFrags / (totalBattles - survivedBattles)

        averageBattlesPerDay = totalBattles / dateDiff
        username = usefulData['nickname']

        print('\n' + str(username) + ' starting from ' + dateCreated.strftime("%d/%m/%y")
              + ' UTC (' + str(dateDiff) + ' day(s))')
        print('Service level: ' + str(serviceLevel))
        print('Total battles: ' + str(totalBattles) + ' ('
              + '{:.2f}'.format(averageBattlesPerDay) + ' per day)')
        print('Win rate: ' + '{:.2f}'.format(winRate) + '%')
        print('Average EXP: ' + '{:.0f}'.format(averageXp))
        print('Average damage: ' + '{:.0f}'.format(averageDamage))
        print('Kill / Death Ratio: ' + '{:.2f}'.format(killdeathRatio) + '%')
        print('Main battery hit ratio: ' + '{:.2f}'.format(hitRatio) + '%')
        point = self.activePoint(averageBattlesPerDay, serviceLevel)
        if point >= 5:
            print('This player is not active')

        # Newline...
        print('')

    def activePoint(self, averageBattles, serviceLevel):
        # If it is more than 5 points... This player is inactivate
        point = 0

        if int(serviceLevel) < 13:
            point += 1
        elif int(serviceLevel) < 10:
            point += 2
        elif int(serviceLevel) < 6:
            point += 3

        if averageBattles == 0:
            point += 99
        elif 0 < averageBattles <= 0.20:
            point += 9
        elif 0.20 < averageBattles <= 0.5:
            point += 3
        elif 0.5 < averageBattles <= 1.0:
            point += 1

        return point

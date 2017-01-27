import requests
import json
import datetime
import time

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
    playerDataByDateAPI = ''

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
        self.playerDataByDateAPI = 'https://api.worldofwarships.' + str(self.server) + \
                                   '/wows/account/statsbydate/?application_id=' + str(self.application_id)

    # Search for username
    def getUsername(self, name):

        postdata = dict(search=name, language='en')
        username = requests.post(self.playerAPI, data=postdata)
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
            while (i < element):
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

        postdata = dict(account_id=account_id, language='en')
        playerData = requests.post(self.playerDataAPI, data=postdata)
        if playerData is None or '"error"' in playerData:
            print('Input String is not valid')
            # Quit this app
            exit(1)
        else:
            playerDataJson = json.loads(playerData.text)
            return playerDataJson

    def getDataForDate(self, dataOne, dataTwo):

        # Calculate dataOne - dataTwo
        if dataOne == '' or dataTwo == '':
            # There is no data inside dataOne
            return (0, 0, 0, 0, 0)

        winRate = 0
        averageXp = 0
        killDeathRatio = 0
        averageDamage = 0

        battles = int(dataOne['battles']) - int(dataTwo['battles'])
        xp = int(dataOne['xp']) - int(dataTwo['xp'])
        win = int(dataOne['wins']) - int(dataTwo['wins'])
        survived = int(dataOne['survived_battles']) - int(dataTwo['survived_battles'])
        frags = int(dataOne['frags']) - int(dataTwo['frags'])
        damage = int(dataOne['damage_dealt']) - int(dataTwo['damage_dealt'])
        death = battles - survived
        if death == 0:
            death = 1

        if battles > 0:
            winRate = win / battles * 100
            averageXp = xp / battles
            killDeathRatio = frags / death
            averageDamage = damage / battles

        return (winRate, averageXp, killDeathRatio, averageDamage, battles)

    def getinformationForTodayAndYesterday(self, account_id):

        # Get date string for today and yesterday
        today = datetime.date.today().strftime('%Y%m%d')
        yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y%m%d')
        daybefore = (datetime.date.today() - datetime.timedelta(days=2)).strftime('%Y%m%d')
        dateString = str(today) + ',' + str(yesterday) + ',' + str(daybefore)

        postdata = dict(account_id=account_id, language='en', dates=dateString)
        playerData = requests.post(self.playerDataByDateAPI, data=postdata)
        if playerData is None or '"error"' in playerData:
            print('Input String is not valid')
            # Quit this app
            exit(1)
        else:
            playerDataJson = json.loads(playerData.text)
            if not str(today) in playerDataJson and not str(yesterday in playerDataJson):
                print('There is currently no data for today and yesterday')
                return ''
            else:
                # Get useful information
                yesterdayData = ''
                todayData = ''
                daybeforeData = ''

                # Some player does not have enough data
                if not "\"pvp\":null" in playerData.text:
                    if str(yesterday) in playerDataJson['data'][str(account_id)]['pvp']:
                        yesterdayData = playerDataJson['data'][str(account_id)]['pvp'][str(yesterday)]
                    if str(today) in playerDataJson['data'][str(account_id)]['pvp']:
                        todayData = playerDataJson['data'][str(account_id)]['pvp'][str(today)]
                    if str(daybefore) in playerDataJson['data'][str(account_id)]['pvp']:
                        daybeforeData = playerDataJson['data'][str(account_id)]['pvp'][str(daybefore)]

                dataToday =  self.getDataForDate(todayData, yesterdayData)
                dataYesterday = self.getDataForDate(yesterdayData, daybeforeData)
                TYData = dataToday + dataYesterday

                # Today and Yesterday data
                return TYData

    # print out useful for this player
    def printInformation(self, data, account_id, todayData):

        winRateToday = 0
        averageDamageToday = 0
        averageXpToday = 0
        killdeathRatioToday = 0
        battleToday = 0

        winRateY = 0
        averageDamageY = 0
        averageXpY = 0
        killdeathRatioY = 0
        battleY = 0

        # Get data for today and yesterday
        if todayData == True:
            playerDataToday = self.getinformationForTodayAndYesterday(account_id)
            if not str(playerDataToday) == '':
                winRateToday = playerDataToday[0]
                averageXpToday = playerDataToday[1]
                killdeathRatioToday = playerDataToday[2]
                averageDamageToday = playerDataToday[3]
                battleToday = playerDataToday[4]
                winRateY = playerDataToday[5]
                averageXpY = playerDataToday[6]
                killdeathRatioY = playerDataToday[7]
                averageDamageY = playerDataToday[8]
                battleY = playerDataToday[9]

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

        print('\n' + str(username) + ' | ' + str(dateDiff) + ' day(s)')
        print('Service level: ' + str(serviceLevel))
        print('Total battles: ' + str(totalBattles) + ' ('
              + '{:.2f}'.format(averageBattlesPerDay) + '/day)'
              + ' | ' + str(battleToday) + ' | ' + str(battleY))
        print('Win rate: ' + '{:.2f}'.format(winRate) + '%'
              + ' | ' + '{:.2f}'.format(winRateToday) + '%'
              + ' | ' + '{:.2f}'.format(winRateY) + '%')
        print('Average EXP: ' + '{:.0f}'.format(averageXp)
              + ' | ' + '{:.0f}'.format(averageXpToday)
              + ' | ' + '{:.0f}'.format(averageXpY))
        print('Average damage: ' + '{:.0f}'.format(averageDamage)
              + ' | ' + '{:.0f}'.format(averageDamageToday)
              + ' | ' + '{:.0f}'.format(averageDamageY))
        print('Kill / Death Ratio: ' + '{:.2f}'.format(killdeathRatio)
              + ' | ' + '{:.2f}'.format(killdeathRatioToday)
              + ' | ' + '{:.2f}'.format(killdeathRatioY))
        print('Main battery hit ratio: ' + '{:.2f}'.format(hitRatio) + '%')
        point = self.activePoint(averageBattlesPerDay, serviceLevel)
        if point >= 5:
            print('This player is not active')

        # Newline
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

    def itisjustajoke(self):
        # Make player's stat all 99999
        print('The data above is not accurate!\nDisplaying Accurate Data')
        print('Service level: 99')
        print('Total battles: 99999')
        print('Win rate: 100%')
        print('Average EXP: 9999')
        print('Average damage: 99999')
        print('Kill / Death Ratio: NEVER DIED!')
        print('Main battery hit ratio: 100%\n')

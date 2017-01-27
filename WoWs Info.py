from WoWsClass import *
import sys

# Simple Interface
print('###   WoWs Info Python Alpha   ###\n----------------------------------')

# Whether a joke should be displayed
joke = False
# Whether show today's and yesterday's data
pastData = True

# Infinite loop until user quits
keepSearching = True
while keepSearching:
    try:
        WoWs = WoWsClass(3, 'demo')
        dataJson = WoWs.enterUsername()

        if dataJson != '':
            # Get the number of possible names
            element = len(dataJson['data'])

            # Infinite loop until get only one user name or 25 possible choices
            while not 1 <= element <= 25:
                if element == 0:
                    # Ask user to re-enter their name...
                    while (WoWs.getElementFromData(dataJson)) == 0:
                        dataJson = WoWs.enterUsername()
                elif element > 25:
                    # Ask user to re-enter their name...
                    while (WoWs.getElementFromData(dataJson)) > 25:
                        print('There are too many results, please re-enter your user name.')
                        dataJson = WoWs.enterUsername()

            # Choose a player or there is only one name
            if element == 1:
                # Print out user information
                account_id = dataJson['data'][0]['account_id']
            elif 1 < element <= 25:
                # Let user to choose their name
                account_id = dataJson['data'][int(WoWs.chooseUsername(element))]['account_id']

            # Print out user's id and get information about it
            print('\nYour Account ID is ' + str(account_id))

            # Get information from account_id and print it out
            playerData = WoWs.getInformationFromId(account_id)

            if playerData != '':
                # True for today's and yesterday's data. False for only average data
                WoWs.printInformation(playerData, account_id, pastData)

            # Display some random jokes
            if joke == True:
                WoWs.itisjustajoke()
                joke = False
    except:
        print("Error:", sys.exc_info()[0])
    finally:
        # Always ask for user input...
        againSearch = input('Would you like to search another player? (y/n): ')
        if againSearch == 'n':
            keepSearching = False

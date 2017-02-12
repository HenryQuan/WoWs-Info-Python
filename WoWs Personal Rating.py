import json

def getRatingComment(rating):
    # There are eight comment in total
    if rating >= 0 and rating <= 750:
        print('Keep it up')
    elif rating <= 1100:
        print('Below Average')
    elif rating <= 1350:
        print('Average')
    elif rating <= 1550:
        print('Good')
    elif rating <= 1750:
        print('Very Good')
    elif rating <= 2100:
        print('Great')
    elif rating <= 2450:
        print('Unicum')
    elif rating <= 9999:
        print('Super Unicum')
    else:
        print('Error')

print('\nWorld of Warship Personal Rating\n(http://wows-numbers.com/personal/rating)')

# load json file locally
with open('expected.json') as json_data:
    data = json.load(json_data)

# Get total number of data
shipCount = len(data['data'])

damage = 0
frag = 0
winRate = 0

# Accumulating averageDamage, averageFrags and average winRate
for key in data['data'].keys():
    damage += data['data'][key]['average_damage_dealt']
    frag += data['data'][key]['average_frags']
    winRate += data['data'][key]['win_rate']

expectedDamage = damage / shipCount
expectedFrags = frag / shipCount
expectedWinRate = winRate / shipCount

print('\n' + str(expectedDamage) + '\n' + str(expectedFrags) + '\n' + str(expectedWinRate) + '\n')

# Calculate with your data
# Change your data here... This is not accurate but only a estimated value. Please visit wows-number for more information
actualDmg = 99999
actualWins = 99.9
actualFrags = 99.9

rDmg = actualDmg/expectedDamage
rWins = actualWins/expectedWinRate
rFrags = actualFrags/expectedFrags

nDmg = max(0, (rDmg - 0.4) / (1 - 0.4))
nFrags = max(0, (rFrags - 0.1) / (1 - 0.1))
nWins = max(0, (rWins - 0.7) / (1 - 0.7))

PR = 700 * nDmg + 300 * nFrags + 150 * nWins
print('Your personal rate is ' + str(PR))
getRatingComment(PR)

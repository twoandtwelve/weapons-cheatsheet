import requests
from bs4 import BeautifulSoup

url = 'https://calamitymod.wiki.gg/wiki/Weapons'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

allWeapons = {}

# for loop through all div tags with class 'itemlist terraria'
for weapon in soup.find_all('div', class_='itemlist terraria'):

    # check the previous h3 tag for the weapon type
    weaponType = weapon.find_previous('h3').text

    # check the previous h4 tag for the stage of the game
    weaponStage = weapon.find_previous('h4').text

    # If weaponType is 'Other', prepend the text of the previous h2 tag
    if weaponType == 'Others' or weaponType == 'Other':
        previous_h2 = weapon.find_previous('h2').text.strip()
        if previous_h2 == 'Melee weapons':
            weaponType = 'Melee Other'
        elif previous_h2 == 'Ranged weapons':
            weaponType = 'Ranged Other'
        elif previous_h2 == 'Magic weapons':
            weaponType = 'Magic Other'
        elif previous_h2 == 'Summon weapons':
            weaponType = 'Summon Other'
        elif previous_h2 == 'Rogue Weapons':
            weaponType = 'Rogue Other'
        elif previous_h2 == 'Classless weapons':
            weaponType = 'Classless Other'

    # If weaponStage is 'Post Moon Lord', change it to 'Post-Moon Lord'
    if weaponStage == 'Post Moon Lord':
        weaponStage = 'Post-Moon Lord'

    # If weaponStage is 'Pre Hardmode', change it to 'Pre-Hardmode'
    if weaponStage == 'Pre Hardmode':
        weaponStage = 'Pre-Hardmode'

    # If weaponType is 'Boomerangs', if the previous h2 is 'Melee weapons', change it to 'Melee Boomerangs' andif the previous h2 is 'Rogue Weapons', change it to 'Rogue Boomerangs'
    if weaponType == 'Boomerangs':
        previous_h2 = weapon.find_previous('h2').text.strip()
        if previous_h2 == 'Melee weapons':
            weaponType = 'Melee Boomerangs'
        elif previous_h2 == 'Rogue Weapons':
            weaponType = 'Rogue Boomerangs'


    # for loop through all the a tags in the div tag
    for a in weapon.find_all('a'):
        weaponName = a.text
        weaponLink = a['href']

        if weaponName:  # Check if weaponName is not an empty string
            weaponLink = a['href']

            # make weaponName and weaponLink a tuple and append them to the allWeapons dictionary using the weaponType and weaponStage as the key
            # for example: allWeapons[('Swords', 'Pre-Hardmode')][0] = [('Basher', '/wiki/Basher')]
            allWeapons.setdefault((weaponType, weaponStage), []).append((weaponName, weaponLink))


# Make a list of all weapon types
weaponTypes = list(set([weaponType for weaponType, weaponStage in allWeapons.keys()]))

# Make a list of all weapon stages
weaponStages = list(set([weaponStage for weaponType, weaponStage in allWeapons.keys()]))

# in allWeapons, if there does not exist a key with the weaponType and weaponStage, add an empty list
for weaponType in weaponTypes:
    for weaponStage in weaponStages:
        allWeapons.setdefault((weaponType, weaponStage), [])


















    










# Connect to Google Sheets
#scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
#creds = Credentials.from_service_account_file("C:/Users/Jacky/Downloads/canvas-voltage-413712-79ca3c89bbc3.json", scopes=scope)
#client = gspread.authorize(creds)

# Open the Google Sheets document
#sheet = client.open('Calamity Weapons')

# Select the first worksheet
#worksheet = sheet.get_worksheet(0)

# Clear existing content in the worksheet
#worksheet.clear()



import requests
from bs4 import BeautifulSoup

def parseWeapons(soup):

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

        # If weaponType is 'Boomerangs', if the previous h2 is 'Melee weapons', change it to 'Melee Boomerangs' and if the previous h2 is 'Rogue Weapons', change it to 'Rogue Boomerangs'
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

    return allWeapons

def printWeapons(allWeapons):
    numWeapons = 0
    craftableWeapons = 0
    purchasableWeapons = 0
    fishedWeapons = 0
    droppedAndChestWeapons = 0
    exhumedWeapons = 0
    somethingElse = 0

    # loop through all the keys in allWeapons and loop through all the weapons in the lists
    for weaponType, weaponStage in allWeapons.keys():
        for weaponName, weaponLink in allWeapons[(weaponType, weaponStage)]:
            
            
            url = 'https://calamitymod.wiki.gg' + weaponLink
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')  

            # check if there is an h3 tag with the text 'Recipe'
            if soup.find('h3', string='Recipe'):
                craftableWeapons += 1
                print(weaponName + ' is craftable')
                
            # check if there is a th tag with the text 'Dropped by'
            elif soup.find('th', string='Dropped by'):
                droppedAndChestWeapons += 1
                print(weaponName + ' is dropped')

            # check if there is a p tag that contains the text 'sold by the' or 'purchased from the'
            elif soup.find(lambda tag: tag.name == 'p' and ('sold by the' in tag.text.lower() or 'purchased from the' in tag.text.lower())):
                purchasableWeapons += 1
                print(weaponName + ' is purchasable')


            # check if there is a p tag that contains the text 'fished' or 'fishing'
            elif soup.find(lambda tag: tag.name == 'p' and ('fished' in tag.text.lower() or 'fishing' in tag.text.lower())):
                fishedWeapons += 1
                print(weaponName + ' is fished')

            # check if there is a p tag that contains the text 'exhumed'
            elif soup.find(lambda tag: tag.name == 'p' and 'exhumed' in tag.text.lower()):
                exhumedWeapons += 1
                print(weaponName + ' is exhumed')

            
            else:
                print(weaponName + ' something else...')
                somethingElse += 1
            
            numWeapons += 1


    # print the number of weapons that are craftable, purchasable, and dropped
    print('Craftable Weapons: ' + str(craftableWeapons))
    print('Purchasable Weapons: ' + str(purchasableWeapons))
    print('Fished Weapons: ' + str(fishedWeapons))
    print('Dropped and Looted Weapons: ' + str(droppedAndChestWeapons))
    print('Exhumed Weapons: ' + str(exhumedWeapons))
    print('Something Else: ' + str(somethingElse))
    print('Total Weapons: ' + str(numWeapons))

#######################################################################################################
def main():
    url = 'https://calamitymod.wiki.gg/wiki/Weapons'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    allWeapons = parseWeapons(soup)

    # Make a list of all weapon types
    weaponTypes = list(set([weaponType for weaponType, weaponStage in allWeapons.keys()]))

    # Make a list of all weapon stages
    weaponStages = list(set([weaponStage for weaponType, weaponStage in allWeapons.keys()]))

    # in allWeapons, if there does not exist a key with the weaponType and weaponStage, add an empty list
    for weaponType in weaponTypes:
        for weaponStage in weaponStages:
            allWeapons.setdefault((weaponType, weaponStage), [])


    printWeapons(allWeapons)


if __name__ == "__main__":
    main()



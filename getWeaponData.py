import requests
from bs4 import BeautifulSoup
from datetime import datetime

def parseWeapons(soup):
    allWeapons = {}
    for weapon in soup.find_all('div', class_='itemlist terraria'):
        weaponType = weapon.find_previous('h3').text
        weaponStage = weapon.find_previous('h4').text

        if weaponType == 'Others' or weaponType == 'Other':
            previous_h2 = weapon.find_previous('h2').text.strip()
            if previous_h2 == 'Melee weapons':
                weaponClass = 'Melee'
                weaponType = 'Melee Other'
            elif previous_h2 == 'Ranged weapons':
                weaponClass = 'Ranged'
                weaponType = 'Ranged Other'
            elif previous_h2 == 'Magic weapons':
                weaponClass = 'Magic'
                weaponType = 'Magic Other'
            elif previous_h2 == 'Summon weapons':
                weaponClass = 'Summon'
                weaponType = 'Summon Other'
            elif previous_h2 == 'Rogue Weapons':
                weaponClass = 'Rogue'
                weaponType = 'Rogue Other'
            elif previous_h2 == 'Classless weapons':
                weaponClass = 'Classless'
                weaponType = 'Classless Other'
        else:
            weaponClass = weapon.find_previous('h2').text.strip().split()[0]

        if weaponStage == 'Post Moon Lord':
            weaponStage = 'Post-Moon Lord'
        if weaponStage == 'Pre Hardmode':
            weaponStage = 'Pre-Hardmode'
        if weaponType == 'Boomerangs':
            previous_h2 = weapon.find_previous('h2').text.strip()
            if previous_h2 == 'Melee weapons':
                weaponClass = 'Melee'
                weaponType = 'Melee Boomerangs'
            elif previous_h2 == 'Rogue Weapons':
                weaponClass = 'Rogue'
                weaponType = 'Rogue Boomerangs'

        for a in weapon.find_all('a'):
            weaponName = a.text
            weaponLink = a['href']
            if weaponName:
                weaponLink = a['href']
                allWeapons.setdefault((weaponType, weaponStage), []).append((weaponName, weaponClass, weaponLink))

    return allWeapons

def printWeapons(allWeapons):
    numWeapons = 0
    craftableWeapons = 0
    purchasableWeapons = 0
    fishedWeapons = 0
    droppedAndChestWeapons = 0
    exhumedWeapons = 0
    somethingElse = 0

    for weaponType, weaponStage in allWeapons.keys():
        for weaponName, weaponClass, weaponLink in allWeapons[(weaponType, weaponStage)]:
            url = 'https://calamitymod.wiki.gg' + weaponLink
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')  

            if soup.find('h3', string='Recipe'):
                craftableWeapons += 1
                print(weaponName + ' is craftable')
            elif soup.find('th', string='Dropped by'):
                droppedAndChestWeapons += 1
                print(weaponName + ' is dropped')
            elif soup.find(lambda tag: tag.name == 'p' and ('sold by the' in tag.text.lower() or 'purchased from the' in tag.text.lower())):
                purchasableWeapons += 1
                print(weaponName + ' is purchasable')
            elif soup.find(lambda tag: tag.name == 'p' and ('fished' in tag.text.lower() or 'fishing' in tag.text.lower())):
                fishedWeapons += 1
                print(weaponName + ' is fished')
            elif soup.find(lambda tag: tag.name == 'p' and 'exhumed' in tag.text.lower()):
                exhumedWeapons += 1
                print(weaponName + ' is exhumed')
            else:
                print(weaponName + ' something else...')
                somethingElse += 1
            numWeapons += 1

    print('Craftable Weapons: ' + str(craftableWeapons))
    print('Purchasable Weapons: ' + str(purchasableWeapons))
    print('Fished Weapons: ' + str(fishedWeapons))
    print('Dropped and Looted Weapons: ' + str(droppedAndChestWeapons))
    print('Exhumed Weapons: ' + str(exhumedWeapons))
    print('Something Else: ' + str(somethingElse))
    print('Total Weapons: ' + str(numWeapons))

def writeWeaponsToFile(allWeapons, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"Script completed at: {completion_time}\n")
        for (weaponType, weaponStage), weapons_list in allWeapons.items():
            for weaponName, weaponClass, weaponLink in weapons_list:
                line = f"{weaponName} | {weaponClass} | {weaponStage} | {weaponType} | {weaponLink}\n"
                f.write(line)

#######################################################################################################
def main():
    start_time = datetime.now()
    
    url = 'https://calamitymod.wiki.gg/wiki/Weapons'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    allWeapons = parseWeapons(soup)
    writeWeaponsToFile(allWeapons, 'weapons.txt')
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print(f"Completed successfully. Runtime of {duration} s.")

if __name__ == "__main__":
    main()

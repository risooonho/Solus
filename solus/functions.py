#from classes import *
from dicts import *

def quit_querry(game):
    while True:
        y_n = raw_input('Do you want to quit?\nY/N:')

        if y_n == 'Y' or y_n == 'y':
            print('BYE!!!')
            game.is_running = False
            break
        elif y_n == 'N' or y_n == 'n':
            print('Keep playing!')
            break
        else:
            print('TRY AGAIN!')

#Function creates a new player with name and difficulty from user, returns player object
def create_player():
    player_name = ''
    #Check input, if valid name then set player_name, if not then ask again
    while not player_name:
        player_name = raw_input(PROMPTS['create player'])
        if not player_name:
            print('TRY AGAIN!')

    #Check input, if valid number and valid range then set difficulty, if not then ask again
    while True:
        try:
            difficulty = int(raw_input(PROMPTS['choose difficulty']))
        except ValueError:
            print('TRY AGAIN!')
            continue

        if 1 <= difficulty <= 3:
            break
        else:
            print('TRY AGAIN!')
            continue

    #create player with above info
    player= Player(player_name, difficulty)
    return player

#Function handles an encounter with another character.
#Need to add more options for encounter, run, etc...
def encounter(A,B):
    #while loop for input
    #while True:
        #y_n = raw_input('Do you want to fight %s?\nY/N:'% B.name)

        #if y_n == 'Y' or y_n == 'y':

    fight(A, B)


        #break
        #elif y_n == 'N' or y_n == 'n':
            #print('BYE!')
            #break
        #else:
            #print('TRY AGAIN!')

#Function initiates a fight, takes character objects A attacks first.
#Function calls strike function which will modify character health and is_alive.
def fight(A, B):
    #unpack stats into a temp list
    a = [A.hp, A.attk, A.dfnc, A.is_alive]
    b = [B.hp, B.attk, B.dfnc, B.is_alive]
    #Initiate loop if both chars are alive
    while a[3] and b[3]:
        #Strike called with A attacking B, modifies B's hp
        b[0], b[3] = strike(a, b)
        #if b is still alive...
        if b[3]:
            #Strike called with B attacking A, modifies A's hp
            a[0], a[3] = strike(b, a)
            if not a[3]:
                A.kill()
                break
        #if B is not alive
        else:
            B.kill()
            #end the fight
            break
    #repack stats into attributes
    A.hp, A.attk, A.dfnc, A.is_alive = a
    B.hp, B.attk, B.dfnc, B.is_alive = b

#Function handles an individual attack in a fight. takes the stats of the fighters
#Returns defenders stats (the attacker's stats do not change)
def strike(attkr_stats, dfndr_stats):
    #if defenders defence is larger than attackers attact, reduce defenders hp by half attack value
    if dfndr_stats[2] >= attkr_stats[1]:
        #Reduce defenders hp by attack value
        dfndr_stats[0] -= attkr_stats[1]/2

    #if defenders defence is smaller than attackers attact, reduce defenders hp by full attack value
    elif dfndr_stats[2] <= attkr_stats[1]:
        dfndr_stats[0] -= attkr_stats[1]
    #Rraise flag if neither happens
    else:
        print('Something went wrong in strike()')
    #Check if defender is dead at the end of the strike
    if dfndr_stats[0] <= 0:
        #set defender is_alive to false
        dfndr_stats[3] = False
    #Returns defender's updated stats (only things changed should be hp and is_alive)
    return (dfndr_stats[0], dfndr_stats[3])

#Function applies weapons bonus to character, takes character and weapon name
def equip_weapon(character, name):
    #look through inventory for item wanted to equip
    for i in range(len(character.inventory)):
        #if item in inventory matches the one wanted ...
        if character.inventory[i].name == name:
            #add bonus to characte's attack and set equipped
            character.attk += character.inventory[i].attk_bonus
            character.inventory[i].is_equipped = True
            return
    #Flag that no item was found
    print('That item was not found and not equipped!')

#Function picks up equipment and adds to inventory
#Need check for inventory size and inventory limiting
def pickup_equipment(character, equipment):
    character.inventory.append(equipment)
    equip_weapon(character, equipment.name)
    equipment.kill()

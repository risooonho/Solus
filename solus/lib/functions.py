"""Docstring for Functions."""


def quit_querry(game):
    """Ask player if they want to quit."""
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


# Function handles an encounter with another character.
# Need to add more options for encounter, run, etc...


def encounter(A, B):
    """Facilitate an encounter."""
    fight(A, B)


def fight(A, B):
    """Facilitate a fight between two characters, modifies stats in-place."""
    # unpack stats into a temp list
    a = [A.hp, A.attk, A.dfnc, A.is_alive]
    b = [B.hp, B.attk, B.dfnc, B.is_alive]
    # Initiate loop if both chars are alive
    while a[3] and b[3]:
        # Strike called with A attacking B, modifies B's hp
        b[0], b[3] = strike(a, b)
        # if b is still alive...
        if b[3]:
            # Strike called with B attacking A, modifies A's hp
            a[0], a[3] = strike(b, a)
            if not a[3]:
                A.kill()
                break
        # if B is not alive
        else:
            B.kill()
            # end the fight
            break
    # repack stats into attributes
    A.hp, A.attk, A.dfnc, A.is_alive = a
    B.hp, B.attk, B.dfnc, B.is_alive = b


def strike(attkr_stats, dfndr_stats):
    """Facilitate a strike from attacker to defender. Return defender stats."""
    # if defenders defence is larger than attackers attact,
    # reduce defenders hp by half attack value
    if dfndr_stats[2] >= attkr_stats[1]:
        # Reduce defenders hp by attack value
        dfndr_stats[0] -= attkr_stats[1] / 2

    # if defenders defence is smaller than attackers attact, reduce defenders
    # hp by full attack value
    elif dfndr_stats[2] <= attkr_stats[1]:
        dfndr_stats[0] -= attkr_stats[1]
    # Rraise flag if neither happens
    else:
        print('Something went wrong in strike()')
    # Check if defender is dead at the end of the strike
    if dfndr_stats[0] <= 0:
        # set defender is_alive to false
        dfndr_stats[3] = False
    # Returns defender's updated stats (change hp and is_alive)
    return (dfndr_stats[0], dfndr_stats[3])

# Function applies weapons bonus to character, takes character and weapon name


def equip_weapon(character, name):
    """Apply weapon stats to character."""
    # look through inventory for item wanted to equip
    for i in range(len(character.inventory)):
        # if item in inventory matches the one wanted ...
        if character.inventory[i].name == name:
            # add bonus to characte's attack and set equipped
            character.attk += character.inventory[i].attk_bonus
            character.inventory[i].is_equipped = True
            return
    # Flag that no item was found
    print('That item was not found and not equipped!')

# Function picks up equipment and adds to inventory
# Need check for inventory size and inventory limiting


def pickup_equipment(character, equipment):
    """Add equipment to character's inventory and remove sprite from map."""
    character.inventory.append(equipment)
    if len(character.inventory) == 1:
        equip_weapon(character, equipment.name)
    equipment.kill()

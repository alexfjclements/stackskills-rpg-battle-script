from classes.game import Person, bcolours
from classes.magic import spell
from classes.inventory import Item
import random


# Create Black Magic
fire = spell("Fire", 25, 600, "black")
thunder = spell("Thunder", 25, 600, "black")
blizzard = spell("Blizzard", 25, 600, "black")
meteor = spell("Meteor", 40, 1200, "black")
quake = spell("Quake", 14, 140, "black")

# Create White Magic
cure = spell("Cure", 25, 620, "white")
cura = spell("Cura", 32, 1500, "white")
curaga = spell("Curaga", 50, 6000, "white")

# Create some Items
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Super Potion", "potion", "Heals 500 HP", 1000)
elixer = Item("Elixer", "elixer", "Fully restores HP/MP of one party member", 9999)
hielixer = Item("Mega Elixer", "elixer", "Fully restores party HP/MP", 9999)

grenade = Item("Grenade", "attack", "Deals 500 damage", 500)

player_spells = [fire, thunder, blizzard, meteor, cure, cura]
enemy_spells = [fire, meteor, curaga]
player_items = [{"item": potion, "quantity": 15}, {"item": hipotion, "quantity": 5},
                {"item": superpotion, "quantity": 5}, {"item": elixer, "quantity": 5},
                {"item": hielixer, "quantity": 5}, {"item": grenade, "quantity": 5}]

# Instantate People
player1 = Person("Valos:", 3260, 132, 300, 34, player_spells, player_items)
player2 = Person("Nick :", 4160, 188, 311, 34, player_spells, player_items)
player3 = Person("Robot:", 3089, 174, 288, 34, player_spells, player_items)

enemy1 = Person("Imp  ", 1250, 130, 560, 325, enemy_spells, [])
enemy2 = Person("Magus", 11200, 701, 525, 25, enemy_spells, [])
enemy3 = Person("Imp  ", 1250, 130, 560, 325, enemy_spells, [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

running = True

print(bcolours.FAIL + bcolours.BOLD + "AN ENEMY ATTACKS!" + bcolours.ENDC)

while running:
    print("=======================================================================")

    # Print out player and enemy stats
    print("\n\n")
    print("NAME                     HP                                        MP")
    for player in players:
        player.get_stats()

    print("\n")

    for enemy in enemies:
        enemy.get_enemy_stats()

    # Allow players to choose actions
    for player in players:

        player.choose_action()
        choice = input("    Choose action: ")
        index = int(choice) - 1

        # If player attacks:
        if index == 0:
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)
            enemies[enemy].take_damage(dmg)
            print("You attacked " + enemies[enemy].name.replace(" ", "") + " for", dmg, "points of damage.")

            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name.replace(" ", "") + " has died.")
                del enemies[enemy]

            # Check if player won.
            if len(enemies) == 0:
                print(bcolours.OKGREEN + "You win!" + bcolours.ENDC)
                running = False

        # If player chooses magic:
        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("    Choose magic: ")) - 1

            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolours.FAIL + "\nNot enough MP\n" + bcolours.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == "white":
                player.heal(magic_dmg)
                print(bcolours.OKBLUE + "\n" + spell.name + " heals for", str(magic_dmg), "HP." + bcolours.ENDC)

            elif spell.type == "black":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(magic_dmg)
                print(bcolours.OKBLUE + "\n" + spell.name + " deals", str(magic_dmg), "points of damage to " + enemies[enemy].name.replace(" ", "") + bcolours.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ", "") + " has died.")
                    del enemies[enemy]

                # Check if player won.
                if len(enemies) == 0:
                    print(bcolours.OKGREEN + "You win!" + bcolours.ENDC)
                    running = False

        # If player chooses items:
        elif index == 2:
            player.choose_item()
            item_choice = int(input("    Choose item: ",)) - 1

            if item_choice == -1:
                continue

            if player.items[item_choice]["quantity"] == 0:
                print(bcolours.FAIL + "\n" + "None left..." + bcolours.ENDC)
                continue

            item = player.items[item_choice]["item"]
            player.items[item_choice]["quantity"] -= 1

            if item.type == "potion":
                player.heal(item.prop)
                print(bcolours.OKGREEN + "\n" + item.name + " heals for", str(item.prop), "HP" + bcolours.ENDC)

            elif item.type == "elixer":

                if item.name == "Mega Elixer":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp

                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                print(bcolours.OKGREEN + "\n" + item.name + " fully restores HP/MP" + bcolours.ENDC)

            elif item.type == "attack":

                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(item.prop)
                print(bcolours.FAIL + "\n" + item.name + " deals", str(item.prop), "points of damage to " + enemies[enemy].name.replace(" ", "") + bcolours.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ", "") + " has died.")
                    del enemies[enemy]

                # Check if player won.
                if len(enemies) == 0:
                    print(bcolours.OKGREEN + "You win!" + bcolours.ENDC)
                    running = False

    print("\n")
    # Enemy attack phase.
    for enemy in enemies:
        enemy_choice = random.randrange(0, 2)

        # If enemy chooses magic:
        if enemy_choice == 1:
            spell, magic_dmg = enemy.choose_enemy_spell()

            if magic_dmg == 0:
                enemy_choice = 0

            else:
                enemy.reduce_mp(spell.cost)

                if spell.type == "white":
                    enemy.heal(magic_dmg)
                    print(bcolours.OKBLUE + spell.name + " heals " + enemy.name.replace(" ", "") + " for", str(magic_dmg),
                          "HP." + bcolours.ENDC)

                elif spell.type == "black":
                    target = random.randrange(0, 3)
                    players[target].take_damage(magic_dmg)
                    print(bcolours.OKBLUE + enemy.name.replace(" ", "") + "'s " + spell.name + " deals", str(magic_dmg),
                          "points of damage to " +
                          players[target].name.replace(" ", "") + bcolours.ENDC)

                    if players[target].get_hp() == 0:
                        print(players[target].name.replace(" ", "") + " has died.")
                        del players[target]

                    # Check if enemy won.
                    if len(players) == 0:
                        print(bcolours.FAIL + "Your enemies have defeated you!" + bcolours.ENDC)
                        running = False

        # If enemy chooses attack:
        if enemy_choice == 0:
            # Chose attack.
            target = random.randrange(0, 3)
            enemy_dmg = enemy.generate_damage()

            players[target].take_damage(enemy_dmg)
            print(enemy.name.replace(" ", "") + " attacks " + players[target].name.replace(" ", "") + " for", enemy_dmg, "points of damage.")

            if players[target].get_hp() == 0:
                print(players[target].name.replace(" ", "") + " has died.")
                del players[target]

            # Check if enemy won.
            if len(players) == 0:
                print(bcolours.FAIL + "Your enemies have defeated you!" + bcolours.ENDC)
                running = False
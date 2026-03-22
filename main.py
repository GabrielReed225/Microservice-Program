import time
import json
import os
import csv

def main_menu():
    """Prints the main menu instructions and options"""
    print()
    print("Type 1-5 to select the corresponding option")
    print("Type 1 to start game")
    print("Type 2 to for help")
    print("Type 3 to load a saved game")
    print("Type 4 to delete a saved game")
    print("Type 5 to exit")
    return

def class_choice():
    """Prints the class choice instructions and options"""
    print()
    print("Type 1 to choose Wizard as your class")
    print("Type 2 to choose Cleric as your class")
    print("Type 3 to choose Rogue as your class")
    print("Type 4 to choose Fighter as your class")
    print("Type 5 to choose Artificer as your class")
    print("Type 6 to learn more about each class")

def game_menu():
    """Prints the game menu instructions and options"""
    print()
    print("How would you like to proceed adventurer? Type 1-5 to select the corresponding option")
    print("Type 1 to view the immediate area")
    print("Type 2 to view inventory")
    print("Type 3 to move")
    print("Type 4 to see character stats")
    print("Type 5 to save game")
    print("Type 6 to Quit and return to main menu")

def movement():
    while True:
        print()
        print("Type 1-4 to enter your movement")
        print("Type 1 to move North")
        print("Type 2 to move South")
        print("Type 3 to move East")
        print("Type 4 to move West")
        print()
        user_movement = movement_input()
        if user_movement == "Invalid":
            continue
        else:
            return user_movement


def movement_input():
    try:
        user_movement = int(input("Please enter your movement: "))
        if user_movement > 4 or user_movement < 1:
            print("Please enter a number between 1 and 4")
            return "Invalid"
        if user_movement == 1:
            return "North"
        elif user_movement == 2:
            return "South"
        elif user_movement == 3:
            return "East"
        elif user_movement == 4:
            return "West"
        else:
            print("Please enter a number between 1 and 4")
            return "Invalid"
    except ValueError:
        print("Please enter a number between 1 and 4")
        return "Invalid"

def inventory(character):
    deletable_items = []
    count = 1
    for item in character["inventory"]:
        if not item['unique']:
            deletable_items.append(item["name"])
        print(f"{count} - {item["name"]} x{item['quantity']}")
        count += 1
    while True:
        print()
        print("What would you like to do next? Type the corresponding number.")
        print("Type 1 to use an item")
        print("Type 2 to see item description")
        print("Type 3 to return")
        try:
            print()
            options = int(input("Input: "))
            if options == 1:
                while True:
                    try:
                        print()
                        print("Enter the number corresponding to the item you wish to use, type 0 to cancel")
                        print()
                        count = 1
                        for item in character["inventory"]:
                            if not item['unique']:
                                print(f"{count} - {item["name"]} x{item['quantity']}")
                                count += 1
                        print()
                        optionss = int(input("Input: "))
                        if optionss == 0:
                            break
                        if optionss < 1 or optionss > len(deletable_items):
                            print("Invalid input, try again")
                            continue
                        print()
                        print(f"Are you certain you wish to use {deletable_items[optionss - 1]}?")
                        user_input = input("Y/N: ")
                        if user_input == 'Y':
                            if character["health"] == character["max_health"]:
                                print("You are already at full health!")
                                continue
                            remove_item(character["inventory"], deletable_items[optionss - 1])
                            if deletable_items[optionss - 1] == "healing potion":
                                character["health"] += character["max_health"] * 0.5
                                if character["health"] > character["max_health"]:
                                    character["health"] = character["max_health"]
                            print("Item used and removed from your inventory!")
                            break
                        if user_input == 'N':
                            continue
                        else:
                            print("Invalid choice, try again")
                    except IndexError:
                        print("You do not have that many unique items in your inventory! Try again")
                        print()
                        continue
                    except ValueError:
                        print("Invalid choice, try again")
                        continue
                continue
            elif options == 2:
                while True:
                    try:
                        print()
                        print("Enter the number corresponding to which items description you want")
                        print()
                        count = 1
                        for item in character["inventory"]:
                            print(f"{count} - {item["name"]} x{item['quantity']}")
                            count += 1
                        print()
                        user_choice = int(input("Input: "))
                        print()
                        if user_choice < 1 or user_choice > len(character["inventory"]):
                            print("Invalid choice, try again")
                            continue
                        print(character["inventory"][user_choice - 1]["description"])
                        break
                    except IndexError:
                        print("You do not have that many unique items in your inventory! Try again")
                        continue
                    except ValueError:
                        print("Invalid choice, try again")
                        continue
                continue
            elif options == 3:
                game_menu()
                break
            else:
                print("Invalid choice, try again")
                continue

        except ValueError:
            print("Invalid choice, try again")
            continue


def add_item(inventory, item_name, unique, description):
    for item in inventory:
        if item["name"] == item_name and item["unique"]:
            return
    if unique:
        inventory.append({
            "name": item_name,
            "unique": unique,
            "quantity": 1,
            "description": description
        })
        return

    for item in inventory:
        if item["name"] == item_name and not item["unique"]:
            item["quantity"] += 1
            return

    inventory.append({
        "name": item_name,
        "unique": unique,
        "quantity": 1,
        "description": description
    })

def remove_item(inventory, name):
    for index, item in enumerate(inventory):
        if item["name"] == name:
            if item["unique"]:
                return # unique items cannot be removed
            item["quantity"] -= 1
            if item["quantity"] == 0:
                inventory.pop(index)
            return


def random_gen(action, number1: int, number2: int):

    service_dir = "RNG"

    request_data = {
        "action": action,
        "min_value": number1,
        "max_value": number2,
    }

    request_path = os.path.join(service_dir, "request.json")
    with open(request_path, "w") as f:
        json.dump(request_data, f, indent=4)


    response_path = os.path.join(service_dir, "response.json")
    while True:
        try:
            with open(response_path, "r") as f:
                data = json.load(f)
                break
        except (json.JSONDecodeError, FileNotFoundError):
            time.sleep(0.1)
            continue
    response = data.get("result")

    os.remove(response_path)
    return response

def key_generation():
    service_dir = "CUD"

    read_path = os.path.join(service_dir, "data.json")
    while True:
        try:
            with open(read_path, "r") as f:
                data = json.load(f)
                break
        except (json.JSONDecodeError, FileNotFoundError):
            time.sleep(0.1)
            continue
    if not data:
        key = 1
    else:
        key = 1
        for item in data:
            key += 1
    return key

def read_game_save():
    service_dir = "CUD"

    read_path = os.path.join(service_dir, "data.json")
    while True:
        try:
            with open(read_path, "r") as f:
                data = json.load(f)
                break
        except (json.JSONDecodeError, FileNotFoundError):
            time.sleep(0.1)
            continue
    for item in data:
        print(data[item])
    return data


def game_save_CUD(operation, character_data, key=None):
    service_dir = "CUD"

    if operation == "create":
        key = key_generation()

    request_data = {
        "operation": operation,
        "file": "./data.json",
        "key": key,
        "entry": character_data,
    }

    request_path = os.path.join(service_dir, "request.json")
    with open(request_path, "w") as f:
        json.dump(request_data, f, indent=4)

    response_path = os.path.join(service_dir, "response.json")
    while True:
        try:
            with open(response_path, "r") as f:
                data = json.load(f)
                break
        except (json.JSONDecodeError, FileNotFoundError):
            time.sleep(0.1)
            continue
    response = data.get("result")
    os.remove(response_path)
    return response

def retreive_game(task):
    data = read_game_save()
    if not data:
        return ("Invalid")
    max_key = key_generation()
    while True:
        try:
            print()
            print(f"Enter the number corresponding to the game you wish to access, type {max_key} to see the list of saves again")
            choice = int(input("Input: "))

            if choice < 1 or choice > max_key:
                print("Invalid choice, try again")
                continue
            elif choice == max_key:
                read_game_save()
                continue
            else:
                if task == "load":
                    return read_game_save()[str(choice)]
                elif task == "delete":
                    return str(choice), read_game_save()[str(choice)]
                elif task == "update":
                    return str(choice)

        except ValueError:
            print("Invalid choice, try again")
            continue


def damage_calculator(operation: str, number1: int, number2: int):

    service_dir = "add-subtract"

    request_data = {
        "operation": operation,
        "number1": number1,
        "number2": number2
    }

    request_path = os.path.join(service_dir, "request.json")
    with open(request_path, "w") as f:
        json.dump(request_data, f, indent=4)


    response_path = os.path.join(service_dir, "response.json")
    while True:
        try:
            with open(response_path, "r") as f:
                data = json.load(f)
                break
        except (json.JSONDecodeError, FileNotFoundError):
            time.sleep(0.1)
            continue
    response = data.get("result")

    os.remove(response_path)
    return response


def print_csv_lines(filename):
    """Reads a CSV file and prints each row as a list."""
    with open(filename, newline='') as csvfile:
        reader_obj = csv.reader(csvfile)
        for row in reader_obj:
            print(row)

def generate_report(character_data):
    character_data = {"name": character_data["name"],
                 "class": character_data["class"],
                 "health": character_data["health"],
                 "max_health": character_data["max_health"],
                 "damage": character_data["damage"],
                 "attack ability": character_data["attack ability"],
                 "special ability": character_data["special ability"],
                 "location": character_data["location"],
                 "subzone": character_data["subzone"],
                 }

    service_dir = "report-generator"

    request_data = {
        "data_source": "dictionary",
        "data": character_data
    }

    request_path = os.path.join(service_dir, "request.json")
    with open(request_path, "w") as f:
        json.dump(request_data, f, indent=4)

    response_path = os.path.join(service_dir, "response.json")
    while True:
        try:
            with open(response_path, "r") as f:
                data = json.load(f)
                break
        except (json.JSONDecodeError, FileNotFoundError):
            time.sleep(0.1)
            continue

    response = data.get("csv_file")
    response = os.path.join(service_dir, response)

    print_csv_lines(response)
    os.remove(response_path)
    return

def navigation(character, direction):
    service_dir = "navigation"
    request_data = {
        "file": "./navigation.json",
        "key": direction,
        "location": (character["location"], character["subzone"])
    }
    request_path = os.path.join(service_dir, "request.json")
    with open(request_path, "w") as f:
        json.dump(request_data, f, indent=4)


    response_path = os.path.join(service_dir, "response.json")
    while True:
        try:
            with open(response_path, "r") as f:
                data = json.load(f)
                break
        except (json.JSONDecodeError, FileNotFoundError):
            time.sleep(0.1)
            continue
    response = data.get("result")

    os.remove(response_path)
    return response

def random_event(character_stats, descriptions):
    if character_stats["location"] == 'The Valley of the Gods':
        events = {
            "1": "You run across a highwayman!",
            "2": "The ground beneath you gives way, and you find yourself in a cavern",
            "3": "A sudden storm causes you to take shelter",
            "4": "You see a strange woman with a robe",
        }
        chosen_event = random_gen("generate_integer", 1, 2)
        output = str(chosen_event)
        if chosen_event == 1:
            while True:
                try:
                    print()
                    print(f"{events[output]} How do you proceed?")
                    print("Type 1 to engage combat")
                    print("Type 2 to flee and return to previous location")
                    if character_stats["class"] == 'fighter':
                        print("Type 3 to 'convince' the highwayman he doesnt want to fight you")
                    print()
                    choice = int(input("Response: "))
                    if choice < 1 or choice > 2:
                        print("Invalid choice. Try again.")
                        continue
                    if choice == 2:
                        print("Retreating ... ")
                        time.sleep(1)
                        return 1
                    if choice == 1:
                        print("Engaging highwayman in combat.")
                        highwayman_health = 36
                        while True:
                            try:
                                print()
                                print("How do you proceed?")
                                print(f"Type 1 to use {character_stats['attack ability']} ")
                                print("Type 2 to open inventory")
                                print("Type 3 to flee and return to previous location")
                                print()
                                choice = int(input("Response: "))
                                if choice < 1 or choice > 3:
                                    print("Invalid choice. Try again.")
                                    continue
                                if choice == 3:
                                    print("Retreating ... ")
                                    time.sleep(1)
                                    return 1
                                if choice == 2:
                                    inventory(character_stats)
                                    continue
                                if choice == 1:
                                    print()
                                    print(f"Using {character_stats['attack ability']}")
                                    print(f"You hit highwayman for {character_stats['damage']} damage!")
                                    highwayman_health = damage_calculator("subtract", highwayman_health, character_stats["damage"])
                                    if highwayman_health == 0:
                                        break
                                    print()
                                    print("Highwayman attacks back!")
                                    time.sleep(1)
                                    attack = random_gen("generate_integer",2, 5)
                                    print(f"Highwayman attacks you for {attack} points of damage")
                                    character_stats['health'] = damage_calculator("subtract", character_stats['health'], attack)
                                    if character_stats["health"] <= 0:
                                        return -1

                                if choice == 4:
                                    if character_stats["class"] == 'fighter':
                                        print()
                                        print("The highwayman runs away")
                                        break
                                    else:
                                        print("Invalid choice. Try again.")
                                        continue


                            except ValueError:
                                print("Invalid choice. Try again.")
                                continue
                        add_item(character_stats['inventory'], "healing potion", False, "restore 50% of a user's max health")
                        print("Highwayman defeated! You receive a healing potion!")
                        return 1
                except ValueError:
                    print("Invalid choice, try again")
                    continue
        if chosen_event == 2:
            have_rope = 0
            for item in character_stats["inventory"]:
                if item['name'] == 'rope':
                    have_rope += 1
            while True:
                try:
                    print()
                    print(f"{events[output]} How do you proceed?")
                    print("Type 1 to follow the tunnel")
                    if have_rope == 1:
                        print("Type 2 to use your rope and return to previous location")
                    print()
                    if character_stats["class"] == "wizard":
                        print("Type 3 to teleport to back up")
                    choice = int(input("Response: "))
                    if choice < 1 or choice > 3:
                        print("Invalid choice. Try again.")
                        continue
                    if choice == 2:
                        if have_rope == 1:
                            print("You use the rope to climb out of the tunnel and return to previous location ")
                            break
                        else:
                            print("Invalid choice. Try again.")
                            continue
                    if choice == 1:
                        loc = random_gen("generate_integer", 1, 3)
                        character_stats["subzone"] = loc
                        print(f"You emerge from the tunnel at {descriptions[character_stats["location"]][character_stats["subzone"]]["main"]}")
                        break
                    if choice == 3:
                        if character_stats["class"] == "wizard":
                            break
                        else:
                            print("Invalid choice. Try again.")
                            continue


                except ValueError:
                    print("Invalid choice, try again")
                    continue

        if chosen_event == 3:
            while True:
                try:
                    print()
                    print(f"{events[output]}")
                    print("After taking shelter, you notice a half-buried chest. How do you proceed?")
                    print("Type 1 to ignore the chest")
                    print("Type 2 to inspect the chest")
                    print("Type 3 to open the chest")
                    if character_stats["class"] == "artificer" or character_stats["class"] == "rogue":
                        print("Type 4 to carefully and safely open the chest")
                    print()
                    choice = int(input("Response: "))
                    if choice < 1 or choice > 4:
                        print("Invalid choice. Try again.")
                        continue
                    if choice == 1:
                        return 1
                    if choice == 2:
                        check = random_gen("generate_integer",1, 2)
                        if check == 2:
                            print("Upon inspection, you realized the chest is cursed and you proceed to ignore it")
                            return 1
                        if check == 2:
                            print("You determine that the chest is safe to open")
                            add_item(character_stats['inventory'], "gold coin", False, "currency used in this land")
                            print("You received a gold coin!")
                            return 1
                    if choice == 3:
                        check = random_gen("generate_integer",1, 3)
                        if check == 1:
                            print("Luckily, the chest was safe to open. ")
                            add_item(character_stats['inventory'], "gold coin", False, "currency used in this land")
                            add_item(character_stats['inventory'], "healing potion", False, "restore 50% of a user's max health")
                            print("You received a gold coin and a healing potion!")
                            return 1
                        else:
                            print("The chest was cursed! You feel a moment of intense agonizing pain and lose take your maximum hitpoints in damage!")
                            damage_taken = round(character_stats["max_health"] / 2)
                            character_stats["health"] = damage_calculator("subtract", character_stats["health"], damage_taken)
                            if character_stats["health"] <= 0:
                                return -1
                            return 1
                    if choice == 4:
                        if character_stats["class"] == "rogue" or character_stats["class"] == "artificer":
                            print("You disable any traps and open the chest ")
                            add_item(character_stats['inventory'], "gold coin", False, "currency used in this land")
                            print("You received a gold coin!")
                            return 1
                        else:
                            print("Invalid choice, try again")
                            continue
                except ValueError:
                    print("Invalid choice, try again")
                    continue

        if chosen_event == 4:
            while True:
                try:
                    print()
                    print(f"{events[output]} How do you proceed?")
                    print("Type 1 to approach the woman")
                    print("Type 2 to turn around and return to previous location")
                    print()
                    choice = int(input("Response: "))
                    if choice < 1 or choice > 2:
                        print("Invalid choice. Try again.")
                        continue
                    if choice == 2:
                        print("Backing away... ")
                        time.sleep(1)
                        return 1
                    if choice == 1:
                        have_item = 0
                        for item in character_stats["inventory"]:
                            if item["name"] == 'Strange Talisman':
                                have_item += 1
                                break
                        if have_item == 0:
                            print("strange woman: You don't have my talisman! Begone!")
                            damage_taken = round(character_stats["health"] / 2)
                            character_stats["health"] = damage_calculator("subtract", character_stats["health"], damage_taken)
                            print(f"You have taken {damage_taken} damage.")
                            print("The strange woman teleports away")
                            if character_stats["class"] == "cleric":
                                while True:
                                    print()
                                    print("Would you like to heal? Y/N")
                                    print()
                                    heal_or_not = int(input("Response: "))
                                    if heal_or_not == "N":
                                        break
                                    elif heal_or_not == "Y":
                                        character_stats["health"] = character_stats["max_health"]
                                        break
                                    else:
                                        print("Invalid choice. Try again.")
                                        continue

                        if have_item == 1:
                            print("strange woman: I sense you carry something of mine.")
                            while True:
                                try:
                                    print()
                                    print("Type 1 to show the her the Strange Talisman")
                                    print("Type 2 to tell her you carry nothing of hers")
                                    print()
                                    choices = int(input("Response: "))
                                    if choices < 1 or choices > 2:
                                        print("Invalid choice. Try again.")
                                        continue
                                    if choices == 2:
                                        print("strange woman: Begone then fool.")
                                        damage_taken = round(character_stats["health"] / 2)
                                        character_stats["health"] = damage_calculator("subtract", character_stats["health"], damage_taken)
                                        print(f"You have taken {damage_taken} damage.")
                                        print("The strange woman teleports away")
                                        if character_stats["class"] == "cleric":
                                            while True:
                                                print()
                                                print("Would you like to heal? Y/N")
                                                print()
                                                heal_or_not = int(input("Response: "))
                                                if heal_or_not == "N":
                                                    break
                                                elif heal_or_not == "Y":
                                                    character_stats["health"] = character_stats["max_health"]
                                                    break
                                                else:
                                                    print("Invalid choice. Try again.")
                                                    continue
                                        break
                                    if choices == 1:
                                        print("strange woman: My talisman! Hand it over and I'll give you a gold coin")
                                        while True:
                                            try:
                                                print()
                                                print("Type 1 to give her the Strange Talisman")
                                                print("Type 2 to refuse to hand over the Strange Talisman")
                                                print()
                                                choicess = int(input("Response: "))
                                                if choicess < 1 or choicess > 2:
                                                    print("Invalid choice. Try again.")
                                                    continue
                                                if choicess == 2:
                                                    print("strange woman: Insolent whelp! The talisman is mine!")
                                                    print("The strange woman launches a powerful magic attack at you")
                                                    print()
                                                    time.sleep(5)
                                                    character_stats["health"] = 1
                                                    print("You awaken from the strange woman's attack, barely alive at 1 hitpoint")
                                                    print("You think to yourself 'I should probably hand over the talisman if I encounter her again.")
                                                    if character_stats["class"] == "cleric":
                                                        while True:
                                                            print()
                                                            print("Would you like to heal? Y/N")
                                                            print()
                                                            heal_or_not = int(input("Response: "))
                                                            if heal_or_not == "N":
                                                                break
                                                            elif heal_or_not == "Y":
                                                                character_stats["health"] = character_stats[
                                                                    "max_health"]
                                                                break
                                                            else:
                                                                print("Invalid choice. Try again.")
                                                                continue
                                                    break
                                                if choicess == 1:
                                                    print("An excellent choice dear, as promised, 1 gold coin. Farewell.")
                                                    for item in character_stats["inventory"]:
                                                        if item["name"] == "Strange Talisman":
                                                            character_stats["inventory"].remove(item)
                                                    add_item(character_stats['inventory'], "gold coin", False, "currency used in this land")
                                                    print("You received a gold coin!")
                                                    events.pop(output)
                                                    break
                                            except ValueError:
                                                print("Invalid choice. Try again.")
                                                continue
                                    break
                                except ValueError:
                                    print("Invalid choice. Try again.")
                                    continue
                        return 1
                except ValueError:
                    print("Invalid choice. Try again.")
                    continue

    return 0

def create_character(player_data):
    print()
    print("Greetings adventurer, choose a character class, each has unique abilities")
    class_choice()
    choices = ("wizard", "cleric", "rogue", "fighter", "artificer")
    attack_ability = ("Fireball", "Holy Fire", "Stab", "Heroic Strike", "Shoot")
    special_ability = ("Teleport", "Heal", "Sneak", "Persuade", "Technological Solution")
    max_health = (20, 20, 25, 30, 25)
    damage = (18, 18, 12, 15, 12)
    while True:
        try:
            print()
            choice = int(input("Choose a character class: "))
            if choice < 1 or choice > 6:
                print("Invalid choice, try again")
                class_choice()
                continue
            elif choice == 6:
                print("Wizards gain Fireball as their base attack, and Teleport as their special ability")
                print("Clerics gain Holy Fire as their base attack, and Heal aS their special ability")
                print("Rogues gain stab as their base attack, and Sneak as their special ability")
                print("Fighters gain Heroic Strike as their base attack, and Persuade as their special ability")
                print("Artificers gain shoot as their base attack, and Technological Solution as their special ability")
                print("Class choices affects health, damage and choice options within the game")
                print()
                print("Press enter to return to choices")
                input()
                class_choice()
                continue
            else:
                confirm = input(f"Are you sure you would like to choose {choices[choice-1]}? (Y/N): ")
                if confirm == "N":
                    class_choice()
                    continue
                elif confirm == "Y":
                    player_data["class"] = choices[choice - 1]
                    player_data["level"] = 1
                    player_data["health"] = max_health[choice - 1]
                    player_data["max_health"] = max_health[choice - 1]
                    player_data["damage"] = damage[choice - 1]
                    player_data["special ability"] = special_ability[choice - 1]
                    player_data["attack ability"] = attack_ability[choice - 1]
                    player_data["max_health"] = max_health[choice - 1]
                    player_data["location"] = "The Valley of the Gods"
                    player_data["subzone"] = "Allie's Village"
                    while True:
                        print()
                        name = input("What is your name? ")
                        confirmation = input(f"Are you sure you want {name} to be your name?? Y/N: ")
                        if confirmation == "N":
                            print()
                            continue
                        elif confirmation == "Y":
                            player_data["name"] = name
                            break
                        else:
                            print("Invalid input, try again")
                            print()
                            continue
                    return
                else:
                    print("Invalid input, try again")
                    class_choice()
                    continue

        except ValueError:
            print("Invalid choice, try again")
            class_choice()
            continue




def game(character_data):
    descriptions = {
        "The Valley of the Gods": {
            "Allie's House": { "main" :"Allie's house, a cottage in a small village located in the easternmost portion of the Valley of the Gods.",
                 "extra": "You cannot travel east, to the west you notice a path leading towards a wooden bridge, to the north you see a riverbank, and south is blocked by mountains"
                 },
            "Riverbank": {"main": "A quiet riverbank with crystal-clear water.",
                "extra": "The path east is blocked by mountains, to the west you see an exit to the valley, to the west you see a small wooded area, and to the south lies Allie's village"
                },
            "The Frosted Pass" : {"main": "A narrow pass that leads to The Whispering Forest",
                                  "extra": "To the north lies The Whispering Forest, the south leads towards a wooden bridge, a riverbank lies to the east, and a strange tower lies to the west"
                },
            "Weathered Bridge": {"main": "A weathered wooden bridge stretching over the river.",
                "extra": "Allie's village lies to the east, to the north ou see an exit to the valley, to the south you see an abandoned fort, a foul odor emanates from the west"
                },
            "Abandoned Fort":{"main": "An ancient and crumbling fort that has seen better days",
                              "extra": "To the north you notice a wooden bridge, something doesnt seem right to the south, to the west lies an acncient crypt, and the path east is blocked by mountains "
                },
            "Ancient Crypts":{"main": "A ancient crypt, forgotten & lost to time",
                              "extra": "To the North you hear a strange noise, to the east you notice an abandoned fort, the paths to the south and west are blocked by mountains",
                },
            "Strange Tower":{"main": "A strange-looking tower that feels like it holds a secret",
                             "extra": "To the east you see an exit to the valley, to the west you notice a broken-down wagon, the path north and south are blocked by mountains "

            }
        }
    }
    character = {"name": "",
                 "class": "",
                 "level": 0,
                 "health": 0,
                 "max_health": 0,
                 "damage": 0,
                 "xp": 0,
                 "attack ability": "",
                 "special ability": "",
                 "inventory": [],
                 "quest_log": [],
                 "quests_completed": [],
                 "location": "",
                 "subzone": "",
                 "flags":[]
                 }
    if character_data is None:
        create_character(character)
        print()
        print("You found a healing potion! Would you like to add this to your inventory? (Y/N)" )
        while True:
            yes_no = input("Y/N: ")
            if yes_no == "N":
                break
            if yes_no == "Y":
                add_item(character["inventory"], "healing potion", False, "restore 50% of a user's max health")
                print("Item added to your inventory!")
                break
            else:
                print("Please enter a valid choice")
                print()
                continue
        add_item(character["inventory"], "Glimmerglass Pendant", True, "A one-of-a-kind piece of jewelry given to you by a former lover")
        print()
        print(f"NPC: Hello there {character['name']}, my name is Allie! This is The Valley of the Gods.")
            # f"I need your help to defeat an evil warlord who terrorizes these lands.")
            # print("Allie: First, you must recover the Amulet of Thregh from a garrison north of here. Return to me when this task is finished")
    else:
        character = character_data
        print("Saved game successfully loaded")

    while True:
        game_menu()
        print()
        try:
            choice = int(input("Input: "))
            if choice < 1 or choice > 6:
                print("Invalid choice, try again")
                game_menu()
                continue
            if choice == 4:
                print()
                print("Your character stats:")

                generate_report(character)
                continue

            if choice == 5:
                while True:
                    print()
                    print("Do you wish to override an existing save? (Y/N). Type C to cancel")
                    yes_no = input("Y/N: ")
                    if yes_no == "N":
                        print()
                        print(game_save_CUD("create", character))
                        break
                    elif yes_no == "Y":
                        print()
                        key_value = retreive_game("update")
                        if key_value == "Invalid":
                            print("No saves to overwrite!")
                            break
                        print(game_save_CUD("update", character, key_value[0]))
                        break
                    elif yes_no == "C":
                        break
                    else:
                        print("Please enter a valid choice")
                        continue
            if choice == 6:
                while True:
                    print()
                    print("Are you sure you wish to exit the game? All unsaved progress will be lost. (Y/N)")
                    stay_leave = input("Input: ")
                    if stay_leave == "N":
                        break
                    if stay_leave == "Y":
                        return -1
                    else:
                        print("Invalid input, try again")
                        continue
            if choice == 2:
                print()
                inventory(character)
                continue
            if choice == 1:
                print(descriptions[character["location"]][character["subzone"]]["main"])
                while True:
                    print()
                    print("Would you like to scan the horizon?")
                    print("Type 1 to scan the horizon")
                    print("Type 2 to return to game menu")
                    try:
                        print()
                        search = int(input("Input: "))
                        if search < 1 or search > 2:
                            print("Invalid choice, try again")
                            continue
                        if search == 1:
                            print(descriptions[character["location"]][character["subzone"]]["extra"])
                        game_menu()
                        break
                    except ValueError:
                        print("Invalid choice, try again")
                        continue
            if choice == 3:
                while True:
                    direction = movement()
                    valid_movement = navigation(character, direction)
                    time.sleep(1)
                    if valid_movement == "Blocked":
                        print("That direction is blocked. Try another direction.")
                        print()
                        continue
                    elif valid_movement == "-1":
                        exploration = random_event(character, descriptions)
                        if exploration == -1:
                            print("You died. Returning to main menu ...")
                            return -1
                    elif valid_movement == { "The Whispering Forest": "The Frosted Pass" }:
                        character["location"] = "The Whispering Forest"
                        character["subzone"] = "The Frosted Pass"
                        print(character["location"], character["subzone"])
                        break
                    else:
                        character["subzone"] = valid_movement
                        break
                game_menu()
        except ValueError:
            print("Please enter a valid choice")
            game_menu()
            continue

def main():
    print()
    print("Greeting adventurer, welcome to Clullealas")
    print("What would you like to do?")
    while True:
        print()
        try:
            main_menu()
            print()
            choice = int(input("Input: "))
            character_data = None
            if choice < 1 or choice > 5:
                print("Please enter a valid choice")
                main_menu()
                continue
            if choice == 3:
                character_data = retreive_game("load")
                choice = 1
            if choice == 4:
                key_value = retreive_game("delete")
                print(game_save_CUD("delete", key_value[1], key_value[0]))
                continue
            if choice == 5:
                print("Exiting... Goodbye!")
                break
            if choice == 2:
                print("This is a text-based adventure game, you will be presented with a list of options to choose from, you must type in a valid response (number).")
                print("Upon entering a valid number, you will then be given another set of choices or returned to the start game menu.")
                print("Upon entering invalid input, you will be prompted to resubmit input")
                print()
                main_menu()
                continue
            if choice == 1:
                ending = game(character_data)
                if ending == -1:
                    main_menu()
                    continue
                else:
                    print("Congratulations adventurer, you have defeated the evil warlord and saved the land!")
                    print("You have now completed the adventure! What would you like to do next?")
                    main_menu()
                    continue
        except ValueError:
            print("Please enter a valid choice")
            main_menu()
            continue



if __name__ == "__main__":
    main()
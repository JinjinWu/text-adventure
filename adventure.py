from game_data import World, Item, Location
from player import Player

if __name__ == "__main__":
    WORLD = World("map.txt", "locations.txt", "items.txt")
    PLAYER = Player(4, 4)   # starting location of player

    print("To get a list of all possible actions in this game, type help.\n")

    # list of possible actions
    menu = ["go", "look", "inventory", "take", "drop", "wear", "open", "unlock", "score", "quit"]

    # total number of moves allowed
    time = 60

    # Obstacle: closed door
    opened = False

    # Obstacle: locked door
    unlocked = False

    while not PLAYER.victory:
        # creates new location object
        location = WORLD.get_location(PLAYER.x, PLAYER.y)

        time -= 1
        print("You have {0} minutes left until the exam starts.\n".format(time))

        if location.visited == "False":
            print(location.long)
            print(location.brief)
            location.is_visited(location.position, WORLD.locations)
            PLAYER.score += PLAYER.add_score(5)
        else:
            print(location.brief)

        print("Items in here:", str(location.items))

        # creating item instances within location instance
        if location.items != "None":
            for item in location.items:
                item = Item(item, WORLD.items)

        # Obstacle: can't go to junction
        def is_cold():
            if "scarf (being worn)" not in PLAYER.inventory:
                print("It's too cold to go outside like this! Especially for your sensitive neck.")
                PLAYER.move_east()

        # Obstacle: can't go to Circuit Break Cafe
        def is_ex():
            if "sunglasses (being worn)" not in PLAYER.inventory:
                print("WAIT A MOMENT. You see your ex in Circuit Break Cafe! AND with somebody new hanging off them.")
                print("You are not in the mood for pity talks. There must be some way to hind your face.")
                PLAYER.move_north()

        # ask for user action
        choice = input("\n>")

        # parsing user input
        if len(choice.split()) == 0:
            print("Please enter a command and stop wasting your time.")

        elif (choice.split()[0]).lower() == "go":
            if len(choice.split()) == 1:
                print("Please pick a direction.")
            elif (choice.split()[1]).lower() == "north":
                PLAYER.move_north()
                if WORLD.get_location(PLAYER.x, PLAYER.y) == "not a room":
                    print("That way is blocked.")
                    PLAYER.move_south()
            elif (choice.split()[1]).lower() == "south":
                PLAYER.move_south()
                if WORLD.get_location(PLAYER.x, PLAYER.y) == "not a room":
                    print("That way is blocked.")
                    PLAYER.move_north()
                elif location.position == "6":
                    is_ex()
            elif (choice.split()[1]).lower() == "east":
                PLAYER.move_east()
                if WORLD.get_location(PLAYER.x, PLAYER.y) == "not a room":
                    print("That way is blocked.")
                    PLAYER.move_west()
            elif (choice.split()[1]).lower() == "west":
                PLAYER.move_west()
                if WORLD.get_location(PLAYER.x, PLAYER.y) == "not a room":
                    print("That way is blocked.")
                    PLAYER.move_east()
                elif location.position == "6":
                    is_cold()
            else:
                print("That's not a valid direction.")

        elif (choice.split()[0]).lower() == "take":
            item = " ".join(choice.split()[1:])
            if item.lower() in location.items:
                if item.lower() == "scarf" and location.position == "5" and not opened:
                    if not unlocked:
                        print("The scarf is stuck between a side door and its frame! You can't take it!")
                    else:
                        print("The door is still closed!")
                else:
                    print("Taken.")
                    PLAYER.add_item(item)
                    location.remove_item(WORLD.items, item)
            else:
                print("You can't take that.")

        elif (choice.split()[0]).lower() == "drop":
            item = " ".join(choice.split()[1:])
            if item.lower() in PLAYER.inventory:
                print("Dropped.")
                PLAYER.remove_item(item)
                location.add_item(WORLD.items, item)

                if item.lower() in ["cheat sheet", "tcard", "lucky pen"]:
                    PLAYER.score += Item(item, WORLD.items).get_target_points(item, WORLD.items)

            else:
                print("You can't drop that.")

        elif (choice.split()[0]).lower() == "wear":
            if choice.split()[1] in ["scarf", "sunglasses"] and len(choice.split()) == 2:
                if choice.split()[1] in PLAYER.inventory:
                    PLAYER.wear_item(choice.split()[1])
                    print("You put it on.")
            else:
                print("You can't wear that!")

        elif (choice.split()[0]).lower() == "open":
            if location.position != "5":
                print("There's nothing to open!")
            elif (choice.split()[1]).lower() != "door" and len(choice.split()) != 2:
                print("You can't unlock that!")
            elif not unlocked:
                print("You can't open the door! It's locked!")
            else:
                opened = True
                print("Opened.")

        # unlock command: needed to unlock door obstacle
        elif (choice.split()[0]).lower() == "unlock":
            if (choice.split()[1]).lower() == "door" and len(choice.split()) == 2:
                if "key" in PLAYER.inventory and location.position == "5":
                    unlocked = True
                    print("You unlocked it!")
                elif "key" in PLAYER.inventory and location.position != "5":
                    print("There's nothing to unlock here!")
                else:
                    print("You don't have anything to unlock.")
            else:
                print("You can't unlock that!")

        elif choice.lower() == "look":
            print(location.long)

        elif choice.lower() == "inventory":
            print("You currently have: " + str(PLAYER.inventory))

        elif choice.lower() == "score":
            print("Your current score is {0}.".format(PLAYER.score))

        elif choice.lower() == "help":
            print(menu)

        elif choice.lower() == "quit":
            PLAYER.victory = True
            print("Winners never quit and quitters never win! You lose.")
            print("You got {0} points.".format(PLAYER.score))

        else:
            print("That's not a verb I recognize.")

        # check if endgame conditions have been met
        if PLAYER.score == 110:
            PLAYER.victory = True
            print("YES! You made it with all your items! And with a full score of 110!")
            print("Now just go ace your exam!")
        elif time == 0:
            PLAYER.victory = True
            print("Oh no, it's too late! You're missing your exam!")
            print("At least you got {0} points?".format(PLAYER.score))

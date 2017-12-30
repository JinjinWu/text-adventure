class Location:

    def __init__(self, location_number, locations_dict, items_dict):
        ''' Creates a new location.
        :param location_number: (str) number associated with location instance
        :param locations_dict: (dictionary) location data created under World class
        :param items_dict: (dictionary) item data created under World class
        '''

        self.position = location_number
        self.brief = self.get_brief_description(location_number, locations_dict)
        self.long = self.get_full_description(location_number, locations_dict)
        self.visited = locations_dict[location_number][0]
        self.items = self.items_in_location(items_dict)

    def get_brief_description(self, location_number, locations_dict):
        '''Return str brief description of location stored in dictionary.
        :param location_number: (str) number associated with location instance
        :param locations_dict: (dictionary) location data created under World class
        '''
        return locations_dict[location_number][1]

    def get_full_description(self, location_number, locations_dict):
        '''Return str long description of location stored in dictionary.
        :param location_number: (str) number associated with location instance
        :param locations_dict: (dictionary) location data created under World class
        '''
        return locations_dict[location_number][2]

    def items_in_location(self, items_dict):
        '''Return list of items in location instance if present.
        Return str "None" if there are no items in location instance.
        Checks if position of each item in items_dict matches with position
        of location instance.
        :param items_dict: (dictionary) item data created under World class
        '''
        items_list = []
        for item in items_dict.keys():
            if self.position == items_dict[item][0]:
                items_list.append(item)
        if items_list == []:
            return "None"
        return items_list

    def is_visited(self, location_number, locations_dict):
        ''' Returns None.
        When called, changes status of whether a location has been visited to True.
        The status that gets changed is stored in the locations dictionary.
        :param location_number: (str) number associated with location instance
        :param locations_dict: (dictionary) location data created under World class
        '''
        locations_dict[location_number][0] = True

    def remove_item(self, items_dict, item):
        ''' Returns None.
        Changes the current position of the item to "0" a nonexistent position on the map.
        :param items_dict: (dictionary) item data created under World class
        :param item: (str) name of item in location
        '''
        items_dict[item][0] = "0"

    def add_item(self, items_dict, item):
        ''' Returns None.
        Changes the current position of the item from "0" to the position of the location object.
        :param items_dict: (dictionary) item data created under World class
        :param item: (str) name of item in location
        '''
        items_dict[item][0] = self.position


class Item:

    def __init__(self, name, items_dict):
        '''Create item referred to by string name, with integer "start"
        being the integer identifying the item's starting location,
        the integer "target" being the item's target location, and
        integer target_points being the number of points player gets
        if item is deposited in target location.

        The only thing you must NOT change is the name of this class: Item.
        All item objects in your game MUST be represented as an instance of this class.
        '''

        self.name = name
        self.current = items_dict[name][0]
        self.target = items_dict[name][1]
        self.target_points = items_dict[name][2]

    def get_target_points(self, name, items_dict):
        '''Return int points awarded for depositing the item in its target location.'''
        if items_dict[name][0] == "10":
            return 20
        else:
            return 0

class World:

    def __init__(self, mapdata, locdata, itemdata):
        '''
        Creates a new World object, with a map, and data about every location and item in this game world.

        :param mapdata: name of text file containing map data in grid format (integers represent each location, separated by space)
                        map text file MUST be in this format.
                        E.g.
                        1 -1 3
                        4 5 6
                        Where each number represents a different location, and -1 represents an invalid, inaccessible space.
        :param locdata: name of text file containing location data
                        E.g.
                        Location 0
                        False
                        Short description
                        Long description
                        END
        :param itemdata: name of text file containing item data
                        E.g.
                        1 10 20 item name
        :return:
        '''
        self.map = self.load_map(mapdata) # The map MUST be stored in a nested list as described in the docstring for load_map() below
        # self.locations ... You may choose how to store location and item data.
        self.locations = self.load_locations(locdata) # This data must be stored somewhere. Up to you how you choose to do it...
        self.items = self.load_items(itemdata) # This data must be stored somewhere. Up to you how you choose to do it...

    def load_map(self, filename):
        '''
        Store map from filename (map.txt) in the variable "self.map" as a nested list of strings OR integers like so:
            1 2 5
            3 -1 4
        becomes [['1','2','5'], ['3','-1','4']] OR [[1,2,5], [3,-1,4]]
        RETURN THIS NEW NESTED LIST.
        :param filename: string that gives name of text file in which map data is located
        :return: return nested list of strings/integers representing map of game world as specified above
        '''

        map = []

        file = open(filename, "r")

        for line in file.readlines():
            map.append(line.split())
        file.close()

        return map

    def load_locations(self, filename):
        '''
        Store all locations from filename (locations.txt) into the variable "self.locations"
        however you think is best.
        Remember to keep track of the integer number representing each location.
        Make sure the Location class is used to represent each location.
        Change this docstring as needed.
        :param filename: name of text file containing location data
        :return: a dictionary with location numbers as keys
        '''

        locations = {}

        location_file = open(filename, "r")

        for line in location_file:

            index = location_file.readline().split()
            if index == ['FILE', 'END']:
                location_file.close()
                return locations

            visited = location_file.readline()

            brief = location_file.readline()

            long = ""
            while line.strip() != "END":
                line = location_file.readline()
                long += line

                locations[index[1]] = [visited.strip(), brief.strip(), long.strip("\nEND\n")]


    def load_items(self, filename):
        '''
        Store all items from filename (items.txt) into ... whatever you think is best.
        Make sure the Item class is used to represent each item.
        Change this docstring accordingly.
        :param filename: name of text file containing item data
        :return: a dictionary with names of items as keys
        '''

        items = {}

        file = open(filename, "r")

        for line in file:
            info = line.split()
            name = ""

            for word in info[3:]:
                name += word + " "

            info[3] = name.strip()
            items[info[3]] = info[:3]

        file.close()
        return items

    def get_location(self, x, y):
        '''Check if location exists at location (x,y) in world map.
        Return Location object associated with this location if it does. Else, return None.
        Remember, locations represented by the number -1 on the map should return None.
        :param x: integer x representing x-coordinate of world map
        :param y: integer y representing y-coordinate of world map
        :return: Return Location object associated with this location if it does. Else, return None.
        '''

        # check if coordinates exist on map
        if y < len(self.map) and x < len(self.map[0]):
            # check if location exists
            if self.map[y][x] == "-1":
                return "not a room"
            else:
                # creates new location object with number on map at coordinates x,y
                return Location(self.map[y][x], self.locations, self.items)
        else:
            return None


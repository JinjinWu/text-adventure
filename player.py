class Player:

    def __init__(self, x, y, score=0):
        '''
        Creates a new Player.
        :param x: x-coordinate of position on map
        :param y: y-coordinate of position on map
        :param score: (int) score of player

        '''
        self.x = x
        self.y = y
        self.inventory = []
        self.score = score
        self.victory = False

    def move(self, dx, dy):
        '''
        Given integers dx and dy, move player to new location (self.x + dx, self.y + dy)
        :param dx: int amount x-coordinate moves by
        :param dy: int amount y-coordinate moves by
        :return: None
        '''
        self.x += dx
        self.y += dy

    def move_north(self):
        '''These integer directions are based on how the map must be stored
        in our nested list World.map'''
        self.move(0,-1)

    def move_south(self):
        self.move(0,1)

    def move_east(self):
        self.move(1,0)

    def move_west(self):
        self.move(-1,0)

    def add_item(self, item):
        '''
        Add item to list of inventory items.
        :param item: name of item object
        :return: None
        '''
        self.inventory.append(item)

    def remove_item(self, item):
        '''
        Remove item from list of inventory items.
        :param item: name of item object
        :return: None
        '''
        self.inventory.remove(item)

    def get_inventory(self):
        '''
        Return list of inventory items.
        :return: str of list elements
        '''
        return "You currently have:", self.inventory

    def wear_item(self, item):
        '''
        Changes name of item in inventory to show that it is being worn.
        :param item:  name of item object
        :return: None
        '''
        self.inventory.remove(item)
        self.inventory.append("{0} (being worn)".format(item))

    def add_score(self, score):
        '''
        :param score: increased score amount in int
        :return: int amount
        '''
        return score



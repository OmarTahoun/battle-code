from battlecode import BCAbstractRobot, SPECS
import battlecode as bc
import random
# import nav

__pragma__('iconv')
__pragma__('tconv')
__pragma__('opov')


# don't try to use global variables!!

class MyRobot(BCAbstractRobot):

    already_been = {}
    base = None
    destination = None
    enemyCastles = []
    pendingCastleLoc = None # have to send over two turns, this is for when we've only sent half a castle loc
    partialCastleLocsRecieved = dict()
    adjacentdirs = [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1],]
    spawnloc = None
    step = -1
    #
    def loc_in_list(self, elt, lst):
        if len(lst) < 1:
            return False
        for e in lst:
            if e[0] == elt[0] and e[1] == elt[1]:
                return True
        return False

    def get_neighbors(self, grid):
        x = self.me['x']
        y = self.me['y']
        rows = cols = len(grid)
        neighbors = []

        if x < rows-1:
            neighbors.append([y,x+1])
            if y > 0:
                neighbors.append([y-1,x+1])
            if y < cols-1:
                neighbors.append([y+1,x+1])

        if x > 0:
            neighbors.append([y,x-1])
            if y > 0:
                neighbors.append([y-1,x-1])
            if y < cols-1:
                neighbors.append([y+1,x-1])

        if y < cols-1:
            neighbors.append([y+1,x])

        if y > 0:
            neighbors.append([y-1,x])
        return neighbors

    def find_best_neighbor(self, neighbors, grid, castle):
        x = self.me['x']
        y = self.me['y']
        new_neighbors = []
        best = None
        shortest = 49**2 + 49**2
        for neighbor in neighbors:
            if grid[neighbor[0]][neighbor[1]] == True:
                new_neighbors.append(neighbor)
        for neighbor in new_neighbors:
            dist = (castle[0] - neighbor[0])**2 + (castle[1] - neighbor[1])**2
            if dist<shortest:
                shortest = dist
                best = neighbor
        choice = (best[0] - y, best[1] - x)
        return choice





    def turn(self):
        attackable = []
        attack_radius = SPECS['UNITS'][SPECS["CRUSADER"]]['ATTACK_RADIUS']
        visible_robot_map = self.get_visible_robot_map()
        visible = self.get_visible_robots()

        self.step += 1
        self.log("START TURN " + self.step)

        if self.me['unit'] == SPECS['CRUSADER']:
            self.log("Crusader health: " + str(self.me['health']))

            # get attackable robots
            for r in visible:
                #Make sure it's visable
                if not self.is_visible(r):
                    continue
                # Get Distance to the bot
                distance_to_r = (r['x'] - self.me['x'])**2 + (r['y'] - self.me['y'])**2

                # If the bot is not on my team and is within the attac radius
                if r['team'] != self.me['team']:
                    if attack_radius[0] <= distance_to_r <= attack_radius[1]:
                        # add it to the list
                        attackable.append(r)

                    if r['unit'] == 0 and not self.loc_in_list([r['x'], r['y']], self.enemyCastles):
                        self.log("enemy castle at " + str(r['x']) + str(r['y']))
                        self.enemyCastles.append([r['x'], r['y']])

            if attackable:
                # attack first robot
                r = attackable[0]
                self.log('attacking! ' + str(r) + ' at loc ' + (r['x'] - self.me['x'], r['y'] - self.me['y']))
                return self.attack(r['x'] - self.me['x'], r['y'] - self.me['y'])
            else:
                choices = [(0,-1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]
                if len(self.enemyCastles) > 0:
                    around_me = self.get_neighbors(self.get_passable_map())
                    choice = self.find_best_neighbor(around_me, self.get_passable_map(), self.enemyCastles[0])
                else:
                    choice = random.choice(choices)
                self.log('TRYING TO MOVE IN DIRECTION ' + str(choice))
                return self.move(*choice)

        elif self.me['unit'] == SPECS['CASTLE']:
            if self.step < 10:
                self.log("Building a crusader at " + str(self.me['x']+1) + ", " + str(self.me['y']+1))
                return self.build_unit(SPECS['CRUSADER'], 1, 1)

        else:
            self.log("Castle health: " + self.me['health'])


robot = MyRobot()

from battlecode import BCAbstractRobot, SPECS
import battlecode as bc
import random
import nav

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

            if attackable:
                # attack first robot
                r = attackable[0]
                self.log('attacking! ' + str(r) + ' at loc ' + (r['x'] - self.me['x'], r['y'] - self.me['y']))
                return self.attack(r['x'] - self.me['x'], r['y'] - self.me['y'])
            else:
                choices = [(0,-1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]
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

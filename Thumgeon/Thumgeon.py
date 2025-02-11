# Thumgeon

# Explore an endless, tough-as-nails pseudorandom dungeon
# crawler. Collect items, potions, and weapons, kill monsters
# with aforementioned loot -- and stay alive!

# Written by Mason Watmough for TinyCircuits.
# Last edited 31-Jan-2025

'''
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

from machine import freq, Pin

import thumby
from time import ticks_ms
import time
from random import seed as random_seed, randint
from gc import enable as gc_enable, collect as gc_collect
import gc
gc_enable()
random_seed()

thumby.display.setFPS(30)
fontWidth = const(6) # 6 pixels per character


# Sprite data for game objects

swordSpr = bytes([3,7,14,92,56,48,200,64])
bowSpr = bytes([0,129,126,129,129,90,60,0])
potSpr = bytes([4,113,210,174,212,174,210,116])
keySpr = bytes([0,24,36,36,24,8,24,8])
snackSpr = bytes([96,192,184,52,42,19,14,4])
pantsSpr = bytes([0,252,254,14,14,254,252,0])
shirtSpr = bytes([156,254,254,212,172,254,254,156])
magicSpr = bytes([66,219,60,110,76,32,219,66])
blockSpr = bytes([160,110,170,102,10,230,170,102]) # Walls
stairSpr = bytes([126,253,253,241,241,193,193,126])
signSpr = bytes([28,42,54,250,238,54,42,28])
doorSpr = bytes([254,6,3,1,1,3,6,254])
chestSpr = bytes([252,70,126,74,82,126,70,252])
hpupSpr = bytes([124,16,96,0,240,82,39,2])
mpupSpr = bytes([120,16,32,16,120,2,7,2])
itemSprites = (swordSpr, bowSpr, potSpr, keySpr, snackSpr, pantsSpr, shirtSpr, magicSpr, hpupSpr, mpupSpr)

blobSpr = bytes([96,144,248,152,248,240,224,192])
spiritSpr = bytes([0,12,18,62,114,76,32,0])
arachSpr = bytes([96,208,240,116,114,228,120,0])
skeleSpr = bytes([48,8,214,127,213,10,48,0])
wizardSpr = bytes([144,204,254,247,204,16,122,4])
tempestSpr = bytes([0,20,84,92,170,174,42,12])
monsterSprites = (blobSpr, spiritSpr, arachSpr, skeleSpr, wizardSpr, tempestSpr)

shopSpr = bytes([128,228,106,210,64,254,72,254,64,92,98,92,64,126,202,132,255,
    234,245,234,245,234,229,48,174,249,63,249,174,48,224,255])

# Icons for HUD
hpSpr = bytes([30,62,120,62,30])
mpSpr = bytes([72,108,62,27,9])

signMessages = (
    bytes("I wonder\nif anyone\nwill see\nthis...?", 'ascii'),
    bytes("I've been\ndown here\nfor DAYS!", 'ascii'),
    bytes("Who keeps\nleaving\nweapons\ndown\nhere?", 'ascii'),
    bytes("Always\nremember:\nfinders\nkeepers!", 'ascii'),
    bytes("Man, I\nhad so\nmuch\ngold...\n...had...", 'ascii'),
    bytes("Hang in\nthere!\n- M.W.", 'ascii'),
    bytes("Happy\ncrawling,\nfellow\nknight.", 'ascii'),
    bytes("Only $8\nfor an\nULTRA\nSWORD!?", 'ascii'),
    bytes("Why do\nall these\npotions\ntaste so\nterrible?", 'ascii'),
    bytes("Am I the\nonly\nperson\ndown\nhere?", 'ascii'),
    bytes("This food\ncould be\ncenturies\nold...", 'ascii'),
    bytes("It smells\nlike an\nancient\ncloset.", 'ascii'),
    bytes("How many\nknights\nhave been\ndown\nhere?", 'ascii'),
    bytes("Who took\nmy epic\nbow!?", 'ascii'),
    bytes("Who keeps\nleaving\nrocks in\nmy shirt?", 'ascii'),
    bytes("Man...\nI'm\ntired.", 'ascii'),
    bytes("How do\nskeletons\ncarry gold\nwithout\npockets?", 'ascii'),
    bytes("HELP!\nWIZARD\nTURNED\nME INTO\nA SIGN", 'ascii'),
    bytes("I just\nkeep\ngoing\ndeeper.", 'ascii'),
    bytes("SCORPIONS\n\nSCORPIONS\nin a\nDUNGEON!", 'ascii'),
    bytes("Sure is\ndrafty\nfor a\ndungeon.", 'ascii'),
    bytes("Cool\nplace!\nToo many\nrooms.\n7 / 10", 'ascii'),
    bytes("SIX\nbroken\nbows and\nnot ONE\nsnack.", 'ascii'),
)

swLstate=1
swRstate=1
swUstate=1
swDstate=1
swAstate=1
swBstate=1

# Blocking input function

def getcharinputNew():
    global swLstate
    global swRstate
    global swUstate
    global swDstate
    global swAstate
    global swBstate
    
    if(swLstate==0 and thumby.buttonL.pressed()):
        swLstate=1
        return 'L'
    elif(swLstate==1 and not thumby.buttonL.pressed()):
        swLstate=0

    if(swRstate==0 and thumby.buttonR.pressed()):
        swRstate=1
        return 'R'
    elif(swRstate==1 and not thumby.buttonR.pressed()):
        swRstate=0

    if(swUstate==0 and thumby.buttonU.pressed()):
        swUstate=1
        return 'U'
    elif(swUstate==1 and not thumby.buttonU.pressed()):
        swUstate=0

    if(swDstate==0 and thumby.buttonD.pressed()):
        swDstate=1
        return 'D'
    elif(swDstate==1 and not thumby.buttonD.pressed()):
        swDstate=0

    if(swAstate==0 and thumby.buttonB.pressed()):
        swAstate=1
        return '1'
    elif(swAstate==1 and not thumby.buttonB.pressed()):
        swAstate=0

    if(swBstate==0 and thumby.buttonA.pressed()):
        swBstate=1
        return '2'
    elif(swBstate==1 and not thumby.buttonA.pressed()):
        swBstate=0

    return ' '


goldChr = "$" # Symbol for in-game currency or gold
curMsg = ""
lastHit = ""
floorNo = 1

def addhp(n):
    player.hp += n
    if(player.hp > player.maxhp):
        player.hp = player.maxhp

def addmp(n):
    player.mp += n
    if(player.mp > player.maxmp):
        player.mp = player.maxmp

def addgp(n=randint(1,5)+floorNo):
    player.gp += n
    if(player.gp > 9999):
        player.gp = 9999

class dungeonTile:
    def __init__(self, ttype, *data):
        self.tiletype = ttype
        self.tiledata = []
        for i in range(len(data)):
            self.tiledata.append(data[i])

    def actOn(self):
        global curMsg
        global roomno
        global floorNo
        global exitSpawned
        if(self.tiletype == 1):
            # Tile is a block
            curMsg = "a wall."

        elif(self.tiletype == 2):
            # Tile is a door
            if(len(self.tiledata) == 0):
                curMsg = "ERR!"
            else:
                curMsg = "" # entered
                global currentRoom
                global player
                currentRoom.getTile(player.tilex, player.tiley).tiletype = 0
                currentRoom = self.tiledata[0]
                player.tilex = self.tiledata[1]
                player.tiley = self.tiledata[2]

        elif(self.tiletype == 3):
            gc_collect()
            thumby.display.fill(0)
            thumby.display.drawSprite(loadingScreen)
            thumby.display.update()
            # Tile is stairs to next floor
            curMsg = "the exit?"
            roomno = 0
            exitSpawned = False
            floorNo = floorNo + 1
            currentRoom = None
            gc_collect()
            currentRoom = dungeonRoom()
            gc_collect()
            generateRoom(currentRoom)
            gc_collect()
            if(currentRoom.getTile(player.tilex, player.tiley).tiletype != 0):
                pos = getRandomFreePosition(currentRoom)
                player.tilex, player.tiley = pos[0], pos[1]
            saveAll(player,save)
            gc_collect()
            loadScreen()

        elif(self.tiletype == 4):
            # Tile is a sign
            if(len(self.tiledata) == 0):
                curMsg = "nothing."
            else:
                # Draw the sign's text
                thumby.display.fill(0)
                y = 0
                signMsg = str(self.tiledata, 'ascii')
                for line in signMsg.split("\n"):
                    thumby.display.drawText(line, 0, y, 1)
                    y = y + 8
                thumby.display.update()

                # Wait for the player to finish reading
                while(getcharinputNew() == ' '):
                    thumby.display.update()
                curMsg = ""

        elif(self.tiletype == 6):
            # Tile is a chest
            chestGold = randint(1, 9)
            if(randint(0,99) == 0): # 1% Bonus
                chestGold += randint(10, 30)
            addgp(chestGold)
            curMsg = "got "+goldChr+str(chestGold)+"!"
            self.tiledata.clear()
            self.tiletype = 0

        elif(self.tiletype == 7):
            # Tile is an item
            curMsg = itemname(self)
            # Check to see if the player can carry it
            if(player.maxwt - itemwt(itemname(self)) >= player.wt):
                # Pick it up off the ground
                player.inventory.append(itemname(self))
                player.wt = player.wt + itemwt(itemname(self))
                self.tiledata.clear()
                self.tiletype = 0
            else:
                # Explain why we can't pick it up.
                curMsg = "no room!"

        elif(self.tiletype == 8):
            # Tile is a monster
            if(player.helditem == -1):
                # Attack with hand for 1-3 dmg
                dmg = randint(1, 3)
                self.tiledata[1] = self.tiledata[1] - dmg
                curMsg = "hit " + str(dmg) + "pts"
                if(self.tiledata[1] <= 0):
                    # Monster is dead
                    self.tiledata.clear()
                    self.tiletype = 0
                    addgp()
            else:
                # Attack with held item
                if(player.mp >= manacost(player.inventory[player.helditem])):
                    player.mp = player.mp - manacost(player.inventory[player.helditem])
                    dmgrng = itemdmg(player.inventory[player.helditem])
                    dmg = randint(dmgrng[0], dmgrng[1])
                    self.tiledata[1] = self.tiledata[1] - dmg
                    curMsg = "hit " + str(dmg) + "pts"
                    if(self.tiledata[1] <= 0):
                        # Monster is dead
                        self.tiledata.clear()
                        self.tiletype = 0
                        addgp()
                    if(player.inventory[player.helditem] == "bsc lch" or player.inventory[player.helditem] == "adv lch" or player.inventory[player.helditem] == "ult lch"):
                        # Leech spell, add damage to health
                        addhp(dmg)
                    # Check if we're using a confusion spell
                    if(player.inventory[player.helditem] == "bsc cnfs"):
                        self.tiledata[2] = self.tiledata[2] + 3
                    elif(player.inventory[player.helditem] == "adv cnfs"):
                        self.tiledata[2] = self.tiledata[2] + 5
                    elif(player.inventory[player.helditem] == "ult cnfs"):
                        self.tiledata[2] = self.tiledata[2] + 8

                    # Check if we're using a healing spell
                    if(player.inventory[player.helditem] == "bsc heal"):
                        addhp(3)
                    elif(player.inventory[player.helditem] == "adv heal"):
                        addhp(5)
                    elif(player.inventory[player.helditem] == "ult heal"):
                        addhp(8)
                else:
                    # Couldn't cast, punch instead
                    dmg = randint(1, 3)
                    curMsg = "hit " + str(dmg) + "pts"
                    self.tiledata[1] = self.tiledata[1] - dmg
                    if(self.tiledata[1] <= 0):
                        # Monster is dead
                        self.tiledata.clear()
                        self.tiletype = 0
                        addgp()

        elif(self.tiletype == 9):
            # Shop tile, open shop inventory
            actpos = 0
            selpos = 0
            inventory = 0
            curMsg = ""
            while(swAstate != 1):
                thumby.display.fill(0)
                if(inventory == 0):
                    if(len(player.inventory) > 0):
                        selpos = min(selpos, len(player.inventory)-1)
                        thumby.display.drawText(player.inventory[selpos], 0, 8, 1)
                        thumby.display.drawText(goldChr+str(itemprice(player.inventory[selpos])[1]), 0, 16, 1)
                    thumby.display.drawFilledRectangle(0, 0, 24, 8, 1-actpos)
                    thumby.display.drawText("inv", 0, 0, actpos)
                    thumby.display.drawFilledRectangle(32, 0, 32, 8, actpos)
                    thumby.display.drawText("sell", 32, 0, 1-actpos)
                else:
                    if(len(currentRoom.shopInv) > 0):
                        selpos = min(selpos, len(currentRoom.shopInv)-1)
                        thumby.display.drawText(currentRoom.shopInv[selpos], 0, 8, 1)
                        thumby.display.drawText(goldChr+str(itemprice(currentRoom.shopInv[selpos])[0]), 0, 16, 1)
                    thumby.display.drawFilledRectangle(0, 0, 32, 8, 1-actpos)
                    thumby.display.drawText("shop", 0, 0, actpos)
                    thumby.display.drawFilledRectangle(40, 0, 24, 8, actpos)
                    thumby.display.drawText("buy", 40, 0, 1-actpos)
                thumby.display.drawText(goldChr+str(player.gp), 64-len(str(player.gp))*fontWidth, 32, 1)
                thumby.display.update()
                while(getcharinputNew() == ' '):
                    thumby.display.update()
                if(swUstate == 1):
                    selpos = max(0, selpos-1)
                elif(swDstate == 1):
                    if(inventory == 0):
                        # In player inv
                        selpos = min(len(player.inventory)-1, selpos+1)
                    else:
                        # In shop inv
                        selpos = min(len(currentRoom.shopInv)-1, selpos+1)
                elif(swLstate == 1):
                    actpos = 0
                elif(swRstate == 1):
                    actpos = 1
                elif(swBstate == 1):
                    # Player hit selection
                    if(actpos == 0):
                        # Player changed inventory
                        if(inventory == 0):
                            inventory = 1
                        else:
                            inventory = 0
                    else:
                        # Player traded item
                        if(inventory == 0 and len(player.inventory) > 0):
                            # Sell item
                            player.wt = player.wt - itemwt(player.inventory[selpos])
                            if(player.helditem == selpos):
                                player.helditem = -1
                            if(player.pantsitem == selpos):
                                player.pantsitem = -1
                            if(player.shirtitem == selpos):
                                player.shirtitem = -1
                            currentRoom.shopInv.append(player.inventory[selpos])
                            addgp(itemprice(player.inventory[selpos])[1])
                            player.inventory.pop(selpos)
                        else:
                            if(player.gp >= itemprice(currentRoom.shopInv[selpos])[0]):
                                # Buy item
                                player.wt = player.wt + itemwt(currentRoom.shopInv[selpos])
                                player.gp = player.gp - itemprice(currentRoom.shopInv[selpos])[0]
                                player.inventory.append(currentRoom.shopInv[selpos])
                                currentRoom.shopInv.pop(selpos)
                            else:
                                thumby.display.drawText("Not", 0, 24, 1)
                                thumby.display.drawText("enough", 0, 32, 1)
                                thumby.display.update()
                                while(getcharinputNew() == ' '):
                                    thumby.display.update()

        elif(player.helditem != -1):
            # If the player is holding an item, try using it
            if(itemtile(player.inventory[player.helditem]).tiledata[0] == 0):
                # Held item is a sword
                curMsg = "swing!"
            elif(itemtile(player.inventory[player.helditem]).tiledata[0] == 1):
                # Held item is a bow, shoot an arrow
                x = player.tilex
                y = player.tiley
                if(player.facing == 0):
                    # Player is facing upwards
                    y = player.tiley - 1
                    while(currentRoom.getTile(x, y).tiletype == 0):
                        y = y - 1
                elif(player.facing == 2):
                    # Player is facing downward
                    y = player.tiley + 1
                    while(currentRoom.getTile(x, y).tiletype == 0):
                        y = y + 1
                elif(player.facing == 1):
                    # Player is facing right
                    x = player.tilex + 1
                    while(currentRoom.getTile(x, y).tiletype == 0):
                        x = x + 1
                elif(player.facing == 3):
                    # Player is facing left
                    x = player.tilex - 1
                    while(currentRoom.getTile(x, y).tiletype == 0):
                        x = x - 1
                if(currentRoom.getTile(x, y).tiletype == 8):
                    # Hit monster, deal damage
                    dmgrng = itemdmg(player.inventory[player.helditem])
                    dmg = randint(dmgrng[0], dmgrng[1])
                    currentRoom.getTile(x, y).tiledata[1] = currentRoom.getTile(x, y).tiledata[1] - dmg
                    curMsg = "hit " + str(dmg) + "pts"
                    if(currentRoom.getTile(x, y).tiledata[1] <= 0):
                        # Monster is dead
                        currentRoom.getTile(x, y).tiledata.clear()
                        currentRoom.getTile(x, y).tiletype = 0
                        addgp()
                else:
                    curMsg = "missed."

            elif(itemtile(player.inventory[player.helditem]).tiledata[0] == 7):
                # Held item is a spell, try casting it
                if(player.mp >= manacost(player.inventory[player.helditem])):
                    player.mp = player.mp - manacost(player.inventory[player.helditem])
                    x = player.tilex
                    y = player.tiley
                    if(player.facing == 0):
                        # Player is facing upwards
                        y = player.tiley - 1
                        while(currentRoom.getTile(x, y).tiletype == 0):
                            y = y - 1
                    elif(player.facing == 2):
                        # Player is facing downward
                        y = player.tiley + 1
                        while(currentRoom.getTile(x, y).tiletype == 0):
                            y = y + 1
                    elif(player.facing == 1):
                        # Player is facing right
                        x = player.tilex + 1
                        while(currentRoom.getTile(x, y).tiletype == 0):
                            x = x + 1
                    elif(player.facing == 3):
                        # Player is facing left
                        x = player.tilex - 1
                        while(currentRoom.getTile(x, y).tiletype == 0):
                            x = x - 1
                    if(currentRoom.getTile(x, y).tiletype == 8 and player.inventory[player.helditem] != "bsc heal" and player.inventory[player.helditem] != "adv heal" and player.inventory[player.helditem] != "ult heal"):
                        # Hit monster, deal damage
                        dmgrng = itemdmg(player.inventory[player.helditem])
                        dmg = randint(dmgrng[0], dmgrng[1])
                        currentRoom.getTile(x, y).tiledata[1] = currentRoom.getTile(x, y).tiledata[1] - dmg
                        curMsg = "hit " + str(dmg) + "pts"
                        if(currentRoom.getTile(x, y).tiledata[1] <= 0):
                            # Monster is dead
                            currentRoom.getTile(x, y).tiledata.clear()
                            currentRoom.getTile(x, y).tiletype = 0
                            addgp()

                        if(player.inventory[player.helditem] == "bsc cnfs"):
                            currentRoom.getTile(x, y).tiledata[2] = currentRoom.getTile(x, y).tiledata[2] + 3
                        elif(player.inventory[player.helditem] == "adv cnfs"):
                            currentRoom.getTile(x, y).tiledata[2] = currentRoom.getTile(x, y).tiledata[2] + 5
                        elif(player.inventory[player.helditem] == "ult cnfs"):
                            currentRoom.getTile(x, y).tiledata[2] = currentRoom.getTile(x, y).tiledata[2] + 8

                        if(player.inventory[player.helditem] == "bsc lch" or player.inventory[player.helditem] == "adv lch" or player.inventory[player.helditem] == "ult lch"):
                            # Leech spell, add damage to health
                            addhp(dmg)
                    elif(player.inventory[player.helditem] != "bsc tlpt" and player.inventory[player.helditem] != "adv tlpt" and player.inventory[player.helditem] == "ult tlpt"):
                        curMsg = "missed."
                    if(player.helditem != -1 and player.inventory[player.helditem] == "bsc tlpt"):
                        currentRoom.getTile(player.tilex, player.tiley).tiletype = 0
                        if(x - player.tilex < 0):
                            dx = x - player.tilex + 1
                            if(dx < -3):
                                dx = -3
                            player.tilex = player.tilex + dx
                        elif(x - player.tilex > 0):
                            dx = x - player.tilex - 1
                            if(dx > 3):
                                dx = 3
                            player.tilex = player.tilex + dx
                        if(y - player.tiley < 0):
                            dy = y - player.tiley + 1
                            if(dy < -3):
                                dy = -3
                            player.tiley = player.tiley + dy
                        elif(y - player.tiley > 0):
                            dy = y - player.tiley - 1
                            if(dy > 3):
                                dy = 3
                            player.tiley = player.tiley + dy
                    elif(player.helditem != -1 and player.inventory[player.helditem] == "adv tlpt"):
                        currentRoom.getTile(player.tilex, player.tiley).tiletype = 0
                        if(x - player.tilex < 0):
                            dx = x - player.tilex + 1
                            if(dx < -5):
                                dx = -5
                            player.tilex = player.tilex + dx
                        elif(x - player.tilex > 0):
                            dx = x - player.tilex - 1
                            if(dx > 5):
                                dx = 5
                            player.tilex = player.tilex + dx
                        if(y - player.tiley < 0):
                            dy = y - player.tiley + 1
                            if(dy < -5):
                                dy = -5
                            player.tiley = player.tiley + dy
                        elif(y - player.tiley > 0):
                            dy = y - player.tiley - 1
                            if(dy > 5):
                                dy = 5
                            player.tiley = player.tiley + dy
                    elif(player.helditem != -1 and player.inventory[player.helditem] == "ult tlpt"):
                        currentRoom.getTile(player.tilex, player.tiley).tiletype = 0
                        if(x - player.tilex < 0):
                            dx = x - player.tilex + 1
                            if(dx < -7):
                                dx = -7
                            player.tilex = player.tilex + dx
                        elif(x - player.tilex > 0):
                            dx = x - player.tilex - 7
                            if(dx > 7):
                                dx = 7
                            player.tilex = player.tilex + dx
                        if(y - player.tiley < 0):
                            dy = y - player.tiley + 1
                            if(dy < -7):
                                dy = -7
                            player.tiley = player.tiley + dy
                        elif(y - player.tiley > 0):
                            dy = y - player.tiley - 1
                            if(dy > 7):
                                dy = 7
                            player.tiley = player.tiley + dy
                    if(player.inventory[player.helditem] == "bsc heal"):
                        addhp(3)
                    elif(player.inventory[player.helditem] == "adv heal"):
                        addhp(5)
                    elif(player.inventory[player.helditem] == "ult heal"):
                        addhp(8)
                else:
                    curMsg = "no mana!"

            elif(player.helditem != -1 and itemtile(player.inventory[player.helditem]).tiledata[0] == 2):
                # Held item is a potion, drink it
                curMsg = "yuck!"
                if(player.inventory[player.helditem] == "sml hpot"):
                    addhp(5)
                elif(player.inventory[player.helditem] == "sml mpot"):
                    addmp(5)
                elif(player.inventory[player.helditem] == "big hpot"):
                    addhp(8)
                elif(player.inventory[player.helditem] == "big mpot"):
                    addmp(8)
                player.wt = player.wt - itemwt(player.inventory[player.helditem])
                player.inventory.pop(player.helditem)
                player.helditem = -1

            elif(player.helditem != -1 and player.inventory[player.helditem] == "food"):
                # Held item is food, eat it
                curMsg = "yum!"
                player.inventory.pop(player.helditem)
                player.helditem = -1
                player.wt = player.wt - 1
                addhp(3)

            elif(player.helditem != -1 and player.inventory[player.helditem] == "hpup"):
                # Held item is hpup
                curMsg = "+5 maxhp!"
                player.wt = player.wt - itemwt(player.inventory[player.helditem])
                player.inventory.pop(player.helditem)
                player.helditem = -1
                player.maxhp = player.maxhp + 5

            elif(player.helditem != -1 and player.inventory[player.helditem] == "mpup"):
                # Held item is hpup
                curMsg = "+5 maxmp!"
                player.wt = player.wt - itemwt(player.inventory[player.helditem])
                player.inventory.pop(player.helditem)
                player.helditem = -1
                player.maxmp = player.maxmp + 5

            else:
                # Action couldn't be resolved
                curMsg = "???"

        else:
            # Action couldn't be resolved
            curMsg = "???"


weaponLevel = {
    0: "brkn",
    1: "basic",
    2: "",
    3: "good",
    4: "ultra",
    5: "epic"
}
potionLevel = {
    0: "sml ",
    1: "big "
}
spellLevel = {
    0: "bsc ",
    1: "adv ",
    2: "ult "
}
spellType = {
    0: "fblt",
    1: "eblt",
    2: "cnfs",
    3: "lch",
    4: "tlpt",
    5: "heal"
}

# TODO: Refactor lists of items
t1Items = ("brknswd", "basicswd", "brknbow", "basicbow", "sml hpot", "sml mpot", "food", "shirt", "pants", "bsc cnfs", "bsc fblt", "bsc eblt", "bsc tlpt", "bsc lch", "bsc heal")
t2Items = ("swd", "bow", "goodswd", "goodbow", "big hpot", "big mpot", "hpup", "mpup", "adv cnfs", "adv fblt", "adv eblt", "adv tlpt", "adv lch", "adv heal")
t3Items = ("epicswd", "ultraswd", "epicbow", "ultrabow", "ult cnfs", "ult fblt", "ult eblt", "ult tlpt", "ult lch", "ult heal")

def manacost(itemName):
    items = {
        "bsc cnfs": 3,
        "bsc fblt": 4,
        "bsc eblt": 5,
        "bsc lch": 3,
        "bsc tlpt": 4,
        "bsc heal": 5,
        "adv cnfs": 5,
        "adv fblt": 7,
        "adv eblt": 8,
        "adv lch": 6,
        "adv tlpt": 7,
        "adv heal": 9,
        "ult cnfs": 9,
        "ult fblt": 10,
        "ult eblt": 11,
        "ult lch": 9,
        "ult tlpt": 8,
        "ult heal": 12,
    }
    return items.get(itemName, 0)

# Given an item name, return the buy/sell price in gp
def itemprice(itemName):
    items = {
        "brknswd": [4, 2],
        "basicswd": [10, 4],
        "swd": [20, 8],
        "goodswd": [35, 15],
        "epicswd": [55, 20],
        "ultraswd": [70, 25],
        "brknbow": [4, 2],
        "basicbow": [10, 4],
        "bow": [20, 8],
        "goodbow": [35, 15],
        "epicbow": [55, 20],
        "ultrabow": [70, 25],
        "bsc cnfs": [14, 5],
        "bsc fblt": [12, 6],
        "bsc eblt": [13, 5],
        "bsc lch": [15, 7],
        "bsc heal": [17, 8],
        "bsc tlpt": [15, 7],
        "adv cnfs": [30, 10],
        "adv fblt": [25, 10],
        "adv eblt": [25, 11],
        "adv lch": [32, 15],
        "adv heal": [35, 17],
        "adv tlpt": [32, 15],
        "ult cnfs": [55, 20],
        "ult fblt": [50, 18],
        "ult eblt": [50, 20],
        "ult lch": [65, 30],
        "ult heal": [75, 37],
        "ult tlpt": [65, 30],
        "pants": [15, 8],
        "shirt": [15, 8],
        "food": [6, 3],
        "sml hpot": [10, 5],
        "sml mpot": [10, 5],
        "big hpot": [15, 7],
        "big mpot": [15, 7],
        "hpup": [50, 25],
        "mpup": [50, 25],
    }
    return items.get(itemName, [0, 0])

# Given an item name, return the range of damage it can deal
def itemdmg(itemName):
    items = {
        "brknswd": [2, 5],
        "basicswd": [3, 7],
        "swd": [5, 8],
        "goodswd": [7, 10],
        "epicswd": [10, 15],
        "ultraswd": [13, 20],
        "brknbow": [2, 4],
        "basicbow": [3, 5],
        "bow": [3, 7],
        "goodbow": [5, 8],
        "epicbow": [7, 9],
        "ultrabow": [8, 11],
        "bsc cnfs": [0, 1],
        "bsc fblt": [3, 6],
        "bsc eblt": [4, 6],
        "bsc lch": [1, 2],
        "adv cnfs": [1, 2],
        "adv fblt": [6, 8],
        "adv eblt": [6, 8],
        "adv lch": [2, 4],
        "ult cnfs": [1, 3],
        "ult fblt": [8, 10],
        "ult eblt": [9, 11],
        "ult lch": [3, 5],
    }
    return items.get(itemName, [1, 3])


# Given an item tile, spit out the name of the item
def itemname(itemTile):
    swords = {
        -1: "brknswd",
        0: "basicswd",
        1: "swd",
        2: "goodswd",
        3: "epicswd",
        4: "ultraswd",
    }
    bows = {
        -1: "brknbow",
        0: "basicbow",
        1: "bow",
        2: "goodbow",
        3: "epicbow",
        4: "ultrabow",
    }
    pots = {
        0: "sml hpot",
        1: "sml mpot",
        2: "big hpot",
        3: "big mpot",
    }
    spells = {
        0: "bsc cnfs",
        1: "bsc fblt",
        2: "bsc eblt",
        3: "bsc lch",
        4: "bsc tlpt",
        5: "bsc heal",
        6: "adv cnfs",
        7: "adv fblt",
        8: "adv eblt",
        9: "adv lch",
        10: "adv tlpt",
        11: "adv heal",
        12: "ult cnfs",
        13: "ult fblt",
        14: "ult eblt",
        15: "ult lch",
        16: "ult tlpt",
        17: "ult heal",
    }
    if(itemTile.tiledata[0] == 0):
        return swords.get(itemTile.tiledata[1], "??? swd")
    elif(itemTile.tiledata[0] == 1):
        return bows.get(itemTile.tiledata[1], "??? bow")
    elif(itemTile.tiledata[0] == 2):
        return pots.get(itemTile.tiledata[1], "??? pot")
    elif(itemTile.tiledata[0] == 3):
        return "key"
    elif(itemTile.tiledata[0] == 4):
        return "food"
    elif(itemTile.tiledata[0] == 5):
        return "pants"
    elif(itemTile.tiledata[0] == 6):
        return "shirt"
    elif(itemTile.tiledata[0] == 7):
        return spells.get(itemTile.tiledata[1], "??? tome")
    elif(itemTile.tiledata[0] == 8):
        return "hpup"
    elif(itemTile.tiledata[0] == 9):
        return "mpup"
    else:
        return "???"

# Given the name of an item, spit out the equivalent tile
def itemtile(itemName):
    tiles = {
        "brknswd": dungeonTile(7, 0, -1),
        "basicswd": dungeonTile(7, 0, 0),
        "swd": dungeonTile(7, 0, 1),
        "goodswd": dungeonTile(7, 0, 2),
        "epicswd": dungeonTile(7, 0, 3),
        "ultraswd": dungeonTile(7, 0, 4),
        "??? swd": dungeonTile(7, 0, -2),
        "brknbow": dungeonTile(7, 1, -1),
        "basicbow": dungeonTile(7, 1, 0),
        "bow": dungeonTile(7, 1, 1),
        "goodbow": dungeonTile(7, 1, 2),
        "epicbow": dungeonTile(7, 1, 3),
        "ultrabow": dungeonTile(7, 1, 4),
        "??? bow": dungeonTile(7, 1, -2),
        "sml hpot": dungeonTile(7, 2, 0),
        "sml mpot": dungeonTile(7, 2, 1),
        "big hpot": dungeonTile(7, 2, 2),
        "big mpot": dungeonTile(7, 2, 3),
        "??? pot": dungeonTile(7, 2, -2),
        "key": dungeonTile(7, 3),
        "food": dungeonTile(7, 4),
        "pants": dungeonTile(7, 5),
        "shirt": dungeonTile(7, 6),
        "bsc cnfs": dungeonTile(7, 7, 0),
        "bsc fblt": dungeonTile(7, 7, 1),
        "bsc eblt": dungeonTile(7, 7, 2),
        "bsc lch": dungeonTile(7, 7, 3),
        "bsc tlpt": dungeonTile(7, 7, 4),
        "bsc heal": dungeonTile(7, 7, 5),
        "adv cnfs": dungeonTile(7, 7, 6),
        "adv fblt": dungeonTile(7, 7, 7),
        "adv eblt": dungeonTile(7, 7, 8),
        "adv lch": dungeonTile(7, 7, 9),
        "adv tlpt": dungeonTile(7, 7, 10),
        "adv heal": dungeonTile(7, 7, 11),
        "ult cnfs": dungeonTile(7, 7, 12),
        "ult fblt": dungeonTile(7, 7, 13),
        "ult eblt": dungeonTile(7, 7, 14),
        "ult lch": dungeonTile(7, 7, 15),
        "ult tlpt": dungeonTile(7, 7, 16),
        "ult heal": dungeonTile(7, 7, 17),
        "??? tome": dungeonTile(7, 7, -2),
        "hpup": dungeonTile(7, 8),
        "mpup": dungeonTile(7, 9),
    }
    return tiles.get(itemName, dungeonTile(0, 0, 0))

# Given the name of an item, return its weight
def itemwt(itemName):
    switcher = {
        "brknswd": 2,
        "basicswd": 2,
        "swd": 2,
        "goodswd": 3,
        "epicswd": 3,
        "ultraswd": 3,
        "??? swd": 2,
        "brknbow": 2,
        "basicbow": 2,
        "bow": 2,
        "goodbow": 2,
        "epicbow": 3,
        "ultrabow": 3,
        "??? bow":2,
        "sml hpot": 1,
        "sml mpot": 1,
        "big hpot": 2,
        "big mpot": 2,
        "??? pot": 1,
        "key": 1,
        "food": 1,
        "pants": 3,
        "shirt": 3,
        "bsc cnfs": 1,
        "bsc fblt": 1,
        "bsc eblt": 1,
        "bsc lch": 1,
        "bsc tlpt": 1,
        "bsc heal": 1,
        "adv cnfs": 1,
        "adv fblt": 1,
        "adv eblt": 1,
        "adv lch": 1,
        "adv tlpt": 1,
        "adv heal": 1,
        "ult cnfs": 1,
        "ult fblt": 1,
        "ult eblt": 1,
        "ult lch": 1,
        "ult tlpt": 1,
        "ult heal": 1,
        "??? tome": 1,
        "hpup": 2,
        "mpup": 2,
    }
    return switcher.get(itemName, 0)


class dungeonRoom:
    def __init__(self):
        gc_collect()
        self.tiles = []
        self.shopInv = []
        self.hasShop = False
        
        
        for y in range(5):
            for x in range(9):
                if x == 0 or x == 8 or y == 0 or y == 4:
                    # Wall tiles
                    self.tiles.append(dungeonTile(1))
                else:
                    # Floor tiles
                    self.tiles.append(dungeonTile(0))

    # draws the tiles of the room ONLY
    def drawRoom(self, xx=0, yy=0):
        for x in range(9):
            for y in range(5):
                tile = self.tiles[y * 9 + x]
                if tile.tiletype == 1:
                    # Block tile
                    thumby.display.blit(blockSpr, x * 8 + xx, y * 8 + yy, 8, 8, -1, 0, 0)
                elif tile.tiletype == 2:
                    # Door tile
                    thumby.display.blit(doorSpr, x * 8 + xx, y * 8 + yy, 8, 8, -1, 0, 0)
                elif tile.tiletype == 3:
                    # Stairs tile
                    thumby.display.blit(stairSpr, x * 8 + xx, y * 8 + yy, 8, 8, -1, 0, 0)
                elif tile.tiletype == 4:
                    # Sign tile
                    thumby.display.blit(signSpr, x * 8 + xx, y * 8 + yy, 8, 8, -1, 0, 0)
                elif tile.tiletype == 5:
                    # The player
                    thumby.display.drawText("@", (x * 8) + 1 + xx, (y * 8) + 1 + yy, 1)
                elif tile.tiletype == 6:
                    # Chest tile
                    thumby.display.blit(chestSpr, x * 8 + xx, y * 8 + yy, 8, 8, -1, 0, 0)
                elif tile.tiletype == 7:
                    # item tile
                    thumby.display.blit(itemSprites[int(tile.tiledata[0])], x * 8 + xx, y * 8 + yy, 8, 8, -1, 0, 0)
                elif tile.tiletype == 8:
                    # Monster tile
                    if ticks_ms() % 1000 > 500:
                        thumby.display.blit(monsterSprites[int(tile.tiledata[0])], x * 8 + xx, y * 8 + yy, 8, 8, 0, 0, 0)
                    else:
                        thumby.display.blit(monsterSprites[int(tile.tiledata[0])], x * 8 + xx, y * 8 - 1 + yy, 8, 8, 0, 0, 0)
        if self.hasShop:
            thumby.display.blit(shopSpr, 16 + xx, 8 + yy, 16, 16, -1, 0, 0)


    def getTile(self, tx, ty):
        return self.tiles[ty*9+tx]
    


class playerobj:
    def __init__(self):
        self.hp = 20
        self.maxhp = 20
        self.armor = 0
        self.mp = 15
        self.maxmp = 15
        # self.name = newname
        self.tilex = 4
        self.tiley = 2
        self.wt = itemwt("basicswd") + itemwt("pants") + itemwt("sml hpot") + itemwt("sml mpot") + itemwt("bsc cnfs")
        self.maxwt = 30
        self.inventory = ["basicswd", "pants", "sml hpot", "sml mpot", "bsc cnfs"]
        self.helditem = 0 # Pre-equip basicswd
        self.shirtitem = -1
        self.pantsitem = 1 # Pre-equip pants
        self.facing = 0 # 0 up, 1 right, 2 down, 3 left.
        self.gp = 0
    
    def unload(self):
        list = [self.hp, self.maxhp, self.armor, self.mp, self.maxmp, self.tilex, self.tiley, self.wt, self.inventory,
                self.helditem, self.shirtitem, self.pantsitem, self.gp]
        return list

    def load(self, list):
        if list is not None:
            self.hp, self.maxhp, self.armor, self.mp, self.maxmp, self.tilex, self.tiley, self.wt, self.inventory, self.helditem, self.shirtitem, self.pantsitem, self.gp = list
        


def getRandomFreePosition(room):
    px = randint(1, 7)
    py = randint(1, 3)
    # Check that tile is empty and there are no doors this could block
    while(room.getTile(px, py).tiletype != 0 or ((px==4 and (py==1 or py==3)) or (py==2 and (px==1 or px==7))) ):
        px = randint(1, 7)
        py = randint(1, 3)
    return [px, py]

floorNo = 1
roomno = 0
maxrooms = 12
exitSpawned = False


# Procedural generation of dungeon rooms
def generateRoom(room):
    global roomno
    global maxrooms
    global exitSpawned
    global currentRoom
    if(roomno < maxrooms):
        roomno = roomno + 1
        # Generating doors may create up to 3 more rooms
        for k in [0,1,2]:
            # Each wall has a 1 in (k+1) chance of having a door to another room
            if(randint(0, k) == 0):
                # Adding a door, there's an equal chance for N/E/S/W location
                doorDefined = False
                if(randint(0, 1) == 0):
                    # Add either a North or South door
                    doorOutX = playerOutX = doorBackX = playerBackX = 4
                    if(randint(0, 1) == 0 and room.getTile(4, 0).tiletype != 2):
                        # Put door on North wall
                        doorOutY = 0
                        playerOutY = doorOutY+1
                        # Returning door on South wall
                        doorBackY = 4
                        playerBackY = doorBackY-1
                        doorDefined = True
                    elif(room.getTile(4, 4).tiletype != 2):
                        # Put door on South wall
                        doorOutY = 4
                        playerOutY = doorOutY-1
                        # Returning door on North wall
                        doorBackY = 0
                        playerBackY = doorBackY+1
                        doorDefined = True
                else:
                    # Add either a West or East door
                    doorOutY = playerOutY = doorBackY = playerBackY = 2
                    if(randint(0, 1) == 0 and room.getTile(0, 2).tiletype != 2):
                        # Put door on West wall
                        doorOutX = 0
                        playerOutX = doorOutX+1
                        # Returning door on East wall
                        doorBackX = 8
                        playerBackX = doorBackX-1
                        doorDefined = True
                    elif(room.getTile(8, 2).tiletype != 2):
                        # Put door on East wall
                        doorOutX = 8
                        playerOutX = doorOutX-1
                        # Returning door on West wall
                        doorBackX = 0
                        playerBackX = doorBackX+1
                        doorDefined = True
                # Generate doorways for leaving and returning
                if(doorDefined):
                    room.getTile(doorOutX,doorOutY).tiletype = 2
                    room.getTile(doorOutX,doorOutY).tiledata.append(dungeonRoom())
                    room.getTile(doorOutX,doorOutY).tiledata.append(playerBackX)
                    room.getTile(doorOutX,doorOutY).tiledata.append(playerBackY)
                    room.getTile(doorOutX,doorOutY).tiledata[0].getTile(doorBackX,doorBackY).tiletype = 2
                    room.getTile(doorOutX,doorOutY).tiledata[0].getTile(doorBackX,doorBackY).tiledata.append(room)
                    room.getTile(doorOutX,doorOutY).tiledata[0].getTile(doorBackX,doorBackY).tiledata.append(playerOutX)
                    room.getTile(doorOutX,doorOutY).tiledata[0].getTile(doorBackX,doorBackY).tiledata.append(playerOutY)
                    # Recursively generate doors and new rooms until maxrooms
                    generateRoom(room.getTile(doorOutX,doorOutY).tiledata[0])

    # Place stairs to exit floor in the last room, at fixed position
    if(not exitSpawned):
        room.getTile(7, 3).tiletype = 3
        exitSpawned = True

    # Each room (except starting room) has a 10% chance of having a shopkeep
    if(room != currentRoom and randint(0, 9) == 0):
        room.hasShop = True
        room.getTile(2, 1).tiletype = 9
        room.getTile(3, 1).tiletype = 9
        room.getTile(2, 2).tiletype = 9
        room.getTile(3, 2).tiletype = 9
        for i in range(randint(2, 4)):
            room.shopInv.append(t1Items[randint(0, len(t1Items)-1)])
        for i in range(randint(1, 3)):
            room.shopInv.append(t2Items[randint(0, len(t2Items)-1)])
        for i in range(randint(0, 2)):
            room.shopInv.append(t3Items[randint(0, len(t3Items)-1)])

    # Each room has a 10% chance of having a sign
    if(randint(0, 9) == 0):
        room.getTile(4, 2).tiletype = 4
        room.getTile(4, 2).tiledata = signMessages[randint(0, len(signMessages) - 1)]

    # Each room has a 15% chance of having a chest in it
    if(randint(0, 19) < 3):
        pos = getRandomFreePosition(room)
        room.getTile(pos[0], pos[1]).tiletype = 6

    # Each room has a 35% chance of having a piece of loot in it
    if(randint(0, 19) <  7):
        pos = getRandomFreePosition(room)
        item = dungeonTile(0)
        lootChance = randint(0, 99)
        if(lootChance < 88):
            # 88% is basic-tier loot
            lootTier = 0
            lootType = randint(0, 5)
        elif(lootChance < 98):
            # 10% is normal or good-tier loot
            lootTier = 1
            lootType = randint(0, 4)
        else:
            # 2% is epic or ultra-tier loot
            lootTier = 2
            lootType = randint(0, 2)
        if(lootType == 0):
            # Sword
            item = itemtile(weaponLevel.get(randint(0,1)+(2*lootTier))+"swd")
        elif(lootType == 1):
            # Bow
            item = itemtile(weaponLevel.get(randint(0,1)+(2*lootTier))+"bow")
        elif(lootType == 2):
            # Spell
            item = itemtile(spellLevel.get(lootTier)+spellType.get(randint(0,5), "??? tome"))
        elif(lootType == 3):
            # Potion
            if(randint(0, 1) == 0):
                item = itemtile(potionLevel.get(lootTier)+"hpot")
            else:
                item = itemtile(potionLevel.get(lootTier)+"mpot")
        elif(lootType == 4):
            # Player stats booster
            if(lootTier == 0):
                if(randint(0, 1) == 0):
                    item = itemtile("shirt")
                else:
                    item = itemtile("pants")
            else:
                if(randint(0, 1) == 0):
                    item = itemtile("hpup")
                else:
                    item = itemtile("mpup")
        else:
            # Food
            item = itemtile("food")
        room.getTile(pos[0], pos[1]).tiletype = item.tiletype
        room.getTile(pos[0], pos[1]).tiledata = item.tiledata.copy()

    # Each room has a 50% chance of one or more monsters
    if(randint(0, 1) == 0):
        monsters = 1
        # 10% chance the room contains a horde of monsters (except first room)
        if(room != currentRoom and randint(0, 9) == 0):
            if(floorNo < 4):
                monsters = 2
            else:
                monsters = 3
                if(room != currentRoom and randint(0, 5) == 0):
                    monsters = 4
            
        for i in range(monsters):
            pos = getRandomFreePosition(room)
            room.getTile(pos[0], pos[1]).tiletype = 8
            room.getTile(pos[0], pos[1]).tiledata.append(randint(0, len(monsterSprites) - 1))
            room.getTile(pos[0], pos[1]).tiledata.append(randint(10, 15) + 2 * floorNo)
            room.getTile(pos[0], pos[1]).tiledata.append(1)


# Draw the entire gamestate, including Heads-Up-Display (HUD)
def drawGame():
    global display
    global curMsg
    thumby.display.fill(0)
    currentRoom.drawRoom()
    
    hpHUDWidth=(len(str(player.hp))+1)*fontWidth
    thumby.display.drawRectangle(1, 1, hpHUDWidth, 8, 1)
    thumby.display.drawFilledRectangle(0, 0, hpHUDWidth, 8, 0)
    thumby.display.drawText(str(player.hp), 6, 0, 1)
    thumby.display.blit(hpSpr,0,0,5,8,-1,0,0)

    mpHUDWidth=(len(str(player.mp))+1)*fontWidth
    thumby.display.drawRectangle(71-mpHUDWidth, 1, 32, 8, 1)
    thumby.display.drawFilledRectangle(72-mpHUDWidth, 0, 32, 8, 0)
    thumby.display.drawText(str(player.mp), 73-mpHUDWidth, 0, 1)
    thumby.display.blit(mpSpr,67,0,5,8,-1,0,0)

    floorHUD=str(floorNo)+"F"
    floorHUDWidth=len(floorHUD)*fontWidth
    thumby.display.drawRectangle(71-floorHUDWidth, 31, 32, 9, 1)
    thumby.display.drawFilledRectangle(72-floorHUDWidth, 32, 32, 8, 0)
    thumby.display.drawText(floorHUD, 73-floorHUDWidth, 33, 1)

    if(curMsg == ""):
        # Default will show the Player's gold pieces
        curMsg = goldChr+str(player.gp)

    curMsgWidth=len(curMsg)*fontWidth
    thumby.display.drawRectangle(0, 31, curMsgWidth+1, 9, 1)
    thumby.display.drawFilledRectangle(0, 32, curMsgWidth, 8, 0)
    thumby.display.drawText(curMsg, 0, 33, 1)

    thumby.display.update()

def showGame(x, y):
    global display
    global curMsg
    currentRoom.drawRoom(x,y)
    
    hpHUDWidth = (len(str(player.hp)) + 1) * fontWidth
    thumby.display.drawRectangle(x + 1, y + 1, hpHUDWidth, 8, 1)
    thumby.display.drawFilledRectangle(x + 0, y + 0, hpHUDWidth, 8, 0)
    thumby.display.drawText(str(player.hp), x + 6, y + 0, 1)
    thumby.display.blit(hpSpr, x + 0, y + 0, 5, 8, -1, 0, 0)

    mpHUDWidth = (len(str(player.mp)) + 1) * fontWidth
    thumby.display.drawRectangle(x + 71 - mpHUDWidth, y + 1, 32, 8, 1)
    thumby.display.drawFilledRectangle(x + 72 - mpHUDWidth, y + 0, 32, 8, 0)
    thumby.display.drawText(str(player.mp), x + 73 - mpHUDWidth, y + 0, 1)
    thumby.display.blit(mpSpr, x + 67, y + 0, 5, 8, -1, 0, 0)

    floorHUD = str(floorNo) + "F"
    floorHUDWidth = len(floorHUD) * fontWidth
    thumby.display.drawRectangle(x + 71 - floorHUDWidth, y + 31, 32, 9, 1)
    thumby.display.drawFilledRectangle(x + 72 - floorHUDWidth, y + 32, 32, 8, 0)
    thumby.display.drawText(floorHUD, x + 73 - floorHUDWidth, y + 33, 1)

    if curMsg == "":
        # Default will show the Player's gold pieces
        curMsg = goldChr + str(player.gp)

    curMsgWidth = len(curMsg) * fontWidth
    thumby.display.drawRectangle(x + 0, y + 31, curMsgWidth + 1, 9, 1)
    thumby.display.drawFilledRectangle(x + 0, y + 32, curMsgWidth, 8, 0)
    thumby.display.drawText(curMsg, x + 0, y + 33, 1)




def updateTurn():
    global turnCounter
    # Restore the player's mana every fourth turn
    if(turnCounter % 3 == 0):
        turnCounter = 0
        addmp(1)
    turnCounter = turnCounter + 1

    # Update Monsters
    for y in [1,2,3]:
        for x in [1,2,3,4,5,6,7]:
            # Check across playable area 3x7 tiles of 5x9 dungeon, for monster tile
            if(currentRoom.getTile(x, y).tiletype == 8):
                # If the monster is not stunned, it can act
                if(currentRoom.getTile(x, y).tiledata[2] == 0):
                    xOffset = 0
                    yOffset = 0
                    dx = player.tilex - x
                    dy = player.tiley - y
                    # If the monster is within range, attack the player
                    if((dx == 0 and abs(dy) == 1) or (dy == 0 and abs(dx) == 1)):
                        global lastHit
                        # Make a random attack damage
                        dmg = randint(1, 5) + randint(0, floorNo)
                        # Handle armor
                        if(player.shirtitem != -1):
                            dmg = dmg - (2+int(floorNo/4))
                        if(player.pantsitem != -1):
                            dmg = dmg - (1+int(floorNo/8))
                        dmg = 1 if dmg < 1 else dmg
                        player.hp = player.hp - dmg
                        lastHit = {0: "blob", 1: "spirit", 2: "arachnid", 3: "skeleton", 4: "wizard", 5: "tempest"}.get(currentRoom.getTile(x, y).tiledata[0], "???")
                    # Else if the monster is not in range, try to move closer
                    elif(abs(dx) > abs(dy)):
                        if(dx < 0):
                            xOffset = -1 # Left
                        else:
                            xOffset = 1 # Right
                    else:
                        if(dy < 0):
                            yOffset = -1 # Up
                        else:
                            yOffset = 1 # Down
                    # Move the monster to the offset tile if it's empty
                    if(currentRoom.getTile(x+xOffset, y+yOffset).tiletype == 0):
                        currentRoom.getTile(x+xOffset, y+yOffset).tiletype = 8
                        currentRoom.getTile(x+xOffset, y+yOffset).tiledata = currentRoom.getTile(x, y).tiledata.copy()
                        currentRoom.getTile(x+xOffset, y+yOffset).tiledata[2] = 1 # Monster is stunned for 1 turn
                        currentRoom.getTile(x, y).tiledata.clear()
                        currentRoom.getTile(x, y).tiletype = 0
                else:
                    # Monster is stunned, decrease the timer
                    currentRoom.getTile(x, y).tiledata[2] = currentRoom.getTile(x, y).tiledata[2] - 1




##-Save-##




def saveAll(player,save = 'save1'):
    global floorNo
    gc_collect()
    p = player.unload()
    thumby.saveData.setItem(save, [p,floorNo])
    thumby.saveData.save()


##------##

##-load-##


def loadAll(save = 'save1'):
    global floorNo
    gc_collect()
    p, fnum = thumby.saveData.getItem(save)
    player = playerobj()
    player.load(p)
    floorNo = fnum

    return player


##------##




##-New Menus-##


# BITMAP: width: 72, height: 40
startSpr = bytearray([160,110,170,102,10,230,170,102,160,110,170,102,10,230,170,102,160,110,170,102,10,6,10,6,0,14,10,6,10,230,170,102,160,110,170,102,10,230,170,102,160,110,170,102,10,6,10,6,0,14,10,6,10,230,170,102,160,110,170,102,10,230,170,102,160,110,170,102,10,230,170,102,
           160,110,170,102,10,230,170,102,160,96,160,96,0,2,2,254,2,2,0,254,16,8,8,240,0,120,128,128,64,248,0,248,8,48,8,240,0,16,40,168,168,120,0,112,168,168,168,48,0,112,136,136,136,112,0,248,16,8,8,240,0,224,160,96,160,110,170,102,10,230,170,102,
           160,110,170,102,10,230,170,102,160,110,170,102,10,230,170,102,160,110,170,102,10,6,10,6,0,14,10,6,10,230,170,102,160,96,160,96,0,224,160,96,160,110,170,102,10,6,10,6,0,14,10,6,10,230,170,102,160,110,170,102,10,230,170,102,160,110,170,102,10,230,170,102,
           160,110,170,102,10,230,170,102,160,96,160,96,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,224,160,96,160,110,170,102,10,230,170,102,
           160,110,170,102,10,230,170,102,160,110,170,102,10,230,170,102,160,110,170,102,10,230,170,102,160,110,170,102,10,230,170,102,160,96,160,96,0,224,160,96,160,110,170,102,10,230,170,102,160,110,170,102,10,230,170,102,160,110,170,102,10,230,170,102,160,110,170,102,10,230,170,102])

saveSpr = bytearray([160,110,170,102,10,230,170,102,160,110,170,102,10,230,170,102,160,110,170,102,10,230,170,102,160,110,170,102,10,230,170,102,160,110,170,102,10,230,170,102,160,110,170,102,10,230,170,102,160,110,170,102,10,230,170,102,160,110,170,102,10,230,170,102,160,110,170,102,10,230,170,102,
           160,110,170,102,10,6,10,6,0,112,136,136,0,248,32,192,0,96,144,96,0,160,80,0,96,208,160,0,0,224,160,96,160,110,170,102,10,6,10,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,14,10,6,10,230,170,102,
           160,110,170,102,10,6,138,198,192,128,0,72,84,36,0,104,88,112,0,56,64,56,0,48,104,80,0,0,0,224,160,96,160,110,170,102,10,6,10,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,14,10,6,10,230,170,102,
           160,110,170,102,10,6,11,7,1,2,240,200,228,232,224,160,192,0,0,0,0,0,0,0,0,0,0,40,28,252,184,96,160,110,170,102,10,6,10,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,14,10,6,10,230,170,102,
           160,110,170,102,10,230,170,102,160,110,170,103,10,230,171,103,160,110,170,102,10,230,170,102,160,110,170,102,10,230,170,102,160,110,170,102,10,230,170,102,160,110,170,102,10,230,170,102,160,110,170,102,10,230,170,102,160,110,170,102,10,230,170,102,160,110,170,102,10,230,170,102])

loadingSpr = bytearray([160,110,170,102,10,230,170,102,160,110,170,102,10,6,10,198,32,238,42,198,10,6,10,6,0,14,10,6,10,230,170,102,160,110,170,102,10,230,170,102,160,110,170,102,10,6,10,6,0,14,10,6,10,6,10,6,0,14,10,6,10,230,170,102,160,110,170,102,10,230,170,102,
           160,110,170,102,10,230,170,102,160,96,160,96,0,0,2,4,7,3,1,0,0,0,0,0,0,0,64,160,32,0,64,192,128,14,202,6,202,6,10,166,0,0,192,64,128,0,128,64,192,0,0,0,0,0,0,0,0,24,84,92,84,184,168,40,0,14,10,6,10,230,170,102,
           160,110,170,102,10,6,10,6,0,0,32,152,252,238,152,32,244,8,0,0,0,192,224,160,64,0,2,2,1,0,3,2,3,0,1,2,1,0,0,131,128,128,131,0,3,0,2,3,3,0,0,0,0,224,160,96,160,96,160,97,1,224,160,96,160,110,170,102,10,230,170,102,
           160,110,170,102,10,230,170,102,160,110,171,103,11,231,171,102,160,96,160,102,1,250,175,122,161,102,160,96,0,192,224,224,224,64,0,0,0,192,35,21,87,247,85,19,32,192,0,0,0,0,0,52,30,254,190,124,160,110,170,102,10,230,170,102,160,110,170,102,10,230,170,102,
           160,110,170,102,10,230,170,102,160,110,170,102,10,230,170,102,160,110,170,102,10,230,170,102,160,110,170,102,10,231,171,103,161,99,160,96,1,226,176,125,162,99,162,125,16,226,161,96,160,110,170,102,10,230,170,102,160,110,170,102,10,230,170,102,160,110,170,102,10,230,170,102])

thumby.saveData.setName('Thumgeon')
save = 'save1'

start = thumby.Sprite(72, 40, startSpr, 0, 0)
saveScreen = thumby.Sprite(72, 40, saveSpr, 0, 0)
loadingScreen = thumby.Sprite(72, 40, loadingSpr, 0, 0)

while(thumby.actionJustPressed()):
    thumby.display.update()
        
thumby.display.fill(0)
thumby.display.drawSprite(start)
while(not thumby.actionJustPressed()):
    tick = ticks_ms() % 1000 < 500
    if tick == 1:
        thumby.display.drawFilledRectangle(17, 25, 41, 7, 0)
        thumby.display.drawText(">Start<", 17, 25, 1)
    else:
        thumby.display.drawFilledRectangle(17, 25, 41, 7, 0)
        thumby.display.drawText(" Start", 17, 25, 1)
    thumby.display.update()
    
thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)
saves = [0,0,0]
select = 0
if thumby.saveData.hasItem('save1'):
    saves[0] = 1
if thumby.saveData.hasItem('save2'):
    saves[1] = 1
if thumby.saveData.hasItem('save3'):
    saves[2] = 1

clicked = False
slide = 72

while True:
    thumby.display.fill(0)
    thumby.display.blit(startSpr,int(slide)-72,0,72,40,0,0,0)
    thumby.display.blit(saveSpr,int(slide),0,72,40,0,0,0)
    thumby.display.blit(spiritSpr,18+int(slide),24,8, 8, 0, 0, 0)
    for x in range(3):
        if saves[x]:
            if select == x:
                thumby.display.drawText(":", 62+int(slide), 11+(x*7), 1)
                thumby.display.drawText("-", 62+int(slide), 11+(x*7), 1)
            thumby.display.drawText("Save"+str(x+1), 42+int(slide), 11+(x*7), 1)
            
        else:
            if select == x:
                thumby.display.drawText(":", 62+int(slide), 11+(x*7), 1)
                thumby.display.drawText("-", 62+int(slide), 11+(x*7), 1)
            thumby.display.drawText("None", 44+int(slide), 11+(x*7), 1)
    thumby.display.update()
    
    if slide/6 < 2:
        s = 2
    else:
        s = slide/6
    slide -= s
    if int(slide) <= 0:
        break
        



while True:
    thumby.display.drawSprite(saveScreen)
    tick = ticks_ms() % 1000 < 500
    if tick == 1:
        thumby.display.blit(spiritSpr,18,24,8, 8, 0, 0, 0)
    else:
        thumby.display.blit(spiritSpr,18,23,8, 8, 0, 0, 0)
    for x in range(3):
        if saves[x]:
            if select == x:
                thumby.display.drawText(":", 62, 11+(x*7), 1)
                thumby.display.drawText("-", 62, 11+(x*7), 1)
            thumby.display.drawText("Save"+str(x+1), 42, 11+(x*7), 1)
            
        else:
            if select == x:
                thumby.display.drawText(":", 62, 11+(x*7), 1)
                thumby.display.drawText("-", 62, 11+(x*7), 1)
            thumby.display.drawText("None", 44, 11+(x*7), 1)
    
    thumby.display.update()
    
    if thumby.buttonD.pressed():
        if select != 2 and clicked == False:
            select += 1
        clicked = True
    
    if thumby.buttonU.pressed():
        if select != 0 and clicked == False:
            select -= 1
        clicked = True
    
    if not thumby.buttonD.pressed() and not thumby.buttonU.pressed():
        clicked = False
    
    if thumby.actionJustPressed():
        save = 'save'+str(select+1)
        break
    

thumby.display.setFont("/lib/font5x7.bin", 5, 7, 1)

slide = 40

while True:
    thumby.display.fill(0)
    thumby.display.blit(saveSpr,0,int(slide)-40,72,40,0,0,0)
    thumby.display.blit(loadingSpr,0,int(slide),72,40,0,0,0)
    thumby.display.update()
    
    if slide/6 < 2:
        s = 2
    else:
        s = slide/6
    slide -= s
    if int(slide) == 0:
        break





def loadScreen():
    slide = 72

    while True:
        thumby.display.fill(0)
        currentRoom.getTile(player.tilex, player.tiley).tiletype = 5
        showGame(0,0)
        thumby.display.drawFilledRectangle(int(slide)-72, 0, 72, 40, 0)
        thumby.display.blit(loadingSpr,int(slide)-72,0,72,40,0,0,0)
        thumby.display.update()
        if slide/8 < 2:
            s = 2
        else:
            s = slide/8
        slide -= s
        if int(slide) == 0:
            break


##-----------##
#a
DeathMain = bytearray([160,110,170,102,10,6,10,6,0,110,138,6,138,102,10,6,128,142,138,6,10,134,10,6,0,142,10,6,10,6,10,6,0,14,138,134,10,230,10,6,128,174,10,6,10,6,138,134,128,14,10,6,138,134,10,230,0,14,10,6,10,230,170,102,160,110,170,102,10,230,170,102,
           160,110,170,102,10,230,170,102,160,96,160,111,0,224,160,103,168,104,168,103,0,231,168,104,164,111,160,96,0,224,160,96,160,103,168,104,9,239,160,96,168,111,168,96,0,231,170,106,170,99,160,103,8,232,169,111,160,96,160,96,0,224,160,96,160,110,170,102,10,230,170,102,
           160,110,170,102,10,230,170,102,160,110,170,102,10,6,10,6,0,0,0,48,88,120,120,88,48,0,0,0,0,0,0,64,224,238,234,198,10,6,10,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,14,10,6,10,230,170,102,
           160,110,170,102,10,230,170,102,160,108,190,126,30,52,0,0,16,44,2,209,37,63,37,209,2,44,16,0,0,224,160,99,161,111,171,102,10,6,10,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,14,10,6,10,230,170,102,
           160,110,170,102,10,230,170,102,160,110,170,102,10,230,170,102,160,110,171,103,10,230,170,103,161,110,170,102,10,230,170,102,160,110,170,102,10,230,170,102,160,96,160,96,0,224,160,96,160,96,160,96,0,224,160,96,160,96,160,96,0,224,160,96,160,110,170,102,10,230,170,102])


# BITMAP: width: 18, height: 19
deathUI1 = bytearray([0,128,128,31,14,31,0,12,26,20,0,30,136,30,0,132,132,0,
           7,8,8,192,70,73,6,128,143,1,14,0,7,201,0,64,74,129,
           0,0,0,7,5,4,0,7,0,7,0,2,5,7,0,0,5,0]) 
# BITMAP: width: 18, height: 19
deathUI2 = bytearray([0,128,128,31,14,31,0,12,26,20,0,30,136,30,0,1,21,2,
            7,8,8,192,70,73,6,128,143,1,14,0,7,201,0,66,66,128,
            0,0,0,7,5,4,0,7,0,7,0,2,5,7,0,0,5,0])
# BITMAP: width: 18, height: 19
deathUI3 = bytearray([0,128,128,31,14,31,0,12,26,20,0,30,136,30,0,129,149,2,
            7,8,8,192,70,73,6,128,143,1,14,0,7,201,0,0,10,1,
            0,0,0,7,5,4,0,7,0,7,0,2,5,7,0,1,1,0])

'''
If your looking at this code to make some cool change question first if it really worth it
If you still have a soul after reading all this code then you didn't look at it close enough
'''
# Main game loop
while(True):
    
    thumby.display.fill(0)
    thumby.display.drawSprite(loadingScreen)
    thumby.display.update()
    
    turnCounter = 0
    roomno = 0
    
    exitSpawned = False
    saved = False
    
    if saves[select] == 1 and thumby.saveData.hasItem(save):
        currentRoom = dungeonRoom()
        player = loadAll(save)
        generateRoom(currentRoom)
        
    else:
        floorNo = 1
        gc_collect()
        # Make the starting room
        currentRoom = dungeonRoom()
        currentRoom.tiles[2*9+2] = dungeonTile(4)
        currentRoom.tiles[2*9+2].tiledata = bytes("Welcome!\n\nA to act\nB for inv\n - have fun!", 'ascii')
        generateRoom(currentRoom)
        # Make the player
        player = playerobj()
        saveAll(player,save)
    

    loadScreen()
    

    while(player.hp > 0):
        
        # Put the player in their correct location
        currentRoom.getTile(player.tilex, player.tiley).tiletype = 5
        drawGame()
        
        
        
        # Get and handle input
        if(getcharinputNew() != ' '):
            thumby.display.update()
            # Handle d-pad
            if(thumby.dpadPressed()):
                # Prepare to move the player some offset in x and y
                xOffset = 0
                yOffset = 0
                if(thumby.buttonU.pressed()):
                    player.facing = 0
                    yOffset = -1
                elif(thumby.buttonD.pressed()):
                    player.facing = 2
                    yOffset = 1
                elif(thumby.buttonL.pressed()):
                    player.facing = 3
                    xOffset = -1
                elif(thumby.buttonR.pressed()):
                    player.facing = 1
                    xOffset = 1
                # Change the player's location if the offset tile is empty
                if(currentRoom.getTile(player.tilex+xOffset, player.tiley+yOffset).tiletype == 0):
                    currentRoom.getTile(player.tilex, player.tiley).tiletype = 0
                    player.tilex = player.tilex+xOffset
                    player.tiley = player.tiley+yOffset
                    currentRoom.getTile(player.tilex, player.tiley).tiletype = 5
                curMsg = ""
                updateTurn()

            # Handle action 'A'-button
            elif(thumby.buttonA.pressed()):
                curMsg = "act on?"
                drawGame()
                while(getcharinputNew() == ' '):
                    thumby.display.update()
                if(thumby.dpadPressed()):
                    if(thumby.buttonU.pressed()):
                        player.facing = 0
                        currentRoom.getTile(player.tilex, player.tiley-1).actOn()
                    elif(thumby.buttonD.pressed()):
                        player.facing = 2
                        currentRoom.getTile(player.tilex, player.tiley+1).actOn()
                    elif(thumby.buttonL.pressed()):
                        player.facing = 3
                        currentRoom.getTile(player.tilex-1, player.tiley).actOn()
                    elif(thumby.buttonR.pressed()):
                        player.facing = 1
                        currentRoom.getTile(player.tilex+1, player.tiley).actOn()
                    updateTurn()
                else: # Pressing A/B again cancels the action
                    curMsg = ""

            # Handle inventory 'B'-button
            elif(thumby.buttonB.pressed()):
                selpos = 0
                actpos = 1
                while(getcharinputNew() != '1'): # not B-button
                    thumby.display.update()
                    # Menu navigation
                    if(thumby.buttonU.pressed()):
                        selpos = selpos-1
                    elif(thumby.buttonD.pressed()):
                        selpos = selpos+1
                    if(thumby.buttonL.pressed()):
                        actpos = 0
                    elif(thumby.buttonR.pressed()):
                        actpos = 1
                    while(thumby.dpadPressed()):
                        thumby.display.update()

                    getcharinputNew()
                    # Handle item selection
                    if(swBstate == 1):

                        if(actpos == 1):
                            # Equip selected item
                            if(player.inventory[selpos] == "shirt"):
                                player.shirtitem = selpos
                            elif(player.inventory[selpos] == "pants"):
                                player.pantsitem = selpos
                            else:
                                player.helditem = selpos
                            curMsg = "eqp'd."
                            updateTurn()
                            break

                        elif(actpos == 0 and len(player.inventory) != 0):
                            # Drop selected item
                            curMsg = "where?"
                            drawGame()
                            while(getcharinputNew() == ' '):
                                thumby.display.update()
                            tile = itemtile(player.inventory[selpos])

                            # Try to drop the item where the player selected
                            xOffset = 0
                            yOffset = 0
                            if(thumby.buttonU.pressed()):
                                yOffset = -1
                            elif(thumby.buttonD.pressed()):
                                yOffset = 1
                            elif(thumby.buttonL.pressed()):
                                xOffset = -1
                            elif(thumby.buttonR.pressed()):
                                xOffset = 1
                            # Item can be dropped if the offset tile is empty
                            if(currentRoom.getTile(player.tilex+xOffset, player.tiley+yOffset).tiletype == 0):
                                currentRoom.getTile(player.tilex+xOffset, player.tiley+yOffset).tiletype = tile.tiletype
                                currentRoom.getTile(player.tilex+xOffset, player.tiley+yOffset).tiledata = tile.tiledata
                                curMsg = "dropped"
                                # Remove the item from the inventory
                                player.wt = player.wt - itemwt(player.inventory[selpos])
                                player.inventory.pop(selpos)
                                # Make sure the player isn't holding it anymore
                                if(player.helditem == selpos):
                                    player.helditem = -1
                                if(player.shirtitem == selpos):
                                    player.shirtitem = -1
                                if(player.pantsitem == selpos):
                                    player.pantsitem = -1
                            else:
                                # Offset tile is occupied so the item can't be dropped
                                curMsg = "can't!"
                            updateTurn()
                            break


                    # Make sure our selection is actually valid
                    if(selpos < 0):
                        selpos = 0
                    if(selpos >= len(player.inventory)):
                        selpos = len(player.inventory)-1

                    # Only 3 lines to use for showing items
                    l1 = ""
                    l2 = ""
                    l3 = ""
                    if(selpos < len(player.inventory) and len(player.inventory) > 0):
                        l1 = player.inventory[selpos]
                        l1 += '<'
                    if(selpos+1 < len(player.inventory)):
                        l2 = player.inventory[selpos+1]
                    if(selpos+2 < len(player.inventory)):
                        l3 = player.inventory[selpos+2]

                    # Draw everything
                    thumby.display.fill(0)
                    wtHUD=str(player.wt)+"/"+str(player.maxwt)+"wt"
                    thumby.display.drawText(wtHUD, 73-(len(wtHUD)*fontWidth), 0, 1)
                    # Highlight the equipped item(s)
                    if(player.helditem == selpos or player.pantsitem == selpos or player.shirtitem == selpos):
                        thumby.display.drawFilledRectangle(0, 8, len(l1)*fontWidth, 8, 1)
                        thumby.display.drawText(l1, 0, 8, 0)
                    else:
                        thumby.display.drawText(l1, 0, 8, 1)
                    if(player.helditem == selpos+1 or player.pantsitem == selpos+1 or player.shirtitem == selpos+1):
                        thumby.display.drawFilledRectangle(0, 16, len(l2)*fontWidth, 8, 1)
                        thumby.display.drawText(l2, 0, 16, 0)
                    else:
                        thumby.display.drawText(l2, 0, 16, 1)
                    if(player.helditem == selpos+2 or player.pantsitem == selpos+2 or player.shirtitem == selpos+2):
                        thumby.display.drawFilledRectangle(0, 24, len(l3)*fontWidth, 8, 1)
                        thumby.display.drawText(l3, 0, 24, 0)
                    else:
                        thumby.display.drawText(l3, 0, 24, 1)
                    thumby.display.drawFilledRectangle(0, 32, 32, 8, 1-actpos)
                    thumby.display.drawText("drop", 0, 32, actpos)
                    thumby.display.drawFilledRectangle(48, 32, 24, 8, actpos)
                    thumby.display.drawText("eqp", 48, 32, 1-actpos)
                    thumby.display.update()
            else:
                # Clear the current message
                curMsg = ""
            drawGame()
    
    select = 0
    
    thumby.actionJustPressed() # Debounce
    x = False
    while(thumby.actionJustPressed()):
        thumby.display.update()
    
    while(not thumby.actionJustPressed()):
        
        thumby.display.fill(0)
        thumby.display.drawSprite(thumby.Sprite(72,40,DeathMain,0,0))
        if select == 0:
            thumby.display.drawSprite(thumby.Sprite(18, 19, deathUI1, 44, 17))
        elif select == 1:
            thumby.display.drawSprite(thumby.Sprite(18, 19, deathUI2, 44, 17))
        else:
            thumby.display.drawSprite(thumby.Sprite(18, 19, deathUI3, 44, 17))
         
        thumby.display.update()
        if not x:
            time.sleep(0.25)
            x = True
        if(thumby.buttonL.justPressed()) or (thumby.buttonU.justPressed()):
            select -= 1
        if(thumby.buttonR.justPressed()) or (thumby.buttonD.justPressed()):
            select += 1
        select = max(min(select,2),0)
        

    # Free memory
    del currentRoom
    del player
    curMsg = ""
    gc_collect()

    if(select == 2):
        thumby.reset() # Exit game to main menu
    elif select == 0:
        thumby.saveData.delItem(save)
        
    # Else: Restart game loop

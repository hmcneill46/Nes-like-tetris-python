##THINGS TO DO
## DONE                Visulize score and Next box
## DONE                When you die and try and turn error occurs, and if you place piece on ground error occurs
## DONE                Randomizer make Better, with 2nd roll if chooses same piece twice 
## Better Rotations
## Sort out what happens in time delay after piece is placed
## DONE                Put boarders on pieces
## Post 29 lines to transition
## Pause Menu
## Flash Getting Tetris
## sound and music
## Moving while pushing down fix
## DONE                Push down points
## DONE                Top scores
## Nicer Line Breaking
## Not so random pieces that 2 computers can have the same of with a seed
## Fix DAS timings, das charges after piece drop, and before new piece, and doesnt go to 16 when you push it next to a block instanty


Level = 0
multiplyer = 4

import pygame
import random
import matrixsystem
import ast

listsettings = open("Settings","r").read().split("\n")
#listsettings = open("settings NTSC.txt","r").read().split("\n")

for n in range(len(listsettings)):
    listsettings[n] = listsettings[n].split(" = ")
settings = {}
for n in listsettings:
    settings[n[0]] = n[1]
settings["FRAMELEVELS"] = settings["FRAMELEVELS"]

##Display setup

pygame.init()

#multiplyer = float(input("What do you want the screen multipler to be 1-4 recommended, the higher you go the worse the perfomance: "))

SCREEN_WIDTH = int(256*multiplyer) ## Recommend 256, 512, 768 and 1024

#SCREEN_WIDTH = 1200 ## FULLSCREEN SETTING

SCREEN_HEIGHT = int(SCREEN_WIDTH*(896/1024))

GAMERES = int(SCREEN_WIDTH*(320/1024))

size = [SCREEN_WIDTH,SCREEN_HEIGHT]

screen = pygame.display.set_mode(size)

#screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN) ## FULLSCREEN SETTING
active_sprites = pygame.sprite.Group()
display_sprites = pygame.sprite.Group()
top_sprites = pygame.sprite.Group()
floor_sprites_list = pygame.sprite.Group()
clock = pygame.time.Clock()

Topscoresfile = open("Topscores.txt","a+")
Topscoresfile.seek(0)
if Topscoresfile.read() == "":
    Topscoresfile.write("LANCE:5000:0\n")
    Topscoresfile.write("OTASAN:7500:5\n")
    Topscoresfile.write("HOWARD:10000:9\n")
Topscoresfile.seek(0)
Topscores = Topscoresfile.read().split("\n")
for n in range(len(Topscores)):
    if Topscores[n] == "":Topscores.remove(Topscores[n])
    else:Topscores[n] = Topscores[n].split(":")
TopScore = int(Topscores[-1][1])

###############

##Block setup

BLOCKS=[[[-1,0],[0,0],[0,1],[1,0]                     ], #0 T
        [[-1,0],[0,0],[1,0],[1,1]                     ], #1 J
        [[-1,0],[0,0],[0,1],[1,1]                     ], #2 Z
        [[-0.5,0.5],[-0.5,-0.5],[0.5,-0.5],[0.5,0.5]  ], #3 O
        [[-1,1],[0,1],[0,0],[1,0]                     ], #4 S
        [[-1,1],[-1,0],[0,0],[1,0]                    ], #5 L
        [[-1.5,0.5],[-0.5,0.5],[0.5,0.5],[1.5,0.5]    ]] #6 I

BLOCKCOLOURS = [[(0, 88, 248),(63, 191, 255)],   ## 0
                [(0, 171, 0),(184, 248, 24)],    ## 1
                [(219, 0, 205),(248, 120, 248)], ## 2
                [(0, 88, 248),(91, 219, 87)],    ## 3
                [(231, 0, 91),(88, 248, 152)],   ## 4
                [(88, 248, 152),(107, 136, 255)],## 5
                [(248, 56, 0),(127, 127, 127)],  ## 6
                [(107, 71, 255),(171, 0, 35)],   ## 7
                [(0, 88, 248),(248, 56, 0)],     ## 8
                [(248, 56, 0),(255, 163, 71)]]   ## 9

#############

##Game setup

levelframes = ast.literal_eval(settings["FRAMELEVELS"])

linestotransition = [10,20,30,40,50,60,70,80,90,100,100,100,100,100,100,100,110,120,130,140,150,160,170,180,190,200,200,200,200,200]

UP_BUTTON = int(settings["UP_BUTTON"])
LEFT_BUTTON = int(settings["LEFT_BUTTON"])
DOWN_BUTTON = int(settings["DOWN_BUTTON"])
RIGHT_BUTTON = int(settings["RIGHT_BUTTON"])
A_BUTTON = int(settings["A_BUTTON"])
B_BUTTON = int(settings["B_BUTTON"])
SELECT_BUTTON = int(settings["SELECT_BUTTON"])
START_BUTTON = int(settings["START_BUTTON"])

framecounter = 0

done = False

############

## Number Setup
whitenumbersprites = []
for n in range(10):
    whitenumbersprites.append(pygame.transform.scale(pygame.image.load("White Numbers//"+str(n)+".png"), (int(SCREEN_WIDTH*(28/1024)),int(SCREEN_WIDTH*(28/1024)))))

rednumbersprites = []
for n in range(10):
    rednumbersprites.append(pygame.transform.scale(pygame.image.load("Red Numbers//"+str(n)+".png"), (int(SCREEN_WIDTH*(28/1024)),int(SCREEN_WIDTH*(28/1024)))))

###############

##Class setup

Boardpos = (SCREEN_WIDTH*(382/1024),SCREEN_WIDTH*(158/1024))

class Square(pygame.sprite.Sprite):
    def __init__(self,width,height,alignment,x,y,col):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(col)
        self.rect = self.image.get_rect()
        if alignment == "c":
            self.rect.centerx = x
            self.rect.centery = y
        elif alignment == "tr":
            self.rect.x = x
            self.rect.y = y
        display_sprites.add(self)

class FrontSquare(pygame.sprite.Sprite):
    def __init__(self,width,height,alignment,x,y,col):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(col)
        self.rect = self.image.get_rect()
        if alignment == "c":
            self.rect.centerx = x
            self.rect.centery = y
        elif alignment == "tr":
            self.rect.x = x
            self.rect.y = y
        top_sprites.add(self)

class ShowBox(pygame.sprite.Sprite):
    def __init__(self,blockno,alignment,xpos,ypos,length,height,col,blocktype):
        self.blocktype = blocktype
        self.blockno = blockno
        super().__init__()
        self.image = pygame.Surface([length, height])
        self.image.fill(col)
        self.rect = self.image.get_rect()
        if alignment == "c":
            self.rect.centerx = xpos
            self.rect.centery = ypos
        elif alignment == "tr":
            self.rect.x = xpos
            self.rect.y = ypos
        display_sprites.add(self)
    def delete(self):
        display_sprites.remove(self)
            
class Number(pygame.sprite.Sprite):
    def __init__(self,number,x,y,col):
        super().__init__()
        self.number = number
        self.colour = col
        if self.colour == "r":
            self.image = rednumbersprites[number]
        else:
            self.image = whitenumbersprites[number]
        #self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        top_sprites.add(self)
    def update(self,number):
        self.number = number
        if self.colour == "r":
            self.image = rednumbersprites[number]
        else:
            self.image = whitenumbersprites[number]

class Box(pygame.sprite.Sprite):
    def __init__(self,blockno,xpos,ypos,length,height,level,blocktype):
        self.blocktype = blocktype
        self.level = level
        self.blockno = blockno
        super().__init__()
        self.image = BlockSprites[self.level][self.blocktype]
        self.rect = self.image.get_rect()
        self.rect.centerx = xpos
        self.rect.centery = ypos
        active_sprites.add(self)
        self.active = True
    def update(self,level):
        self.level = level
        self.image = BlockSprites[self.level][self.blocktype]
    def xmove(self,amount):
        self.rect.centerx += amount
    def ymove(self,amount):
        self.rect.centery += amount
    def deactivate(self):
        self.active = False
        active_sprites.remove(self)
        floor_sprites_list.add(self)
    def delete(self):
        floor_sprites_list.remove(self)

class StatsColours(): ## Colours behind side blocks to give them colours
    def __init__(self,Clevel):
        self.level =int(str(Clevel)[-1])
        self.squares = []
        self.squares.append(FrontSquare(SCREEN_WIDTH*(68/1024),SCREEN_WIDTH*(104/1024),"tr",SCREEN_WIDTH*(104/1024),SCREEN_WIDTH*(340/1024),BLOCKCOLOURS[self.level][0])) ## POS
        self.squares.append(FrontSquare(SCREEN_WIDTH*(68/1024),SCREEN_WIDTH*(44/1024),"tr",SCREEN_WIDTH*(104/1024),SCREEN_WIDTH*(468/1024),BLOCKCOLOURS[self.level][1])) ## POS
        self.squares.append(FrontSquare(SCREEN_WIDTH*(68/1024),SCREEN_WIDTH*(108/1024),"tr",SCREEN_WIDTH*(104/1024),SCREEN_WIDTH*(532/1024),BLOCKCOLOURS[self.level][0])) ## POS
        self.squares.append(FrontSquare(SCREEN_WIDTH*(68/1024),SCREEN_WIDTH*(44/1024),"tr",SCREEN_WIDTH*(104/1024),SCREEN_WIDTH*(656/1024),BLOCKCOLOURS[self.level][1])) ## POS
        self.squares.append(FrontSquare(SCREEN_WIDTH*(92/1024),SCREEN_WIDTH*(20/1024),"tr",SCREEN_WIDTH*(96/1024),SCREEN_WIDTH*(736/1024),BLOCKCOLOURS[self.level][0])) ## POS
    def update(self,level):
        self.level = int(str(level)[-1])
        for n in range(len(self.squares)):
            if n%2 == 0:
                self.squares[n].image.fill(BLOCKCOLOURS[self.level][0])
            else:
                self.squares[n].image.fill(BLOCKCOLOURS[self.level][2])

class Player1():
    def __init__(self,startlevel):
        global TopScore
        self.piececount = [0,0,0,0,0,0,0]
        self.placedframe = -21
        self.holdingA = False
        self.holdingB = False
        self.endholddown = False
        self.moving = 0
        self.das_charge = 0
        self.linescleared = 0
        self.startlevel = startlevel
        self.level = startlevel
        self.Cblock = random.randint(0,6)
        self.Nextblock = random.randint(0,6)

        self.pushdownpoints = 0

        self.nextbox = NextBox()
        self.nextbox.update(self.Nextblock,self.level)

        self.piececount[self.Cblock] += 1
        if self.Nextblock == self.Cblock:
            self.Nextblock = random.randint(0,6)
        self.score = 0

        self.SCORE = Numbers(SCREEN_WIDTH*(768/1024),SCREEN_WIDTH*(224/1024),6,"w")
        self.TOPSCORE = Numbers(SCREEN_WIDTH*(768/1024),SCREEN_WIDTH*(128/1024),6,"w")
        self.LINES = Numbers(SCREEN_WIDTH*(608/1024),SCREEN_WIDTH*(64/1024),3,"w")
        self.LEVEL = Numbers(SCREEN_WIDTH*(832/1024),SCREEN_WIDTH*(640/1024),2,"w")
        
        self.TOPSCORE.update(TopScore)

        self.PIECESTATS = []
        for n in range(7):
            self.PIECESTATS.append(Numbers(SCREEN_WIDTH*(192/1024),SCREEN_WIDTH*(352/1024)+n*SCREEN_WIDTH*(64/1024),3,"r"))
        for n in range(7):
            self.PIECESTATS[n].update(self.piececount[n])

        
        self.statcols = StatsColours(self.level)
        self.SCORE.update(self.score)
        self.LINES.update(self.linescleared)
        self.LEVEL.update(self.level)
        self.Blocks = []
        if int(BLOCKS[self.Cblock][0][0]) == BLOCKS[self.Cblock][0][0]:
            for n in range(4):
                self.Blocks.append(Box(n,
                                       (GAMERES/2)+(BLOCKS[self.Cblock][n][0])*(GAMERES/10)+(GAMERES/20)+Boardpos[0],
                                       ((BLOCKS[self.Cblock][n][1])*(GAMERES/10))+(GAMERES/20)+Boardpos[1],
                                       GAMERES/(320/28),GAMERES/(320/28),
                                       BLOCKCOLOURS[int(str(self.level)[-1])][self.Cblock],
                                       self.Cblock))
        else:
            for n in range(4):
                self.Blocks.append(Box(n,
                                       (GAMERES/2)+(BLOCKS[self.Cblock][n][0]-0.5)*(GAMERES/10)+(GAMERES/20)+Boardpos[0],
                                       ((BLOCKS[self.Cblock][n][1]+0.5)*(GAMERES/10))+(GAMERES/20)+Boardpos[1],
                                       GAMERES/(320/28),GAMERES/(320/28),
                                       BLOCKCOLOURS[int(str(self.level)[-1])][self.Cblock],
                                       self.Cblock))
        self.CurrentBlocks = BLOCKS[self.Cblock]
    def left(self):
        for n in self.Blocks:
            n.xmove(-(GAMERES/10))
    def right(self):
        for n in self.Blocks:
            n.xmove(GAMERES/10)
    def down(self):
        for n in self.Blocks:
            n.ymove(GAMERES/10)
    def up(self):
        for n in self.Blocks:
            n.ymove(-(GAMERES/10))
    def piecedeactivate(self):
        if self.pushdownpoints != 0:
            self.score += self.pushdownpoints
            self.pushdownpoints = 0
            self.SCORE.update(self.score)
        self.endholddown = True
        checkrows = []
        for n in self.Blocks:
            checkrows.append(n.rect.y)
        for n in self.Blocks:
            n.deactivate()
        checkrows = sorted(checkrows)
        linesatonce = 0
        for n in checkrows:
            self.rowcount = 0
            for i in floor_sprites_list:
                if i.rect.y == n:
                    self.rowcount += 1
            if self.rowcount == 10:
                linesatonce += 1
                for i in floor_sprites_list:
                    if i.rect.y == n:
                        i.delete()
                for i in floor_sprites_list:
                    if i.rect.y < n:
                        i.ymove(GAMERES/10)
        if linesatonce == 1:self.score += (self.level+1)*(40)
        if linesatonce == 2:self.score += (self.level+1)*(100)
        if linesatonce == 3:self.score += (self.level+1)*(300)
        if linesatonce == 4:self.score += (self.level+1)*(1200)
        self.linescleared += linesatonce
        if linesatonce > 0:
            self.SCORE.update(self.score)
            self.LINES.update(self.linescleared)
            if self.level == self.startlevel and self.linescleared >= linestotransition[self.startlevel]:
                self.level +=1
                self.LEVEL.update(self.level)
                self.statcols.update(self.level)
                for n in floor_sprites_list:
                    n.image.fill(BLOCKCOLOURS[int(str(self.level)[-1])][n.blocktype])
            elif self.linescleared - linestotransition[self.startlevel] >= 10*(self.level - self.startlevel):
                self.level +=1
                self.LEVEL.update(self.level)
                self.statcols.update(self.level)
                for n in floor_sprites_list:
                    n.image.fill(BLOCKCOLOURS[int(str(self.level)[-1])][n.blocktype])
    def RotateCCW(self):
        self.rotatedBlocks = matrixsystem.matrixtocoordinates(matrixsystem.MMultiply([[0,1],[-1,0]],matrixsystem.coordinatestomatrix(self.CurrentBlocks)))
        for n in range(len(self.Blocks)):
            self.Blocks[n].xmove((GAMERES/10)*(self.rotatedBlocks[n][0] - self.CurrentBlocks[n][0]))
            self.Blocks[n].ymove((GAMERES/10)*(self.rotatedBlocks[n][1] - self.CurrentBlocks[n][1]))
        self.CurrentBlocks = self.rotatedBlocks
    def RotateCW(self):
        self.rotatedBlocks = matrixsystem.matrixtocoordinates(matrixsystem.MMultiply([[0,-1],[1,0]],matrixsystem.coordinatestomatrix(self.CurrentBlocks)))
        for n in range(len(self.Blocks)):
            self.Blocks[n].xmove((GAMERES/10)*(self.rotatedBlocks[n][0] - self.CurrentBlocks[n][0]))
            self.Blocks[n].ymove((GAMERES/10)*(self.rotatedBlocks[n][1] - self.CurrentBlocks[n][1]))
        self.CurrentBlocks = self.rotatedBlocks
    def update(self):
        if framecounter == self.placedframe+20:
            self.NewBlock()
        
        ##Gravity
        if (pygame.key.get_pressed()[DOWN_BUTTON] == 1 and not self.endholddown):
            if self.level > 28:
                if framecounter % 1 == 0:
                    self.down()
                    self.pushdownpoints+=1
            else:
                if framecounter % 2 == 0:
                    self.down()
                    self.pushdownpoints+=1

        elif pygame.key.get_pressed()[DOWN_BUTTON] == 0:
            self.endholddown = False
            self.pushdownpoints = 0
        if self.level < 29:
            if (framecounter % levelframes[self.level] == 0 and framecounter != 0) and self.pushdownpoints == 0:
                self.down()
        else:
            if (framecounter % 1 == 0 and framecounter != 0) and self.pushdownpoints == 0:
                self.down()
        self.deactivate = False
        for n in self.Blocks:
            if n.rect.y < 2*GAMERES+Boardpos[1]:
                for p in floor_sprites_list:
                    if n.rect.y == p.rect.y and n.rect.x == p.rect.x:
                        self.deactivate = True
            else:
                self.deactivate = True
        if self.deactivate:
            self.up()
            self.piecedeactivate()
            self.Blocks = []
            self.placedframe = framecounter
        #########
            
        ##B Rotate
        if pygame.key.get_pressed()[B_BUTTON] == 1 and not self.holdingB:
            self.RotateCCW()
            self.holdingB = True
        elif pygame.key.get_pressed()[B_BUTTON] != 1:
            self.holdingB = False

        self.cwrotateout = False
        for n in self.Blocks:
            if n.rect.x >= Boardpos[0] and n.rect.x < GAMERES+Boardpos[0] and n.rect.y < 2*GAMERES+Boardpos[1]:
                for p in floor_sprites_list:
                    if n.rect.y == p.rect.y and n.rect.x == p.rect.x:
                        self.cwrotateout = True
            else:
                self.cwrotateout = True
                
        if self.cwrotateout:
            self.RotateCW()
        ##########
            
        ##A Rotate
        if pygame.key.get_pressed()[A_BUTTON] == 1 and not self.holdingA:
            self.RotateCW()
            self.holdingA = True
        elif pygame.key.get_pressed()[A_BUTTON] != 1:
            self.holdingA = False

        self.ccwrotateout = False
        for n in self.Blocks:
            if n.rect.x >= Boardpos[0] and n.rect.x < GAMERES+Boardpos[0] and n.rect.y < 2*GAMERES+Boardpos[1]:
                for p in floor_sprites_list:
                    if n.rect.y == p.rect.y and n.rect.x == p.rect.x:
                        self.ccwrotateout = True
            else:
                self.ccwrotateout = True
        if self.ccwrotateout:
            self.RotateCCW()
        ##########
            
        ##DAS
        if pygame.key.get_pressed()[LEFT_BUTTON] == 1 and pygame.key.get_pressed()[DOWN_BUTTON] != 1: ##LEFT
            self.moving = "left"
            if self.das_charge == int(settings["DASMAX"]) or self.das_charge == 0:
                self.left()
            if self.das_charge == int(settings["DASMAX"]):
                self.das_charge = int(settings["DASMAX"])-int(settings["DASCHANGE"])-1
            self.das_charge+=1
        elif pygame.key.get_pressed()[RIGHT_BUTTON] == 1 and pygame.key.get_pressed()[DOWN_BUTTON] != 1: ##RIGHT
            self.moving = "right"
            if self.das_charge == int(settings["DASMAX"]) or self.das_charge == 0:
                self.right()
            if self.das_charge == int(settings["DASMAX"]):
                self.das_charge = int(settings["DASMAX"])-int(settings["DASCHANGE"])-1
            self.das_charge+=1
        else:
            self.das_charge=0
        #####

        ##Check if in wall
        self.getout = False
        for n in self.Blocks:
            if n.rect.x >= Boardpos[0] and n.rect.x < GAMERES+Boardpos[0]:
                for p in floor_sprites_list:
                    if n.rect.y == p.rect.y and n.rect.x == p.rect.x:
                        self.getout = True
            else:
                self.getout = True
        if self.getout:
            if self.moving == "left":
                self.right()
            else:
                self.left()
            self.das_charge = int(settings["DASMAX"])
        
        

        ##################
    def NewBlock(self):
        self.Cblock = self.Nextblock

        self.piececount[self.Cblock] += 1
        for n in range(7):
            self.PIECESTATS[n].update(self.piececount[n])

        self.Nextblock = random.randint(0,6)
        if self.Nextblock == self.Cblock:
            self.Nextblock = random.randint(0,6)
        self.nextbox.update(self.Nextblock,self.level)
        self.CurrentBlocks = BLOCKS[self.Cblock]
        if int(BLOCKS[self.Cblock][0][0]) == BLOCKS[self.Cblock][0][0]:
            for n in range(4):
                self.Blocks.append(Box(n,
                                       (GAMERES/2)+(BLOCKS[self.Cblock][n][0])*(GAMERES/10)+(GAMERES/20)+Boardpos[0],
                                       ((BLOCKS[self.Cblock][n][1])*(GAMERES/10))+(GAMERES/20)+Boardpos[1],
                                       GAMERES/(320/28),GAMERES/(320/28),
                                       BLOCKCOLOURS[int(str(self.level)[-1])][self.Cblock],
                                       self.Cblock))
        else:
            for n in range(4):
                self.Blocks.append(Box(n,
                                       (GAMERES/2)+(BLOCKS[self.Cblock][n][0]-0.5)*(GAMERES/10)+(GAMERES/20)+Boardpos[0],
                                       ((BLOCKS[self.Cblock][n][1]+0.5)*(GAMERES/10))+(GAMERES/20)+Boardpos[1],
                                       GAMERES/(320/28),GAMERES/(320/28),
                                       BLOCKCOLOURS[int(str(self.level)[-1])][self.Cblock],
                                       self.Cblock))
        for n in self.Blocks:
            for p in floor_sprites_list:
                if n.rect.y == p.rect.y and n.rect.x == p.rect.x:
                    self.piecedeactivate()
                    self.gameover()
    def gameover(self):
        global TopScore
        global Topscoresfile

        if self.score > TopScore:
            TopScore = self.score
            self.TOPSCORE.update(TopScore)
            Topscoresfile.write("HARRY:"+str(TopScore)+":"+str(self.level)+"\n")

        self.placedframe = -21
        self.holdingA = False
        self.holdingB = False
        self.endholddown = False
        self.moving = 0
        self.das_charge = 0
        self.linescleared = 0
        self.level = self.startlevel
        self.Cblock = random.randint(0,6)
        self.Nextblock = random.randint(0,6)
        self.nextbox.update(self.Nextblock,self.level)
        self.Blocks = []
        for n in floor_sprites_list:
            n.delete()
        self.NewBlock()
        self.score = 0
        self.SCORE.update(self.score)
        self.LINES.update(self.linescleared)
        self.LEVEL.update(self.level)
        self.statcols.update(self.level)
        for n in range(7):
            self.piececount[n] = 0
        for n in range(7):
            self.PIECESTATS[n].update(self.piececount[n])

class NextBox():
    def __init__(self):
        self.Blocks = []
    def update(self,block,level):
        self.level = level
        for n in self.Blocks:
            n.delete()
        self.block = block
        self.Blocks = []
        if self.block != 0:
            if int(BLOCKS[self.block][0][0]) == BLOCKS[self.block][0][0]:
                for n in range(4):
                    self.Blocks.append(ShowBox(n,
                                        "c",
                                        SCREEN_WIDTH*(830/1024)+(BLOCKS[self.block][n][0])*(GAMERES/10),
                                        ((BLOCKS[self.block][n][1]-1)*(GAMERES/10))+SCREEN_WIDTH*(494/1024),
                                        GAMERES/(320/28),GAMERES/(320/28),
                                        BLOCKCOLOURS[int(str(self.level)[-1])][self.block],
                                        self.block))
            else:
                for n in range(4):
                    self.Blocks.append(ShowBox(n,
                                        "c",
                                        SCREEN_WIDTH*(830/1024)+(BLOCKS[self.block][n][0]-0.5)*(GAMERES/10)+(GAMERES/20),
                                        ((BLOCKS[self.block][n][1]-0.5)*(GAMERES/10))+SCREEN_WIDTH*(494/1024),
                                        GAMERES/(320/28),GAMERES/(320/28),
                                        BLOCKCOLOURS[int(str(self.level)[-1])][self.block],
                                        self.block))
        else:
            for n in range(4):
                self.Blocks.append(ShowBox(n,
                                            "c",
                                            SCREEN_WIDTH*(830/1024)+(BLOCKS[self.block][n][0]-0.5)*(GAMERES/10)+(GAMERES/20),
                                            ((BLOCKS[self.block][n][1]-0.5)*(GAMERES/10))+SCREEN_WIDTH*(478/1024),
                                            GAMERES/(320/28),GAMERES/(320/28),
                                            BLOCKCOLOURS[int(str(self.level)[-1])][self.block],
                                            self.block))

class Numbers():
    def __init__(self,x,y,nodigits,col):
        self.colour = col
        self.digits = []
        self.nodigits = nodigits
        for n in range(self.nodigits):
            self.digits.append(Number(0,x+n*SCREEN_WIDTH*(32/1024),y,self.colour))
    def update(self, number):
        if len(str(number)) > self.nodigits:
            print("Too long of a number rip")
        else:
            self.newnum = "0"*(self.nodigits-len(str(number)))+str(number)
            self.counter = 0
            for n in self.digits:
                n.update(int(self.newnum[self.counter]))
                self.counter+=1

#############

Player1 = Player1(Level)

Backgroundparts = [pygame.transform.scale(pygame.image.load('Background/Bottom.png'),(int(SCREEN_WIDTH*(324/1024)),int(SCREEN_WIDTH*(92/1024)))),pygame.transform.scale(pygame.image.load('Background/Left.png'),(int(SCREEN_WIDTH*(380/1024)),int(SCREEN_HEIGHT))),pygame.transform.scale(pygame.image.load('Background/Right.png'),(int(SCREEN_WIDTH*(320/1024)),int(SCREEN_HEIGHT))),pygame.transform.scale(pygame.image.load('Background/Top.png'),(int(SCREEN_WIDTH*(324/1024)),int(SCREEN_WIDTH*(156/1024))))]
## 0 = Bottom
## 1 = Left
## 2 = Right
## 3 = Top
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    Player1.update()
    screen.fill((0,0,0))
    display_sprites.draw(screen)
    floor_sprites_list.draw(screen)
    active_sprites.draw(screen)
    top_sprites.draw(screen)
    framecounter +=1
    clock.tick(float(settings["FPS"]))
    screen.blit(Backgroundparts[1],(0,0))
    screen.blit(Backgroundparts[3],(SCREEN_WIDTH*(380/1024),0))
    screen.blit(Backgroundparts[0],(SCREEN_WIDTH*(380/1024),SCREEN_WIDTH*(804/1024)))
    screen.blit(Backgroundparts[2],(SCREEN_WIDTH*(704/1024),0))
    pygame.display.set_caption("NES Tetris ["+settings["SETTINGS_NAME"]+"] ["+str(round(clock.get_fps(),2))+"] ["+str(Player1.das_charge)+"]")
    pygame.display.flip()
pygame.quit()

import pygame
import random
import ctypes   #For messagebox
import copy     #For deepcopy

pygame.init()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player,self).__init__()
        self.surface = pygame.Surface((26,26))
        self.surface.fill((0,0,255))
        self.rect = self.surface.get_rect(center=(50,HEIGHT-100))

    def update(self,pressedKeys, lines):
        #Player movement
        if(pressedKeys[pygame.K_UP] and not(pressedKeys[pygame.K_DOWN] or pressedKeys[pygame.K_LEFT] or pressedKeys[pygame.K_RIGHT])):
            self.rect.move_ip(0, -1)
        if(pressedKeys[pygame.K_DOWN] and not(pressedKeys[pygame.K_UP] or pressedKeys[pygame.K_LEFT] or pressedKeys[pygame.K_RIGHT])):
            self.rect.move_ip(0, 1)
        if(pressedKeys[pygame.K_LEFT] and not(pressedKeys[pygame.K_DOWN] or pressedKeys[pygame.K_UP] or pressedKeys[pygame.K_RIGHT])):
            self.rect.move_ip(-1, 0)
        if(pressedKeys[pygame.K_RIGHT] and not(pressedKeys[pygame.K_DOWN] or pressedKeys[pygame.K_LEFT] or pressedKeys[pygame.K_UP])):
            self.rect.move_ip(1, 0)
        
        
    def updateCollision(self,pressedKeys,lines):
        if(self.rect.centerx < 50):
            self.rect.centerx = 50
        if(self.rect.centery > HEIGHT-100):
            self.rect.centery = HEIGHT-100
        if(self.rect.centerx > WIDTH-50):
            self.rect.centerx = WIDTH-50
        if(self.rect.centery < 100):
            self.rect.centery = 100
            
        #Makes sures player cannot go through an edge
        for line in lines:
            #If player hits an edge
            if(self.rect.colliderect(line)):
                wentIn = False
                blockMovement = False

                #Hits left edge
                if(line.collidepoint(self.rect.centerx + 1, self.rect.centery) and line.width == 1):
                    #Checks if right side of player is inside an incursion
                    for poly in polys:
                        if(not(poly.collidepoint(self.rect.midright)) and poly.collidepoint(self.rect.midleft)):
                            blockMovement = True

                    if(blockMovement):
                        self.rect.centerx = self.rect.centerx + 1
                    wentIn = True
                        
                #Hits right edge
                elif(line.collidepoint(self.rect.centerx - 1, self.rect.centery) and line.width == 1):
                    #Checks if left side of player is inside an incursion
                    for poly in polys:
                        if(not(poly.collidepoint(self.rect.midleft)) and poly.collidepoint(self.rect.midright)):
                            blockMovement = True

                    if(blockMovement):
                        self.rect.centerx = self.rect.centerx - 1
                    wentIn = True
                        
                #Hits bottom edge
                elif(line.collidepoint(self.rect.centerx, self.rect.centery - 1) and line.width > 1):
                    #Checks if top side of player is inside an incursion
                    for poly in polys:
                        if(not(poly.collidepoint(self.rect.midtop)) and poly.collidepoint(self.rect.midbottom)):
                            blockMovement = True

                    if(blockMovement):
                        self.rect.centery = self.rect.centery - 1
                    wentIn = True
                        
                #Hits top edge
                elif(line.collidepoint(self.rect.centerx, self.rect.centery + 1) and line.width > 1):
                    #Checks if bottom side of player is inside an incursion
                    for poly in polys:
                        if(not(poly.collidepoint(self.rect.midbottom)) and poly.collidepoint(self.rect.midtop)):
                            blockMovement = True

                    if(blockMovement):
                        self.rect.centery = self.rect.centery + 1
                    wentIn = True

                #If we found a line break, if not find another line
                if(wentIn):
                    break

class Qix(pygame.sprite.Sprite):                             
    def __init__(self):
        super(Qix, self).__init__()
        self.surface = pygame.Surface((20, 20))  
        self.surface.fill((102, 0, 102)) 
        self.rect = self.surface.get_rect(
            center=((WIDTH - 200, HEIGHT - 400))
        )

    def update(self,lines,player):
        global qix_speedx, qix_speedy, startPushPos, startPos, endPos, drawLines, lives, hit, isPressedKeys

        self.rect.x += qix_speedx
        self.rect.y += qix_speedy

        #Collision with edge
        if(self.rect.collidelist(lines) != -1):
            line = lines[self.rect.collidelist(lines)]

            #Hits horizontal line
            if(line.height == 1):
                qix_speedy *= -1
                
            #Hits vertical line
            elif(line.width == 1):
                qix_speedx *= -1

        #Hits an incursion line
        if(screen.get_at((self.rect.centerx,self.rect.centery))[:3] == (255,255,255) and self.rect.collidelist(lines) == -1):
            drawLines = []
            player.rect.centerx = startPushPos[0]
            player.rect.centery = startPushPos[1]
            startPushPos = startPos = endPos = (0,0)
            if(pygame.key.get_pressed().count(1) == 0):
                isPressedKeys = False
            if(lives > 1):
                ctypes.windll.user32.MessageBoxW(0, "Careful, you lost a life!", "Hit!", 0)
            lives = lives - 1
            hit = True

class Sparx1(pygame.sprite.Sprite):
    def __init__(self):
        super(Sparx1,self).__init__()
        self.surface = pygame.Surface((5,5))
        self.surface.fill((255,165,0))
        self.rect = self.surface.get_rect(center=(50,HEIGHT-600))

    def update(self,direction,randInt):
        sparxcenterx = self.rect.centerx
        sparxcentery = self.rect.centery
        if(randInt == 0):
            if(screen.get_at((sparxcenterx-1, sparxcentery))[:3] == (255,255,255) and direction != "right"):
                direction = "left"
            elif(screen.get_at((sparxcenterx+1, sparxcentery))[:3] == (255,255,255) and direction != "left"):
                direction = "right"
            elif(screen.get_at((sparxcenterx, sparxcentery-1))[:3] == (255,255,255) and direction != "down"):
                direction = "up"
            elif(screen.get_at((sparxcenterx, sparxcentery+1))[:3] == (255,255,255) and direction != "up"):
                direction = "down"
        elif(randInt == 1):
            if(screen.get_at((sparxcenterx+1, sparxcentery))[:3] == (255,255,255) and direction != "left"):
                direction = "right"
            elif(screen.get_at((sparxcenterx-1, sparxcentery))[:3] == (255,255,255) and direction != "right"):
                direction = "left"
            elif(screen.get_at((sparxcenterx, sparxcentery-1))[:3] == (255,255,255) and direction != "down"):
                direction = "up"
            elif(screen.get_at((sparxcenterx, sparxcentery+1))[:3] == (255,255,255) and direction != "up"):
                direction = "down"
        elif(randInt == 2):
            if(screen.get_at((sparxcenterx, sparxcentery+1))[:3] == (255,255,255) and direction != "up"):
                direction = "down"
            elif(screen.get_at((sparxcenterx, sparxcentery-1))[:3] == (255,255,255) and direction != "down"):
                direction = "up"
            elif(screen.get_at((sparxcenterx-1, sparxcentery))[:3] == (255,255,255) and direction != "right"):
                direction = "left"
            elif(screen.get_at((sparxcenterx+1, sparxcentery))[:3] == (255,255,255) and direction != "left"):
                direction = "right"
        else:
            if(screen.get_at((sparxcenterx, sparxcentery-1))[:3] == (255,255,255) and direction != "down"):
                direction = "up"
            elif(screen.get_at((sparxcenterx, sparxcentery+1))[:3] == (255,255,255) and direction != "up"):
                direction = "down"
            elif(screen.get_at((sparxcenterx-1, sparxcentery))[:3] == (255,255,255) and direction != "right"):
                direction = "left"
            elif(screen.get_at((sparxcenterx+1, sparxcentery))[:3] == (255,255,255) and direction != "left"):
                direction = "right"
        if direction == 'up':
            self.rect.move_ip(0, -1)
        elif direction == 'down':
            self.rect.move_ip(0, 1)
        elif direction == 'left':
            self.rect.move_ip(-1, 0)
        elif direction == 'right':
            self.rect.move_ip(1, 0)
        return direction

class Sparx2(pygame.sprite.Sprite):
    def __init__(self):
        super(Sparx2,self).__init__()
        self.surface = pygame.Surface((5,5))
        self.surface.fill((255,165,0))
        self.rect = self.surface.get_rect(center=(50+700,HEIGHT-600))

    def update(self,direction,randInt):
        global sparx2Count
        
        sparxcenterx = self.rect.centerx
        sparxcentery = self.rect.centery
        if(randInt == 0):
            if(screen.get_at((sparxcenterx-1, sparxcentery))[:3] == (255,255,255) and direction != "right"):
                direction = "left"
            elif(screen.get_at((sparxcenterx+1, sparxcentery))[:3] == (255,255,255) and direction != "left"):
                direction = "right"
            elif(screen.get_at((sparxcenterx, sparxcentery-1))[:3] == (255,255,255) and direction != "down"):
                direction = "up"
            elif(screen.get_at((sparxcenterx, sparxcentery+1))[:3] == (255,255,255) and direction != "up"):
                direction = "down"
        elif(randInt == 1):
            if(screen.get_at((sparxcenterx+1, sparxcentery))[:3] == (255,255,255) and direction != "left"):
                direction = "right"
            elif(screen.get_at((sparxcenterx-1, sparxcentery))[:3] == (255,255,255) and direction != "right"):
                direction = "left"
            elif(screen.get_at((sparxcenterx, sparxcentery-1))[:3] == (255,255,255) and direction != "down"):
                direction = "up"
            elif(screen.get_at((sparxcenterx, sparxcentery+1))[:3] == (255,255,255) and direction != "up"):
                direction = "down"
        elif(randInt == 2):
            if(screen.get_at((sparxcenterx, sparxcentery+1))[:3] == (255,255,255) and direction != "up"):
                direction = "down"
            elif(screen.get_at((sparxcenterx, sparxcentery-1))[:3] == (255,255,255) and direction != "down"):
                direction = "up"
            elif(screen.get_at((sparxcenterx-1, sparxcentery))[:3] == (255,255,255) and direction != "right"):
                direction = "left"
            elif(screen.get_at((sparxcenterx+1, sparxcentery))[:3] == (255,255,255) and direction != "left"):
                direction = "right"
        else:
            if(screen.get_at((sparxcenterx, sparxcentery-1))[:3] == (255,255,255) and direction != "down"):
                direction = "up"
            elif(screen.get_at((sparxcenterx, sparxcentery+1))[:3] == (255,255,255) and direction != "up"):
                direction = "down"
            elif(screen.get_at((sparxcenterx-1, sparxcentery))[:3] == (255,255,255) and direction != "right"):
                direction = "left"
            elif(screen.get_at((sparxcenterx+1, sparxcentery))[:3] == (255,255,255) and direction != "left"):
                direction = "right"
                
        if(sparx2Count % 2 == 0):
            if direction == 'up':
                self.rect.move_ip(0, -1)
            elif direction == 'down':
                self.rect.move_ip(0, 1)
            elif direction == 'left':
                self.rect.move_ip(-1, 0)
            elif direction == 'right':
                self.rect.move_ip(1, 0)

        sparx2Count += 1
        
        return direction

WIDTH = 800
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Qix Game")

#Game Field
lines = []
lines.append(pygame.Rect(50, 100, 1, 500))
lines.append(pygame.Rect(50, HEIGHT-100, 700, 1))
lines.append(pygame.Rect(WIDTH-50, 100, 1, 500))
lines.append(pygame.Rect(50, 100, 700, 1))

#Incursion Lines
drawLines = []
#Polygons
polys = []

#For Area calculations/font
area = 0
textFont1 = pygame.font.SysFont("arial",20)
textFont2 = pygame.font.SysFont("arial",24)
overlaps = []

player = Player()

qix_speedx, qix_speedy = 1,1
qix = Qix()

sparx1 = Sparx1()
sparx2 = Sparx2()
sparx2Count = 0

randInt = 0

clock = pygame.time.Clock()

startPos = endPos = (0,0)
startPushPos = (0,0)

direction1 = ""
direction2 = ""

lives = 3
#Please add the path of the heart image below:
heart = pygame.image.load(r'.\heart.png')
heart = pygame.transform.scale(heart.convert_alpha(), (30, 30))

#To allow for player to print line while moving
drawNum = 0

#Check if the player got hit
hit = False
#Check if the there are any pressedKeys
isPressedKeys = True

running = True

while(running):

    #Checks event queue
    for event in pygame.event.get():

        if(event.type == pygame.KEYDOWN):
            #If presses escape, close
            if(event.key == pygame.K_ESCAPE):
                running = False
            elif(event.key == pygame.K_UP or event.key == pygame.K_DOWN or
                 event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):
                
                if(event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):
                    drawNum = 1
                elif(event.key == pygame.K_UP or event.key == pygame.K_DOWN):
                    drawNum = 2

                if(startPos == (0,0)):
                    startPos = (player.rect.centerx,player.rect.centery)

                if(startPushPos == (0,0) and len(drawLines) == 0):
                    startPushPos = (player.rect.centerx,player.rect.centery)

        elif(event.type == pygame.KEYUP):
            if(event.key == pygame.K_UP or event.key == pygame.K_DOWN or
               event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):
                
                drawNum = 0

                if(endPos == (0,0) and pygame.key.get_pressed().count(1) == 0 and hit == False):
                    endPos = (player.rect.centerx, player.rect.centery)
                    
                if(hit == True):
                    hit = False
            
        #If clicks on exit, close
        elif(event.type == pygame.QUIT):
            running = False

    #Collision check for sparx and player
    if(player.rect.colliderect(sparx1.rect)):
        if(direction1 == "up"):
            direction1 = "down"
            sparx1.rect.centery = sparx1.rect.centery + 2
        elif(direction1 == "down"):
            direction1 = "up"
            sparx1.rect.centery = sparx1.rect.centery - 2
        elif(direction1 == "left"):
            direction1 = "right"
            sparx1.rect.centerx = sparx1.rect.centerx + 2
        elif(direction1 == "right"):
            direction1 = "left"
            sparx1.rect.centerx = sparx1.rect.centerx - 2

        if(pygame.key.get_pressed().count(1) == 0):
            isPressedKeys = False
        if(lives > 1):
            ctypes.windll.user32.MessageBoxW(0, "Careful, you lost a life!", "Hit!", 0)
        lives = lives - 1
        hit = True

    elif(player.rect.colliderect(sparx2.rect)):
        sparx2Count = 0
        if(direction2 == "up"):
            sparx2.rect.centery = sparx2.rect.centery + 2
            direction2 = "down"
        elif(direction2 == "down"):
            direction2 = "up"
            sparx2.rect.centery = sparx2.rect.centery - 2
        elif(direction2 == "left"):
            direction2 = "right"
            sparx2.rect.centerx = sparx2.rect.centerx + 2
        elif(direction2 == "right"):
            direction2 = "left"
            sparx2.rect.centerx = sparx2.rect.centerx - 2

        if(pygame.key.get_pressed().count(1) == 0):
            isPressedKeys = False
        if(lives > 1):
            ctypes.windll.user32.MessageBoxW(0, "Careful, you lost a life!", "Hit!", 0)
        lives = lives - 1
        hit = True
    
    #Collision check for sparx and incursion
    if(sparx1.rect.center == startPushPos and player.rect.collidelist(lines) == -1):
        if(direction1 == "up"):
            direction1 = "down"
            sparx1.rect.centery = sparx1.rect.centery + 20
        elif(direction1 == "down"):
            direction1 = "up"
            sparx1.rect.centery = sparx1.rect.centery - 20
        elif(direction1 == "left"):
            direction1 = "right"
            sparx1.rect.centerx = sparx1.rect.centerx + 20
        elif(direction1 == "right"):
            direction1 = "left"
            sparx1.rect.centerx = sparx1.rect.centerx - 20
            
        player.rect.center = startPushPos
        drawLines = []
        startPushPos = (0,0)
        if(pygame.key.get_pressed().count(1) == 0):
            isPressedKeys = False
        if(lives > 1):
            ctypes.windll.user32.MessageBoxW(0, "Careful, you lost a life!", "Hit!", 0)
        lives = lives - 1
        hit = True
        
    elif(sparx2.rect.center == startPushPos and player.rect.collidelist(lines) == -1):
        if(direction2 == "up"):
            sparx2.rect.centery = sparx2.rect.centery + 20
            direction2 = "down"
        elif(direction2 == "down"):
            direction2 = "up"
            sparx2.rect.centery = sparx2.rect.centery - 20
        elif(direction2 == "left"):
            direction2 = "right"
            sparx2.rect.centerx = sparx2.rect.centerx + 20
        elif(direction2 == "right"):
            direction2 = "left"
            sparx2.rect.centerx = sparx2.rect.centerx - 20
            
        player.rect.center = startPushPos
        drawLines = []
        startPushPos = (0,0)
        if(pygame.key.get_pressed().count(1) == 0):
            isPressedKeys = False
        if(lives > 1):
            ctypes.windll.user32.MessageBoxW(0, "Careful, you lost a life!", "Hit!", 0)
        lives = lives - 1
        hit = True
    
    #Black screen
    screen.fill((0,0,0))

    #If pressed more than 1 key
    if(pygame.key.get_pressed().count(1) > 1 and startPos != (0,0)):
        endPos = (player.rect.centerx, player.rect.centery)

    #Reset positions if player was hit
    if(hit == True):
        startPushPos = startPos = endPos = (0,0)
        if not(isPressedKeys):
            hit = False
            isPressedKeys = True

    #Adds new lines
    #   NOTE: only press one arrow button at a time
    if(startPos != (0,0) and endPos != (0,0)):
        drawLines.append(pygame.draw.line(screen,(255,255,255),startPos,endPos))
        
        if(pygame.key.get_pressed().count(1) > 0):
            startPos = (player.rect.centerx, player.rect.centery)
            endPos = (0,0)
        else:
            startPos = endPos = (0,0)

    #If player hits an edge
    for line in lines:
        if(line.collidepoint(player.rect.centerx, player.rect.centery) and drawLines != []
           and startPos == (0,0) and endPos == (0,0)):
            
            #Get vertices
            vertices = []
            for dline in drawLines:
                vertices.append((dline.x,dline.y))
            
            #Remove lines that are overlapping
            for dline in drawLines:
                if(line.height == 1 and dline.height == 1 and line.y == dline.y and line.width > dline.width):      #Horizontal line
                    drawLines.remove(dline)
                    vertices.remove((dline.x,dline.y))
                elif(line.width == 1 and dline.width == 1 and line.x == dline.x and line.height > dline.height):    #Vertical line
                    drawLines.remove(dline)
                    vertices.remove((dline.x,dline.y))

            #Gets width and height
            width = 1
            height = 1
            topx = WIDTH
            topy = HEIGHT
            for l in drawLines:
                if(l.width > width):
                    width = l.width
                if(l.height > height):
                    height = l.height
                    
            #Gets top left coordinate of rectangle
            for v in vertices:
                if(v[0] < topx):
                    topx = v[0]
                if(v[1] < topy):
                    topy = v[1]

            #Adds a polygon to polys (to fill the incursion)
            #If it is a straight line
            if(len(drawLines) == 1):
                #Vertical line
                if(drawLines[0].width == 1):    
                    if(topx < WIDTH//2):
                        polys.append(pygame.Rect(51,topy+1,topx-51,height-2))
                        area = area + (topx - 50)*height
                    else:
                        polys.append(pygame.Rect(topx+1,topy+1,749-topx,height-2))
                        area = area +(750 - topx)*height
                #Horizontal line
                else:                           
                    if(topy < HEIGHT//2):
                        polys.append(pygame.Rect(topx+1,101,width-2,topy-101))
                        area = area + width*(topy - 100)
                    else:
                        polys.append(pygame.Rect(topx+1,topy+1,width-2,599-topy))
                        area = area + width*(600 - topy)
            #If there are multiple lines
            else:
                polys.append(pygame.Rect(topx+1,topy+1,width-2,height-2))
                area = area + width*height

            #This if-else block is for calculating the area
                #Remove polys that are only lines
            if(polys[-1].width < 1 and polys[-1].height < 1):
                area = area - width*height
                polys.pop()
            else:
                #Add overlapped areas
                for poly in polys:
                    if(poly != polys[-1] and polys[-1].clip(poly).width != 0 and polys[-1].clip(poly).height != 0):
                        if not(polys[-1].clip(poly) in overlaps):
                            overlaps.append(polys[-1].clip(poly))

                overlapsCopy = copy.deepcopy(overlaps)

                #Remove duplicate overlaps
                for poly in overlaps:
                    if(poly != overlaps[-1] and overlaps[-1].clip(poly).width != 0 and overlaps[-1].clip(poly).height != 0):
                        overlapsCopy.remove(poly)
                        
                overlaps = overlapsCopy

                #Delete overlapped area
                for poly in overlaps:
                    area = area - poly.width * poly.height
                    
                overlaps = []
            
            #Add the incursion lines to the lines list if successful
            lines = lines + drawLines
            drawLines = []
            startPushPos = (0,0)


    #Draw lines and green polygons
    for polygon in polys:
        pygame.draw.rect(screen,(0,150,0),polygon)
    
    for line in lines:
        pygame.draw.rect(screen,(255,255,255),line)

    for line in drawLines:
        pygame.draw.rect(screen,(255,255,255),line)

    #Draw line as player moves
    if(drawNum == 1):
        pygame.draw.line(screen,(255,255,255),startPos,(player.rect.centerx,startPos[1]))
    elif(drawNum == 2):
        pygame.draw.line(screen,(255,255,255),startPos,(startPos[0],player.rect.centery))
        
    #Gets a dict of the keys pressed
    pressedKeys = pygame.key.get_pressed()
    #Update the player 
    player.update(pressedKeys, lines)
    #Update the player collisions
    player.updateCollision(pressedKeys, lines)

    #Update the qix movement
    qix.update(lines,player)

    #updates sparx1 and priotorizes direction based on the randInt
    randInt = random.randint(0,3)
    direction1 = sparx1.update(direction1,randInt)
    direction2 = sparx2.update(direction2,randInt)

    #Draw the player onto the screen
    screen.blit(player.surface,player.rect)

    #Draw area label
    areaLabel = textFont1.render("Claimed: " + "%.2f" %(area/(500*700)*100) + "%",1,(255,255,255))
    areaNeededLabel = textFont2.render("Area Needed: 50%",1,(255,255,255))
    screen.blit(areaLabel,(50,70))
    screen.blit(areaNeededLabel,(300,20))

    #Draw the qix onto the screen
    screen.blit(qix.surface, qix.rect) 

    #Draw the sparx onto the screen
    screen.blit(sparx1.surface,sparx1.rect)
    screen.blit(sparx2.surface,sparx2.rect)

    #Players lives - need to integrate this when collision occurs
    if lives == 3:
        screen.blit(heart, (620, 65))
        screen.blit(heart, (660, 65))
        screen.blit(heart, (700, 65))

    elif lives == 2:
        screen.blit(heart, (660, 65))
        screen.blit(heart, (700, 65))

    elif lives == 1:
        screen.blit(heart, (700, 65))
    else:
        ctypes.windll.user32.MessageBoxW(0, "You ran out of lives, try again!", "Lost", 0)
        running = False

    pygame.display.flip()

    if(area/(500*700)*100 >= 50):
        ctypes.windll.user32.MessageBoxW(0, "You Win! Thanks for playing!", "Winner!", 0)
        running = False

    clock.tick(240)

pygame.quit()


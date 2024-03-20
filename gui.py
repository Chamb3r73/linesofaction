import pygame
import numpy as np
import math
from game import Game # import the game logic and board

Game = Game()
pygame.init()
# initialise pygame and imported Game logic

#font = pygame.font.SysFont('times new roman', 40) # import the font to be used
font = pygame.font.Font('resources/Times New Roman MT Std Bold Condensed.ttf', 40)
#bigfont = pygame.font.SysFont('times new roman', 60)
bigfont = pygame.font.Font('resources/Times New Roman MT Std Bold Condensed.ttf', 60)
# adding background images that can dynamically be selected:
blueimage = pygame.image.load('resources/blue.png') # define background image
blueimage = pygame.transform.scale(blueimage, (1440, 900)) # transform image to fit into window size
turtleimage = pygame.image.load('resources/turtle.jpg') # define background image
turtleimage = pygame.transform.scale(turtleimage, (1440, 900)) # transform image to fit into window size
mountainimage = pygame.image.load('resources/mountain.jpg') # define background image
mountainimage = pygame.transform.scale(mountainimage, (1440, 900)) # transform image to fit into window size
sunsetimage = pygame.image.load('resources/sunset2.jpg') # define background image
sunsetimage = pygame.transform.scale(sunsetimage, (1440, 900)) # transform image to fit into window size
turtle3image = pygame.image.load('resources/_turtle3.jpg') # define background image
turtle3image = pygame.transform.scale(turtle3image, (1440, 900)) # transform image to fit into window size
mountain2image = pygame.image.load('resources/_mountain2.jpg') # define background image
mountain2image = pygame.transform.scale(mountain2image, (1440, 900)) # transform image to fit into window size
turtle2image = pygame.image.load('resources/_turtle2.jpg') # define background image
turtle2image = pygame.transform.scale(turtle2image, (1440, 900)) # transform image to fit into window size

clock = pygame.time.Clock() # the clock variable is initialised but assigned value (60) later
class GameVariables(): # Class that stores variables that need to be used between classes as the turn progresses
    # contains methods to set and return the variables here
    def __init__(self, highlightlist, currentturn, startingcoord, winner, startingaicoord, bestmove, turnnumber, trackingOrigin, trackingDestination, background):
        self.__highlightlist = highlightlist
        self.__currentturn = currentturn
        self.__startingcoord = startingcoord
        self.__winner = winner
        self.__startingaicoord = startingaicoord
        self.__bestmove = bestmove
        self.__turnnumber = turnnumber
        self.__trackingOrigin = trackingOrigin
        self.__trackingDestination = trackingDestination
        self.__backgroundoptions = [blueimage, turtleimage, mountainimage, sunsetimage, turtle3image, mountain2image, turtle2image]
        self.__background = self.__backgroundoptions[background]
        self.__backgroundnumber = background
    
    def editlist(self, newlist):
        self.__highlightlist = newlist

    def changeturn(self): # change the turn for both the variable stored in this class and the turn variable in Game
        if self.__currentturn == 'w':
            self.__currentturn = 'b'
            Game.currentturn = 'b'
        else:
            self.__currentturn = 'w'
            Game.currentturn = 'w'
    
    def setstartingcoord(self, startingcoord):
        self.__startingcoord = startingcoord
    
    def checkforwin(self):
        self.__winner = Game.checkforwin()
        return self.__winner

    def returnlist(self):
        return self.__highlightlist
    
    def returnturn(self):
        return self.__currentturn
    
    def returnstartingcoord(self):
        return self.__startingcoord
    
    def givefullplayername(self):
        if self.__currentturn == 'b':
            playername = 'Blue'
        else:
            playername = 'Red'
        return playername
    
    def givefullwinnername(self, player):
        if player == 'b':
            playername = 'Blue'
        else:
            playername = 'Red'
        return playername
    
    def setprevaiturndata(self, startingaicoord, bestmove):
        self.__startingaicoord = startingaicoord
        self.__bestmove = bestmove
    
    def returnaistarting(self):
        return self.__startingaicoord
    
    def returnbestmove(self):
        return self.__bestmove
    
    def incrementturnnumber(self):
        self.__turnnumber+=1

    def returnturnnumber(self):
        return self.__turnnumber
    
    def settrackingdata(self, origin, destination):
        self.__trackingOrigin = origin
        self.__trackingDestination = destination
    
    def returntrackingOrigin(self):
        return self.__trackingOrigin
    
    def returntrackingDestination(self):
        return self.__trackingDestination

    def setbackground(self, backgroundnumber):
        self.__background = self.__backgroundoptions[backgroundnumber]
    
    def returnbackground(self):
        return self.__background
    
    def nextbackground(self):
        if self.__backgroundnumber == len(self.__backgroundoptions)-1:
            self.__backgroundnumber = 0
        else:
            self.__backgroundnumber += 1
        self.__background = self.__backgroundoptions[self.__backgroundnumber]

    def resetall(self):
        self.__highlightlist = []
        self.__currentturn = 'w'
        self.__startingcoord = []
        self.__winner = None
        self.__turnnumber = 1
        self.__trackingOrigin = ''
        self.__trackingDestination = ''
    
GameVariablesObj = GameVariables([], 'w', '', None, '', '', 1, '', '', 0) # intialise the object

class Screen(): # main screen class that governs the display and runs the main game loop
    def __init__(self):
        pygame.display.set_caption('Lines of Action') # set window caption
        self.screen = pygame.display.set_mode((1440, 900)) # create the window and define size
        self.screen.fill((9, 52, 87)) # set background colour
        self.running = True # variable that makes sure the game is quit properly when exited, and makes the screen loop
        self.difficultytoname = {
            1:'Computer - Easy',
            2:'Computer - Medium',
            3:'Computer - Hard',
            4:'Computer - Cheating',
            0:'Human'
        }
    
    def main(self):
        self.screen.fill((9, 52, 87)) # set background colour for this screen
        self.screen.blit(GameVariablesObj.returnbackground(), (0, 0)) # set background image
        while self.running == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False # ends the code once window exited
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SLASH:
                        GameVariablesObj.nextbackground()
            self.screen.blit(GameVariablesObj.returnbackground(), (0, 0)) # set background image to refresh every frame so the button acts instantly
            startAIbutton = Button(750, 100, 600, 200, 'Begin Game vs AI', lambda: self.selectdifficulty()) # buttons to select which opponent to play against
            startHUMANbutton = Button(100, 100, 600, 200, 'Begin Game vs Human', lambda: self.board(False, 0)) # lambda so I can pass the isAI value through without having the function called at runtime
            startAIbutton.draw(self.screen)
            startHUMANbutton.draw(self.screen) # adding the buttons to the draw stack
            instructionsbutton = Button(420, 400, 600, 200, 'Show Instructions', self.instructions)
            instructionsbutton.draw(self.screen)
            #swapbackgroundbutton = Button(1230, 790, 200, 50, 'Change BG', lambda: GameVariablesObj.nextbackground())
            #defaultbutton = Button(1230, 650, 200, 50, 'Blue', lambda: GameVariablesObj.setbackground(0))
            #turtlebutton = Button(1230, 720, 200, 50, 'Turtle', lambda: GameVariablesObj.setbackground(1))
            #mountainbutton = Button(1230, 790, 200, 50, 'Mountain', lambda: GameVariablesObj.setbackground(2))
            #swapbackgroundbutton.draw(self.screen)
            #defaultbutton.draw(self.screen)
            #turtlebutton.draw(self.screen)
            #mountainbutton.draw(self.screen)
            pygame.display.update() # execute the draw stack and display on screen
    
    def selectdifficulty(self):
        self.screen.fill((9, 52, 87))
        self.screen.blit(GameVariablesObj.returnbackground(), (0, 0)) # set background image
        while self.running == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False # ends the code once window exited
            startEasyButton = Button(100, 300, 300, 200, 'Easy', lambda: self.board(True, 1))
            startMediumButton = Button(450, 300, 300, 200, 'Medium', lambda: self.board(True, 2))
            startHardButton = Button(100, 550, 300, 200, 'Hard', lambda: self.board(True, 3))
            startCheatingButton = Button(450, 550, 300, 200, 'Cheating', lambda: self.board(True, 4))
            startEasyButton.draw(self.screen)
            startMediumButton.draw(self.screen)
            startHardButton.draw(self.screen)
            startCheatingButton.draw(self.screen)
            selectdifficultytextsurface = font.render(f'Select your difficulty: ', True, (255, 255, 255))
            self.screen.blit(selectdifficultytextsurface, (100, 220))
            selectdifficultytitlesurface1 = bigfont.render(f'COMPUTER', True, (255, 255, 255))
            self.screen.blit(selectdifficultytitlesurface1, (900, 200))
            selectdifficultytitlesurface2 = bigfont.render(f'DIFFICULTY', True, (255, 255, 255))
            self.screen.blit(selectdifficultytitlesurface2, (900, 300))
            selectdifficultytitlesurface3 = bigfont.render(f'SELECT', True, (255, 255, 255))
            self.screen.blit(selectdifficultytitlesurface3, (900, 400))
            quittoMainMenuButton = Button(1330, 15, 100, 50, 'Back', lambda: self.quittoMainMenu(), [(17, 78, 128), (14, 67, 110)])
            quittoMainMenuButton.draw(self.screen)
            pygame.display.update()

    def quittoMainMenu(self):
        Game.resetboard()
        GameVariablesObj.resetall()
        self.main()

    def board(self, isAI, difficulty): # scene method for the main game vs AI opponent
        #print(difficulty)
        Game.resetboard() # put back in later
        GameVariablesObj.resetall() # before the scene loop, make sure the board and variables are empty ready for a new game
        self.screen.fill((9, 52, 87)) # set backrgound colour
        self.screen.blit(GameVariablesObj.returnbackground(), (0, 0)) # set background image
        while self.running == True: # loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False # ends the code once window exited
            clock.tick(60) # fps and clock speed
            board = Board(GameVariablesObj.returnlist()) # instantiate board object, inside the loop so it updates every turn
            winner = GameVariablesObj.checkforwin() # checking if game over
            if winner != None: # the function returns the name of the winner if there is one, or None if not
                self.gamefinish(board, winner, isAI, difficulty) # if the game is over, proceed to the game over screen
            self.screen.fill((9, 52, 87)) # draw over the background so nothing overlaps each loop
            self.screen.blit(GameVariablesObj.returnbackground(), (0, 0)) # set background image
            board.draw(self.screen, isAI, difficulty) # isAI flag set to True so the AI turn is run
            # the screen class creates a board object
            # which initialises a list of all the tiles
            # the screen class calls the boards draw method
            # which calls each tiles draw method
            # which puts a suitable rectangle and circle in the buffer
            #the screen class then updates the screen
            # turn number stuff:
            turnnumbersurface = font.render(f'Move: {GameVariablesObj.returnturnnumber()}', True, (255, 255, 255))
            currentplayersurface = font.render(f'Turn: {GameVariablesObj.givefullplayername()}', True, (255, 255, 255))
            self.screen.blit(turnnumbersurface, (100, 190))
            self.screen.blit(currentplayersurface, (100, 250))
            # title and gamemode:
            titleTextSurface = font.render(f'Lines Of Action', True, (255, 255, 255))
            gamemodeSurface1 = font.render(f'Playing Against:', True, (255, 255, 255))
            gamemodeSurface2 = font.render(f'{self.difficultytoname[difficulty]}', True, (255, 255, 255))
            self.screen.blit(titleTextSurface, (1080, 150))
            self.screen.blit(gamemodeSurface1, (1080, 250))
            self.screen.blit(gamemodeSurface2, (1080, 290))
            # the coordinate grid:
            gridsurfaceA = font.render('A', True, (255, 255, 255))
            gridsurfaceB = font.render('B', True, (255, 255, 255))
            gridsurfaceC = font.render('C', True, (255, 255, 255))
            gridsurfaceD = font.render('D', True, (255, 255, 255))
            gridsurfaceE = font.render('E', True, (255, 255, 255))
            gridsurfaceF = font.render('F', True, (255, 255, 255))
            gridsurfaceG = font.render('G', True, (255, 255, 255))
            gridsurfaceH = font.render('H', True, (255, 255, 255))
            gridsurface1 = font.render('1', True, (255, 255, 255))
            gridsurface2 = font.render('2', True, (255, 255, 255))
            gridsurface3 = font.render('3', True, (255, 255, 255))
            gridsurface4 = font.render('4', True, (255, 255, 255))
            gridsurface5 = font.render('5', True, (255, 255, 255))
            gridsurface6 = font.render('6', True, (255, 255, 255))
            gridsurface7 = font.render('7', True, (255, 255, 255))
            gridsurface8 = font.render('8', True, (255, 255, 255))
            self.screen.blit(gridsurfaceA, (430, 730))
            self.screen.blit(gridsurfaceB, (510, 730))
            self.screen.blit(gridsurfaceC, (590, 730))
            self.screen.blit(gridsurfaceD, (670, 730))
            self.screen.blit(gridsurfaceE, (750, 730))
            self.screen.blit(gridsurfaceF, (830, 730))
            self.screen.blit(gridsurfaceG, (910, 730))
            self.screen.blit(gridsurfaceH, (990, 730))
            self.screen.blit(gridsurface1, (350, 100))
            self.screen.blit(gridsurface2, (350, 180))
            self.screen.blit(gridsurface3, (350, 260))
            self.screen.blit(gridsurface4, (350, 340))
            self.screen.blit(gridsurface5, (350, 420))
            self.screen.blit(gridsurface6, (350, 500))
            self.screen.blit(gridsurface7, (350, 580))
            self.screen.blit(gridsurface8, (350, 660))
            quittoMainMenuButton = Button(1330, 15, 100, 50, 'Quit', lambda: self.quittoMainMenu(), [(17, 78, 128), (14, 67, 110)])
            quittoMainMenuButton.draw(self.screen)
            pygame.display.update() # update the whole screen, drawing the elements in the buffer
    
    def instructions(self): # scene method to show the instructions
        self.screen.fill((9, 52, 87))
        self.screen.blit(GameVariablesObj.returnbackground(), (0, 0)) # set background image
        while self.running == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False # ends the code once window exited
            # defining the texts to be displayed
            textsurface1 = font.render('Lines of Actions Rules', True, (255, 255, 255)) # for text, set antialiasing to true mainly in order to be able to use 24 bit colour instead of 8 bit (and also to anti alias it i guess)
            textsurface2 = font.render('Objective: Form a fully connected line (horizontally, vertically or diagonally) with your', True, (255, 255, 255))
            textsurface3 = font.render('pieces.', True, (255, 255, 255))
            textsurface4 = font.render('Movement: Click a piece to see its available locations. Each piece can move the number', True, (255, 255, 255))
            textsurface5 = font.render('of spaces equivalent to the total number of pieces in that axis.', True, (255, 255, 255))
            textsurface6 = font.render('Pieces can move over their own pieces, but not enemy pieces. Pieces can land and take', True, (255, 255, 255))
            textsurface7 = font.render('enemy pieces, but not their own pieces.', True, (255, 255, 255))
            textsurface8 = font.render('If your move completes the line for both you and your opponent, you win.', True, (255, 255, 255))
            textsurface9 = font.render('It is possible to complete your opponents objective for them on your own turn.', True, (255, 255, 255))
            # adding the texts into the screen buffer
            self.screen.blit(textsurface1, (10, 10))
            self.screen.blit(textsurface2, (10, 90))
            self.screen.blit(textsurface3, (10, 130))
            self.screen.blit(textsurface4, (10, 220))
            self.screen.blit(textsurface5, (10, 260))
            self.screen.blit(textsurface6, (10, 350))
            self.screen.blit(textsurface7, (10, 390))
            self.screen.blit(textsurface8, (10, 460))
            self.screen.blit(textsurface9, (10, 540))
            startHUMANbutton = Button(100, 600, 600, 200, 'Begin Game vs Human', lambda: self.board(False, 0)) # button to go into the game
            startAIbutton = Button(750, 600, 600, 200, 'Begin Game vs AI', lambda: self.selectdifficulty()) # button to go into the game
            startAIbutton.draw(self.screen)
            startHUMANbutton.draw(self.screen)
            quittoMainMenuButton = Button(1330, 15, 100, 50, 'Back', lambda: self.quittoMainMenu(), [(17, 78, 128), (14, 67, 110)])
            quittoMainMenuButton.draw(self.screen)
            pygame.display.update() # update the screen

    def gamefinish(self, board, winningplayer, isAI, difficulty): # scene for when the game has finished
        self.screen.fill((9, 52, 87))
        self.screen.blit(GameVariablesObj.returnbackground(), (0, 0)) # set background image
        while self.running == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False # ends the code once window exited
            board.finaldraw(self.screen) # calls the finaldraw method of the board, which doesnt allow for interaction (only displays the board)
            textsurface1 = bigfont.render('Game Over!', True, (255, 255, 255))
            textsurface2 = bigfont.render(f'The winner is: {GameVariablesObj.givefullwinnername(winningplayer)}', True, (255, 255, 255))
            self.screen.blit(textsurface1, (900, 50))
            self.screen.blit(textsurface2, (900, 200))
            returntoMainMenuButton = Button(900, 300, 400, 200, 'Main Menu', lambda: self.quittoMainMenu())
            rematchButton = Button(900, 550, 400, 200, 'Rematch', lambda: self.board(isAI, difficulty)) # buttons and text to start a new game
            rematchButton.draw(self.screen)
            returntoMainMenuButton.draw(self.screen)
            gridsurfaceA = font.render('A', True, (255, 255, 255))
            gridsurfaceB = font.render('B', True, (255, 255, 255))
            gridsurfaceC = font.render('C', True, (255, 255, 255))
            gridsurfaceD = font.render('D', True, (255, 255, 255))
            gridsurfaceE = font.render('E', True, (255, 255, 255))
            gridsurfaceF = font.render('F', True, (255, 255, 255))
            gridsurfaceG = font.render('G', True, (255, 255, 255))
            gridsurfaceH = font.render('H', True, (255, 255, 255))
            gridsurface1 = font.render('1', True, (255, 255, 255))
            gridsurface2 = font.render('2', True, (255, 255, 255))
            gridsurface3 = font.render('3', True, (255, 255, 255))
            gridsurface4 = font.render('4', True, (255, 255, 255))
            gridsurface5 = font.render('5', True, (255, 255, 255))
            gridsurface6 = font.render('6', True, (255, 255, 255))
            gridsurface7 = font.render('7', True, (255, 255, 255))
            gridsurface8 = font.render('8', True, (255, 255, 255))
            self.screen.blit(gridsurfaceA, (110, 730))
            self.screen.blit(gridsurfaceB, (180, 730))
            self.screen.blit(gridsurfaceC, (260, 730))
            self.screen.blit(gridsurfaceD, (340, 730))
            self.screen.blit(gridsurfaceE, (420, 730))
            self.screen.blit(gridsurfaceF, (500, 730))
            self.screen.blit(gridsurfaceG, (580, 730))
            self.screen.blit(gridsurfaceH, (660, 730))
            self.screen.blit(gridsurface1, (30, 100))
            self.screen.blit(gridsurface2, (30, 180))
            self.screen.blit(gridsurface3, (30, 260))
            self.screen.blit(gridsurface4, (30, 340))
            self.screen.blit(gridsurface5, (30, 420))
            self.screen.blit(gridsurface6, (30, 500))
            self.screen.blit(gridsurface7, (30, 580))
            self.screen.blit(gridsurface8, (30, 660))
            pygame.display.update()
    

class Button(): # button class to make button objects (works similar to the Tile)
    def __init__(self, x, y, width, height, text, onclickfunc=None, colour=None):
        # button properties
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.onclickfunc = onclickfunc
        if colour == None:
            self.colours = {
                'inactive':(0, 0, 0),
                'hover':(30, 30, 30),
                'click':(100, 100, 100)
            }
        else:
            self.colours = {
                'inactive':colour[0],
                'hover':colour[1],
                'click':(100, 100, 100)
            }
        # creating button components using the properties (the rectangle, the background, the text)
        self.buttonrectangle = pygame.Rect(self.x, self.y, self.width, self.height) # the rectangle for the button
        self.buttonsurface = pygame.Surface((self.width, self.height)) # the background of the rectangle
        self.buttonsurface.fill(self.colours['inactive']) # set the colour of the rectangle surface
        self.textsurface = font.render(text, True, (255, 255, 255)) # the text in the rectangle

    def draw(self, display):
        # each tick the draw function checks if there is a mouse and if it clicks, executes the click function
        mousepos = pygame.mouse.get_pos()
        self.buttonsurface.fill(self.colours['inactive'])
        if self.buttonrectangle.collidepoint(mousepos): # is the mouse inside the button rectangle
            self.buttonsurface.fill(self.colours['hover']) # set it to the hover colour
            if pygame.mouse.get_pressed(num_buttons=3)[0]: # if the mouse if pressed down (num_buttons means it is testing for left middle and right click (no side buttons)). [0] takes the status of the left mouse button
                    self.buttonsurface.fill(self.colours['click']) # set to the pressed colour
                    self.onclickfunc() # and execute the function of the button
                    # this repeats at whatever clock speed as long as you hold the mouse down but it doesnt matter since once it trasnfers scenes the button goes away

        # actually drawing the button:
        pygame.draw.rect(display, (255, 0, 255), self.buttonrectangle)
        self.buttonsurface.blit(self.textsurface, [ # investigate why these numbers
            self.buttonrectangle.width/2 - self.textsurface.get_rect().width/2,
            self.buttonrectangle.height/2 - self.textsurface.get_rect().height/2
        ])
        display.blit(self.buttonsurface, self.buttonrectangle) # adds the button to the buffer

class Board(): # board class that manages the board object
    def __init__(self, highlighted):
        self.board = Game.board # import the board from game.py
        self.highlighted = highlighted # when you click a tile, it calculates the possible moves and passes them into this list so they can be displayed
        self.trackingOrigin = GameVariablesObj.returntrackingOrigin()
        self.trackingDestination = GameVariablesObj.returntrackingDestination()
        self.tilelist = self.maketilelist() # calls its own method when the board object is made to create a list of Tile class objects based on each position in the board

    def maketilelist(self):
        # use the first 800x800 pixels for the board and the next 640 pixels for menuing and text
        tilelist = [] # intialise list
        y = 0
        x=0 # x and y are counters to represent the pixel coordinates on the window which increments as the loop continues
        count = 0
        for rowcount, row in enumerate(self.board): # for each row in the board
            x=0
            for piece in row: # for each piece in each row
                # set background colour for the tile
                if rowcount % 2 == 0: # even rows start black
                    if count % 2 == 0: # every second box is black
                        if str(int((y/80)+1))+':'+str(int((x/80)+1)) in self.trackingOrigin or str(int((y/80)+1))+':'+str(int((x/80)+1)) in self.trackingDestination:
                            colour = (97, 74, 104) # alternative colour for moved tile
                        else:
                            colour = (0, 0, 0) # starts with black then alternates white tiles etc
                    else:
                        if str(int((y/80)+1))+':'+str(int((x/80)+1)) in self.trackingOrigin or str(int((y/80)+1))+':'+str(int((x/80)+1)) in self.trackingDestination:
                            colour = (97, 74, 104)
                        else:
                            colour =  (255, 255, 255)
                else:
                    if count % 2 == 0: # odd rows start white
                        if str(int((y/80)+1))+':'+str(int((x/80)+1)) in self.trackingOrigin or str(int((y/80)+1))+':'+str(int((x/80)+1)) in self.trackingDestination:
                            colour = (97, 74, 104) # alternative colour for moved tile
                        else:
                            colour = (255, 255, 255) # starts with black then alternates white tiles etc
                    else:
                        if str(int((y/80)+1))+':'+str(int((x/80)+1)) in self.trackingOrigin or str(int((y/80)+1))+':'+str(int((x/80)+1)) in self.trackingDestination:
                            colour = (97, 74, 104) # alternative colour for moved tile
                        else:
                            colour =  (0, 0, 0)
                if piece == 'w': # adding pieces over tiles
                    # tile white
                    if str(int((y/80)+1))+':'+str(int((x/80)+1)) in self.highlighted: # converting the x and y pixel locations into board coordinates
                        tilelist.append(Tile(x, y, 'w', colour, True)) # if it is a highlighted piece set the flag to true
                        # creating a tile object to add to the list
                    else:
                        tilelist.append(Tile(x, y, 'w', colour, False))
                elif piece == 'b':
                    # tile black
                    if str(int((y/80)+1))+':'+str(int((x/80)+1)) in self.highlighted:
                        tilelist.append(Tile(x, y, 'b', colour, True))
                    else:
                        tilelist.append(Tile(x, y, 'b', colour, False))
                else:
                    # tile empty
                    if str(int((y/80)+1))+':'+str(int((x/80)+1)) in self.highlighted:
                        tilelist.append(Tile(x, y, '0', colour, True)) # if a highlighted piece, make the tile object with highlighted set to true
                    else:
                        tilelist.append(Tile(x, y, '0', colour, False)) # if not
                count += 1
                x+=80 # increment the pixels
            y+=80
        return tilelist # return the list of tiles
    
    def draw(self, display, isAI, difficulty): # when board draw method is called, it calls the tile objects own draw method for each tile it has
        for tile in self.tilelist:
            tile.draw(display, isAI, difficulty) # the isAI flag is passed down again
    
    def finaldraw(self, display): # to call each tile's final draw method which doesnt allow for interaction and only displays the tiles
        for tile in self.tilelist:
            tile.finaldraw(display)

class Tile(): # class to make an object for each tile in the board
    def __init__(self, x, y, piecetype, colour, highlighted):
        # tile properties
        self.x = x+400 # adding on offsets here. dont need to be redone when making the list of tiles because they get calculated normally
        self.y = y+80 # does have to be unoffset when making the coord
        self.finalx = x+80
        self.piecetype = piecetype
        self.colour = colour
        self.width = 80
        self.height = 80
        self.highlighted = highlighted # bool if the tile is highlighted or not
        self.pressed = False # the pressed value has to be outside the draw loop otherwise it wont work
        # creates the rectangle of the tile to be drawn later using the properties of the object
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height) # rectangle objects that are the background of each tile
        self.finalrect = pygame.Rect(self.finalx, self.y, self.width, self.height) # different x value because the board in the game over screen starts from closer to the left side of the screen than the normal board which is in the middle

    def isinputvalid(self, giveninput): # tests inputs based on what tile gets clicked
        giveninput = giveninput.split(':')[0]+giveninput.split(':')[1]
        if len(giveninput) != 2: # too long 
            return False
        giveninputy = int(giveninput[:1])
        giveninputx = int(giveninput[1:])
        if giveninputy > 8 or giveninputy < 1 or giveninputx > 8 or giveninputx < 1: # out of bounds
            return False
        if Game.board[giveninputy-1][giveninputx-1] != GameVariablesObj.returnturn(): # not your own piece
            return False
        return True # otherwise return true
    
    def draw(self, display, isAI, difficulty): # tile object draw method called from board draw method earlier. also now handles pressing
        mousepos = pygame.mouse.get_pos() # tiles are pressable
        if self.rect.collidepoint(mousepos): # is the mouse over the tile
            if pygame.mouse.get_pressed(num_buttons=3)[0]: # num_buttons=3 means pygame is checking for left click middle click and right click, and [0] is checking for leftclick specifically
                if self.pressed == False: # checks if clicked before so it doesnt execute multiple times when the click is held
                    coord = str(int(((self.y-80)/80)+1))+':'+str(int(((self.x-400)/80)+1)) # convert the location of the click (pixels) into a board coordinate
                    if self.isinputvalid(coord) == True: # check the input is valid (inbounds and current turn) otherwise dont update the list
                        GameVariablesObj.editlist(Game.calclegalmoves(coord)) # if the input is valid (ie pressing on one of your pieces), calls the Game method to genereate the legal moves for that piece and adds it to the list in GameVariables
                        GameVariablesObj.setstartingcoord(coord) # also sets the coord you pressed so the game knows which piece to move if you choose to move from there
                    else: # if the input isnt valid, this means you have clicked on an empty or opponent's tile, as you cannot land on your own tile
                        if coord in GameVariablesObj.returnlist(): # check if the piece you clicked on in inside the list of moves generated for the selected piece
                            # if it is, make the move
                            Game.makemove(GameVariablesObj.returnstartingcoord(), coord) # Game method that makes the move given the location and starting piece
                            GameVariablesObj.editlist([])
                            GameVariablesObj.settrackingdata(GameVariablesObj.returnstartingcoord(), coord)
                            GameVariablesObj.setstartingcoord('')
                            GameVariablesObj.incrementturnnumber()
                            GameVariablesObj.changeturn() # clear the list of possible moves and starting coord, then change the turn for the next player
                            if isAI: # if playing vs ai run the ai turn, otherwise the game loops and proceeds with the next human turn
                                if GameVariablesObj.checkforwin() == None: # prevents ai turn from running if human wins, and makes sure the winner variable is correct.
                                    # ai turn can begin
                                    from minimax import Minimax # the Minimax class is imported here for easy access
                                    boardcopy = np.copy(Game.board) # makes a copy of the board before the move as minimax simulates moves which need to not actually happen in the real board
                                    Minimax = Minimax(GameVariablesObj.returnturn(), Game.board) # instantiate the Minimax object with the board and player turn of the AI player
                                    score = Minimax.minimax(0, 3, GameVariablesObj.returnturn(), -math.inf, math.inf, difficulty) # run the minimax function which will return the score of the found optimal piece
                                    Game.board = boardcopy # restore from the board copy after minimax finishes
                                    # minimax stores the best move and its origin piece in the object properties
                                    #print(Minimax.treesize)
                                    Game.makemove(Minimax.startingcoord, Minimax.bestmove) # the move is made
                                    GameVariablesObj.editlist([])
                                    GameVariablesObj.settrackingdata(Minimax.startingcoord, Minimax.bestmove)
                                    GameVariablesObj.setstartingcoord('')
                                    GameVariablesObj.incrementturnnumber()
                                    GameVariablesObj.changeturn()
                                    GameVariablesObj.checkforwin() # sets self winner to correct var
                                    # reset the Game variables ready for the next turn, and also checks if there has been a winner
                                    # if there is a winner, the GameVariables stores who it is.
                    self.pressed = True # set pressed to true after the click so it isnt executed multiple times if the click is held

        # drawing the items after the logic sequence:
        # draw the base rectangle
        pygame.draw.rect(display, self.colour, self.rect)
        # draw the circles based on colour
        if self.piecetype == 'w': # for now white circles will be red and black circles blue
            pygame.draw.circle(display, (255, 0, 0), (self.x+40, self.y+40), 30) # draw a white piece in the rectangle. rectangles get drawn from the top left of the coords given, so to centre the circles (drawn from their center) the coords are +40 each
        elif self.piecetype == 'b':
            pygame.draw.circle(display, (0, 0, 255), (self.x+40, self.y+40), 30) # draw a black piece in the rectangle
        # and draw a highlight circle in the tile if it is a highlighted piece
        if self.highlighted:
            pygame.draw.circle(display, (255, 0, 255), (self.x+40, self.y+40), 5)

    def finaldraw(self, display): # only needs to draw the tile backgrounds and the pieces, no need to have click functions or highlights
        pygame.draw.rect(display, self.colour, self.finalrect)
        if self.piecetype == 'w': # for now white circles will be red and black circles blue
            pygame.draw.circle(display, (255, 0, 0), (self.finalx+40, self.y+40), 30) # draw a white piece in the rectangle. rectangles get drawn from the top left of the coords given, so to centre the circles (drawn from their center) the coords are +40 each
        elif self.piecetype == 'b':
            pygame.draw.circle(display, (0, 0, 255), (self.finalx+40, self.y+40), 30) # draw a black piece in the rectangle

thing = Screen()
thing.main() # create the screen object and run its main function, starting the program

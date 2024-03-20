# instantiate game class and run on cli
from game import Game
import numpy as np
import math
Game = Game()

def Main(): # main menu loop
    playagain = True
    while playagain == True:
        validbeginorinstructions = False
        while validbeginorinstructions == False:
            startorinstructions = input('Press Enter to start the game or type "?" to Show the instructions: ')
            if startorinstructions in ['', '?']: validbeginorinstructions = True
        LinesOfAction = CommandLineInterface() # instantiate CLI object 
        if startorinstructions == '?':
            print(LinesOfAction.showinstructions())
        else:
            validinput = False
            while validinput == False:
                computerorhuman = input('Type "C" to play aginst the computer, or "H" to play locally: ')
                if computerorhuman == "C":
                    validdifficulty = False
                    while validdifficulty == False:
                        difficulty = input("Enter a difficulty 1-4 for Easy, Medium, Hard or Cheating: ")
                        if difficulty in ['1', '2', '3', '4']: validdifficulty = True
                    validinput = True
                    LinesOfAction.playgame(True, int(difficulty))
                elif computerorhuman == "H":
                    validinput = True
                    LinesOfAction.playgame(False, 0)
                else:
                    print('Not a valid input, please type again')
        checkagain = input('Play Again? Enter Y to play again, or return if not: ').lower()
        if checkagain != 'y':
            playagain = False

class CommandLineInterface():
    def __init__(self):
        self.currentturn = 'w' # the starting turn is set to black, which is swapped to white when the game begins as white always starts
        self.turnnumber = 1
        self.difficultytoname = {
            1:'Computer - Easy',
            2:'Computer - Medium',
            3:'Computer - Hard',
            4:'Computer - Cheating',
            0:'Human'
        }

    def changeturn(self): # function to swap turns in both the CLI object variable and the Game object variable
        if self.currentturn == 'w':
            self.currentturn = 'b'
            Game.currentturn = 'b'
        else:
            self.currentturn = 'w'
            Game.currentturn = 'w'
        self.turnnumber += 1

    def showboard(self): # print the board
        for row in Game.board:
            print(row)

    def showinstructions(self): # return the instructions of the game
        instructions = '''Lines Of Action
        White goes first
        First input the coordinates of the piece you want to move, press enter, then input the coordinates of where you want to move to
        Example:\n84\n66\nMoves the 8th row 4th column piece to the 6th row 6th column square
        To win, have all your pieces form a line, with each piece connected horizontally, vertically or diagonally'''
        return instructions

    def isinputvalid(self, giveninput): # checks if an input is valid for initial selection based on length of data entry, then if it is out of bounds or an illegal move within the board
        try: int(giveninput) # return false if not given as an int
        except: return False
        if len(giveninput) != 2: # input too long
            return False
        giveninputy = int(giveninput[:1])
        giveninputx = int(giveninput[1:])
        if giveninputy > 8 or giveninputy < 1 or giveninputx > 8 or giveninputx < 1: # out of bounds
            return False
        if Game.board[giveninputy-1][giveninputx-1] != self.currentturn: # not your own piece selected to move from
            return False
        return True # otherwise return true

    def playturn(self):
        # get coord to move from
        choosingpiece = True
        validinput = False
        while choosingpiece == True:
            while validinput == False:
                startingcoord = input('Enter the coordinates of the square to move: ')
                if self.isinputvalid(startingcoord) == False:
                    print('Not a valid coord. Please enter again.')
                else:
                    validinput = True
            # fetch possible locations
            validcoords = Game.calclegalmoves(startingcoord)
            print(f'Possible moves: {validcoords}')
            validpiece = False
            # choose where to move to
            while validpiece == False:
                finishedchoosing = input('Type "/" to select a new piece to see moves for, or enter a move: ')
                if finishedchoosing == '/':
                    break
                if finishedchoosing not in validcoords:
                    print('Not a valid move. Please enter again.')
                else:
                    print('success')
                    targetcoord = finishedchoosing
                    validpiece = True
                    choosingpiece = False
            validinput = False

        # make the move on the board
        Game.makemove(startingcoord, targetcoord)

    def gamefinish(self, winner): # called when the game is over to show the winner
        print('Game Over!')
        if winner == 'b':
            winnername = 'Black'
        else:
            winnername = 'White'
        print(f'The Winner is: {winnername}')
    
    def givefullplayername(self, player): # converts name codes into their respective words
        if player == 'b':
            playername = 'Black'
        else:
            playername = 'White'
        return playername

    def playgame(self, isAI, difficulty): # main game loop
        gameover = False
        while gameover == False:
            # change the player (so the default player should be black in order for white to start first)
            fullplayername = self.givefullplayername(self.currentturn)
            print(f'Current player: {fullplayername}')
            print(f'Turn Number: {self.turnnumber}')
            print(f'Playing Lines of Action against {self.difficultytoname[difficulty]}')
            # display the board
            self.showboard()
            # do a turn
            self.playturn()
            # check for win
            winner = Game.checkforwin()
            if winner != None:
                gameover = True
                break
            self.changeturn()
            # check if playing against computer
            if isAI:
                # make ai turn
                from minimax import Minimax # the Minimax class is imported here for easy access
                boardcopy = np.copy(Game.board) # makes a copy of the board before the move as minimax simulates moves which need to not actually happen in the real board
                Minimax = Minimax(self.currentturn, Game.board) # instantiate the Minimax object with the board and player turn of the AI player
                score = Minimax.minimax(0, 3, self.currentturn, -math.inf, math.inf, difficulty) # run the minimax function which will return the score of the found optimal piece
                Game.board = boardcopy
                Game.makemove(Minimax.startingcoord, Minimax.bestmove)
                print(f'Computer moved from: {Minimax.startingcoord} to {Minimax.bestmove}')
                self.changeturn()
            # now the loop goes back to the top and continues the game to the next turn
        # once the game is over the loop is exited and displays game over text
        winnername = self.givefullplayername(winner)
        print('Game Over! The Winner is:')
        print(winnername)
        # display winner and returns up to Main(), which asks to play again or quit


if __name__ == "__main__": # start the program
    Main()

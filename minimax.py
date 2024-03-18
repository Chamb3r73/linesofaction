import numpy as np
import math
import random
from game import Game # import Game methods for use during minimax
Game = Game()

class Stack():
    def __init__(self):
        self.stack = []
    
    def push(self, item):
        self.stack.append(item)
        return self.stack
    
    def pop(self):
        item = self.stack.pop(len(self.stack)-1)
        return item
    
    def give(self):
        return self.stack
boardstack = Stack() # creating a stack object to store previous game states to roll back to

class Minimax():
    def __init__(self, currentturn, graph):
        self.currentturn = currentturn
        self.graph = graph # self.graph is a pointer to the original graph of the Game class
         
        # variables to keep track of minimax progress, and are updated at the end to represent the final move chosen
        self.startingcoord = ''
        self.bestmove = ''
        self.listofmovesfrom = []
        self.movetomake = ''
        self.piecemovedfrom = ''
        self.treesize = 0

    def evaluate(self, board, giveny, givenx, currentturn, originaly, originalx, cd, difficulty): # evaluate function to assess the score of a given move
        giveny = int(giveny)
        givenx = int(givenx)
        board[int(originaly)-1][int(originalx)-1] = '0' # setting the original point to empty as the move is simulated and evaluated
        pointstotal = 0
        # the eval function has 4 parts (in order of priority)

        # centrality: how close a piece is to the center of the board
        distancefromcenter = int(math.sqrt(int(abs(4.5-int(giveny)))**2 + int(abs(4.5-int(givenx)))**2)) # pythagoras to work out the distance the move is from the center
        # anything in the central 4 squares returns 0, and the values can only be integers so there wont be any problems of int() truncating floats
        if difficulty != 2:
            pointstotal += (20-(4*distancefromcenter)) # using 20 - 4*value gives a range of values to emphasise the importance of centrality when making a move, rewarding central pieces more
        else: # on medium value centrality less
            pointstotal += (10-(2*distancefromcenter))

        # concentration: how close all the pieces are relative to each other
        # taking the average x coord and avg y coord of the pieces then doing the same calc as above but with the avg instead of 4.5
        ycoordlist = []
        xcoordlist = []
        for i, y in enumerate(board):
            for j, x in enumerate(y):
                if x == currentturn: # record the positions of the pieces of the current turn, giving a list of the coords
                    ycoordlist.append(i+1)
                    xcoordlist.append(j+1)
        avgx = sum(xcoordlist)/len(xcoordlist)
        avgy = sum(ycoordlist)/len(ycoordlist) 
        distancefromaverage = int(math.sqrt(int(abs(int(avgy)-int(giveny)))**2 + int(abs(int(avgx)-int(givenx)))**2))
        if difficulty != 2:
            pointstotal += (9-distancefromaverage) # 9 - distance from average max value is 9-9 from corner to corner
        else: # on medium, value concetration more
            pointstotal += (27-3*distancefromaverage)

        # connectedness
        # is a piece connnected + how many
        numberofconnected = 0
        try:
            if self.graph[int(giveny)-1][int(givenx)-1] == self.currentturn: numberofconnected += 1.5
        except:
            pass
        try:
            if self.graph[int(giveny)-1][int(givenx)] == self.currentturn: numberofconnected += 1.5
        except:
            pass
        try:
            if self.graph[int(giveny)-1][int(givenx)+1] == self.currentturn: numberofconnected += 1.5
        except:
            pass

        try:
            if self.graph[int(giveny)][int(givenx)-1] == self.currentturn: numberofconnected += 1.5
        except:
            pass
        try:
            if self.graph[int(giveny)][int(givenx)+1] == self.currentturn: numberofconnected += 1.5
        except:
            pass

        try:
            if self.graph[int(giveny)+1][int(givenx)-1] == self.currentturn: numberofconnected += 1.5
        except:
            pass
        try:
            if self.graph[int(giveny)+1][int(givenx)] == self.currentturn: numberofconnected += 1.5
        except:
            pass
        try:
            if self.graph[int(giveny)+1][int(givenx)+1] == self.currentturn: numberofconnected += 1.5
        except:
            pass
        pointstotal += numberofconnected

        # uniformity
        # find the representitive rectangle of the pieces and assign a value depending on how small it is
        # because concetration needs a list of every coord, use the max and min of that and find the area
        lowestx = min(xcoordlist)
        lowesty = min(ycoordlist)
        highestx = max(xcoordlist)
        highesty = max(ycoordlist)
        distributionarea = (highesty-lowesty)*(highestx-lowestx)
        if difficulty != 2: # medium doesnt have this
            pointstotal += distributionarea/10 # distro area / 4. a typical area of a mid game board is about 16, so divide by 4 for a reasonable number

        if difficulty == 1: # if set to easy the evaluation is random
            pointstotal = random.randint(1, 30)
        return pointstotal

    def swapmaximisingplayer(self, player):
        if player == 'w':
            return 'b'
        else:
            return 'w'

    def savegamestate(self, graph): # save the current gamestate so it can be wound back to when trying different turns
        boardstack.push(np.copy(graph))

    def undoonemove(self): # wind back one move as recursion moves up
        oldboard = boardstack.pop()
        self.graph = oldboard

    def minimax(self, currentdepth, maxdepth, maximisingplayer, alpha, beta, difficulty):
        # check if game is over
        winner = Game.checkforwin(True, self.graph)
        if winner == self.currentturn:
            # print("??? BLUE WIN SCENARIO ???")
            return 10000 # return 10000 for a winning move
        elif winner == self.swapmaximisingplayer(self.currentturn):
            # print("!!! RED WIN SCENARIO !!!")
            if difficulty == 1:
                return -15 # on easy 50% chance to block your win
            return -10000 # return -10000 if the opponent is going to win
        # check if max recursion depth
        elif currentdepth == maxdepth:
            return self.evaluate(self.graph, self.movetomake[:1], self.movetomake[-1:], maximisingplayer, self.piecemovedfrom[:1], self.piecemovedfrom[-1:], currentdepth, difficulty)
            # return evaluation score
        else:
            # 1. generate moves
            graphaicoords = []
            allmoves = []
            movesmatchedtoorigin = []
            for i, y in enumerate(self.graph): # generate a list of pieces owned by the player
                for j, x in enumerate(y):
                    if x == maximisingplayer:
                        graphaicoords.append(str(i+1)+':'+str(j+1))
            for pieceno, piece in enumerate(graphaicoords): # for each piece owned, return its possible moves
                possiblemoves = Game.calclegalmoves((str(piece[:1])+str(piece[-1:])), True, self.graph, maximisingplayer, difficulty)
                for moveno, move in enumerate(possiblemoves):
                    if move != '/':
                        allmoves.append(move) # add the moves to the big list of all moves
                        movesmatchedtoorigin.append(piece) # add the piece of origin to another list as many times as there are moves for it
                        # so we can find the starting location of move[n] with movesmatchedtooorigin[n]

            # 2. set best scores for the current layer of recursion
            if maximisingplayer == self.currentturn:
                bestscore = -math.inf # negative inf because finding high scores
            else:
                bestscore = math.inf # pos inf to find lowest scores

            # 3. for move in moves, make move
            for moveno, move in enumerate(allmoves):
                self.treesize+=1
                # save the gamestate so it can be rolled back to after each iteration of move
                self.savegamestate(self.graph)

                # make the move
                self.graph = Game.makemove(movesmatchedtoorigin[moveno], move, True, self.graph, maximisingplayer)
                self.movetomake = move # assign these values so they can be used by evaluation function if at max depth
                self.piecemovedfrom = movesmatchedtoorigin[moveno]

                # 4. recurse minimax
                score = self.minimax(currentdepth+1, maxdepth, self.swapmaximisingplayer(maximisingplayer), alpha, beta, difficulty) # increase depth by 1, swap player and pass through alpha and beta values
                # 5. rollback graph by one after the recursion of this move is done, ready for the next move iteration
                self.undoonemove()
                
                # 6. if minimax finishes on ai turn, check for a higher score, or if it finishes on the enemy turn check for a lower score
                # when the score is returned from reaching max depth or a game over it compares it with other score
                # so once the iteration is finished on the layer, the best score for that layer is found, which is returned as the score of the layer up's iteration
                # then those iterations continue until the best score of those are found
                # this continues until it reaches the depth 0 layer of recursion where the move with the best is found and returned to gui
                if maximisingplayer == self.currentturn:
                    if score > bestscore: 
                        bestscore = score
                        if currentdepth == 0: # returned to the top of the recursion stack and finishing the first function call
                            self.bestmove = move
                            self.startingcoord = movesmatchedtoorigin[moveno] # set these so gui.py can execute the final move chosen
                            self.listofmovesfrom = allmoves
                    alpha = max(alpha, bestscore) # set alpha as the highest value
                else: # (minimising)
                    if score < bestscore: 
                        bestscore = score
                        if currentdepth == 0:
                            self.bestmove = move
                            self.startingcoord = movesmatchedtoorigin[moveno]
                            self.listofmovesfrom = allmoves
                    beta = min(beta, bestscore) # set beta
                if beta <= alpha: # the rest of the tree deemed not worth exploring
                    break

        return bestscore # return the final score, gui.py acccesses the move from the object variables
import numpy as np

# main game logic + variables
class Game():
    def __init__(self):
        self.board = np.array([ # numpy array storing the gamestate board (at gamestart)
        ['0', 'w', 'w', 'w', 'w', 'w', 'w', '0'],
        ['b', '0', '0', '0', '0', '0', '0', 'b'],
        ['b', '0', '0', '0', '0', '0', '0', 'b'],
        ['b', '0', '0', '0', '0', '0', '0', 'b'],
        ['b', '0', '0', '0', '0', '0', '0', 'b'],
        ['b', '0', '0', '0', '0', '0', '0', 'b'],
        ['b', '0', '0', '0', '0', '0', '0', 'b'],
        ['0', 'w', 'w', 'w', 'w', 'w', 'w', '0']
        ]) # uses the default starting positions 
        self.currentturn = 'w' # initial player
        self.playerschart = { # to get who the opponenent is for a given turn
            'w':'b',
            'b':'w'
        }
        
    def resetboard(self):
        # reset the board and starting player to be ready for a new game
        self.board = np.array([ # numpy array storing the gamestate board (at gamestart)
        ['0', 'w', 'w', 'w', 'w', 'w', 'w', '0'],
        ['b', '0', '0', '0', '0', '0', '0', 'b'],
        ['b', '0', '0', '0', '0', '0', '0', 'b'],
        ['b', '0', '0', '0', '0', '0', '0', 'b'],
        ['b', '0', '0', '0', '0', '0', '0', 'b'],
        ['b', '0', '0', '0', '0', '0', '0', 'b'],
        ['b', '0', '0', '0', '0', '0', '0', 'b'],
        ['0', 'w', 'w', 'w', 'w', 'w', 'w', '0']
        ]) # uses the default starting positions 
        self.currentturn = 'w'

    def makemove(self, startingcoord, targetcoord, isexternal=None, graph=None, externalturn=None):
        # function to make a move given what piece and where to
        # the isexternal arguement is used in minimax calculations in order to return a board for the minimax to use instead of editing the 
        # actual board, and use a board given as an arguement instead of the actual board.

        if isexternal:
            board=graph

        # split up coordinates for use from input:
        startingy = int(startingcoord[:1])-1
        startingx = int(startingcoord[-1:])-1
        targety = int(targetcoord[:1])-1
        targetx = int(targetcoord[-1:])-1 # doesnt matter if the coord are given like 32 or 3:2 since it slices into the first and 
        # last character of the input

        # make changes:
        if isexternal == None: # makes the changes on the actual board
            self.board[startingy][startingx] = '0' # set old square to empty
            self.board[targety][targetx] = self.currentturn # occupy new square with current piece
        else: # makes the changes on a copy of the board then returns it
            board[startingy][startingx] = '0' # set old square to empty
            board[targety][targetx] = externalturn # occupy new square with current piece
            return board
    
    def isoccupied(self, ycoord, xcoord): # checks if location in board is occupied by friendly piece (allow going into an enemy occupied square)
        if self.board[ycoord][xcoord] == self.playerschart[self.currentturn] or self.board[ycoord][xcoord] == '0': # allow going into blank 
            # or opposing squares
            # opposing or empty space
            return True
        else:
            # not opposing or empty space
            return False

    def convtoboardcoords(self, validcoords): # changing any coordinates in the form 01 (array format) into 1:2 (board format)
        newcoords = []
        for x in validcoords:
            if x == '/':
                newcoords.append('/')
            else: 
                x1 = int(x[:1])
                x2 = int(x[-1:])
                new = str(x1+1)+':'+str(x2+1)
                newcoords.append(new)
        return newcoords


    def isvalid(self, coord, startingcoord, movetype, currentturn, board, difficulty): # used when finding legal moves from a position, this function finds 
        # if the location for a certain axis is legal
        # - in the bounds of the board
        # - not moving onto itself
        # - not blocked by an enemy piece on its path
        # if all of these are true then the move is legal
        ycoord = int(coord.split(':')[0])
        xcoord = int(coord.split(':')[1]) # get the x and y coords of the target
        startingycoord = int(startingcoord[:1])
        startingxcoord = int(startingcoord[1:]) # x and y coords of the origin piece
        if difficulty == 4:
            board = self.board # if set to cheating then let it use the wrong board when checking for legal moves
            # resulting in the ai being able to pass through opposing pieces

        # out of bounds
        if ycoord < 0 or ycoord > 7 or xcoord < 0 or xcoord > 7:
            return False

        # moving onto itself
        if coord == startingcoord:
            return False

        # blocked by an enemy piece
        # sees where the piece should go, then backtrack the line until its original point, and check if any of those squares have an
        # enemy piece
        if movetype == 'vertup': # this is actually vertdown (vertical axis, below the piece)
            line = [] # empty list for the line of pieces in the axis
            for row in board[startingycoord:ycoord]: # add the pieces of that line into the list
                line.append(row[xcoord])
            if self.playerschart[currentturn] in line: # if any opposing pieces found in that line, it is invalid
                return False
            else:
                if self.isoccupied(ycoord, xcoord) == False: # checks if there is a friendly piece in the final location
                    return False # cant move onto a friendly piece, return false
                else:
                    return True # otherwise the move is valid, return True
        elif movetype == 'vertdown': # and this is doing vertup (vertical axis, above the piece)
            line = []
            for row in board[ycoord+1:startingycoord+1]:  # add one to both to offset the line into the correct position in order for the
                # target not to be inside the line so it doesnt get flagged as jumping over an enemy piece
                line.append(row[xcoord])
            if self.playerschart[currentturn] in line:
                return False
            else:
                if self.isoccupied(ycoord, xcoord) == False:
                    return False
                else:
                    return True
        elif movetype == 'horiright': # horizontal axis, to the right of the piece
            line = board[ycoord][startingxcoord:xcoord]
            if self.playerschart[currentturn] in line:
                return False
            else:
                if self.isoccupied(ycoord, xcoord) == False:
                    return False
                else:
                    return True
        elif movetype == 'horileft': # horizontal axis, to the left of the piece
            line = board[ycoord][xcoord+1:startingxcoord+1] # add one to both to offset the line into the correct position in order for 
            # the target not to be inside the line so it doesnt get flagged as jumping over an enemy piece
            if self.playerschart[currentturn] in line:
                return False
            else:
                if self.isoccupied(ycoord, xcoord) == False: # all the same checking logic as the first 3
                    return False
                else:
                    return True
        elif movetype == 'tLbRright': # checking for diagonals that start in the top left down to bottom right, and going right from the 
            # starting piece
            tLbRoffset = startingxcoord-startingycoord # the offset is how far down or up (see diagram) the line is from the central 
            # (longest) diagonal
            tLbRdiagonal = board.diagonal(tLbRoffset).tolist() # generates a single list of the full diagonal
            line = tLbRdiagonal[(startingycoord-abs(tLbRoffset))+1:(ycoord-abs(tLbRoffset))+1] # selects the corresponding side of the diagonal
            if self.playerschart[currentturn] in line:
                return False
            else:
                if self.isoccupied(ycoord, xcoord) == False:
                    return False
                else:
                    return True
        elif movetype == 'tLbRleft': # checking for diagonals that start in the top left down to bottom right, and going from left of the 
            # starting piece
            tLbRoffset = startingxcoord-startingycoord
            tLbRdiagonal = board.diagonal(tLbRoffset).tolist()
            line = tLbRdiagonal[(ycoord-abs(tLbRoffset))+1:(startingycoord-abs(tLbRoffset))+1] # finding the diagonal line by offet from the
            # central line, then taking the pieces to the left of the starting piece
            if self.playerschart[currentturn] in line:
                return False
            else:
                if self.isoccupied(ycoord, xcoord) == False:
                    return False
                else:
                    return True
        elif movetype == 'tRbLright': # checking for diagonals that start in the top right down to bottom left, and going from right of the
            # starting piece
            tRbLoffset = startingxcoord-(7-startingycoord) # the offset is reversed as the diagonal moves in the opposite direction
            tRbLdiagonal = board[::-1].diagonal(tRbLoffset).tolist() # the board is reversed([::-1]) in order to get the correct 
            # diagonal and the diagonal is turned into the list
            line = tRbLdiagonal[(startingxcoord-abs(tRbLoffset))+1:(xcoord-abs(tRbLoffset))+1] # taking the pieces from the right of the
            # starting piece
            if self.playerschart[currentturn] in line:
                return False
            else:
                if self.isoccupied(ycoord, xcoord) == False:
                    return False
                else:
                    return True
        elif movetype == 'tRbLleft': # top right bottom left diagonal, taking the pieces left of the starting piece
            tRbLoffset = startingxcoord-(7-startingycoord)
            tRbLdiagonal = board[::-1].diagonal(tRbLoffset).tolist()
            line = tRbLdiagonal[(xcoord)+1:(startingxcoord)+1] # generate line with leftward pieces
            if self.playerschart[currentturn] in line:
                return False
            else:
                if self.isoccupied(ycoord, xcoord) == False:
                    return False
                else:
                    return True

    def calclegalmoves(self, startingcoord, isexternal=None, graph=None, externalcurrentturn=None, difficulty=None): # find the legal moves for a given piece
        if isexternal:
            board = graph
            currentturn = externalcurrentturn # is external flag used in order to import its own graph and turn from the minimax
            # calculations instead of the actual game graph
            difficulty = difficulty # get the difficulty so it can cheat if set to cheating
        else:
            board = self.board # otherwise use the real game board and turn
            currentturn = self.currentturn
            difficulty = 0
        startingy = int(startingcoord[:1])-1 # split up starting piece locations
        startingx = int(startingcoord[-1:])-1
        starting = str(startingy)+str(startingx)
        vertpieces = 0
        horipieces = 0
        tLbRdiapieces = 0
        tRbLdiapieces = 0 # counters for number of pieces in each axis

        # find number of vertical pieces
        for row in board:
            if row[startingx] != '0': vertpieces += 1

        # find number of horizontal pieces
        for piece in board[startingy]:
            if piece != '0': horipieces += 1

        # find number of tLbR diagonal pieces
        tLbRoffset = startingx-startingy
        tLbRdiagonal = board.diagonal(tLbRoffset).tolist() # uses the numpy diagonal method to get the diagonal given an offset from
        # the centre diagonal and since .diagonal returns a numpy array use .tolist to turn it into a normal list
        for piece in tLbRdiagonal:
            if piece != '0': tLbRdiapieces += 1

        # find number of tRbL diagonal pieces
        tRbLoffset = startingx-(7-startingy)
        tRbLdiagonal = board[::-1].diagonal(tRbLoffset).tolist() # a[::-1] uses the reversed matrix to get the opposite diagonal
        for piece in tRbLdiagonal:
            if piece != '0': tRbLdiapieces += 1
        
        # after getting pieces in directions, find the move that can be made for each direction and remove the ones that get blocked
        # at most 8 moves since each direction can travel both ways
        # these are given in array coordinates
        possiblecoords = []
        validcoords = []
        vertupcoord = str(startingy+vertpieces)+':'+str(startingx)
        vertdowncoord = str(startingy-vertpieces)+':'+str(startingx)
        horirightcoord = str(startingy)+':'+str(startingx+horipieces)
        horileftcoord = str(startingy)+':'+str(startingx-horipieces)
        tLbRdiarightcoord = str(startingy+tLbRdiapieces)+':'+str(startingx+tLbRdiapieces)
        tLbRdialeftcoord = str(startingy-tLbRdiapieces)+':'+str(startingx-tLbRdiapieces)
        tRbLdiarightcoord = str(startingy-tRbLdiapieces)+':'+str(startingx+tRbLdiapieces)
        tRbLdialeftcoord = str(startingy+tRbLdiapieces)+':'+str(startingx-tRbLdiapieces)
        possiblecoords.extend((vertupcoord, vertdowncoord, horirightcoord, horileftcoord, tLbRdiarightcoord, tLbRdialeftcoord, tRbLdiarightcoord, tRbLdialeftcoord))
        # making a list of moves for all 8 directions, without considering legality
        # then must remove illegal pieces
        movetypes = ['vertup', 'vertdown', 'horiright', 'horileft', 'tLbRright', 'tLbRleft', 'tRbLright', 'tRbLleft']
        for count, coord in enumerate(possiblecoords): # iterate through each possible coord, and call isvalid to check if that move is
            # legal, using the movetypes list to correspond to what check it needs to do
            if self.isvalid(coord, starting, movetypes[count], currentturn, board, difficulty) == False: # verify each move to check if legal
                validcoords.append('/')
            else:
                validcoords.append(coord)
        # valid coord returns the coords in array format so should convert them before displaying. converting:
        validcoords = self.convtoboardcoords(validcoords)
        return validcoords

    def dfs(self, graph, row, col, x, y): # depth first search used when checking if the game is over.
        if graph[x][y] == '0': # if the graph at the given coord is 0 the algorithm is finished
            return
        graph[x][y] = '0' # make the node 0 to prevent double counting if it is revisited

        # orthogonal (straight edges)
        if x != 0: # as long as we arent at the leftmost, recursivly do the next dfs left
            self.dfs(graph, row, col, x-1, y) # the dfs is recursivly called again to keep exploring the path until it finds a zero, then
            # it is brought back up
        if x != row-1: # as long as we arent at the end, dfs right
            self.dfs(graph, row, col, x+1, y)
        if y != 0: # not at the top, go up
            self.dfs(graph, row, col, x, y-1)
        if y != col-1: # down
            self.dfs(graph, row, col, x, y+1)
        # diagonal edges
        if x != 0 and y != 0: # not top left, go up and left
            self.dfs(graph, row, col, x-1, y-1)
        if x != row-1 and y != 0: # not top right, go up and right
            self.dfs(graph, row, col, x+1, y-1)
        if x != 0 and y != col-1: # not bottom left, go down and left
            self.dfs(graph, row, col, x-1, y+1)
        if x != row-1 and y != col-1: # not bottom right, go down and right
            self.dfs(graph, row, col, x+1, y+1)
        # this algorithm is finding all connections from a starting node

    def numIslands(self, graph, colour): # checking for the number of 'islands' to see if a player has won by connecting all
        # their pieces (therefore having one island of pieces instead of multiple)
        row = len(graph)
        col = len(graph[0]) # get the length of the board size
        count=0

        for i in range(row):
            for j in range(col): # for each tile,
                if graph[i][j] == colour: # if a piece is for the given turn, peform dfs which will search through the graph and replace 
                    # each visited item with '0'
                    self.dfs(graph, row, col, i, j) # starting from a valid point, itll go through with dfs until the recursion ends, then 
                    # increments island count by 1
                    count+=1
        return count # if the dfs searches the first piece which is connected to all other friendly pieces, since they have all been
        # replaced by 0s count will not be incremented again since all the pieces were a part of one island and have now been searched
        # therefore the game has been won as there is only one island
    
    def checkforwin(self, isexternal=None, importboard=None): # handler function to check for win
        # call the numislands for each colour and declare a winner and tiebreak if needed
        if isexternal:
            graph = importboard # can import a different graph if being used in minimax calculations
        else:
            graph = self.board
        graphb = [] # generate seperate graphs that only contain the pieces of relevant colour
        for y in graph:
            templine = []
            for x in y:
                if x == 'b':
                    templine.append('b')
                else:
                    templine.append('0')
            graphb.append(templine) # only black pieces
        graphw = []
        for y in graph:
            templine = []
            for x in y:
                if x == 'w':
                    templine.append('w')
                else:
                    templine.append('0')
            graphw.append(templine) # only white pieces
        numIslandsb = self.numIslands(graphb, 'b') # find the number of islands for each colour
        numIslandsw = self.numIslands(graphw, 'w')
        #print(f'B: {numIslandsb}, W: {numIslandsw}')
        if numIslandsb == 1 and numIslandsw == 1: # if they both won on the same turn, the winner is whoever made the move
            winner = self.playerschart[self.currentturn] # the opposite turn is returned as the current turn is swapped, then the game is checked if finished
            # this doesnt need to be done for the standard win scenarios as it is based off who has one island
        elif numIslandsb == 1: # otherwise the winner is whoever has only one island
            winner = 'b'
        elif numIslandsw == 1:
            winner = 'w'
        else: # or if no one has won yet, the winner is None
            winner = None
        return winner

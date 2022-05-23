import sys
import winsound
import random

Empty = ' '
Bot   = 'X'
Human = 'O'

WINCOUNT = 4

class Board:
    def __init__(self):
        self.size = 5 # board is size 5x5
        self.line = [Empty for _ in range(self.size**2)] # 1D
        self.square = [list(Empty * self.size) for _ in range(self.size)] # 2D
        
    def isEmptyLine(self, x): # checks if x is empty for 1D
        if self.line[x] == Empty:
            return True
        else:
            return False

    def isEmptySquare(self, x,y): # checks if [x,y] is empty for 2D
        if self.square[x][y] == Empty:
            return True
        else:
            return False
 
    def printBoard(self): # prints play board
        print("")
        string = ''
        for i in range(5):
            string +=  ' | ' +  str(i) 
        print(string + ' | ')    
        i=0
        for row in [self.line[i*5:(i+1) * 5] for i in range(5)]:
            print( str(i) +'| ' + ' | '.join(row) + ' |')
            i += 1
        print("")

    def convert1d_2d(self, number): # from 1D to 2D
        [x, y] = divmod(number, 5)
        return x, y

    def convert2d_1d(self, x, y):  # from 2D to 1D
        number = x*5 + y
        return number

    def Board2D(self): # 1D array to 2D array
        for i in range(0, self.size**2):
            [x, y] = self.convert1d_2d(i)
            self.square[x][y] = self.line[i]

        return self.square

    def numberEmptySpaces(self):
        n = 0
        for x in range(self.size * self.size):
            if self.line[x] == Empty:
                n += 1
        return n

    def getRow(self, numberOfRow): # returns row value from 2D
        return self.square[numberOfRow]

    def getColumn(self, numberOFColumn): # returns column value from 2D
        return [row[numberOFColumn] for row in self.square]

    def getMainDiagonal(self): # returns 2 main diagonals (5 elements)
        diagonal1 = [self.square[i][i] for i in range(self.size)]
        diagonal2 = []
        j = 0
        for i in reversed(range(self.size)):
            diagonal2.append(self.square[i][j])
            j += 1
        return diagonal1, diagonal2

    def getOtherDiagonal(self): # returns 4 secondary diagonals (4 elements)
        diagonal1 = [self.line[i] for i in [5, 11, 17, 23]]
        diagonal2 = [self.line[i] for i in [1,  7, 13, 19]]
        diagonal3 = [self.line[i] for i in [3,  7, 11, 15]]
        diagonal4 = [self.line[i] for i in [9, 13, 17, 21]]

        return diagonal1, diagonal2, diagonal3, diagonal4

    def calculateLine(self, line): #counts how many bot/human/empty elements are in a line
        botSum   = line.count(Bot)
        humanSum = line.count(Human)
        emptySum = line.count(Empty)
        return botSum, humanSum, emptySum

    def getScoreLine4_5imp(self, line): # heurestic function
        score = 0
        botSum, humSum, emptySum = self.calculateLine(line)
        #Score for Bot
        if botSum >= 4 and (line[0] == Bot or line[self.size-1] == Bot): # Bot wins
            score += 20 ** botSum
        elif humSum == 0 and botSum != 0: # Human "almost" wins
            score += 20 ** botSum
        elif humSum == 1 and (line[0] == Human or line[self.size-1] == Human): # Bot near to win
            score += 8 ** botSum
        else: # Bot is in line without being near to winning
            score += 2 ** botSum

        # Score for Human
        if humSum >= 4 and (line[0] == Human or line[self.size - 1] == Human):  # Human wins
            score -= 20 ** humSum
        elif botSum == 0 and humSum != 0:  # Human "almost" wins
            score -= 20 ** humSum
        elif botSum == 1 and (line[0] == Bot or line[self.size - 1] == Bot):  # Human near to win
            score -= 8 ** humSum
        else:  # Human is in line without being near to winning
            score -= 2 ** humSum
        return score

    def getScoreLine4_4imp(self, line): # heurestic function
        score = 0
        botSum, humSum, emptySum = self.calculateLine(line)
        if humSum == 0 and botSum == self.size-1: # Bot wins
            score += 20 ** botSum
        elif humSum == 0 and botSum >= self.size-2: # Bot wins
            score += 10 ** botSum
        else:
            pass
        if botSum == 0 and humSum == self.size - 1:  # Human wins
            score -= 20 ** humSum
        else:
            pass
        return score

    def evaluate(self):
        score = 0
        for i in range(self.size): # estimate the score for bot/human for row and column
            score += self.getScoreLine4_5imp(self.getRow(i))
            score += self.getScoreLine4_5imp(self.getColumn(i))

        mainDiagonals = self.getMainDiagonal() # estimate the score for bot/human for main diag
        for i in range(2):
            score += self.getScoreLine4_5imp(mainDiagonals[i])
        
        otherDiagonals = self.getOtherDiagonal() # estimate the score for bot/human for second. diag
        for i in range(4):
            score += self.getScoreLine4_4imp(otherDiagonals[i])

        return score


class SmartPlayer:

    def __init__(self):
        self.player = Empty
        self.depth = 5 # max depth for minimax

    def turn(self, game): # bot turn
        if len(game.availableMoves()) == game.size**2:
            bestpos = random.choice(game.availableMoves()) # first place is random
        else:
            score, bestpos = self.minimax_ab(game, self.depth, Bot, -1000000, 1000000) # bot is always the max player
        return bestpos       
              
    def minimax_ab(self, gamestate, depth, player, alpha, beta):

        score = gamestate.evaluate() # gets the score from the actual board
        position = None
   
        max_player = Bot  # yourself
        if player == Bot:
            other_player = Human
        else:    
            other_player = Bot

        gameResult = game.CheckWin4() #checks if there is a winner
        if gameResult == Human:
           return -20**(gamestate.size-1)-gamestate.numberEmptySpaces()*gamestate.size, position
        elif gameResult == Bot:
            return 20**(gamestate.size-1)+gamestate.numberEmptySpaces()*gamestate.size, position
        elif gamestate.checkFullBoard():
            return 0, position

        if depth == 0: # if minimax reaches depth limit -> returns the score
            return score, position

        if player == max_player:
            for i in gamestate.availableMoves():
                gamestate.makeMove(i, player)
                score, dummy = self.minimax_ab(gamestate, depth-1, other_player, alpha, beta)
                if score > alpha:
                    alpha = score
                    position = i
  
                # undo move
                gamestate.line[i] = Empty
                gamestate.current_winner = None

                if beta <= alpha:
                   break

            return alpha, position
        else:
            for i in gamestate.availableMoves():
                gamestate.makeMove(i, player)
                score, dummy = self.minimax_ab(gamestate, depth-1, other_player, alpha, beta)
                if score < beta:
                    beta = score
                    position = i

                gamestate.line[i] = Empty
                gamestate.current_winner = None
                if alpha >= beta:
                    break

            return beta, position

class Player:
    def __init__(self):
        self.player = Human

    def turn(self, gamestate):
        
        x = int(input("Row position for    'O': "))
        y = int(input("Column position for 'O': "))
        if x in range (5) and y in range(5):
            number = gamestate.convert2d_1d(x, y)
            return number
        else:
            return None    


class TicTacToe(Board):
    current_winner = Empty

    def __init__(self):
       super().__init__()

    def setPlayer(self, _player):
        self.player = _player

    def startGame(self):
        print("Welcome to TicTacToe game!")
        print("Bot:    "+Bot)
        print("Player: "+Human)
        result = random.choice([1, 2]) #first turn is random
        if result == 1:
            self.player = Bot # bot has the first move
        else:
            self.player = Human # bot has the first move
       
    def checkFullBoard(self):
        for x in range(0, self.size**2):
                if self.isEmptyLine(x):
                    return False
        return True

    def CheckWin4(self): # checks for 4 same elements
        self.Board2D() # fill the square with line values
        mark = Empty
        
        #ROWS
        x = 0
        for x in range(self.size):
            if not self.isEmptySquare(x, 2):
                if (self.square[x][1] == self.square[x][2] == self.square[x][3]) and ((self.square[x][0] == self.square[x][1]) or (self.square[x][3] == self.square[x][4])):
                   mark = self.square[x][2]
                   break
        
        if mark == Empty:
            #COLUMNS
            y = 0
            for y in range(self.size):
                if not self.isEmptySquare(2, y):
                    if (self.square[1][y] == self.square[2][y] == self.square[3][y]) and ((self.square[0][y] == self.square[1][y]) or (self.square[3][y] == self.square[4][y])):
                        mark = self.square[2][y]
                        break
        
        if mark == Empty:
            #LIL DIAGONALS 1
            if not self.isEmptySquare(1, 0):
                if self.square[1][0] == self.square[2][1] == self.square[3][2] == self.square[4][3]:
                    mark = self.square[2][1]
        if mark == Empty:
            if not self.isEmptySquare(0, 1):
                if self.square[0][1] == self.square[1][2] == self.square[2][3] == self.square[3][4]:
                   mark = self.square[0][1]
        
        if mark == Empty:   
            #LIL DIAGONALS 2
            if not self.isEmptySquare(0, 3):
                if self.square[0][3] == self.square[1][2] == self.square[2][1] == self.square[3][0]:
                    mark = self.square[0][3]
        if mark == Empty:
            if not self.isEmptySquare(1, 4):
               if self.square[1][4] == self.square[2][3] == self.square[3][2] == self.square[4][1]:
                   mark = self.square[1][4]
        
        if mark == Empty:
            #BIG DIAGONALS
            if not self.isEmptySquare(2, 2):
                if (self.square[1][1] == self.square[2][2] == self.square[3][3]) and ((self.square[0][0] == self.square[1][1]) or (self.square[3][3] == self.square[4][4])):
                    mark = self.square[2][2]
        if mark == Empty:    
            if not self.isEmptySquare(2, 2):
               if (self.square[1][3] == self.square[2][2] == self.square[3][1]) and ((self.square[0][4] == self.square[1][3]) or (self.square[3][1] == self.square[4][0])):
                   mark = self.square[2][2]
        
        return mark

    def availableMoves(self):
        return [i for i, x in enumerate(self.line) if x == Empty]

    def makeMove(self, x, player):
        if self.isEmptyLine(x):
            self.line[x] = player
            self.current_winner = self.CheckWin4()
            return True
        return False

    def gameOver(self):
        winner = self.CheckWin4()

        if winner == Empty: #no win yet
            if self.checkFullBoard():
                print("Game Over")
                print("DRAW")
            else:
                return False
        else:
            print("Game Over")
            print("WON: ", winner)
            self.printBoard()

        return True
 

    def changePlayer(self): # changing players
        if (self.player == Bot):
            self.player = Human
        else:
            self.player = Bot


if __name__  ==  "__main__":

    game=TicTacToe()
    human=Player() 
    bot=SmartPlayer() 

    game.startGame()
    game.printBoard()
    
    while not game.gameOver():
        print(game.player + "->Turn:")
        if game.player == Human:
            resultMove = human.turn(game)
        else:
            resultMove = bot.turn(game)
            winsound.Beep(440, 500)
            if resultMove == None:  # error state, returns first available position
                possible_moves = game.availableMoves()
                resultMove = possible_moves[0]
    
        if resultMove == None:
            print('Turn error  - next Turn ') 
        else:           
            if game.makeMove(resultMove, game.player):
                game.printBoard()  # print result
                game.changePlayer()  # switches player
            else:
                print('Next Turn>')


# -*- coding: utf-8 -*-
	
import copy

class ConnectFour:
    def __init__(self):
        # Alustetaan liikkeiden määrä nollaan (42 liikkeen jälkeen lauta on täynnä) ja kenen vuoro on algoritmissa
        self.moves = 0
        self.turn = 0

    def PrintGameBoard(self, board):
        # Tämä funktio piirtää pelilaudan
        print('  0   1   2   3   4   5   6')
        for i in range(5, -1, -1):
            print('|---|---|---|---|---|---|---|')
            print("| ",end="")
            for j in range(7):
                print(board[i][j],end="")
                if j != 6:
                    print(" | ",end="")
                else:
                    print(" |")
        print('`---------------------------´')

    def LegalRow(self, col, board):
        # Tämä funktio tarkistaa sarakkeella jo olevien merkkien määrän ja palauttaa mille riville uusi merkki menee. Jos sarake on täynnä funktio palauttaa arvon -1
        stacks = [[x[i] for x in board] for i in range(len(board[0]))]
        countofitems = stacks[col].count("x") + stacks[col].count("o")
        if (countofitems) < 6:
            return (countofitems)
        else:
            return -1
			
    def LegalMoves(self, board):
        # Tämä funktio palauttaa lailliset siirrot listassa tietyssä järjestyksessä
        legalmoves = []
        stacks = [[x[i] for x in board] for i in range(len(board[0]))] 
        order = [3,2,4,1,5,0,6]
        for i in order:
            if self.LegalRow(i, board)!=-1:
                legalmoves.append(i)
        return legalmoves

    def MakeMove(self, board, col, player, row):
        # Tämä funktio tekee siirron ja kasvattaa tehtyjen siirtojen lukumäärää yhdellä
        board[row][col] = player
        self.moves += 1
        return board
		
    def UnmakeMove(self, board, col, row):
        # Tämä funktio korvaa aiemmin tehdyn siirron tyhjällä ja pienentää tehtyjen siirtojen lukumäärää yhdellä
        board[row][col] = " "
        self.moves -= 1
        return board

    def IsWinning(self, currentplayer, board):
        # Tämä funktio tarkistaa onko pelilaudalla vuorossa olevalla pelaajalla neljä perättäistä merkkiä peräkkäin
        for i in range(6):
            for j in range(4):
                if board[i][j] == currentplayer and board[i][j+1] == currentplayer and board[i][j+2] == currentplayer and board[i][j+3] == currentplayer:
                    return True
        for i in range(3):
            for j in range(7):
                if board[i][j] == currentplayer and board[i+1][j] == currentplayer and board[i+2][j] == currentplayer and board[i+3][j] == currentplayer:
                    return True     
        for i in range(3):
            for j in range(4):
                if board[i][j] == currentplayer and board[i+1][j+1] == currentplayer and board[i+2][j+2] == currentplayer and board[i+3][j+3] == currentplayer:
                    return True
        for i in range(3,6):
            for j in range(4):
                if board[i][j] == currentplayer and board[i-1][j+1] == currentplayer and board[i-2][j+2] == currentplayer and board[i-3][j+3] == currentplayer:
                    return True
        return False
		               
    def PlayerMove(self, board, player):
        # Tämä funktio pyytää pelaajan tekevän liikkeen ja palauttaa uuden pelilaudan tehdyn liikkeen jälkeen
        allowedmove = False
        while not allowedmove:
            try:
                print("Choose a column where you want to make your move (0-6): ",end="")
                col =input()
                col=int(col)
                row = self.LegalRow(col, board)
            except (NameError, ValueError, IndexError, TypeError, SyntaxError) as e:
                print("Give a number as an integer between 0-6!")
            else:
                if row != -1 and (col<=6 and col>=0):
                    board[row][int(col)] = player
                    self.moves += 1
                    allowedmove = True
                elif col>6 or col<0:
                    print("The range was 0-6!!!")
                else:
                    print("This column is full")
        return board
			
    def SwitchPlayer(self, player):
        # Tämä funktio vaihtaa vuoroa tarkastamalla nykyisen pelaajan merkin ja palauttamalla seuraavan pelaajan merkin
        if player=="x":
            nextplayer="o"
        else:
            nextplayer="x"
        return nextplayer
			
    def evaluation(self, board):
        # Tämä funktio laskee pelilaudalle arvion ohjeiden mukaan. 
        list = []
        player = "x"
        opponent = "o"
        if self.IsWinning(player, board):
            score = -512
        elif self.IsWinning(opponent, board):
            score = +512
        elif self.moves==42:
            score=0
        else:
            score = 0
            for i in range(6):  # Lisätään listaan vaakasuuntaiset segmentit
                for j in range(4):
                    list.append([str(board[i][j]),str(board[i][j+1]),str(board[i][j+2]),str(board[i][j+3])])
            for i in range(3): # Lisätään listaan pystysuuntaiset segmentit
                for j in range(7):
                    list.append([str(board[i][j]),str(board[i+1][j]),str(board[i+2][j]),str(board[i+3][j])])
            for i in range(3): # Lisätään listaan diagonaaliset segmentit
                for j in range(4):
                    list.append([str(board[i][j]),str(board[i+1][j+2]),str(board[i+2][j+2]),str(board[i+3][j+3])])
            for i in range(3, 6): # Lisätään listaan diagonaaliset segmentit
                for j in range(4):
                    list.append([str(board[i][j]),str(board[i-1][j+2]),str(board[i-2][j+2]),str(board[i-3][j+3])])
            for k in range(len(list)): # Pisteytetään segmentit ohjeiden mukaisesti
                if ((list[k].count(str("x"))>0) and (list[k].count(str("o"))>0)) or list[k].count(" ")==4:
                    score += 0
                if list[k].count(player)==1 and list[k].count(opponent)==0:
                    score -= 1
                if list[k].count(player)==2 and list[k].count(opponent)==0:
                    score -= 10
                if list[k].count(player)==3 and list[k].count(opponent)==0:
                    score -= 50
                if list[k].count(opponent)==1 and list[k].count(player)==0:
                    score += 1
                if list[k].count(opponent)==2 and list[k].count(player)==0:
                    score += 10
                if list[k].count(opponent)==3 and list[k].count(player)==0:
                    score += 50
            if self.turn==player:
                score -= 16
            else:
                score += 16
        return score
		      
    def alphabetapruning(self, board, depth, opponent, alpha, beta):
        #Funktion parametrit:
		#
		#self: yläluokan ConnectFour kaikki parametrit
		#board: pelilauta 6x7 matriisina
		#depth: etsintäsyvyys (älä valitse liian suurta etsintäsyvyyttä, koska laskenta saattaa kestää liian kauan)
        #opponent: vastustajan merkki
        #alpha: alphan numeroarvo
        #beta: betan numeroarvo
        #
		#Funktio palauttaa:
		#largestvalue, position: suurimman arvon, johon päästään sijoittamalla pelimerkki johonkin sarakkeista ja sarakkeen numero
        values = []
        cols = []
		#########################################################################
		#SINUN KOODISI TÄHÄN
		#########################################################################
        if self.moves != 42 or depth > 0:
            if opponent == "o":
                v = -1000000000000
                bestCol = None
                for column in self.LegalMoves(board):
                    newBoard = self.MakeMove(board,column,"x",self.LegalRow(column, board))
                    nValue, nColumn = self.alphabetapruning(newBoard, depth - 1, "x", alpha, beta)
                    newBoard = self.UnmakeMove(board,column, self.LegalRow(column, board))
                    if v < nValue:
                        v = nValue
                        bestCol = column
                    alpha = max(alpha, v)
                    if beta <= alpha:
                        break
                return v, bestCol
            else:
                v = 1000000000000
                bestCol = None
                for column in self.LegalMoves(board):
                    newBoard = self.MakeMove(board,column,"o",self.LegalRow(column, board))
                    nValue, nColumn = self.alphabetapruning(newBoard, depth - 1, "o", alpha, beta)
                    newBoard = self.UnmakeMove(board,column, self.LegalRow(column, board))
                    if v > nValue:
                        v = nValue
                        bestCol = column
                    beta = min(beta, v)
                    if beta <= alpha:
                        break
                return v, bestCol
        else:
            return self.evaluation(board), None

								
    def minimax(self, board, depth, opponent):
		#Funktion parametrit:
		#
		#self: yläluokan ConnectFour kaikki parametrit
		#board: pelilauta 6x7 matriisina
		#depth: etsintäsyvyys (älä valitse liian suurta etsintäsyvyyttä, koska laskenta saattaa kestää liian kauan)
        #opponent: vastustajan merkki
        #
		#Funktio palauttaa:
		#largestvalue, position: suurimman arvon, johon päästään sijoittamalla pelimerkki johonkin sarakkeista ja sarakkeen numero
        values = []
        cols = []
		#########################################################################
		#SINUN KOODISI TÄHÄN
		#########################################################################
        for node in self.LegalMoves(board):
            if depth == 0 or self.moves == 42:
                return self.evaluation(board), node
            
            if opponent == "x": # max
                bestValue = float('-inf')
                newBoard = self.MakeMove(board, node, "o", self.LegalRow(node, board))
                v, position = self.minimax(newBoard, depth, "o")
                if v > bestValue:
                    bestValue = v
                else:
                    position = node

            else:           # Minimizer
                bestValue = float('inf')
                newBoard = self.MakeMove(board, node, "x", self.LegalRow(node, board))
                v, position = self.minimax(newBoard, depth - 1, "x")
                if v < bestValue:
                    bestValue = v
                else:
                    position = node
            print(bestValue)
            print(position)
            return bestValue, position
					
    def searchingfunction(self, board, depth, opponent):
        # Tämä funktio kutsuu alpfabeta-pruning (tai minimax) algoritmia, jonka jälkeen päivittää pelilaudan saadulla liikkeella ja palauttaa uuden pelilaudan
        newboard = copy.deepcopy(board)
        value, position = self.alphabetapruning(newboard, depth, opponent, -1000000000, 1000000000)
        #value, position=self.minimax(newboard, depth, opponent)
        board = self.MakeMove(board, position, opponent, self.LegalRow(position, board))
        return board

def PlayerGoesFirst():
    # Tämä funktio kysyy kumpi pelaajista aloittaa. Pelaaja on X ja tietokone on O
    print("Player is X and AI is O")
    player = 'x'
    opponent = 'o'
    print('Do you want to play first? (y/n) : ',end="")
    return input().lower().startswith('y')
    
def PlayAgain():
    # Tämä funktio kysyy pelin päätyttyä pelataanko uudestaan
    print('Do you want to play again? (y/n) :',end="")
    return input().lower().startswith('y')
	
def main():
    # Pääfunktio
    print("Connect4")
    print("-"*34)
    while True:
        connectfour = ConnectFour()
        gameisgoing = True
        table  = [[],[],[],[],[],[]]
        for i in range(7):
            for j in range(6):
                table[j].append(" ")
        player = "x"
        opponent = "o"
        if PlayerGoesFirst():
            turn = "x"
        else:
            turn = "o"
        while gameisgoing:
            connectfour.PrintGameBoard(table)
            if turn=="x":
                table = connectfour.PlayerMove(table, player)
                if connectfour.IsWinning(player, table):
                    connectfour.PrintGameBoard(table)
                    print('You won the game!')
                    gameisgoing = False
                else:
                    if connectfour.moves==42:
                        connectfour.PrintGameBoard(table)
                        print('Game is tie')
                        gameisgoing=False
                    else:
                        turn = "o"
            else:
                table = connectfour.searchingfunction(table, 6, opponent)# Tällä rivillä tapahtuu AI:n liike joko minimax algoritmilla tai alphabeta-pruning algoritmilla
                if connectfour.IsWinning(opponent, table):
                    connectfour.PrintGameBoard(table)
                    print('Computer won the game')
                    gameisgoing = False
                else:
                    if connectfour.moves==42:
                        connectfour.PrintGameBoard(table)
                        print('Game is tie')
                        gameisgoing=False
                    else:
                        turn = "x"
        if not PlayAgain():
            print("Game ended")
            print("-"*34)
            break

if __name__ == '__main__':
    main()
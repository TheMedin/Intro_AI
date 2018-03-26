# -*- coding: utf-8 -*-
import random

def IsWinning(board):
    # Tämä funktio tarkistaa onko pelilaudalla 3 peräkkäistä samaa merkkiä ja palauttaa totuusarvon (True tai False).
    if ((board[6] == board[7] and board[7] == board[8] and board[6] != "-") or      # ylimmäinen vaakarivi
    (board[3] == board[4] and board[3] == board[5] and board[3] != "-") or          # keskimmäinen vaakarivi
    (board[0] == board[1] and board[0] == board[2] and board[0] != "-") or          # alimmainen vaakarivi
    (board[0] == board[3] and board[0] == board[6] and board[0] != "-") or          # vasen pystyrivi
    (board[1] == board[4] and board[1] == board[7] and board[1] != "-") or          # keskimmäinen pystyrivi
    (board[2] == board[5] and board[2] == board[8] and board[2] != "-") or          # oikea pystyrivi
    (board[2] == board[4] and board[2] == board[6] and board[2] != "-") or          # ensimmäinen diagonaali
    (board[0] == board[4] and board[0] == board[8] and board[0] != "-")):           # toinen diagonaali
        return True
    else:
        return False
	
		
def Minimax(board, maximizingplayer, player):
    #Funktion parametrit:
    #
    #board: pelilauta listana, joka sisältää 9 arvoa. Indeksi nolla viittaa vasempaan alkukulmaan ja indeksi 8 oikeaan yläkulmaan
    #maximizingplayer: kertoo funktiolle totuusarvona, onko kyseessä maksimoiva pelaaja (True) vai minimoiva pelaaja(False)
    #player: kertoo funktiolle, onko "X" vai "O" vuoro pelata merkkinsä
    #
	#Funktio palauttaa:
    #
    #bestvalue, bestmove: parhaan arvon ja liikkeen, jolla paras arvo saavutettiin
    if len(set(board)) == 1:      # Pelaa aluksi keskelle, jos tietokone saa aloittaa. (Optimaalisin vaihtoehto, kun pelilauta on tyhjä)
        return 0,4           
    if player=="O":               # Tallennetaan seuraavan pelaajan merkin arvo muuttujaan nextplayer
        nextplayer="X"
    else:
        nextplayer="O"
    legal_moves = []
    for i in range(len(board)):   # Tarkistaa tyhjät paikat ja listää ne listaan legal_moves
        if board[i]=="-":
            legal_moves.append(i)
    #########################################################################
    #SINUN KOODISI TÄHÄN
    #########################################################################
    if legal_moves:
        if maximizingplayer:
            bestValue = -2
            bestMove = None
            for move in legal_moves:
                board[move] = player
                if IsWinning(board):
                    v = 1
                else:
                    v, vMove = Minimax(board, False, nextplayer)
                board[move] = "-"
                if bestValue < v:
                    bestValue = v
                    bestMove = move
        else:
            bestValue = 2
            bestMove = None
            for move in legal_moves:
                board[move] = player
                if IsWinning(board):
                    v = -1
                else:
                    v, vMove = Minimax(board, True, nextplayer)
                board[move] = "-"
                if bestValue > v:
                    bestValue = v
                    bestMove = move
        return bestValue, bestMove
    return 0, None


def PrintBoard(board):
    # Tämä funktio printtaa pelilaudan
    print(' -7---8---9- ')
    print('|   |   |   |')
    print('| ' + board[6] + ' | ' + board[7] + ' | ' + board[8] + ' |')
    print('|   |   |   |')
    print('|-4---5---6-|')
    print('|   |   |   |')
    print('| ' + board[3] + ' | ' + board[4] + ' | ' + board[5] + ' |')
    print('|   |   |   |')
    print('|-1---2---3-|')
    print('|   |   |   |')
    print('| ' + board[0] + ' | ' + board[1] + ' | ' + board[2] + ' |')
    print('|   |   |   |')
    print(13*'-')
	
def PlayersMark():
    # Tämä funktio kysyy, onko pelaaja X vai O
    mark = ''                         
    while not (mark == 'X' or mark == 'O'):
        print('Do you want to be X or O: ',end="")
        mark = input().upper()
    if mark == 'X':
        return ['X', 'O']
    else:
        return ['O', 'X']

def WhoStarts():
    # Tämä funktio arpoo, kumpi pelaajista aloittaa
    if random.randint(0, 1) == 0:
        return 'computer'
    else:
        return 'player'
		

def EmptySpace(board, move):
    # Tämä funktio tarkistaa, onko pelaajan antama liike laillinen
    if board[move] == '-':
        return True
    else:
        return False
		
def PlayersMove(board):
    # Tämä funktio kysyy pelaajan siirron ja palauttaa sen, mikäli se on laillinen
    move = ' '
    while move not in '1 2 3 4 5 6 7 8 9'.split() or not EmptySpace(board, int(move)-1):
        print('Where do you want to move? (1-9): ',end="")
        move = input()
    return int(move)-1
	
def PlayAgain():
    # Tämä funktio kysyy, haluaako pelaaja pelata uudestaan
    print('Do you want to play again? (yes or no) :',end="")
    return input().lower().startswith('y')
	
def main():
    # Pääfunktio
    print("3x3 TicTacToe")
    while True:
        board=["-","-","-","-","-","-","-","-","-"]
        playersmark, computersmark = PlayersMark()
        turn = WhoStarts()
        if turn=="player":
            print("You are going to start the game")
        else:
            print("Computer (minimax) starts the game")
        gameisgoing = True
        while gameisgoing:
            if turn == 'player':
                PrintBoard(board)
                move = PlayersMove(board)
                board[move] = playersmark
                if IsWinning(board):
                    PrintBoard(board)
                    print('You won the game!')
                    gameisgoing = False
                else:
                    if board.count("-")==0:
                        PrintBoard(board)
                        print('The game is tie.')
                        break
                    else:
                        turn = 'computer'
            else:
                value, move = Minimax(board, True, computersmark)
                board[move] = computersmark
                if IsWinning(board):
                    PrintBoard(board)
                    print('Computer won the game')
                    gameisgoing = False
                else:
                    if board.count("-")==0:
                        PrintBoard(board)
                        print('The game is tie.')
                        break
                    else:
                        turn = 'player'
        if not PlayAgain():
            print("Game Over")
            break
   		
if __name__ == '__main__':
    main()
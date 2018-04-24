# -*- coding: utf-8 -*-
import time
import queue
import random

class EightPuzzle:
    def __init__(self):
        # Tässä funktiossa alustetaan 3x3 lauta listana
        self.targetstate = list(range(1, 9))
        self.targetstate.append(0)

    def PrintState(self, state):
        # Tämä funktio printtaa lista matriisi formaatissa
        for (index, value) in enumerate(state):
            print("{}".format(value),end="")
            if index==2 or index==5 or index==8:
                print("")
        print("")

    def LegalMoves(self, position):
        # Tämä funktio ratkaisee laillisten siirtojen paikan matriisissa
        values = [1, -1, 3, -3]
        legalmoves = []
        for x in values:
            if 0 <= position + x < 9:
                if x == 1 and (position==2 or position==5 or position==8):
                    continue
                if x == -1 and (position==0 or position==3 or position==6):
                    continue
                legalmoves.append(x)
        return legalmoves

    def FindNextStates(self, state):
        # Tämä funktio ratkaisee seuraavat mahdolliset siirrot nykyisestä tilasta
        legalmoves = {}
        for position in range(9):
            legalmoves[position] = self.LegalMoves(position)
        emptyspace = state.index(0)
        moves = legalmoves[emptyspace]
        nextstates = []
        for move in moves:
            state_x = state[:]
            (state_x[emptyspace + move], state_x[emptyspace]) = (state_x[emptyspace], state_x[emptyspace + move])
            nextstates.append(state_x)
        return nextstates

    def DrawState(self, state):
        # Tämä funktio valitsee seuraavan tilan sattumanvaraisesti. Tätä funktiota tarvitaan sekoittaessa peliä
        nextstates = self.FindNextStates(state)
        randomstate = random.choice(nextstates)
        return randomstate

    def InitialState(self, shuffles=200):
        # Tämä funktio ratkaisee alkutilan pelille. Sekoitetaan 200 kertaa mikäli sekoitusten määrää ei ole annettu etukäteen
        initialstate = (self.targetstate)[:]
        for i in range(shuffles):
            initialstate = self.DrawState(initialstate)
        return initialstate

    def GameSolved(self, state):
        # Tämä funktio tarkistaa, onko peli ratkaistu
        return state == self.targetstate
		
    def Manhattan(self, state):
        # Tämä funktio laskee manhattan etäisyyden nykyiselle tilalle. Manhatten etäisyys lasketaan lisäämällä kaikkiin numeroihin (1-8) horisontaaliset ja vertikaaliset liikkeet saadakseen numero oikealle paikalle.
        manhattanvalue = 0
        for number in state:
            if number != 0:
                greedyvalue = abs(self.targetstate.index(number) - state.index(number))
                (verticalvalue, horizontalvalue) = (greedyvalue // 3, greedyvalue % 3)
                manhattanvalue += verticalvalue + horizontalvalue
        return manhattanvalue
		
    def Hamming(self, state):
        # Tämä funktio laskee kuinka moni laatoista on väärällä paikalla (Hamming etäisyys)
        hamming = 0
        for i in range(9):
            if state[i] != 0 and state[i] != self.targetstate[i]:
                hamming += 1
        return hamming
		
    def GetLowestF(self, openlist, fscore):
        # Tämä funktio tarkistaa avoimen listan pienimmän f-scoren arvon ja palauttaa kyseisen tilan
        value = 10000000000
        for state in openlist:
            if fscore[self.ListToString(state)] < value:
                value = fscore[self.ListToString(state)]
                current = state
        return current
		
    def ListToString(self, numberlist):
        # Tämä funktio muuttaa listan stringiksi
        return ''.join(list(map(str, numberlist)))
	
    def ReconstructPath(self, camefrom, current):
        # Tämä funktio rakentaa polun alkutilasta tavoitetilaan, kun tavoitetila on löydetty
        totalpath = []
        current = self.targetstate
        while self.ListToString(current) in list(camefrom.keys()):
            current = camefrom[self.ListToString(current)]
            totalpath.append(current)
        totalpath.reverse()
        totalpath.append(self.targetstate)
        for i in totalpath:
            self.PrintState(i)
        print("Used total {} moves".format(len(totalpath)-1))
                    
    def Astar(self, state):
        #Funktion parametrit:
        #
        #self: yläluokan EightPuzzle kaikki parametrit
        #state: tila, joka yritetään ratkaista
        #
        #Funktio palauttaa:
        #
        #self.ReconstructPath(camefrom, state): lyhimmän mahdollisen polun, jonka avulla päästää tavoitetilaan
        camefrom = {}
        openlist = []
        closedlist = []
        gscore = {}
        fscore = {}
        openlist.append(state)
        gscore[self.ListToString(state)] = 0
        fscore[self.ListToString(state)] = gscore[self.ListToString(state)] + self.Manhattan(state)
        ######################################################################### 
        #SINUN KOODISI TÄHÄN
        #########################################################################
        while openlist:
            current = self.GetLowestF(openlist, fscore)
            if self.GameSolved(current):
                return self.ReconstructPath(camefrom, current)

            openlist.remove(current)
            closedlist.append(current)

            neighbors = self.FindNextStates(current)
            for neighbor in neighbors:
                if neighbor in closedlist:
                    continue

                if neighbor not in openlist:
                    openlist.append(neighbor)

                tentative_gScore = gscore[self.ListToString(current)] + 1
                #if tentative_gScore >= gscore[self.ListToString(neighbor)]:
                #    continue
                
                camefrom[self.ListToString(neighbor)] = current
                gscore[self.ListToString(neighbor)] = tentative_gScore
                fscore[self.ListToString(neighbor)] = gscore[self.ListToString(neighbor)] + self.Manhattan(neighbor)
        return None
		
def main():
    print('8-Puzzle Solver!')
    print(15 * '-')
    game = EightPuzzle()
    print('The starting state is:') 
    initialstate = game.InitialState(50)
    game.PrintState(initialstate)
    print('The target state will be:')
    game.PrintState(game.targetstate)
    print('The path of solution:')
    game.Astar(initialstate)
	
if __name__ == '__main__':
    main()
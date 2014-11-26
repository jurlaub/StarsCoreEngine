"""
    This file is part of Stars Core Engine, which provides an interface and 
    processing of Stars data. 

    Copyright (C) 2014  <Joshua Urlaub + Contributors>

    Stars Core Engine is free software: you can redistribute it and/or modify
    it under the terms of the Lesser GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Stars Core Engine is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Lesser GNU General Public License for more details.

    You should have received a copy of the Lesser GNU General Public License
    along with Stars Core Engine.  If not, see <http://www.gnu.org/licenses/>.

    Contributors to this project agree to abide by the interpretation expressed 
    in the COPYING.Interpretation document.

"""

import pickle



class GamePickle(object):

    def makePickle(fileName, p_object):
        with open(fileName, "bw") as a_file:    # file closed by the with statement
            pickle.dump(p_object, a_file)


    def unPickle(fileName):
        '''
        unpickle 

        requires a fileName,
            - test if the name uses the game name or fileName (i.e. <name>.hst)
            - add .hst and other values to unpack relevant values

        returns a number of objects:
            gameTemplate = StandardGameTemplate
            game = data after Game
        '''
        with open(fileName, "rb") as fn:
            #(gameTemplate, game) = pickle.load(fn)
            #p_object = pickle.load(fn)
            #return p_object
            return pickle.load(fn)





def printGameValues(game):
    for zz in iter(game.game_universe):
        print("\t%s%s%d%s"%('-'*20, 'UniverseNumber:', zz,'-'*20 ))

        for x in iter(game.game_universe[zz].planets):
            
            nn = game.game_universe[zz].planets[x]

            temp, grav, rad = nn.origHab
            ironC, borC, germC = nn.origConc 
            print("ID:%s, %s:  %s  - Owner:%s" % (nn.ID, nn.name, nn.xy, nn.owner))
            print("\tEnvironment: \t\t(%sc, %sg, %smr) " % (temp, grav, rad))
            print("\tMineral Concentration: \t(i:%skt, b:%skt, g:%skt)" % (ironC, borC, germC))


    print("\n%s%s%s" % ('-'*10, '**** Players ****', '-' * 10))
    
    for player in iter(game.players):
        playerObject = game.players[player]
        print("%s" % ( playerObject.raceName ))
        print("population growth rate: %s" % str(playerObject.race.popGrowthRate))

    print("\n")


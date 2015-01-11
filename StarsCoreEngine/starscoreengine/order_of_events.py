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
from .planet import *
from .player import Player


def OrderOfEvents(game):
    """Controller method that runs all order of events - including scanning.

    Assumes all .x data that will be used is present and loaded into game object. 

    """


    # scrappingFleets(game):
    # waypointZeroLoadTasks(game):
    # waypointZeroTasks():
    # MTMoves(
    # inSpacePackets()
    # fleetsMove():
    # ISFleetgrowth():
    # mineralDecay():
    # wormholesMove():
    # minefieldDetonate():
    # mineralMining():
    # production():
    # universeResearchCapture():

    population(game)

    # newPacketCollisions():
    # fleetsRefuel():
    # randomEvents():

    # fleetBattles():
    # bombing():
    # meetMT():
    # remoteMining():
    # waypointOneTasks():   
    # minefieldDecay():
    # mineLaying():

    # fleetTransfer():
    # waypointOneFleetMerge():
    # instaforming():
    # mineSweeping():
    #  repair():
    # remoteTerraforming():
    # Intel():


    game.year += 1





    


def colonyIterator(players, action):
    ''' iterate through all current colonies held by each player and perform one 
    action

    input: a game's players and one action (action must be a method)
    '''

    pass


def fleetIterator():
    pass


def scrappingFleets(game):
    # (w/possible tech gain)
    pass

def waypointZeroLoadTasks(game):
    # (if done by hand)
    pass

def waypointZeroTasks():
    #waypointZeroUnloadTasks(): # (By hand)
    # waypointZeroColonization_GroundCombat(): #(w/possible tech gain)
    # waypointZeroLoadTasks(): # (Random player order)
    # waypointZeroOtherTasks():
    pass

def MTMoves():
    pass

def inSpacePackets():
    # move. 
    #Packets that will hit planets decay pro-rated by distance traveled.
    # PP packets (de)terraform
    # Packets cause damage (Packets impact, oldest first, in planet-id order)
    # Planets hit that end up with 0 colonists become uninhabited
    # (Player order -lower- determines whose packets hit first)
    pass


def fleetsMove():
    # (run out of fuel, 
    #hit minefields (fields reduce as they are hit, lowest # fleets hits mines first), 
    # stargate & wormhole travel)
    pass

def ISFleetgrowth():
    #Inner Strength colonists grow in fleets. Overflows to player owned planets.
    pass

def mineralDecay():
    # mass pacekts still in space and Salvage decay
    pass

def wormholesMove():
    # endpoints jiggle/degrade/jump
    pass

def minefieldDetonate():
    # SD's fields (possibly damaging again fleet that hit minefield during movement)
    pass

def mineralMining():
    # Including AR waypoint 1 remote mining of colonized worlds.
    pass

def production():
    # (incl. research, packet launch, fleet/starbase construction)
    """
    iterate through all the player objects.
    > player objects have .x file player.turnOrder information separated
    > sequence for production: 
        >> each productionQ is cycled through
        >>>> Total resources for the year is calculated
        >>>> call:    

                resourcesForProduction = Research.colonyResearchTax(colony)
                
                (research tax is taken and in research tax added to Research object)
        >>>> remaining resources can be sent to productionQ for production 
            (or call Research from inside ProductionQ, and then spend resources)

        

        REFERENCE: Research comment for more explaination.

    """

    pass

def universeResearchCapture():
    # SS Spy bonus obtained
    # in a multiverse situation does the ss capture other universe research? - yes? 
    # could the SS races have their own version of Walter (see Fringe :) )
    pass

def population(game):
    # all colony populations grows/dies

    for player in game.players:
        playerObject = game.players[player]
        colonies = playerObject.colonies

        for each, colony in colonies.items():
            #update colony value
            colony.populationGrowth()
    

def newPacketCollisions():
    # that just launched and reach their destination cause damage (Impacts are in planet ID order)
    pass

def fleetsRefuel():
    # at bases
    pass

def randomEvents():
    # (comet strikes, etc.)
    pass

def fleetBattles():
    # (w/possible tech gain)
    pass

def bombing():
    # Player 1 bombing calculated
    # Retro Bomb, delayed effect.
    # Normal/LBU Bomb Damage/OCM Calculated
    # Smart Bomb Damage Calculated
    # Defences Recalculated (Retro Bombing takes effect).
    # Player 2 bombing calculated and so on in order with players 3, 4...
    # Planets with 0 pop lose defenses, planetary scanner, invasion tech gain possibility, the production queue, and the insta-terraforming of CA's.
    pass

def meetMT():
    pass

def remoteMining():
    pass

def waypointOneTasks():   
    # Waypoint 1 unload tasks
    # Waypoint 1 Colonization/Ground Combat resolution (w/possible tech gain)
    # Planets with 0 pop become uninhabited
    # Waypoint 1 load tasks (Random player order)
    pass

def minefieldDecay():
    pass

def mineLaying():
    pass

def fleetTransfer():
    pass

def waypointOneFleetMerge():
    pass

def instaforming():
    #CA
    pass

def mineSweeping():
    pass

def repair():
    #Starbase and fleet 
    pass

def remoteTerraforming():
    # and deterraforming
    pass

def intel():
    # Spotting by scanners
    pass
 

 

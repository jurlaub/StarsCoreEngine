"""
    This file is part of Stars Core Engine, which provides an interface and processing of Game data.
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

    Contributors to this project agree to abide by the interpretation expressed in the 
    COPYING.Interpretation document.

"""


class PlayerBuildList(object):
    """
    PlayerBuildList collects information from different components and generates
    a list of possible items to be produced by a players ProductionQ.
    This list is a super-set of all producable items for all productionQ's


    player designs + research = research costs

    initial list:
    > Mines
    > Factories
    > Minerals
    > Planetary Installations

    > on init - check if designs exist and add these if valid



    source for data
    > raceData - player.method that produces this
    > techTree - player.method gen the most recent one planetaryInstallations 
    > playerDesigns Ships
    > playerDesigns Starbases

    List updated every Turn:
    > minus raceData
    > refresh planetaryInstallations
    > refresh pD



    """

    def __init__(self, player):
        # define where to obtain the information
        self.raceData = player.raceData

        self.buildList = {"Mines" : { "itemType": "Mines", "targetItemsCost": [0,0,0,4]}}

    

    # pull from 



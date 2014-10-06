"""
    This file is part of Stars Core Engine, which provides an interface and processing of Stars data.
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


class Universe(object):
    """
        The universe object should ultimately allow for the creation of multiple universes within a game.

        Within this context, a 'universe' means the space objects associated within the same 2d plane (should the game
         ever develop a 3rd dimension then space objects within a given cubic volume.) A multi-universe context would provide 
        multiple 'galaxies' of space objects that require access through a dimension shift. The respective x,y may shift 
        or may be congruent. In fact, when this becomes fully detailed, game hosts should be able to set the number of 
        universes, universe shifting tech, potential game turn information (as in universes provide delayed
            reporting of turn information) and other values that create delicious game play

        universe ID
        universe x,y size
        game play differences? (i.e. one has higher mineral concentration when game generates, different min
            depletion rates, )
        game races HW or starting players, partial starting players
        universe planet space objects
        universe other space objects (non-player)
        universe events
        universe variables



    """


    def __init__(self):
        pass






class UniverseEvents(object):
    """
        this class describes universe events that could happen every game turn. 
        on game creation the host can set each universe's settings including frequency of events.
        events could be new minerals, wormhole appearance, or negative.
        like a astroid impacting a planet. (severe negative impacts should not occur until later in the game)

        

    """
    pass


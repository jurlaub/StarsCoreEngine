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



# flyweight pattern?  

# is there a way to dynamically add parent classes to a class? 
# !!!! is there a way to send code along with 'JSON' data to the client? 
#   I believe so. This may not be preferred but may be something to consider.
#   answer the fuel calculation problem, the ship design update component problem. 




class BaseTech(object):
    
    def __init__(self, ID):
        self.itemID = ID
        self.name = None            # tech object name (game name for object)
        self.itemType = None

        # Costs
        self.iron= None
        self.bor = None
        self.germ = None
        self.resources = None

        # Some witty 'Mass' related grouping
        self.mass = None

        # Tech Requirements
        self.ener = None
        self.weap = None
        self.prop = None
        self.con = None
        self.elec = None
        self.bio = None


class Weapon(BaseTech):

    def __init__(self):
        self.range = None
        self.damage = None


class Mechanical(BaseTech):

    def __init__(self):
        self.cargo = None

class Armor(BaseTech):

    def __init__(self):
        self.armor = 0

class Shields(BaseTech):

    def __init__(self):
        self.shield = 0



class Hull(BaseTech):

    def __init__(self):
        self.designName = None  # user specified ship design name
        self.shipType = None    # Miner, Transport, Armed, ect.
        self.cargo = None
        
        self.armor = 100
        self.fuelCapacity = 500
        # etc


        # slot defines the hull component composition
        self.slot = {"A":{"engine":1}, "B":{"objectType":"number_of_slots"}}  # each key == specific slot, value is

        # identify slots:
        #   slot type -> General, Engine, Weap, Mech, Elect, etc
        #   how many slots available

        # specify all ship related question?


class ShipDesign(Hull):
    ''' ShipDesign is a specific user defined design of the Hull class 
    '''

    def __init__(self, hullID):
        self.hullID = hullID # points to a Hull object. there is one for each type of ship.
        # component holds the number of items assigned to a design
        self.component = {"A":["itemID", "itemID"], "B":["itemID", "itemID", "itemID"]}  # capacity



    def componentDict(self, key, value):

        '''
        if key is electrical:
            update the ship designs electrical object values?
            update BaseTech values + objects values?
        '''
        pass











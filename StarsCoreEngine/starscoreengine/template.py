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
import random

def getPlanetNameFromTemplate():
    planet_names = planetNameTemplate()
    count = len(planet_names)
    rand = random.randrange(0, count)
    
    return planet_names[rand]

def planetNameTemplate():
    planet_names = ["Alan", "Fenge", "Fenris", "Shill", "239_Alf", "Wolf 359",\
     "Dark Star", "Kirk", "Flo Rida", "Pluto", "Centari", "Mau Tai", "Zeta", 
     "Mars", "Babylon 5", "Quell", "Be Still My Heart", "Soft Light",
     "Vertigo", "Verillon", "Camelot", "Too Much", "Avalon", "Quiver", 
     "Shining Star", "Bamboo II", "Deralon", "Dark Tide", "Everlon", "Eeek!",
     "Exegenesis", "Et'Varloon", "Gallifrey", "Geronimo", "Gytalli", "Hilda",
     "Harriot's Star", "Indigo", "Intel", "Inner Peace", "Jester's Crown", 
     "Jykle", "Kelly's Eye", "Kirkland", "Katie", "Loomiss", "Lester Pike",
     "Mea Tal", "Martoon", "Marcross", "McKenny", "McDevitton", "Reynold's Star",
     "Heinland", "Stross", "Brust", "Mat'Etvel", "Nooon", "Nubia", "Never Land",
     "Narly", "Opal",
     "Oster Den", "Old One", "Ol' Yeller", "Otaah", "Penelope's Star", "Piink",
     "Patrick's Way", "Pla'yet'Oh", "Pu Tai La", "Shei Gua", "Ping Loom", 
     "Q'atell", "007", "Bantha", "Betazoid", "Realist", "New Hope", "Recall",
     "Renovate This", "Sad Tide", "Sally Way", "Sol Two", "Shia Tell", 
     "Shitzu", "Sassyland", "Sardovia", "Telmarie", "Tennyson", "Termaso"
     "Terra", "Tar Rok", "Lok Tar", "Umbria", "Umbridge", "Unrepentant",
     "Unknown Star", "Un'Lo'Tek", "Ventillia", "Vargo II", "Vicktor's Star",
     "Vok'Ba", "Vot'Tark'Le", "Vessel", "Veree", "Ross 359", "Wolf Star", 
     "Wolf's Eye", "Moteland", "Wolfbane", "Transylvania", "Woe Tide", "Wode",
     "Woot", "Waco", "Wackyland", "Wat'up", "Wolfrik", "Yeet", "Yether", "Aether", "Yee",
     "Yent'il", "Yankee", "Coyote", "Yesterday", "Raster", "Xavier", "Xander",
     "Xandidu", "X-Factor", "Xidus", "Xtol", "Zeet", "Zak'To", "Zah'ha'dum", 
     "Zetherland", "Zoot", "4004da", "QWERTY"]
    return planet_names

def planetNamesFromFile():
    #--TODO--
    pass


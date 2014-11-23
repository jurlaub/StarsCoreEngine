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

def getPlanetNameFromTemplate( n):
        planet_names = planetNameTemplate()
        x = int(n % len(planet_names))
        return planet_names[x]

def planetNameTemplate():
        planet_names = ["Alan", "Fenge", "Fenris", "Shill", "239_Alf", "Wolf359",\
         "Dark Star", "Kirk", "Flo Rida", "Pluto", "Centari", "Mau Tai", "Zeta"]
        return planet_names
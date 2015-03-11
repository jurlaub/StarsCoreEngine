"""
    This file is part of Stars Core Engine, which provides an interface and 
    processing of Game data. 

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

from nose.tools import with_setup, assert_equal, assert_not_equal, \
 assert_raises, raises, assert_in, assert_true, assert_false, assert_almost_equals

#import unittest
from ..starscoreengine.battle import *


class TestBattle():
    def setUp(self):
        pass

    def test_extractBoardPositions_2(self):
        calc = extractCoords(getBoardGrid(2), 2)
        expect = [(1, 4), (8, 5)]
        assert_equal(expect, calc)


    def test_extractBoardPositions_3(self):
        calc = extractCoords(getBoardGrid(3), 3)
        expect = [(4, 1), (8, 8), (1, 8)]
        assert_equal(expect, calc)

    def test_extractBoardPositions_4(self):
        calc = extractCoords(getBoardGrid(4), 4)
        expect = [(1, 1), (8, 8), (1, 8), (8, 1)]
        assert_equal(expect, calc)

    def test_extractBoardPositions_5(self):
        calc = extractCoords(getBoardGrid(5), 5)
        expect = [(4, 1), (6, 8), (1, 4), (8, 4), (2, 8)]
        assert_equal(expect, calc)

    def test_extractBoardPositions_6(self):
        calc = extractCoords(getBoardGrid(6), 6)
        expect = [(1, 4), (8, 5), (2, 8), (7, 1), (6, 8), (3, 1)]
        assert_equal(expect, calc)

    def test_extractBoardPositions_7(self):
        calc = extractCoords(getBoardGrid(7), 7)
        expect = [(1, 1), (1, 5), (2, 8), (6, 8), (8, 6), (8, 2), (5, 1)]
        assert_equal(expect, calc)

    def test_extractBoardPositions_8(self):
        calc = extractCoords(getBoardGrid(8), 8)
        expect = [(1, 3), (1, 6), (3, 8), (6, 8), (8, 6), (8, 3), (6, 1), (3, 1)]
        assert_equal(expect, calc)

    def test_extractBoardPositions_9(self):
        calc = extractCoords(getBoardGrid(9), 9)
        expect = [(1, 3), (8, 6), (3, 8), (6, 1), (1, 6), (8, 3), (6, 8), (3, 1), (4, 4)]
        assert_equal(expect, calc)

    def test_extractBoardPositions_10(self):
        calc = extractCoords(getBoardGrid(10), 10)
        expect = [(2, 1), (5, 1), (8, 1), (1, 4), (8, 4), (4, 5), (1, 7), (8, 7), (3, 8), (6, 8)]
        assert_equal(expect, calc)

    def test_extractBoardPositions_11(self):
        calc = extractCoords(getBoardGrid(11), 11)
        expect = [(1, 3), (8, 6), (3, 8), (6, 1), (1, 6), (8, 3), (6, 8), (3, 1), (3, 4), (6, 3), (6, 6)]
        assert_equal(expect, calc)

    def test_extractBoardPositions_12(self):
        calc = extractCoords(getBoardGrid(12), 12)
        expect = [(1, 4), (8, 5), (2, 8), (7, 1), (6, 8), (3, 1), (1, 6), (8, 3), (1, 2), (4, 8), (5, 1), (8, 7)]
        assert_equal(expect, calc)

    def test_calcAccuracy1(self):
        computingPower = 50
        torpAccuracy = 75
        jamming = 0
        assert_almost_equals(87.5, calcAccuracy(computingPower, torpAccuracy, jamming))

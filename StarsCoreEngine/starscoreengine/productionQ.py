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

"""

Note:   See research.py for interaction between productionQ, research, and Order 
        of Events. 


ProductionQ Requirements:
    - Client is required to provide a unique identifier for each productionQ item per colony
    - Client is required to filter production Items producable by a Colony based on colony limitations 
    - If user modifies the productionOrder, Client needs to submit the entire productionOrder. If anything is missing from the order, it will be deleted from the Q




productionQ "Items to Produce" :
        
        ShipDesign:
            Ships 
            Starbase
        Planetary Installations:
            Scanner
            Defenses
            Terraform   # works on the one which would be most beneficial?
        Mines
        Factories
        Minerals
        Special

        Support (expansion on original - for later)
        Dedicate to Research (expansion)



Miniaturization:
        Input: techLevel, techTree, LRT
        Output: revise the values in productionItems
 
        Items that Miniaturization impacts are the PlayerDesigns. No planetInstallations
        are impacted or other items. 

        After Technology research occurs, each players ShipDesigns are updated.
        ProductionQ tracks how much is spent on any given item. The ShipDesign 
        values are compared to the spent items. If more was spent then is needed
        due to Miniaturization then that is unfortunate. (no refunds of minerals 
        or resources, if overspent)


# thoughts on Q
Multiple types of entries:
        1) autoBuild orders
        2) quantity 1 items
        3) quantity n items
        #----------------------


        "materialsUsed" : [0, 0, 0, 0]  == (iron, bor, germ, resources) 

         
        #----------------------

        autoBuild & everything -> 


"""

from .fleets import FleetObject, Starbase, Token
from .fleet_orders import FleetOrders


DEBUG = False    # addToQueue
DEBUG_2 = False
DEBUG_3 = False  # ProductionController and EntryController

class ProductionQ(object):
    """ ProductionQ
    One ProductionQ object should exist for each colony object.


    """


    itemType = ('Ship', 'Starbase', 'Scanner', 'Defenses', 'Mines', \
                 'Factories', 'Terraform', 'Minerals', 'Special')

    defaultSetting = ()     # default options for all Q's

    def __init__(self, colony, player):         # defaultSetting may not be necessary.
        

        #self.productionList = [] # shipDesigns + starbaseDesign + planetInstallations + autoBuild
        self.colony = colony
        self.research = player.research
        self.raceData = player.raceData
        self.designs = player.designs # point is to gather productionQ BuildList -- handled in a different 

        self.player = player  # player to provide costs for a number of itemTypes


        self.prodQueue = []
        self.ExcludedFromResearch = False
        self.customDefaultSettings = []

        self.resources = 0
        self.test_ResourcesConsumed = 0  # use for testing

        self.test_ship = 0

        # productionOrder provides the order for the elements in productionItems
        # each order should point to a unique item
        self.productionOrder = []     
        self.productionItems = {} 

        self.entrybuildtype = ""
        self.entrybuildquantity = 0
        

    def addToQueueFromXFile(self, colonyQ):
        """addToQueueFromXFile()

        Input:  {productionOrder, productionItems} for colony.
        Output: updates colony productionQ

        Requires:
        ProductionQ items must have unique id's
        ProductionQ item "productionID"'s are not changed


        conditions:
        1) user adds 1 to N items
            - if item is not in Q, add it. -> addToQueue method
    
        2) user modifies 1 to N item contents
            - if a quantity 1 item has a quantity increase after production has 
            begun on the item, a new item is added to the productionOrder and productionItems
            - if a quantity N item has a different quantity, then quantity is set to the new quantity number
            - obtainNewKey() method - > that returns a new productionQ key
            - a change in productionID (what should be built) is not allowed. 
            The productionID change is not checked. If Client allows this 
            through, the original production value item will be built.                  
       
        3) user deletes item 
           - if item in productionQ is not in productionList then set quantity to 0
            - setQuantityToZero() method
            - quantity 0 items handled by productionController at end of colony production
        
        4) user changes order of completion
            - handled by the productionOrder list   

        if new orders are only adjusting the productionOrder and are making no 
        other change to the entry, as long as the entry exists in productionItems, 
        the productionItem value can be missing.
        """

        
        self.test_ResourcesConsumed = 0  # set to 0 at the beginnin of the turn

        colonyQOrders = colonyQ["productionOrder"]  # list
        colonyQItems = colonyQ["productionItems"]   # contents

        colonyQOrders_QAdditions = []

        if DEBUG_2: print("NewOrders:\n%s\n%s" % (colonyQOrders,colonyQItems))
        if DEBUG_2: print("ExistinOrders:\n%s\n%s" % (self.productionOrder, self.productionItems))

        # find items in productionQ not in the new ProductionQ orders
        tmpRemoveFromCurrentQ = set(self.productionOrder).difference(colonyQOrders)
        if DEBUG_2: print("items to remove from productionQ set:%s" % tmpRemoveFromCurrentQ)


        # update the productionItems "quantity" = 0 for entries to remove -> because they do not exist in the new queue
        for each in tmpRemoveFromCurrentQ:
            if DEBUG_2: print("%s set to Zero" % each)
            self.setQuantityToZero(each)

        # New orders are added or update existing ProductionQ
        # Note: if work has been done on an item in a colony's ProductionQ, then an additional entry
        #       is added to the colonyQOrders. The next item in colonyQOrders should be this newly added itme
        #       which should not have any work done and is added through the normal way.
        for eachIndex, each in enumerate(colonyQOrders):
            """
            Items-exist truth table
            t = targetItem = colonyQItems[each]
            e = existingItem = self.productionItems[each]  

            e | t 
            -----
            T | T  == things have changed -> update existingItem
            T | F  == involves a reorder of productionOrder (note: not preferred. prefer above (T|T) case)
            F | T  == not present in existingItem, is new and should be added
            F | F  == no action - error case. Entry should not be in either productionOrder or productionItems        

            """

            # --TODO-- call check quantity method here --> has the ceiling been reached


            # Items-exist (T|T)
            if each in self.productionItems and each in colonyQItems:
                # update Queue
                targetItem = colonyQItems[each]
                existingItem = self.productionItems[each]

                # -------------- partially validate input ---------------- 
                #quantity must be an int - skip if incoming order is not int
                if ProductionQ.elementHasUnexpectedValue(targetItem):
                    #print("unexpected object - skipping")
                    continue

                # target item quantity must be a positive int
                elif targetItem["quantity"] < 1:
                    self.productionItems[each]["quantity"] = 0
                    continue
                
                # else:
                #     # 1 :: 1 -> same  
                #     # a < b  -> user increased quantity from last time 
                #     # a > b  -> user decreased quantity 
                #     # a :: 0 -> user removed quantity
                #     existingItem["quantity"] = targetItem["quantity"]


                # work has not been done
                if not ProductionQ.workHasBeenDone(existingItem):
                    
                    # replace existing item's quantity 
                    self.productionItems[each]["quantity"] = targetItem["quantity"]
                    if DEBUG_2: print("addToQueueFromXFile - Items-exist (T|T) index:%d - work not done and quantity set to %s" % (eachIndex, self.productionItems[each]["quantity"]))

                
                # work has been done
                else:
                    
                    # an existingItem with work done is reduced to only produce a single ship.
                    if targetItem["quantity"] == 1:
                        
                        self.productionItems[each]["quantity"] = targetItem["quantity"]
                        if DEBUG_2: print("addToQueueFromXFile - Items-exist (T|T) index:%d - work done and quantity set to 1 == %s" % (eachIndex, self.productionItems[each]["quantity"]))

                        continue
                    
                    # An existingItem has work done but with 'quantity' > 1
                    # extract 1 with work done
                    # sum of single extractedItem + existingItem == targetItem['quantity']
                    else:
                                
                        # ---- mod existing entry --------
                        # set quantity of existingItem with work done to 1
                        self.productionItems[each]["quantity"] = 1


                        # ---- create new item to account for the remaining orders ----
                        # reduce quantity of targetItem by 1
                        targetItem["quantity"] -= 1 
                        
                        tmpNewEntry = {each : targetItem}
                        tmpNewIndex = eachIndex + 1

                        #>> add a new entry to items, insert new Order immediately after the quantity 1 item
                        self.addToQueue(tmpNewEntry, tmpNewIndex)
                        
                        if DEBUG_2: print("addToQueueFromXFile - Items-exist (T|T) index:%d - new entry added:\n%s" % (eachIndex, self.productionOrder))

                        #  --TODO-- test that this works as expected.
                        # obtain newly added item key to add to colonyQOrders
                        tmpNewKey = self.productionOrder[tmpNewIndex]
                        
                        if DEBUG_2: print("addToQueueFromXFile - Items-exist (T|T) index:%d - key for newly added entry:%s" % (eachIndex, tmpNewKey))
                        if DEBUG_2: print("existingItem - \tkey(%s) : %s \nnewItem - \tkey(%s) : %s" %(each, self.productionItems[each], tmpNewKey, self.productionItems[tmpNewKey]  ))
                        #----------- Add to ColonyQOrders-----------------------
                        #            Uses Items-exist (T|F)
                        #            Requires: Continue
                        # it should be the next entry on the colonyQOrders
                        #  
                        colonyQOrders.insert(tmpNewIndex, tmpNewKey)    
                        # ------------------------------------------------------
                        

            
            # Items-exist (T|F)
            elif each in self.productionItems and each not in colonyQItems:
                """
                Conditions:
                > if in self.productionItems but not in colonyQItems
                > may be that there is no update to the element
                > may be that the item does not exist (in either colonyQItems & colonyQOrders)
                > may be that element was added by the "Work has been done - add a new element to the Q" process. 
                
                Requires: 
                    continue
                """
                # no action needed -> reorder handled in the productionOrder
                if DEBUG_2: print("addToQueueFromXFile - Items-exist (T|F) index:%d - No action and not a problem  - Order:%s " % (eachIndex, each))


                continue

            # # Items-exist (F|T)
            elif each not in self.productionItems and each in colonyQItems:
                
                if ProductionQ.elementHasUnexpectedValue(colonyQItems[each]):
                    if DEBUG_2: print("addToQueueFromXFile - Items-exist (F|T).unexpected object - skipping")
                    continue

                v = { each : colonyQItems[each] }
                if DEBUG_2: print("v%s" % (v))

                self.addToQueue(v)
            
            # Items-exist (F|F)
            else:
                # take no action, should not have reached this spot
                #raise ValueError()
                ra = ("addToQueueFromXFile tmpItem# Items-exist (F|F). - reached area that should not be reached")
                raise ValueError(ra)

        self.productionOrder = colonyQOrders    # orders are potentially modifed due to work already done behavior

        # remove quantity zero items?
        self.removeQuantityZeroItems()

    def addToQueue(self, entryDict, insertOrder = None):
        """ addToQueue
        - could be called when items are added from addToQueueFromXFile()
        - could be called during entryController() 

        Input: {kee: {quantity, productionID}}, insertOrder = None
        Output:
            kee is modified to be unique
            item is added to productionOrder, productionItems
            item adds other elements 



        Note:
        insertOrder => inserts new item into productionOrder list as specified, None = results in an append
        entryDict["quantity"] => target quantity, no modifications
        "materialsUsed" : [0, 0, 0, 0]  == (iron, bor, germ, resources)

        """
        
        try:
            

            if len(entryDict) != 1:
                raise ValueError("addToQueue. requires entryDict to a dictionary with 1 key:value entry. %d detected" % len(entryDict))

            entryKey, entryObj = entryDict.popitem()

            if DEBUG: print("addToQueue: entryKey:%s entryObj:%s" % (entryKey, entryObj))


            
            # if DEBUG: print("addToQueue.entry: %s - %s " % (entryKey, entryObj))

            # "materialsUsed" ca
            if "materialsUsed" in entryObj:
                tmpMaterialsUsed = entryObj["materialsUsed"]
            else:
                tmpMaterialsUsed = [0, 0, 0, 0]
            
            # merging itemType and productionID to be the same. designID is added to handle ship/starbases
            if "itemType" in entryObj:
                tmpItemType = entryObj["itemType"]
            elif "productionID" in entryObj:
                tmpItemType = entryObj["productionID"]
            else:
                # for testing - should not be a valid value for normal play.
                tmpItemType = "Default ItemType"    


            if "designID" in entryObj:
                tmpDesignID = entryObj["designID"]
            else:
                tmpDesignID = None


            tmpItem = { "quantity" : entryObj["quantity"], 
                        "productionID" : tmpItemType,
                        "finishedForThisTurn" : False,
                        "itemType": tmpItemType,
                        "materialsUsed" : tmpMaterialsUsed,
                        "designID" : tmpDesignID
            }           


            tmpKey = self.obtainNewKey(entryKey)

            if DEBUG: print("addToQueue. at orderPosition %s - %s:%s " % (insertOrder, tmpKey, tmpItem))

            if insertOrder is not None and insertOrder < len(self.productionOrder):
                # if insertOrder >= len(self.productionOrder):
                #     self.productionOrder.append(tmpKey)
                # else:
                if DEBUG: print("addToQueue.at insert")
                self.productionOrder.insert(insertOrder, tmpKey)


            else:
                if DEBUG: print("addToQueue.at append")
                self.productionOrder.append(tmpKey)

            if DEBUG: print("addToQueue: item:%s" %tmpItem)
            self.productionItems[tmpKey] = tmpItem

            #print("%s \n %s" % (self.productionOrder, self.productionItems))


        except NameError as ne:
            print("ProductionQ.addToQueue() is missing: %s" % ne )

        except ValueError as ve:
            print("ProductionQ.addToQueue() %s" % ve)


    def obtainNewKey(self, kee):
        """
        Input: kee
        Output: a unique kee that is not used in that colony productionQ

        note: not thread safe within a single colony's productionQ. 

        """
        tmpKey = kee
        count = 1

        while True:
            if tmpKey not in self.productionOrder:
                if tmpKey not in self.productionItems:
                    print("obtainNewKey: %s" % tmpKey)
                    return tmpKey

            tmpKey = ("%s%s" %(kee, str(count)))
            count += 1

  
    @staticmethod
    def elementHasUnexpectedValue(targetItem):
        """ 
        productionItem elements should have been vetted during game_xfile processing.
        This method should be used to control the game_xfile process.
        it would reappear within productionQ methods as internal validation. 

        """

        try:
            
            if not isinstance(targetItem["quantity"], int):
                return True

            return False
       
        except ValueError as ve:
            print("%s" % ve)
            
    @staticmethod
    def workHasBeenDone(existingItem):
        """
        Input: productionItem dictionary
        Output: 
            True - work has been done == i.e. an element in "materialsUsed" != 0
            False - work not done == all elements in "materialsUsed" == 0

        Conditions:
            

        Work can be done on an existing item:
        > quantity set to 0
        > quantity @ 1

        



        """
        try:
            # quan
            # correctQuantity = True


            # # if existingItem["quantity"] > 1 or existingItem["quantity"] < 0:
            # #     #correctQuantity = False
            # #     raise ValueError("ValueError :: workHasBeenDone: quantity(%d)" % existingItem["quantity"])

            for each in existingItem["materialsUsed"]:

                # if materials have been used (not 0) then the quantity should be 1
                if each != 0:
                    return True

                    # if not correctQuantity:
                    #     # have a value in the materialsUsed and quantity is greater then 1 or negative
                    #     raise ValueError("ProductionQ.hasWorkBeenDone: materialsUsed and quantity not aligned. materialsUsed can only be greater then 0 when quantity = 1")
                    
                    # else:
                    #     # materials have been used and the quantity of the item is 1
                        # return True  
                
                # continue checking for a non-zero value

            # no materials have been used 
            return False    

        except ValueError as ve:
            print(ve)
            return False
            
    def setQuantityToZero(self, entryKee):
        """ setQuantityToZero
        changes the entry quantity to zeroed

        """
        self.productionItems[entryKee]["quantity"] = 0

    def removeQuantityZeroItems(self):
        """
        productionOrder and productionItems should have the same number of items. 
        This should be handled in the addToQueueFromXFile() method - the quantity
        of items is set to zero.

        during production - when items are completed, they are also set to zero.

        for any item in productionItem's where the quantity is zero, any corresponding
        productionOrder entry and productionItem entry should be removed.

        """
        

        itemsToBeDeleted = []
        ordersToBeDeleted = []

        for eachKey, eachObj in self.productionItems.items():

            if eachObj["quantity"] == 0:

                if eachKey in self.productionOrder:

                    # remove from production order
                    ordersToBeDeleted.append(eachKey)


                itemsToBeDeleted.append(eachKey)


            else:
                continue

        for each in itemsToBeDeleted:

            del self.productionItems[each]
            if DEBUG: print( "Item: %s deleted" % each)

        for each in ordersToBeDeleted:

            tmpV = self.productionOrder.index(each)
            del self.productionOrder[tmpV]
            if DEBUG: print( "Order: %s deleted" % each)
        
    def updateProductionQResources(self):
        """
        input: none (uses self values)
        output: calls colony.calcTotalResources() method to update the colony resources
                updates productionQ.resources value

        precondition: colony.calcTotalResources must be available to revise resources for colony

        called from ProductionQ.productionController

        """
        # colony updates resource calculations
        self.colony.calcTotalResources(self.raceData.popEfficiency)
        self.research.totalResources += self.colony.totalResources


        # obtain from colony the number of resources for production (Note: minus research tax)
        if self.ExcludedFromResearch:
            self.resources  = self.colony.totalResources
        else:
            self.resources  = self.research.colonyResourcesAfterTax(self.colony)

        if DEBUG_3: print("updateProductionQResources: resources:%s" % self.resources)

    def productionController(self):
        """
        The productionController is used to 'parse' through the production list == self.prodQueue 
        
        1) It identifies the amount of resources that can be used for production 
        (Calling the self equivalent of Research.colonyResearchTax(colony) method to obtain the # 
        of resources available )
        >> 20161216 ju - Calls updateProductionQResources()
        
        2)  

        3) if items in the queue cannot be completed due to lack of resources, 
        follows AutoMinerals, and tries again, until production is completed or
        resources depletion.

        4) if not AutoMinerals, and still have resources, complete the next item
        until minerals are depleted.
        then choose the next item in the default list that can be completed, 
        

        Misc) removes completed item if approprate



        20150117 ju - NOTE: ProductionQ instructions may specifiy to produce 'n' of a 
              ShipDesign. Only 1 of a design should be produced at a time.
            Once produced the 'n' value should be decremented. If '0' then proceed
              to the next instruction.
 

        20150207 ju - partially complete items in the queue -> resource 'spent'/'used' 
            must be proportional to the materials available. It would be 
            ridiculious to set aside 100% of the resources with none of the 
            materials. 

            Solution1: use a ratio
            the sum of remaining materials as defined by target item / 
            the sum of available required materials


        productionQ

        "finishedForThisTurn" for all items on the list set to "false"


        while True:

        > Do I have resources left? 
        >> if no -> break
        > Am I at the end of the list?
        >> if yes -> break


        > Find next entry in productionOrder
        >> 
        >> if "finishedForThisTurn" == True, increment counter + continue
        
        >> Act on autoBuild orders only once (unless its autoBuild minerals in order to complete a project)
        >> Autobuild - add autobuild orders to Q, set autobuild to false for turn
        
            if entry is next on list:
                send to entryController -- send entry to self.entryController()  
                elif quantity >= 2: break quantity into two, create 1 single entry at beginning, existing is finishedForThisTurn
                elif new single entry or quantity == 1 : use as many resources as possible (by percentage rules), 


                if AutoMinerals on, minerals are holding up single entry and resources are available, add a build mineral to the beginning of q
                reset loop to 0, continue


        >> if quantity = 0, it will be removed from Q at end -> set finishedForThisTurn = True;        --> if quantity == 0: entry to be deleted
        >> if productionOrder is empty(or at end of list) -> break, left over resources applied to research
       


    
        2b) if "quantity" : n > 1,
            call a special helper method dealing with producing multiples of an 
            item, the method will determine how many 'whole' items can be built 
            with the available resources & materials. The respective items will 
            be built by calling the approprate method.

        2ba) if more of the 'item' needs to be built, quantity > 2,
             A new quantity 1 entry should be entered into the productionQ at 
             the beginning of the list. It should consume as many resources as 
             possible. 
             The quantity > 2 entry should be decremented
        2bb) if the 'item' is quantity == 2:
             A new quantity 1 entry should be entered into the productionQ at 
             the beginning of the list. It should consume as many resources as 
             possible.
             The quantity > 2 entry should be decremented to 1, it should have
             all the 'attributes' necessary for a quantity 1 entry      
        2bc) if 'item' quantity == 1:
             It should consume as many resources as 
             possible.
        2bd) if 'item' quantity == 0:
             item should be removed from productionQ and productionList


        """

        #DEBUG_3 = DEBUG_3

        autobuildMinerals = False       # for minerals if needed.

        #res = 0


        # obtain from colony the number of resources for production (Note: minus research tax)
        # if self.ExcludedFromResearch:
        #     self.resources  = self.colony.totalResources
        # else:
        #     self.resources  = self.research.colonyResourcesAfterTax(self.colony)

        self.updateProductionQResources()

        # handle the produceAutoMineral setting?

        orderIndex = 0 
        # --------------- reset "finishedForThisTurn"  ------------
        # All orders "finishedForThisTurn" == False
        # ---------------------------------------------------------

        if DEBUG_3: print("ProductionQ.productionOrder: %s\nProductionQ.productionItems: %s" %  (self.productionOrder, self.productionItems))
            


        while True:


            orderLength = len(self.productionOrder)
            if DEBUG_3: print("ProductionQ.productionController - start of loop. orderIndex:%d  / orderLength: %d)" % (orderIndex, orderLength))


            if self.resources < 1:  # resources left
                if DEBUG_3: print("ProductionQ.productionController - resources: %d" % self.resources)
                break
            
            elif orderIndex >= orderLength:  # reached empty or end of order
                if DEBUG_3: print("ProductionQ.productionController - orderIndex: %d" % orderIndex)

                break

            
            entryID = self.productionOrder[orderIndex]
            entryObj = self.productionItems[entryID]

            if entryObj["finishedForThisTurn"]: # T/F based on Entry.
                if DEBUG_3: print("ProductionQ.productionController - (%s) finishedForThisTurn orderIndex: %d" % (entryID, orderIndex))
                orderIndex += 1
                continue
            
            elif entryObj["quantity"] == 0:
                if DEBUG_3: print("ProductionQ.productionController - (%s) finishedForThisTurn orderIndex: %d" % (entryID, orderIndex))
                entryObj["finishedForThisTurn"] = True
                orderIndex += 1
                continue


            """
            This checks if a given entry has had work done. If so, it will split apart the
            entry and complete the remaining work on a quantity 1 item. Then it 
            will cycle around again to build more.


            """
            if entryObj["quantity"] > 1 and ProductionQ.workHasBeenDone(entryObj):
                
                if DEBUG_3: print("productionController quantity > 1 and work has been done. Splitting (%s) into two. orderIndex:%d" % (entryID, orderIndex))

                entryObj["finishedForThisTurn"] = True
                orderIndex = 0      # restart at beginning as a quantity 1 entry will be made by splitEntryIntoTwo()

                
                self.splitEntryIntoTwo(entryID)

                if DEBUG_3: print("ProductionQ.productionOrder: %s\nProductionQ.productionItems: %s" %  (self.productionOrder, self.productionItems))


                continue



            # is entry an Autobuild type? 
            # add check for autobuild type   entryObj["itemType"]
            # if autobuildMinerals == True set the autobuildMinerals = True
            targetItemType = self.productionItems[entryID]["itemType"]
            targetDesignID = self.productionItems[entryID]["designID"]
            # if targetItemType in ['Ship', 'Starbase']:
                
            targetItemCosts = self.targetItemCosts(targetItemType, targetDesignID)

            self.entryController(entryID, targetItemCosts)



        # ------- remaining resources spent on research ----
        if self.resources > 0:
            self.research.yearlyResearchResources += self.resources
            self.resources = 0



    

            # if entryObj["finishedForThisTurn"]:
            #     orderIndex += 1
            #     continue
            
            # elif entryObj["quantity"] >= 1:
            #     # start over

            #     #orderIndex = 0
            #     # resubmit for a partial production

            #     continue



            
            # if entryController adds an item to the productionOrder/Items,
            # then start over at the beginning. Reasons include: autobuild orders, ?
            # note: entryController should set items to "finishedForThisTurn"
            # if orderLength == len(self.productionOrder):
            #     #no change in entry controller
            #     orderIndex += 1         # entry completed then increment 
            # else:
            #     orderIndex == 0         # start at beginning

    def targetItemCosts(self, itemType, designID = None):
        """
        Input:  itemType - everything that can be made has type
                productionID - id unique to a design (uses this to obtain the current costs from the productionList)
        Output: [material cost + resources] 

        precondition: 
            targetItemCosts must be updated based on tech levels (ie Miniaturization)- if this is 
            not captured in the productionList then it should be captured 

            itemType does not change from the HARDCODED value found in ProductionQ
                ProductionQ.itemType = ('Ship', 'Starbase', 'Scanner', 'Defenses', 'Mines', \
                 'Factories', 'Terraform', 'Minerals', 'Special')


        --TODO--
        Need to clarify the difference between itemType, productionID and ProductionQ entry
        Ships & Starbases must have a respective itemType but a userdefined productionID.
        (perhaps this is why the original had a max 16 ship designs, where productionID and ship design
            entry were synomonous)


        """
        itemValue = None

        if itemType == "Ship":
            itemValue = self.itemCostsShip(designID)
            return itemValue
        
        elif itemType == "Starbase":
            itemValue =  self.itemCostsStarbase(designID)
            return itemValue
        
        elif itemType == "Scanner":
            itemValue =  self.itemCostsScanner()
            return itemValue
        
        elif itemType == "Defenses":
            itemValue =  self.itemCostsDefenses()
            return itemValue
        
        elif itemType == "Minerals":
            itemValue =  self.itemCostsMinerals()
            return itemValue
        
        elif itemType == "Factories":
            itemValue =  self.itemCostsFactories()
            return itemValue
        
        elif itemType == "Terraform":
            itemValue =  self.itemCostsTerraform()
            return itemValue
        
        elif itemType == "Mines":
            itemValue =  self.itemCostsMines()
            return itemValue
        
        else:
            print("ProductionQ.targetItemCosts() returning None :: not an expected itemType: %s  " % (itemType))
            return itemValue


    # uses Tech Tree values without race specific items.
    def itemCostsDefenses(self):
        return self.raceData.defensesCosts

    def itemCostsTerraform(self):
        return self.raceData.terraformCosts

    def itemCostsScanner(self):
        return self.raceData.scannerCosts

    def itemCostsFactories(self):
        germCost = 4 if not self.raceData.factoryGermCost else 3 
        return [0, 0, germCost, self.raceData.factoryCost]


    def itemCostsMines(self):
        return [0, 0, 0, self.raceData.mineCost]

    def itemCostsShip(self, itemID):
        print("itemCosts - item:%s" % itemID)
        costs = self.designs.currentShips[itemID].currentCosts()
        return costs


    def itemCostsStarbase(self, itemID):
        costs =  self.designs.currentStarbases[itemID].currentCosts()
        return costs


    def itemCostsMinerals(self):
        return self.raceData.mineralCosts

    def splitEntryIntoTwo(self, entryID):
        """
        Input: entryID (value at self.productionItems[orderIndex])
        Output: 
            update currentEntry quantity -= 1
            update currentEntry materialsUsed = zeroed

            adds newEntry to self.productionItems[0]
            newEntry[quantity] = 1
            newEntry[materialsUsed] = any values that was in currentEntry[materialsUsed] before it was zeroed

        precondition: 
            expects values exist in dictionary
            expects values to be correct type


        Accepts a entry. It creates a new entry @ beginning. 
        New Entry = quantity = 1
        New Entry = any work done
        Entry = quantity -= 1
        Entry = work done == [0, 0, 0, 0]

        {kee: {quantity, productionID}}

        """

        currentEntry = self.productionItems[entryID]
        #print("splitEntryIntoTwo:: %s: (q:%d): %s "% (entryID, self.productionItems[entryID]["quantity"], self.productionItems[entryID]["materialsUsed"] ))

        if currentEntry["quantity"] <= 1:
            if DEBUG_3: print("ProductionQ.splitEntryIntoTwo - currentEntry[quantity] <= 1")
            return

        # -----------  extract values from currentEntry --------------
        tmpEntryProductionID = currentEntry["productionID"]
        tmpEntryMaterials = [i for i in currentEntry["materialsUsed"]]
        tmpEntryItemType = currentEntry["itemType"]
        
        
        if tmpEntryProductionID in ['Ship', 'Starbase']: 
            tmpEntryDesignID = currentEntry['designID']
        else:
            tmpEntryDesignID = None


        tmpEntry = {
            entryID : {
                "quantity" : 1, 
                "productionID" : tmpEntryProductionID,
                "materialsUsed" : tmpEntryMaterials,
                "itemType" : tmpEntryItemType,
                "designID" : tmpEntryDesignID
                }}
        

        #self.productionItems[entryID]["quantity"] = self.productionItems[entryID]["quantity"] - 1
        self.productionItems[entryID]["quantity"] -= 1
        self.productionItems[entryID]["materialsUsed"] = [0 for i in tmpEntryMaterials]  # set currentEntry to 0

        #print("splitEntryIntoTwo:: %s: (q:%d): %s "% (entryID, self.productionItems[entryID]["quantity"], self.productionItems[entryID]["materialsUsed"] ))

        if DEBUG_3: print("ProductionQ.splitEntryIntoTwo - tmpEntry: %s" % tmpEntry)

        self.addToQueue(tmpEntry, 0)

        if DEBUG_3: print("ProductionQ.splitEntryIntoTwo - addedToQueue productionItems: %d  productionOrder: %d" % (len(self.productionItems), len(self.productionOrder)))



    def entryController(self, entryID, targetItemCosts, autobuildMinerals = False):
        """

        entryController does both 1 & 2:
        1) build a quantity n (up to max of availableSupplies )
        2) contribute partially to a single entry (that may be added to Queue)


        ------------------------------------------
        Iterative -> solution for entry -> how many can be completed
            Input: entry, target materials & resources, 
            Output: produced items
                    update productionList and productionQ
                    returns True if built something
                    returns False if a partial build

        Precondition: 
                    
                    targetItemCosts values are more then entryUsedMaterials if
                            less then the buildMaterial entry is set to zero
                    targetItemCosts and materialsUsed require the same number 
                            of elements and the same order


        Postcondition: entry required to update finishedForThisTurn for existing
                         and any new entries



        Understand entry:


        --------- hasWorkBeenDone--------------- 
        >> has work been done? (on this entry?) 
            >>  has a partial work on a ship or item been done --> so that the remaining 
                material and resources left to complete 1 is less then the complete design costs

            >> if so & single entry -> produce the 1 with altered materials
            (for later) if so & multiple entry -> need to seperate out

        ------------------------------------- 

        -------- maximumHasBeenReached ------------
                    -- TODO --
        >> have I reached any maximum? (that would stop work on this entry)
        ------------------------------------- 

        -------- buildLimit ----------------------
        > Do I have the resources to complete the entry?
        >> Do I have the materials to complete the entry
        >>> buildLimit answers:
        >>> How many can be completed and what quantity is left over?
        > BuildLimit == 0
        >> then proportional materialsUsed based on availableSupplies
        ------------------------------------- 

        Produce n amount:
        ------------ buildEntry ------------------

        ------------------------------------------
        ------------ consumeMaterials ------------

        ------------------------------------------


        Resolve left over:


        """

        #DEBUG_3 = DEBUG_3
    

        entryObj = self.productionItems[entryID]
        entryQuantity = entryObj["quantity"]
        entryUsedMaterials = entryObj["materialsUsed"]
        entryType = entryObj["itemType"]
        entryFinished = entryObj["finishedForThisTurn"]
        entryDesignID = entryObj["designID"]



        completeAPartiallyWorkedOnEntry = ProductionQ.workHasBeenDone(entryObj) # returns T/F

        ###### Understand entry:  ########

        # --TODO-- have I reached any maximum? (that would stop work on this entry)

        if DEBUG_3: print("entryController: entryID: %s targetItemCosts %s " % (entryID, targetItemCosts))

        """
        # ------------ check whether work has been done -------
        # Assume this is covered by input from xFile and handled later entry controller      
        # if entryQuantity > 1 and ProductionQ.workHasBeenDone(entryObj):
            
        #     if buildQuantity >= 1:
        #         # build a single item, decrement current item, quantity -= 1,  zero out materials used
        #         # return  (p_Controller should restart at zero)
        #         pass
        # ----------------------------------------------------- 
        """       
        if DEBUG_3:print("\tworkHasBeenDone:%s" % completeAPartiallyWorkedOnEntry)
        if completeAPartiallyWorkedOnEntry:

            quantityONE = 1

            # remaining costs for a partially worked on entry.
            tmpTargetCosts = [(targetItemCosts[x] - entryUsedMaterials[x]) for x in range(0,len(targetItemCosts))]
            
            for i in range(0, len(tmpTargetCosts)):
                if tmpTargetCosts[i] < 0: tmpTargetCosts[i] = 0

            # check - if miniturization reduces the remaining costs so that nothing more is needed. 
            #   a way to handle this border case is needed. (limit will return zero)
            if DEBUG_3: print("entryController: completing a partially worked on item - payload sent to buildLimit: %d : %s " % (quantityONE, tmpTargetCosts))
            buildQuantity, buildMaterials = self.buildLimit(quantityONE, tmpTargetCosts)    


        else:

            if DEBUG_3: print("entryController: payload sent to buildLimit - quantity: %d : costs: %s " % (entryQuantity, targetItemCosts))
            buildQuantity, buildMaterials = self.buildLimit(entryQuantity, targetItemCosts)


        #remainingQuantity = entryQuantity - buildQuanity

        ########## Produce Entry && Cleanup  ###########

        if buildQuantity > entryQuantity:
            raise ValueError("ProductionQ.entryController: buildQuantity(%d) greater then entryQuantity(%d)" % (buildQuanity, entryQuantity))

        if buildQuantity > 0:   # buildQuantity cap is entryQuantity 
            
            if DEBUG_3: print("entryController: buildQuantity:%d  designID:%s with costs: %s " % (buildQuantity, entryDesignID, buildMaterials))

            self.buildEntry(entryType, buildQuantity, entryDesignID)
            self.consumeMaterials(buildMaterials)


            entryObj["quantity"] -= buildQuantity
            entryObj["materialsUsed"] = [0, 0, 0, 0]

            if entryObj["quantity"] == 0:
                entryObj["finishedForThisTurn"] = True

            elif entryObj["quantity"] < 0:
                raise ValueError("ProductionQ.entryController: after buiding %d %s; entry 'quantity' is %d" % (buildQuanity,entryObj["productionID"], entryObj["quantity"] ))
            

            return  

        elif buildQuantity == 0:
            # self.buildLimit() will return a proportional amount of materialsUsed.
            if DEBUG_3: print("entryController: buildQuantity:%d  designID:%s with costs: %s " % (buildQuantity, entryDesignID, buildMaterials))


            # for partialProduction ==> this amount is added to the entry["materialsUsed"] 
            for i in range(0, len(entryObj["materialsUsed"])):
                entryObj["materialsUsed"][i] += buildMaterials[i]

            self.consumeMaterials(buildMaterials)

            # cannot do any more with this entry this turn
            entryObj["finishedForThisTurn"] = True
            
            return 
        
        else:  # if a negative value should be an error condition
            
            #entryObj["finishedForThisTurn"] = True
            print("ProductionQ.entryController(Error): buildQuantity is negative")
            
            return 



    def buildEntry(self, entryType, buildQuantity, entryDesignID = None):
        """
        instructs build methods to create produced items.

        input: itemType & number to build
        output: calls the approprate produceN method with buildQuantity. 

        --TODO-- use try block

        """

        self.entrybuildtype = entryType
        self.entrybuildquantity = buildQuantity
        print("ProductionQ.buildEntry: itemType:%s  quantity: %d" %(entryType, buildQuantity))

        if entryType == "Mines":
            self.produceMines(buildQuantity)
        elif entryType == "Factories":
            self.produceFactories(buildQuantity)
        elif entryType == "Ship":
            self.produceShip(buildQuantity, entryDesignID)
        elif entryType == "Starbase":
            self.produceStarbase(buildQuantity, entryDesignID)
        else:
            print("ProductionQ.buildEntry: nothing to build")





    def consumeMaterials(self, consumeMaterials):
        """
        used to reduce elements like iron,bor,germ according to buildQuantity


        """

        tmpMinerals = consumeMaterials[:-1]
        tmpResources = consumeMaterials[-1]

        print("ProductionQ.consumeMaterials: consumeMaterials: %s \ntmpMinerals: %s  tmpResources: %d  test_ResourcesConsumed: %d" % (consumeMaterials, tmpMinerals, tmpResources, self.test_ResourcesConsumed))
        
        self.test_ResourcesConsumed += tmpResources
        self.resources -= tmpResources
        print("test_ResourcesConsumed: %d" % (self.test_ResourcesConsumed))

        self.colony.planet.removeSurfaceMinerals(tmpMinerals)



    
    def buildLimit(self, quantity, targetMaterials):
        """ buildLimit
        will examine the costs associated with an entry. It will answer the 
        question, how many of this entry can be built.

        input: self, materials, quantity
        output: 
            if limitQuantity > 0:
                buildQuantity, [total material cost used]
            if limitQuantity == 0:
                0 , [proportionalRemainder materials]

        precondition: partially produced items cannot have quantity > 1
                        ProductionQ.resources have been updated (in productionController)

        """
        

        availableSupplies = [self.colony.planet.surfaceIron,
                            self.colony.planet.surfaceBor,
                            self.colony.planet.surfaceGerm,
                            self.resources]

        if DEBUG_2: print("buildLimit: targetMaterials(%s) :: availableSupplies(%s) " % (targetMaterials, availableSupplies))

        limitQuantity, limitMaterials = ProductionQ.limit(quantity, targetMaterials, availableSupplies)

        
        if limitQuantity == 0:
            limitMaterials = ProductionQ.proportionalRemainder(targetMaterials, availableSupplies)

        if DEBUG_2: print("buildLimit: Quantity(%d) & Materials(%s) " % (limitQuantity, str(limitMaterials)))


        return limitQuantity, limitMaterials




    @staticmethod
    def proportionalRemainder(targetMaterials, availableSupplies):
        """
        The entry controller is to build as much of the Q as possible in the 
        specified order. If the entry is not totally produced - then a single 
        entry will be added to the Q - which will contain a proportional amount 
        of materials and resources allocated to complete the single entry. 

        input:neededMaterials, availableSupplies
        output: amount of materials to be used proportional to the 

        precondition: 
            no entry is < 0

        Postcondition: 
            returns a list of integers 


        Note: Could use a lot of work. 


        """

        #--TODO-- Fix proportionalRemainder. Resources to material use must be proportional

        # resources to sum(minerals)
        # sum(minerals) to resources

        if DEBUG_3: print("proportionalRemainder: targetMaterials: %s  availableSupplies: %s" % (targetMaterials,availableSupplies))

        ZERO = 0
        tmpProportional = [ZERO for i in targetMaterials]

        # gathers the lesser of needed material vs available material
        for i in range(0, len(targetMaterials)):
            tm = targetMaterials[i]
            am = availableSupplies[i]

            if tm >= am:
                tmpProportional[i] = am 
            else:
                tmpProportional[i] = tm

        if DEBUG_3: print("FIX_ME\tproportionalRemainder: %s" % tmpProportional)

        return tmpProportional

    @staticmethod
    def limit(quantity, neededMaterials, availableSupplies):
        """ limit
        input: quantity, neededMaterials, availableSupplies
        output: quantityToBuild, [ total MaterialsToBeUsedToBuild ] 

        conditions:
            quantities <= 0 return ZERO
            values should be integers, 
            values should be positive

        note: limit is decoupled from buildLimit for testing purposes.
        """

        
        ZERO = 0
        ONE = 1

        if DEBUG: print("----testing productionQ limit -----\n%d:%s availableSupplies:(%s)" %(quantity, str(neededMaterials), str(availableSupplies)))
        tmpMax = quantity
        tmpMin = 0
        tmpBestSoFar = 0

        # ---------- zero in quantity or in neededMaterials ---------
        # quantity requested should be greater then 0
        # neededMaterials should have at least 1 item greater then 0.
        #
        zeroNeededMaterials = ProductionQ.suppliesAreSufficient(neededMaterials, [each * ZERO for each in neededMaterials])
        #
        #
        if quantity <= 0:  #  or if quantity <= 0 and zeroNeededMaterials
            return ZERO, [each * ZERO for each in neededMaterials]
        
        elif quantity == ONE & zeroNeededMaterials: # used materials are more then is necessary to complete item.
            return ONE, [each * ZERO for each in neededMaterials]
        
        elif zeroNeededMaterials:    # means all neededMaterials were 0 and quantity is greater then 1
            return ZERO, [each * ZERO for each in neededMaterials]
        #
        # --------------------------------------------------------



        #-------test to determine if availableSupplies can cover entire entry ----
        # Without having to run the binary search
        # add code here
        #------------------------------------------------------------------------


        while 1:

            tmpMid = (tmpMax + tmpMin) // 2
            tmpMaterials = [each * tmpMid for each in neededMaterials]


            if DEBUG: print("max:%d; min:%d; mid:%d; %s; tmpBestSoFar:%d" % (tmpMax, tmpMin, tmpMid, str(tmpMaterials), tmpBestSoFar))



            if tmpMax < tmpMin:
                return tmpBestSoFar, [each * tmpBestSoFar for each in neededMaterials]

            if DEBUG: print("in_limit availableSupplies:%s" % availableSupplies)
            sufficient = ProductionQ.suppliesAreSufficient(tmpMaterials, availableSupplies)
            
            if DEBUG: print("sufficient:%s" % sufficient)
 


            if sufficient and tmpMid == quantity:
                return tmpMid, tmpMaterials
            
            elif sufficient:
                tmpMin = tmpMid + 1
                tmpBestSoFar = tmpMid
            
            else:
                tmpMax = tmpMid - 1


    @staticmethod
    def suppliesAreSufficient(targetSupplies, availableSupplies):
        """
        availableSupplies are available for production. Each one needs to 
        exceed targetSupplies. If even one targetSupplies values is higher then 
        availableSupplies that means there are not enough resources available to
        complete the productionQ entry. 

        """
        
        #print("targetSupplies:\t\t%s\navailableSupplies:\t\t%s" % (str(targetSupplies), str(availableSupplies)))

        for i in range(0, len(availableSupplies)):
            #print("t:(%s) :: a(%s)" % (targetSupplies[i], availableSupplies[i]))

            if targetSupplies[i] <= availableSupplies[i]:
                
                continue
            else:
                # targetSupplies are greater then available supplies.
                #print("suppliesAreSufficient: False")
                return False

        # all target supplies were found to be less then availableSupplies.
        #print("suppliesAreSufficient: True")
        return True


    @staticmethod
    def getCostsFromTechTree(techTree, techItem):
        pass


    def partialProduction(self, entry):
        """
        input: self, entry in list 
        output: entry is partially produced, materials and resources are partially used,
                    figure out portion of entry to complete.
            what percentage can be used in construction?

        """
        pass

    def updateQCosts(self):
        """
        Q persists across turns, but the cost of ships\starbases will change due to tech changes or redesign,
        not sure how to change the dict of items in the prodQ list with changes to ship designs?

        also need to change costs of design of starbase if upgrading
        """
        pass

    def produceAutoMinerals(self):
        """
        may be the same as produceMinerals. The auto part may be handled in the 
        controller

        """
        pass

    def produceMinerals(self):
        """
        using resources to 'alchemy' minerals
        """

        pass
    
    def produceDefault(self):
        """
        if items on the list cannot be produced because of a need for 

        """
        pass



    def produceShip(self, quantity, designID):
        """
        produces ShipDesign, instantiates Token, looks for available fleet that 
        Token can be added to. If no available fleet, generate fleet. 

        #     precondition:   quantity - number of design to add to token
        #                     design - token design to add to fleet
        #                     colony/planet (planet provides (xy) and universeID)

        #     postcondition:  a fleet object created with colony location & added to fleets

        """

        #--TODO-- spacedock capacity needs to be checked in buildEntry - or earlier - to determine if ship can be built

        newFleetID = self.player.fleetCommand.generateFleetID()
        xy = self.colony.planet.xy
        universeID = self.colony.planet.getPrefex() # universeID where the ship is built

        spaceObjectID = str(self.player.playerNumber) + "_" + str(newFleetID)
        newFleet = FleetObject(self.player, spaceObjectID, xy, universeID)
        newFleet.fleetOrderNumber = newFleetID  # can be generated by the SpaceObjectID

        # add Token to Fleet
        newToken = Token(designID, quantity)
        newFleet.tokens[designID] = newToken

        #add orders reference
        newFleetOrders = FleetOrders(newFleet)
        #self.player.fleetCommand.addFleetOrders(newFleetID, newFleetOrders)
        self.player.fleetCommand.addFleet(newFleetID, newFleet)

        #create new fleet object in universe
        self.colony.planet.universe.addPlayerFleets(spaceObjectID, newFleet)

        if DEBUG_2: print("ProductionQ.produceShip(): key:%s xy(%s) universeID:%s spaceObjectID:%s \n %s " % (newFleetID, xy, universeID, spaceObjectID, newFleet.__dict__))
        


    def produceStarbase(self, quantity, designID):
        """produces starbase, instantiates Token, assigns to Colony. """
        

        newStarbaseID = str(self.colony.planet.ID) + "_" + str(self.player.playerNumber)
        xy = self.colony.planet.xy
        universeID = self.colony.planet.getPrefex()

        newStarbase = Starbase(self.player, newStarbaseID, xy, universeID, self.colony.planet.ID)

        # self.test_ship += 1

        # add Token to Fleet
        newToken = Token(designID, quantity)
        newStarbase.tokens[designID] = newToken

        #--TODO-- update Starbase values like SpaceDock capacity, etc.

        self.colony.planet.orbitalStarbase = newStarbase
        


    def producePlanetaryInstallation(self):
        """
        'Scanner', 'Defenses'

        """
        pass

    def producePlanetUpgrades(self):
        """
        'Terraform', 'Minerals'

        """
        pass

    def produceSpecial(self):
        """ 
        like the MT Genesis device

        """
        pass

    def produceMines(self, quantity):
        """
        produce Mines on a planet
        """

        self.colony.planet.mines += quantity

    def produceFactories(self, quantity):
        """

        """

        self.colony.planet.factories += quantity





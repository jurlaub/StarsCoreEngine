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


class ProductionQ(object):
    """ ProductionQ
    One ProductionQ object should exist for each colony object.


    """
    DEBUG = True

    itemType = ('Ship', 'Starbase', 'Scanner', 'Defenses', 'Mines', \
                 'Factories', 'Terraform', 'Minerals','Special')

    defaultSetting = ()     # default options for all Q's

    def __init__(self, colony, player):         # defaultSetting may not be necessary.
        

        #self.productionList = [] # shipDesigns + starbaseDesign + planetInstallations + autoBuild
        self.colony = colony
        self.research = player.research
        self.raceData = player.raceData
        self.designs = player.designs

        self.prodQueue = []
        self.ExcludedFromResearch = False
        self.customDefaultSettings = []

        self.resources = 0
        self.productionOrder = []   # each order should point to a unique item  
        self.productionItems = {}   # 


        

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

        DEBUG = ProductionQ.DEBUG

        colonyQOrders = colonyQ["productionOrder"]  # list
        colonyQItems = colonyQ["productionItems"]   # contents

        colonyQOrders_QAdditions = []

        if DEBUG: print("NewOrders:\n%s\n%s" % (colonyQOrders,colonyQItems))
        if DEBUG: print("ExistinOrders:\n%s\n%s" % (self.productionOrder, self.productionItems))

        # find items in productionQ not in the new ProductionQ orders
        tmpRemoveFromCurrentQ = set(self.productionOrder).difference(colonyQOrders)
        if DEBUG: print("set:%s" % tmpRemoveFromCurrentQ)


        # update the productionItems "quantity" = 0 for entries to remove -> because they do not exist in the new queue
        for each in tmpRemoveFromCurrentQ:
            if DEBUG: print("%s set to Zero" % each)
            self.setQuantityToZero(each)

        # New orders are added or update existing ProductionQ
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
            # Items-exist (T|T)
            if each in self.productionItems and each in colonyQItems:
                # update Queue
                targetItem = colonyQItems[each]
                existingItem = self.productionItems[each]

                # if the new orders set the order to 0, 
                if ProductionQ.elementHasUnexpectedValue(targetItem):
                    #print("unexpected object - skipping")
                    continue

                elif targetItem["quantity"] < 1:
                    existingItem["quantity"] = 0
                    continue

                # work has not been done
                if not ProductionQ.workHasBeenDone(existingItem):
                    
                    # replace existing item's quantity 
                    existingItem["quantity"] = targetItem["quantity"]
                
                # work has been done
                else:
                    
                    if targetItem["quantity"] == 1:
                        # should not be a possibilty - work should only be done on an individual item
                        # or the above test did not work. either way should not change
                        continue
                    
                    else:
                        # quantity < 1 & == 1 checked earlier. Value must be greater than 1                        
                        targetItem["quantity"] -= 1 
                        
                        tmpNewEntry = {each : targetItem}
                        tmpNewIndex = eachIndex + 1

                        #>> add a new entry to items, insert new Order immediately after the quantity 1 item
                        self.addToQueue(tmpNewEntry, tmpNewIndex)
                        
                        if DEBUG: print("In the addToQueue area:\n%s" % (self.productionOrder))

                        #  
                        tmpNewKey = self.productionOrder[tmpNewIndex]
                        
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
                if DEBUG: print("index%d- Order:%s # Items-exist (T|F)" % (eachIndex, each))


                continue

            # # Items-exist (F|T)
            elif each not in self.productionItems and each in colonyQItems:
                
                if ProductionQ.elementHasUnexpectedValue(colonyQItems[each]):
                    #print("unexpected object - skipping")
                    continue

                v = { each : colonyQItems[each] }
                self.addToQueue(v)
            
            # Items-exist (F|F)
            else:
                # take no action, should not have reached this spot
                #raise ValueError()
                ra = ("addToQueueFromXFile - reached area that should not be reached - Items-exist (F|F) case")
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
            DEBUG = ProductionQ.DEBUG

            if len(entryDict) != 1:
                raise ValueError("addToQueue requires entryDict to a dictionary with 1 key:value entry. %d detected" % len(entryDict))

            entryKey, entryObj = entryDict.popitem()

            # --TODO-- find ItemType method
            
            tmpItem = { "quantity" : entryObj["quantity"], 
                        "productionID" : entryObj["productionID"],
                        "finishedForThisTurn" : False,
                        "itemType":"itemType Ship",
                        "materialsUsed" : [0, 0, 0, 0]
            }           


            tmpKey = self.obtainNewKey(entryKey)

            if DEBUG: print("addToQueue at %s- %s:%s " % (insertOrder, tmpKey, tmpItem))

            if insertOrder and insertOrder < len(self.productionOrder):
                # if insertOrder >= len(self.productionOrder):
                #     self.productionOrder.append(tmpKey)
                # else:
                print("at insert")
                self.productionOrder.insert(insertOrder, tmpKey)


            else:
                print("at append")
                self.productionOrder.append(tmpKey)


            self.productionItems[tmpKey] = tmpItem

            #print("%s \n %s" % (self.productionOrder, self.productionItems))


        except NameError as ne:
            print("ProductionQ.addToQueue() is missing: %s" % ne )

        except ValueError as ve:
            print("%s" % ve)



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
            productionItems["quantity"] == 1; "work" should not be done when 
            quantity > 1

        Work can be done on an existing item:
        > quantity set to 0
        > quantity @ 1

        if quantity > 1 work should not have been done.



        """
        try:
            # quan
            correctQuantity = True


            if existingItem["quantity"] > 1 or existingItem["quantity"] < 0:
                correctQuantity = False

            for each in existingItem["materialsUsed"]:

                # if materials have been used (not 0) then the quantity should be 1
                if each != 0:

                    if not correctQuantity:
                        # have a value in the materialsUsed and quantity is greater then 1 or negative
                        raise ValueError("ProductionQ.hasWorkBeenDone: materialsUsed and quantity not aligned. materialsUsed can only be greater then 0 when quantity = 1")
                    
                    else:
                        # materials have been used and the quantity of the item is 1
                        return True  
                
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
        DEBUG = ProductionQ.DEBUG

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
        

    def productionController(self):
        """
        The productionController is used to 'parse' through the production list == self.prodQueue 
        
        1) It identifies the amount of resources that can be used for production 
        (Calling the self equivalent of Research.colonyResearchTax(colony) method to obtain the # 
        of resources available )
        
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
            Once 
              produced the 'n' value should be decremented. If '0' then proceed
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
       





        """

        autobuildMinerals = False       # for minerals if needed.

        #res = 0


        # obtain from colony the number of resources for production (Note: minus research tax)
        if self.ExcludedFromResearch:
            self.resources  = self.colony.totalResources
        else:
            self.resources  = self.research.colonyResourcesAfterTax(self.colony)

        # handle the produceAutoMineral setting?

        orderIndex = 0 

        # All orders "finishedForThisTurn" == False

        while True:

            orderLength = len(self.productionOrder)
            
            if self.resources < 1:  # resources left
                break
            
            elif orderIndex >= orderLength:  # reached empty or end of order
                break

            
            entryID = self.productionOrder[orderIndex]
            entryObj = self.productionItem[entryID]

            if entryObj["finishedForThisTurn"] == True:
                orderIndex +=1
                continue

            # is entry an Autobuild type? 
            # add check for autobuild type   entryObj["itemType"]
            # if autobuildMinerals == True set the autobuildMinerals = True

            targetItemCosts = self.targetItemCosts(entryID)

            self.entryController(entryID, targetItemCosts)
            
            # if entryController adds an item to the productionOrder/Items,
            # then start over at the beginning. Reasons include: autobuild orders, ?
            # note: entryController should set items to "finishedForThisTurn"
            if orderLength == len(self.productionOrder):
                #no change in entry controller
                orderIndex += 1         # entry completed then increment 
            else:
                orderIndex == 0         # start at beginning


    def targetItemCosts(self, entryID):

        pass

        
    def entryController(self, entryID, targetItemCosts, autobuildMinerals = False):
        """



        ------------------------------------------
    Iterative -> solution for entry -> how many can be completed
        Input: entry, target materials & resources, 
        Output: produced items
                update productionList and productionQ

        Precondition: targetItemCosts values are more then entryUsedMaterials if less then buildMaterial entry set to zero
        Postcondition: entry required to update finishedForThisTurn for existing
                         and any new entries



    Understand entry:
        >> have I reached any maximum? (that would stop work on this entry)
        
        >> has work been done? (on this entry?) 
            >> if so & single entry -> produce the 1 with altered materials
            (for later) if so & multiple entry -> need to 


        -------- buildLimit ----------------------
        > Do I have the resources to complete the entry?
        >> Do I have the materials to complete the entry
        >>> buildLimit answers:
        >>> How many can be completed and what quantity is left over?
        ------------------------------------- 

    Produce n amount:
        ------------ buildEntry ------------------

        ------------------------------------------
        ------------ consumeMaterials ------------

        ------------------------------------------


    Resolve left over:

        >>>> if quantity >= 2: create 1 single entry at beginning, current results in a single entry. 
        >>>> if quantity == 1:  use as many resources as possible (by percentage rules), break
        

        >>>> if no -> (does the Q need to autobuild minerals? if yes, add to beginning, continue) 
                    -> use as many resources and materials as are available, update ironUsed etc.
        
    
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


        ------------------------------------------
        obtain entry
    
        > obtain target materials and resources (access to colony.planet, raceData, research, PlayerDesign)
        count = 0

            

        if count greater then 0:
            produce that many of object
            quantity = quantity - count
            minerals & resources decremented

        # iron = self.colony.planet.surfaceIron
        # bor  = self.colony.planet.surfaceBor
        # germ = self.colony.planet.surfaceGerm


        """

        entryObj = self.productionItems[entryID]
        entryQuantity = entryObj["quantity"]
        entryUsedMaterials = entryObj["materialsUsed"]
        entryType = entryObj["itemType"]

        completeAPartiallyWorkedOnEntry = ProductionQ.workHasBeenDone(entryObj)

        # Understand entry:

        # have I reached any maximum? (that would stop work on this entry)
        
        if completeAPartiallyWorkedOnEntry:
        # ------------ check whether work has been done -------
        # Assume this is covered by input from xFile and handled later entry controller      
        # if entryQuantity > 1 and ProductionQ.workHasBeenDone(entryObj):
            
        #     if buildQuantity >= 1:
        #         # build a single item, decrement current item, quantity -= 1,  zero out materials used
        #         # return  (p_Controller should restart at zero)
        #         pass
        # -----------------------------------------------------

            quantityONE = 1
            tmpTargetCosts = [(targetItemCosts[x] - entryUsedMaterials[x]) for x in range(0,len(targetItemCosts))]
            
            for i in range(0, len(tmpTargetCosts)):
                if tmpTargetCosts[i] < 0: tmpTargetCosts[i] = 0

            buildQuantity, buildMaterials = self.buildLimit(quantityONE, tmpTargetCosts)        

        else:

            buildQuantity, buildMaterials = self.buildLimit(entryQuantity, targetItemCosts)




        # produce n amount
        if buildQuantity > 0:
            
            self.buildEntry(entryType, buildQuantity)
            self.consumeMaterials(buildMaterials)

        else:
            # set entry["finishedForTurn"] == True
            return

        # resolve left over

        if completeAPartiallyWorkedOnEntry:
            pass
        else:
            pass


        

    
    def buildEntry(self, entryType, buildQuantity):

        pass

    def consumeMaterials(self, consumeMaterials):
        """
        used to reduce elements like iron,bor,germ to what is available.

        """
        pass


    
    def buildLimit(self, quantity, targetMaterials):
        """ buildLimit
        will examine the costs associated with an entry. It will answer the 
        question, how many of this entry can be built.

        input: self, materials, quantity
        output: buildQuantity, [total material cost used]

        precondition: partially produced items cannot have quantity > 1
                        ProductionQ.resources have been updated (in productionController)

        """
        DEBUG = ProductionQ.DEBUG

        availableSupplies = [self.colony.planet.surfaceIron,
                            self.colony.planet.surfaceBor,
                            self.colony.planet.surfaceGerm,
                            self.resources]


        limitQuantity, limitMaterials = ProductionQ.limit(quantity, targetMaterials, availableSupplies)

        if DEBUG: print("buildLimit: Quantity(%d) & Materials(%s) " % (limitQuantity, str(limitMaterials)))

        return limitQuantity, limitMaterials


    @staticmethod
    def proportionalRemainder(neededMaterials, availableSupplies):
        """
        The entry controller is to build as much of the Q as possible in the 
        specified order. If the entry is not totally produced - then a single 
        entry will be added to the Q - which will contain a proportional amount 
        of materials and resources allocated to complete the single entry. 

        input:neededMaterials, availableSupplies
        output: amount of materials applied to a single 


        

        proportionalCompletion
        minerals are summed 
        sum of minerals / resources


        """

        pass

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

        DEBUG = ProductionQ.DEBUG
        ZERO = 0

        if DEBUG: print("----testing productionQ limit -----\n%d:%s availableSupplies:(%s)" %(quantity, str(neededMaterials), str(availableSupplies)))
        tmpMax = quantity
        tmpMin = 0
        tmpBestSoFar = 0

        # ---------- zero in quantity or in neededMaterials ---------
        zeroNeededMaterials = ProductionQ.suppliesAreSufficient(neededMaterials, [each * ZERO for each in neededMaterials])
 
        #if DEBUG: print("zeroNeededMaterials(%s):" % (zeroNeededMaterials ))

        if quantity <= 0:
            return ZERO, [each * ZERO for each in neededMaterials]
        elif zeroNeededMaterials:
            
            return ZERO, [each * ZERO for each in neededMaterials]
        # --------------------------------------------------------

        #-------test to determine if availableSupplies can cover entire entry ----
        # add code here
        #------------------------------------------------------------------------


        while True:

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



    def produceShip(self):
        """
        produces ShipDesign, instantiates Token, looks for available fleet that 
        Token can be added to. If no available fleet, generate fleet. 

        """

        pass

    def produceStarbase(self):
        """produces starbase, instantiates Token, assigns to Colony. """
        pass


    def producePlanetaryInstallation(self):
        """
        'Scanner', 'Defenses'

        """
        pass

    def producePlanetUpgrades(self):
        """
        'Mines', 'Factories', 'Terraform', 'Minerals'

        """
        pass

    def produceSpecial(self):
        """ 
        like the MT Genesis device

        """
        pass







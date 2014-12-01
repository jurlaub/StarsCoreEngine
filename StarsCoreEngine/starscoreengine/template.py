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
from .player import RaceData




# -- define the universe data in a standard values object, similar format, 
class StandardGameTemplate(object):
    """
    StandardGameTemplate is a class for generating a standard universe. 
    
    The standard universe data can be modified by passing in a dictionary 
    containing key:value pairs which will be used to update the standard values.

    Use the provided command line arguments to create a custom universe file as 
    well as modify/add technology. 

    """
    '''
    #u_name = ["Prime", "Alpha", "Beta", "Gamma", "Delta", "Omega", "Zeta"]

    planet_density = (.5, 1, 1.5) 
    planets = 10
    standard_universe_size_small = {"UniverseSizeXY":(200,200)}
    standard_universe_size_medium = {"UniverseSizeXY":(600,600)}
    standard_universe_size_large = {"UniverseSizeXY":(1000,1000)}

    standard_universe = {"UniverseNumber":1, "UniverseSizeXY": (200,200), \
    "UniverseName":("Prime"), "UniversePlanets":planets, \
    "PlanetDensity": planet_density[1], "Players":(1)}
    '''

    # instantiate the standard object
    #                           customUniverse = {}, customTech = {}, customVC = {}
    def __init__(self, game_name = None, playerFileList = [], setupDict = {}, universeNumber = 1):
        # instantiates a new game dictionary while merging setup data
        
        # self.game_name = game_name # "rabid_weasels"
        if not game_name:
            self.game_name = "rabid_weasels"
        else:
             self.game_name = game_name # "rabid_weasels"

        self.planet_names = planetNameTemplate()
        self.starting_population = 50000
        self.universeNumber = int(universeNumber)
        self.universe_data = []    # list of universe dictionary data

        #self.technology_data       #template would have technology
        #self.victory_conditions    # standard VC template with changes        


        # ---- HARDCODED =>> requires updating custom setup
        # -- TODO --- Template grabs data from r1 files
        self.players_data = self.getPlayerRaceFile(playerFileList)    # list of player race file names 
        self.player_by_universe = None  # method to sort players into respective universes



        if universeNumber < 1:
            sys.exit("universeNumber must be greater then 1")
        else:

            for i in range(0, int(universeNumber)):
                x = self.standardUniverse()
                x['UniverseNumber'] = i

                #merge setupDict (the customized dictionary) with standard
                if setupDict:
                    tmp_universe = 'UniverseNumber' + str(i)
                    customUniverseObject = setupDict[tmp_universe]

                    x = self.mergeDictionaryData(x, customUniverseObject)

                self.universe_data.append(x)          # NOTE: appending to a list
                


    def standardUniverse(self):
        # standard universe comprises standard settings for 1 universe.

        standard_universe = {"UniverseNumber":0, "UniverseSizeXY": (200,200), \
        "UniverseName": "Prime", "UniversePlanets":6, "Players":1}
        
        return standard_universe

    @classmethod
    def homeworld():
        iron = 78
        bora = 67
        germ = 79


    def mergeDictionaryData(self, dict1, dict2):
        '''
        input: dict1, dict2
        output: dict1

        if items in dict2 are in dict1, merge those items into dict1
        '''

        for n in dict2:
            if n in dict1:
                dict1[n] = dict2[n]

        return dict1

    def getPlayerRaceFile(self, fileList):
        # 'race name'.r1
        # look for all r1 files in folder
        # should match number of players
        raceObjects = []

        for each in fileList:

            #--- TODO  change from grabbing a dev race to grabbing a .r1 file
            # and turning it into a RaceData() object
            raceObjects.append(self.getDevRaceFile(each))

        return raceObjects

    def getDevRaceFile(self, raceName):
        # returns a development file that will substitute as a player race file

        return RaceData(raceName)














def getPlanetNameFromTemplate():
    planet_names = planetNameTemplate()
    count = len(planet_names)
    rand = random.randrange(0, count)
    
    return planet_names[rand]

def planetNameTemplate():
    planet_names = ["Fenge", "Fenris", "Shill", "239_Alf", "Wolf 359",
     "Dark Star", "Kirk", "Flo Rida", "Pluto", "Centari", "Mau Tai", "Zeta", 
     "Mars", "Babylon 5", "Quell", "Be Still My Heart", "Soft Light", "Piink",
     "Vertigo", "Verillon", "Camelot", "Too Much", "Avalon", "Quiver", "Otaah",
     "Shining Star", "Bamboo II", "Deralon", "Dark Tide", "Everlon", "Eeek!",
     "Exegenesis", "Et'Varloon", "Gallifrey", "Geronimo", "Gytalli", "Hilda",
     "Harriot's Star", "Indigo", "Intel", "Inner Peace", "Jester's Crown", 
     "Jykle", "Kelly's Eye", "Kirkland", "Katie", "Loomiss", "Lester Pike",
     "Mea Tal", "Martoon", "Marcross", "McKenny", "McDevitton", "Reynold's Star",
     "Heinland", "Stross", "Brust", "Mat'Etvel", "Nooon", "Nubia", "Never Land",
     "Narly", "Opal", "Oster Den", "Old One", "Ol' Yeller",  "Penelope's Star", 
     "Patrick's Way", "Pla'yet'Oh", "Pu Tai La", "Shei Gua", "Ping Loom", 
     "Q'atell", "007", "Bantha", "Betazoid", "Realist", "New Hope", "Recall",
     "Renovate This", "Sad Tide", "Sally Way", "Sol Two", "Shia Tell", "Aether",
     "Shitzu", "Sassyland", "Sardovia", "Telmarie", "Tennyson", "Termaso"
     "Terra", "Tar Rok", "Lok Tar", "Umbria", "Umbridge", "Unrepentant",
     "Unknown Star", "Un'Lo'Tek", "Ventillia", "Vargo II", "Vicktor's Star",
     "Vok'Ba", "Vot'Tark'Le", "Vessel", "Veree", "Ross 359", "Wolf Star", 
     "Wolf's Eye", "Moteland", "Wolfbane", "Transylvania", "Woe Tide", "Wode",
     "Woot", "Waco", "Wackyland", "Wat'up", "Wolfrik", "Yeet", "Yether",  "Yee",
     "Yent'il", "Yankee", "Coyote", "Yesterday", "Raster", "Xavier", "Xander",
     "Xandidu", "X-Factor", "Xidus", "Xtol", "Zeet", "Zak'To", "Zah'ha'dum", 
     "Zetherland", "Zoot", "4004da", "QWERTY",
    "007", "14 Coli", "3M TA3", "409", "555-1212", "668", "90210", "911", "98053", "A'po", "Abacus", "Abbott", "Abdera", "Abel", "Abrams", "Accord", 
    "Acid", "Adams", "Afterthought", "Ajar", "Albemuth", "Alcoa", "Alexander", "All Work", "Allegro", "Allen", "Allenby", "Almagest", "Almighty", "Alpha Centauri", "Alsea", "Aluminum", 
    "Amontillado", "America", "Andante", "Andromeda", "Angst", "Anthrax", "Apple", "Applegate", "April", "Aqua", "Aquarius", "Arafat", "Arcade", "Arctic", "Arcturius", "Argon", 
    "Ariel", "Aries", "Armonk", "Armstrong", "Arnold", "Arpeggio", "Asgard", "Astair", "Atropos", "Auriga", "Aurora", "Autumn Leaves", "Awk", "Axelrod", "Bach", "Baggy", 
    "Bagnose", "Baker", "Bakwele", "Balder", "Baldrick", "Ball Bearing", "Bambi", "Bar None", "Barbecue", "Barrow", "Barry", "Bart", "Basil", "Basket Case", "Bath", "Beacon", 
    "Beauregard", "Beautiful", "Bed Rock", "Beethoven", "Bentley", "Berry", "Beta", "Betelgeuse", "Bfe", "Bidpai", "Bilbo", "Bilskirnir", "Birthmark", "Black Hole", "Bladderworld", "Blinken", 
    "Bloop", "Blossom", "Blue Ball", "Blue Dwarf", "Blue Giant", "Blush", "Bob", "Boca Raton", "Boethius", "Bog", "Bonaparte", "Bone", "Bones", "Bonn", "Bonus", "Boolean", 
    "Bootes", "Borges", "Boron", "Bountiful", "Braddock", "Bradley", "Brass Rat", "Brin", "Bruski", "Buckshot", "Bufu", "Burgoyne", "Burrito", "Burrow", "Bush", "Buttercup", 
    "Caelum", "Cain", "Calcium", "Callipus", "Cambridge", "Cancer", "Candide", "Candy Corn", "Canis Major", "Canis Minor", "Canterbury", "Capricornus", "Captain Jack", "Carbon", "Carcassonne", "Carter", 
    "Carver", "Cassiopeia", "Castle", "Cathlamet", "Catnip", "Celery", "Celt", "Centaurus", "Cepheus", "Cerberus", "Ceres", "Cern", "Cetus", "Challenger", "Chamber", "Chandrasekhar", 
    "Chaos", "Charity", "Chennault", "Cherry", "Cherub", "Chinese Finger", "Chlorine", "Chopin", "Chubs", "Chunk", "Cinnamon", "Cirrus", "Clapton", "Clark", "Clatsop", "Clausewitz", 
    "Clay", "Climax", "Clinton", "Clotho", "Clover", "Cochise", "Coda", "Code", "Columbia", "Columbus", "Continental", "Contra", "Coolidge", "Cootie", "Copper", "Core", 
    "Corner", "Cornhusk", "Cornwallis", "Corvus", "Cosine", "Costello", "Cotton Candy", "Cougar", "County Seat", "Cousin Louie", "Covenant", "Coyote Corners", "Crabby", "Cramp", "Crazy Horse", "Crisp X", 
    "Croce", "Crow", "Crux", "Curley", "Custer", "Cygnus", "Dachshund", "Daily", "Daisy", "Dalmatian", "Darien", "Dark Planet", "Data", "Dave", "Dawn", "Dayan", 
    "Deacon", "Decatur", "Deep Thought", "Defect", "Delta", "Delta Delta Delta", "Demski", "Deneb", "Denikin", "Denon", "Desert", "Desolate", "Devo", "Devon IV", "Dewey", "Dharma", 
    "Diablo", "Diamond", "Diddley", "Dill Weed", "Dimna", "Dimple", "Dingleberry", "Dingly Dell", "Dinky", "Dipstick", "Discovery", "Distopia", "Ditto", "Dive", "Do Re Mi", "Dog House", 
    "Dollar", "Doodles", "Doris", "Double Tall Skinny", "Dowding", "Down And Out", "Draco", "Draft", "Dry Spell", "Dunsany", "Dwarte", "Dyson", "Early", "Earth", "Esher", "Eden", 
    "Eisenhower", "Elder", "Elephant Ear", "Elron", "Elsinore", "Emerald", "Emoclew", "Emperium Gate", "Empty", "Endeavor", "Eno", "Enterprise", "Epsilon", "Equuleus", "Erasmus", "Eridanus", 
    "Escalator", "Estes", "Esther", "Evergreen", "Excel", "Faith", "False Hopes", "Farragut", "Fez", "Finale", "Finger", "Fizbin", "Flaming Poodle", "Flapjack", "Fleabite", "Flint Stone", 
    "Fluorine", "Floyd", "Fluffy", "Flutter Valve", "Foamytap", "Foch", "Foggy Bottom", "Foresight", "Forest", "Forget-Me-Not", "Forgotten", "Forrest", "Forward", "Foucault's World", "Fox Trot", "Franklin", 
    "Frederick", "Frost", "Fubar", "Fugue", "Gaia 2", "Galbraith", "Gamma", "Gangtok", "Garcia", "Garfunkel", "Gargantua", "Garlic", "Garnet", "Garp", "Gas", "Gasp", 
    "Gates", "Gaye", "Gemini", "Genesis", "Grendel", "Genoa", "Geronimo", "Gertrude", "Gladiolus", "Gladsheim", "Glenn", "Globular Rex", "Godel", "Gold", "Gollum", "Goober", 
    "Goofy", "Gorby", "Gordon", "Gornic", "Gout", "Graceland", "Grant", "Grape", "Grappo", "Graz", "Green House", "Greenbaum", "Greene", "Grep", "Grey Matter", "Grim Reaper", 
    "Grouse", "Guano", "Guderian", "Gueneviere", "Gunk", "H2O", "H2SO4", "Hacker", "Haig", "Hal", "Halsey", "Hammer", "Happy", "Hard Ball", "Harding", "Harlequin", 
    "Harris", "Harrison", "Hawking's Gut", "Hay Seed", "Heart", "Heatwave", "Heaven", "Hedtke", "Helium", "Hell", "Henbane", "Hercules", "Hermit", "Heroin", "Hexnut", "Hiho", 
    "Hill", "Himshaw", "Hindsight", "Ho Hum", "Hodel", "Hoe", "Hoho", "Hollywood", "Homer", "Homogeneous", "Hoof And Mouth", "Hoover", "Hope", "Horselover Fat", "Hot Tip", "Hoth", 
    "Houdini", "Howe", "Hoze-O-Rama", "Huckleberry", "Hull", "Hummingbird", "Humus", "Hunt", "Hurl", "Hydra", "Hydrogen", "Hydroplane", "Hyperbole", "Icarus", "Ice Patch", "Iceball", 
    "Indy", "Inferno", "Infinity Junction", "Innie", "Insane", "Inside-Out", "Invisible", "Io", "Iodine", "Jerilyn", "Jersey", "Joffre", "Johnson", "Jones", "Jubitz", "June", 
    "Juniper", "Jupiter", "K9", "Kaa", "Kalamazoo", "Kalila", "Kan", "Kant", "Kappa", "Karhide", "Kearny", "Kennedy", "Kepler", "Kernel", "Kha Karpo", "Kidney", 
    "King", "Kirk", "Kirkland", "Kitaro", "Kitchener", "Kiwi", "Kline", "Kludge", "Knife", "Knob", "Squidcakes", "Kornilov", "Kosciusko", "Kruger", "Kulu", "Kumquat", 
    "Kutuzov", "Kwaidan", "La Te Da", "Lachesis", "Lafayette", "Lambda", "Larry", "Last Chance", "Latte", "Lavacious", "Lawrence", "Lazy B", "Le Petit Jean", "Lead", "Lead Pants", "Leaky Pipe", 
    "Lee", "Lekgolo", "Lemnitzer", "Leo", "Leo Minor", "Leonardo", "Lever", "Leviathan", "LGM 1", "LGM 2", "LGM 3", "LGM 4", "Lhasa", "Libra", "Limbo", "Lincoln", 
    "Lingo", "Linq", "Lisa", "Lithium", "Little Brother", "Little Sister", "Liver", "Lizard's Beak", "Loan Shark", "Logic", "Loki", "Longstreet", "Lopsided", "Love", "LSD", "Lube Job", 
    "Luigi", "Lukundoo", "Luscious", "Lycra", "Lynx", "Lyra", "M16", "MacArthur", "Macintosh", "Macrohard", "Magellan", "Maggie", "Mallard", "Mamie", "Mana", "Mandelbrot", 
    "Mandrake", "Maple Syrup", "Marge", "Marion", "Marla", "Marlborough", "Mars", "Marshall", "Match", "Mathilda", "Maude", "May", "Mayberry", "McBride", "McCartney", "McClellan", 
    "McFarquardt", "McIntyre", "Me", "Meade", "Medusa", "Melthorne", "Memmon", "Memos", "Mercury", "Midgard", "Midnight", "Milky Way", "Mirror", "Misery", "Mitchell", "Mobius", 
    "Mocha", "Moe", "Mohlodi", "Molalla", "Moltke", "Molybdenum", "Money", "Mongo", "Montcalm", "Montgomery", "Moonbeam", "Morgan", "Moscow", "Mother", "Mountbatten", "Mozart", 
    "Mu", "Klaupaucius", "Mundus", "Mungle", "Murat", "Muskrat", "Muspell", "Mustang", "Myopus", "Nada", "Nadir", "Naledi", "Narnia", "Nastrond", "Nawk", "Nebulae", 
    "Neil", "Nelson", "Neon", "Neptune", "Nerd", "Nessus", "Nether Region", "Neuronos", "Neuter", "Never Never Land", "Nivenyrral", "New", "New Kalapuya", "Ney", "Nickel", "Niflheim", 
    "Nifty", "Nimitz", "Nipso", "Nirvana", "Nitrogen", "Triffid", "No Exit", "No Play", "No Respect", "No Return", "No Vacancy", "Noble Impulse", "Nod", "Nope", "Norm", "Notlob", 
    "Notorious", "Nova", "Novelty", "Nowhere", "Nu", "Nylon", "Oasis", "Oh Ho Ho", "Old", "Ollie", "Olympia", "Omega", "Oop Be Gone", "Opus 10", "Orange", "Orbison", 
    "Oregano", "Orion", "Oshun", "Outie", "Oxygen", "Ozone", "Panacea", "Pansy", "Paradise", "Parsley", "Patton", "PCP", "Pearl", "Peat Moss", "Peekaboo", "Pegasus", 
    "Penance", "Penzance", "Pantagruel", "Perry", "Perseus", "Pershing", "Pervo", "Petra", "Phaeton", "Pheson", "Phi", "Phicol", "Philistia", "Pi", "Pickett", "Pickles", 
    "Pilgrim's Harbor", "Pin Prick", "Pinball", "PiR2", "Pirate", "Pisces", "Pitstop", "Prydun", "Planet 10", "Planet 9", "Planet X", "Pluto", "Poly Gone", "Poly Siren", "Pop", "Potassium", 
    "Pound", "Presley", "PreVious", "Provo", "Prude", "Prune", "Puberty", "Puddn'head", "Puma", "Purgatory", "Puss Puss", "Putty", "Pyxidis", "Qaphqa", "Quark", "Quarter", 
    "Quiche", "Quick Lick", "Quixote", "Radian", "Radish", "Radium", "Raisa", "Raisin", "Rake", "Raster", "Raven's Eye", "Reagan", "Recalc", "Red Ball", "Red Dwarf", "Red Giant", 
    "Red Storm", "Redemption", "Redmond", "Register", "Relight", "Replica", "Resistor", "Resort", "Revelation", "Rex", "Rhenium", "Rho", "Ricketts", "Rickover", "Right", "Ripper Jack", 
    "Rock", "Rockette", "Rodney", "Rogers", "Romeo", "Rommel", "Roosevelt", "Rough Shod", "Rubber", "Ruby", "Rundstedt", "Rutebaga", "Rye", "Saada", "Sad", "Saddam", 
    "Sadie", "Sagittarius", "Salamander", "Salsa", "Sam", "Same Here", "Samsonov", "Sand Castle", "Sands Of Time", "Sapphire", "Sartre", "Saturn", "Scandahoovia", "Scarlett", "Scat", "Schubert", 
    "Schwiiing", "Scorpius", "Scotch", "Scott", "Scotts Valley", "Scotty", "Scud", "Scurvy", "Sea Squared", "Sed", "Selenium", "Senility", "Sequim 3", "Serapa", "Shaft", "Shaggy Dog", 
    "Shangri-La", "Shank", "Shannon", "Shanty", "Scheherezade", "Shelty", "Sheridan", "Sherman", "Shinola", "Ship Shape", "Shoe Shine", "Shrine", "Siberia", "Sigma", "Silicon", "Silver", 
    "Simon", "Simple", "Siren", "Skink", "Skid Row", "Skidmark", "Skloot", "Skunk", "Skynyrd", "Slag", "Slick", "Slime", "Slinky", "Sludge", "Smithers", "Smorgasbord", 
    "Snack", "Snafu", "Snake's Belly", "Sniffles", "Snots", "Snuffles", "Sodium", "Sol", "Spaatz", "Spaceball", "Sparta", "Spay", "Spearmint", "Speed Bump", "Sphairos", "Sphere", 
    "Spitfire", "Spittle", "Split", "Springfield", "Spruance", "Spuds", "Sputnik", "Staff", "Stamp", "Stanley", "Status", "Steeple", "Stellar", "Steppenwolf", "Stilton", "Stilwell", 
    "Sting", "Stinky Socks", "Stonehenge", "Stove Top", "Strange", "Strauss", "Strike 3", "Stuart", "Sulfur", "Sutra", "Swizzle Stick", "Taco", "Talking Desert", "Tangent", "Tanj", "Tank Top", 
    "Tao", "Tartaruga", "Taton", "Tattoo", "Taurus", "Tchaikovsky", "Teela", "Telly", "Terrace", "Texas", "Thomas", "Thyme", "Tierra", "Tiger's Tail", "Timbuktu", "Timoshenko", 
    "Tirpitz", "Tlon", "Tongue", "Toroid", "Tough Luck", "Trial", "Trismegistus", "Trog", "Truck Stop", "True Faith", "Truman", "Trurl", "Tsagigla'lal", "Tull", "Turing's World", "Tweedledee", 
    "Tweedledum", "Twelfth Man", "Tycho B", "Ultima Thule", "Underdog", "Upsilon", "Uqbar", "Uranium", "Uranus", "Ursa Good", "Ursa Major", "Ursa Minor", "Utgard", "Utopia", "Vacancy", "Vacant", 
    "Valhalla", "Vanilla", "Vega", "Venus", "Verdi", "Veritas", "Virgin", "Virgo", "Viscous", "Vista", "Vivaldi", "Vox", "Waco", "Wagner", "Wainwright", "Walla Walla", 
    "Wallaby", "Wallace", "Wammalammadingdong", "Wanker's Corner", "Washington", "Waterfall", "Wavell", "Weed", "Wellington", "Wendy", "Where", "Whiskey", "Whistler's Mother", "Who", "Wilbury", "Wingnut", 
    "Winken", "Winkle", "Winky-Blinky", "Winter", "Witter", "Wizzle", "Wobbly", "Wobegon", "Wood Shed", "Woody", "Woozle", "Worm", "Wrench", "Wrist Rocket", "Wumpus", "X-Lacks", 
    "X-Ray", "Xenon", "Y-Has", "Ya Betcha", "Yank", "Yeager", "Yes", "Yoruba", "Yuppie Puppy", "Zahir", "Zanzibar", "Zappa", "Zarquon", "Zebra", "Zed", "Zeppelin", 
    "Zero", "Zeta", "Zhukovi", "Ziggurat", "Zippy", "Zucchini", "Zulu"

     ]
    return planet_names

def planetNamesFromFile():
    #--TODO--
    pass





def techItemTemplate():
    tech = { "itemID":100, "itemType":"shield",
            "cost": { "iron":1, "bor": 1, "germ":1, "resources": 1, "mass":1},
            "tech": {"ener":0, "weap":0, "prop":0, "con":0, "elec":0, "bio":0} 
            }



'''
ship hulls design:

    uses techItemTemplate for itself
    +
    specifies dictionaries of slots
    mech_slot1 = {}
    mech_slot2 = {}
    weap_slot1 = {}

'''




[See the Wiki for More Information](https://github.com/jurlaub/StarsCoreEngine/wiki)  
[Technology](https://github.com/jurlaub/StarsCoreEngine/wiki/Technology)

#Reason / Motivation
Stars! is a phenomenal game - like ‘space chess’ with spying and race development strategies. I want to see the essence of this game continue far into the future. 

The most significant thrills are the multi-player games, where strategies and counter-strategies evolve as you desperately gather intelligence and sow disinformation. The game provides an infinite variety of gameplay. It starts with desiging the species you will use to explore the galaxy. Will your design work? Do you have the skill needed to play and survive the competition? The Stars community needs the next generation of Stars! This is the first step. 



#Goals 
The overriding intent and goal of this project is to ensure that the essence of Stars! can be extended and played by future generations by assembling the core game engine elements of the Stars Game.

* to encourage and facilitate future game development 
* to establish a baseline from which future modifications can be made
* to describe an overall Stars! Framework from which a complete game will be assembled.

This portion of the project will be considered “code complete” when the following objectives are reached:
* functionally equivalent game files generated 
  * game .xy
  * players .m 
  * players .x orders format defined and are used to generate turns
* all players data can be processed into objects used by the Stars Core Engine
* the Stars Core Engine processes all player orders and game objects according to the Stars Order of Events. 



#Licensing 
This project is under “Lesser GNU General Public License”. 
The scope of this work is to create the core engine that processes the users turns - “basically generating a new year in game terms.” The data will be accessible via JSON objects/files. 

The intention is that other applications or later projects will incorporate the Stars Core Engine library/code base. These other projects will provide the User Interface allowing the user to manipulate the data in the JSON objects. The Stars Core Engine will turn that data into new game turn data that will be ‘consumed’ by the other projects.

Projects that use the Stars Core Engine and expand upon it may be open source or proprietary. Modifications to the original Stars Core Engine component must follow the conditions outlined in the initial license.

*Please Note:* The interpretation of the license used for the Stars Core Engine allows for the creation and distribution of an App that uses the Stars Core Engine via iTunes App Store or other app stores. The Stars Core Engine source must be made available through a web-link or in-app text file. Contributors to this project must agree to this interpretation.



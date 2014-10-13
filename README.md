#TOC
## - Reason / Motivation
- Goals 
- Licensing 
- Technology
  - Minimum necessary setup





#Reason / Motivation
Stars! is a phenomenal game - like ‘space chess’ with spying and race development strategies. I want to see the essence of this game continue far into the future. 

The most significant thrills for me are the multi-player games, where strategies and counter-strategies evolve as you desperately gather intelligence and sow disinformation. Then there is the infinite variety of game concepts, each game resulting in a race that you think will be a “Monster” within the game concept requirements. Will your design work? Do you have the skill needed to play the race and survive competition? 

I remember well games like: Diadachi Wars II, 12 Gates, Rabid Weasels in a Box II, a Babylon 5 reenactment, and more. 

The flexibility of game-play is near infinite. Vanilla (standard) games are fun. Just as fun (or more) are theme games. The result has been years of games and thousands of hours of gameplay. Hardware and OS technology have advanced and the game needs to adapt. The Stars community needs the next generation of Stars! This is the first step. 


#Goals 
The overriding intent and goal of this project is “To ensure that the essence of Stars! can be extended and played by future generations.” 

With this in mind, the purpose of this project is to implement the first piece of the Stars puzzle by assembling the core game engine elements of the Stars Game.

In order to:
encourage and facilitate future game development 
establish a baseline from which future modifications can be made
describe an overall Stars! Framework from which a complete game will be assembled.

This portion of the project will be considered “code complete” when the following objectives are reached:
a JSON object for each player is generated containing the data necessary for a players turn to be viewed in a third-party app/webpage/viewer
a JSON object containing a players updated turn data can be accepted into the library’s overall data file
all players data can be processed into objects used by the Stars Core Engine
the Stars Core Engine processes all player orders and game objects according to the Stars Order of Events. 


#Licensing 
This project is under “Lesser GNU General Public License”. 
The scope of this work is to create the core engine that processes the users turns - “basically generating a new year in game terms.” The data will be accessible via JSON objects/files. 

The intention is that other applications or later projects will incorporate the Stars Core Engine library/code base. These other projects will provide the User Interface allowing the user to manipulate the data in the JSON objects. The Stars Core Engine will turn that data into new game turn data that will be ‘consumed’ by the other projects.

Projects that use the Stars Core Engine and expand upon it may be open source or proprietary. Modifications to the original Stars Core Engine component must follow the conditions outlined in the initial license.

Please Note: The interpretation of the license used for the Stars Core Engine allows for the creation and distribution of an App that uses the Stars Core Engine via iTunes App Store or other app stores. The Stars Core Engine source must be made available through a web-link or in-app text file. Contributors to this project must agree to this interpretation.


#Technology
* Python 3.4.1+
  - https://www.python.org
* Nose
  - https://nose.readthedocs.org/en/latest/
* virtualenv & virtualenvwrapper
  - http://virtualenv.readthedocs.org/en/latest/#
  - http://virtualenvwrapper.readthedocs.org/en/latest/
* Vagrant
  - https://www.vagrantup.com
  - https://vagrantcloud.com/hashicorp/boxes/precise64
* VirtualBox
  - https://www.virtualbox.org
* Python IDE
  - http://www.sublimetext.com/2
  - https://www.jetbrains.com/pycharm/  (Community Edition)
* Git & Github


##Minimum necessary setup:
I believe the minimum required setup would be a virtualenv Python environment running Python 3.4.1 and associated Python Packages. 

###For Linux:
Setting up the above environment should be fairly straightforward.

###For Windows: 
Pycharm’s Community Edition seems to have the option to open a new project within a virtualenv environment. I recently downloaded Pycharm on my work pc and it seemed promising. (This will most-likely be the extent of my windows assistance)

###For Mac:
This should be fairly straightforward like the linux setup. However, I added Vagrant and Virtual Box.


##Setup Assistance using Vagrant and Virtual Box

###My Mac Setup:
On my setup, there are two areas: the virtualenv python environment running in Vagrant on a virtual box and my normal OS. They are connected via a shared folder. I write code on an IDE running outside the virtual environment. It is saved to the shared folder. Git is used for version control and runs outside the virtual environment. The code is run and tested within the virtual environment. 


Vagrant and VirtualBox provide a virtual machine to develop on. Precise64 is the image modal. 

After reading the relevant install documentation, this order of events may be helpful:
* Install Vagrant according to the documentation. 
* Install VirtualBox. 
* Download from vagrantcloud.com the box image used in the project. hashicorp/precise64
* In a terminal window:
  - follow the Vagrant init commands
  - VagrantUp & Vagrant ssh in a terminal window
  - Now inside the virtual machine, check the python version you are running by starting up python
  - follow virtualenv or virtualenvwrapper download/install docs to create an environment 
  - when instantiating a virtualenv instance, make sure to specify the python version. You may need to download the updated version.

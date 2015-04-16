# tournamentRunner
Python script that generates in a round robin style a tournament that call bots to play a game of space invaders against each other. After the tournament is finished the script calculates some statistics

## Dependencies
* Python 2.7.9
* Installed SpaceInvaders Test Harness

## How to install
For the purposes of this installation when root refers to the directory 2015-TestHarness-1.0.0-Windows
* Place the script.py inside of the root directory
* Create directories for the bots that will partake in the tournament inside of the root
* Each bot directory should contain at least the following.
* run.bat
* bot.json
* bot executables, for python this is ussually main.py as per the example python bots

# How to run a tournament
* Open a terminal session / shell session in the root
* run python script.py without any additional arguments, this will display the script usage instructions on screen
* Example: run python script.py mybot player1 player 2, this will initiate a tournament with three players mybot, player1 and player2.
* The script assumes that the root\Replays directory is empty. After the tournament it takes and parses information from all the replay directories to calculate the statistics

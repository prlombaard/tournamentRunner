import os
from os.path import join, getsize
import itertools
import subprocess
import json
import sys
import collections

pipe_r, pipe_w = os.pipe()

def roundRobin():
    """
    Runs SpaceInvadersDuel
    """

def calculateStats():
    print "Gathering stats"

    stats = []

    # walk the Replays directory, search for matchinfo.json

    for root, dirs, files in os.walk('Replays'):
        for name in files:
            # test if matchinfo.json contained in this directory
            if name == "matchinfo.json":
                # matchinfo.json file found
                #print sum(getsize(join(root, name)) for name in files),
                #print name

                # read matchinfo.json to dictionary
                with open(join(root, name), "r") as matchInfoFile:
                    match_info = json.loads(matchInfoFile.read())

                    #transform read dictionary into what i need

                    new_match_info = {}

                    new_match_info['Winner'] = match_info['Winner']
                    new_match_info['Rounds'] = match_info['Rounds']

                    # TODO: change the way that the players are added to the stats list/dictionary
                    new_match_info['Player1'] = match_info['Players'][0]
                    new_match_info['Player2'] = match_info['Players'][1]

                    #print new_match_info
                    stats.append(new_match_info)

    skip = False

    if not skip:
        # print stats
        for i in stats:
            print "Match Info:"
            print i

        # TODO: Currently stats assumes only two unique players that played games against each other, change stats to include 2+player stats
        stats1 = {}
        stats1['Total Rounds'] = sum([ i['Rounds'] for i in stats])
        stats1['Minimum Rounds'] = min([ i['Rounds'] for i in stats])
        stats1['Maximum Rounds'] = max([ i['Rounds'] for i in stats])
        stats1['Range Rounds'] = stats1['Maximum Rounds'] - stats1['Minimum Rounds']
        stats1['Total Rounds'] = sum([ i['Rounds'] for i in stats])
        stats1['Average Rounds'] = stats1['Total Rounds'] / (len(stats) + 0.0)

        # Get the unique players that played in the tournament
        stats1['Players'] = []

        for i in stats:
            stats1['Players'].append(i['Player1']['Name'])
            stats1['Players'].append(i['Player2']['Name'])
        
        stats1['Players'] = sorted(set(stats1['Players']))
        #stats1['TPlayers'] = {}

        # Test how many players have played inthe tournament
        if len(stats1['Players']) > 2:
            print "Calculating %d players' stats" % (len(stats1['Players']))
            for i in xrange(0,len(stats1['Players'])):
                s = "Player" + str(i+1)
                #print s
                #print type(s)
                #tdict = {}
                #tdict[str(s)] = stats1['Players'][i]
                #print tdict
                
                #stats1['TPlayers'][s] = stats1['Players'][i]
                #print stats1['TPlayers'][s]
                stats1[i+1] = stats1['Players'][i]
                stats1[stats1['Players'][i]] = i+1
                #print stats1[stats1['Players'][i]]



            print "Transforming stats to new_stats"

            #print "\n\nstats[]0 before"
            #print stats[1]

            for i, j in zip(stats, xrange(len(stats))):
                #print "\n\nBefore replacements"                
                #print i['Player1']
                #print i['Player2']
                #print "Winner: ", "Player" + str(i['Winner'])
                #print "Global Winner: ", i["Player" + str(i['Winner'])]['Name']
                #print "Global Winner: ", stats1[i["Player" + str(i['Winner'])]['Name']]
                stats[j]['Winner'] = stats1[i["Player" + str(i['Winner'])]['Name']]

                i['Player1']['Number'] = stats1[i['Player1']['Name']]
                i['Player2']['Number'] = stats1[i['Player2']['Name']]
                

                #print "\nAfter replacements"
                #print i['Player1']
                #print i['Player2']
                #print i['Winner']
                
#            print "\n\nstats[]0 after"
#            print stats[1]

            #print "\nAFTER\n"

            #for i in stats:
            #    print "Match Info:"
            #    print i

            print "Tranformed stats"
            print "stats"
            print stats
            print "\n\nstats1"
            print stats1

            # Remove unwanted keys from dictionary
#            for i in xrange(len(stats1['Players'])):
#                #print i+1
#                del stats1[i+1]

            # Count how many wins for each player
            cnt_wins = collections.Counter([i['Winner'] for i in stats])
            #print cnt_wins
            stats1['Total number of wins'] = 0
            for i in xrange(len(stats1['Players'])):
                #print i
                stats1['Player ' + str(i+1) + ' Wins'] = cnt_wins[i+1]

                stats1['Total number of wins'] += stats1['Player ' + str(i+1) + ' Wins']

                # Rank players by most wins to least wins

                stats1['Rank'] = []



        if len(stats1['Players']) == 2:
            # Count how many P1 and P2 winners
            cnt_wins = collections.Counter([i['Winner'] for i in stats])
            #print cnt_wins
            print "Calculating 2 players'stats"
            stats1['Player 1 Wins'] = cnt_wins[1]
            stats1['Player 2 Wins'] = cnt_wins[2]

            stats1['Player 1 Total Kills'] = sum([i['Player1']['Kills'] for i in stats])
            stats1['Player 1 Average Kills'] = stats1['Player 1 Total Kills'] / (len(stats) + 0.0)

            stats1['Player 2 Total Kills'] = sum([i['Player2']['Kills'] for i in stats])
            stats1['Player 2 Average Kills'] = stats1['Player 2 Total Kills'] / (len(stats) + 0.0)       

            stats1['Total number of games'] = stats1['Player 1 Wins'] + stats1['Player 2 Wins']
            stats1['Player 1 Win to lose Ratio'] = stats1['Player 1 Wins'] / (stats1['Total number of games'] - stats1['Player 1 Wins'] + 0.0)
            stats1['Player 2 Win to lose Ratio'] = stats1['Player 2 Wins'] / (stats1['Total number of games'] - stats1['Player 2 Wins'] + 0.0)
            #print [i['Winner'] for i in stats]

        print "\n\nFINAL STATS:"

        for k, v in sorted(stats1.iteritems()):
            print "%s : %s" % (k, v)

        # TODO: Calculate leaderboard based on overall stats

def printUsage():
    """
    This function displays the usage instructions to run the script with example arguments
    """
    print 'Python Tournament Runner and post Tournament Statistics generator usage:'
    print
    print 'python tournameRunner.py bot1name, bot2name, bot2name'
    print

def main(args, skipTournament=True, tournaments_to_play=3, wait_for_user_input=False):
#def main(args, skipTournament=False, tournaments_to_play=1, wait_for_user_input=True):
    if not skipTournament:
        bot_paths = []
        # test if all bot directories are correct
        for dirname in args:
            if os.access(dirname, os.F_OK):
                path = dirname + '/' + "run.bat"
                #print "%s can be accessed" % dirname
                if os.access(path, os.R_OK):
                    print "%s can be accessed" % (path)
                    bot_paths.append(dirname)
            else:
                print "%s can NOT be accessed and is excluded from the tournament" % dirname

        # TODO: Check that if there is only one valid bot remaining that can be accessed then cancel the tournament

        print "Bots and play order that will take part in tournament"
        print bot_paths

        game_nr = 0
        for a, b in itertools.combinations(bot_paths, 2):
            game_nr += 1
            print "Game nr [%d]: %s vs. %s" % (game_nr, a, b)

        if wait_for_user_input:
            s = raw_input('press ENTER to continue')

        for tournament_nr in xrange(tournaments_to_play):
            # TODO: Implement timing to calculate statistics about  how long each game took, average time

            # Let bots play round robin tournament
            for p1, p2 in itertools.combinations(bot_paths, 2):
                #print "Game nr [%d]: %s vs. %s" % (game_nr, a, b)

                #command = ['SpaceInvadersDuel', '-o', 'player1', '-t', 'player2']
                command = ['SpaceInvadersDuel', '-o', p1, '-t', p2]

                prc = subprocess.Popen(command)

                # Wait for process to terminate
                while prc.poll() == None:
                    pass

    calculateStats()


# Check if this script is called as the main module
if __name__ == '__main__':

    # Test number of arguments provided from the shell
    if (len(sys.argv) < 2):
        # Arguments given less than 2
        # print usage information to console
        printUsage()
    else:
        # Correct number of arguments provided
        # Call main function
        print "Arguments provided:"
        for a in sys.argv:
            print a
        main(sys.argv)


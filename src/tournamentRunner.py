import os
from os.path import join, getsize
import itertools
import subprocess
import json
import sys
import collections
import time

pipe_r, pipe_w = os.pipe()

def roundRobin():
    """
    Runs SpaceInvadersDuel
    """

def calculateStats(tournament_times):
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

                i = 0

                # read matchinfo.json to dictionary
                with open(join(root, name), "r") as matchInfoFile:
                    match_info = json.loads(matchInfoFile.read())

                    #transform read dictionary into what i need

                    new_match_info = {}

                    new_match_info['Winner'] = match_info['Winner']
                    new_match_info['Rounds'] = match_info['Rounds']

                    new_match_info['Player1'] = match_info['Players'][0]
                    new_match_info['Player2'] = match_info['Players'][1]

                    # FIXME: Issue #4, Possible bug, this assumes that the amount of directories to be walked is equal to the number of games that was played

                    i += 1

                    new_match_info['Time per game'] = tournament_times[i]

                    #print new_match_info
                    stats.append(new_match_info)

    skip = False

    if not skip:
        # print stats
        for i in stats:
            print "Match Info:"
            print i

        # Fixed: Currently stats assumes only two unique players that played games against each other, change stats to include 2+player stats
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



            #print "Transforming stats to new_stats"

            #print "\n\nstats[]0 before"
            #print stats[1]
            stats1['Player Kills'] = []

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

                t_dict = {}
                t_dict[i['Player1']['Name']] = i['Player1']['Kills']

                stats1['Player Kills'].append(t_dict)

                t_dict = {}
                t_dict[i['Player2']['Name']] = i['Player2']['Kills']

                stats1['Player Kills'].append(t_dict)                
                
                # TODO: Issue #5, Create a counter to count and map total kills to each player name

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

            print "\nTranformed stats"
            print "stats"
            print stats
            print "\n\nstats1"
            print stats1

            leaderboard = {}

            # Count how many wins for each player
            cnt_wins = collections.Counter([i['Winner'] for i in stats])
            #print cnt_wins
            stats1['Total number of wins'] = 0
            stats1['Player Wins'] = []
            for i in xrange(len(stats1['Players'])):
                #print i
                #stats1['Player ' + str(i+1) + ' Wins'] = cnt_wins[i+1]
                tmp_dict = {}
                tmp_dict[cnt_wins[i+1]] = stats1['Players'][i]
                stats1['Player Wins'].append(tmp_dict)
                leaderboard['Player ' + str(i+1) + ' Wins'] = cnt_wins[i+1]

                stats1['Total number of wins'] += cnt_wins[i+1]

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

        # FIXED: Calculate leaderboard based on overall stats
        from operator import itemgetter

        #print list(tuple(i,j) for i,j in stats1['Player Wins'])
        #print list([tuple(i) for i in stats1['Player Wins']])
        sorted_l = sorted(list(i.items()[0] for i in stats1['Player Wins']), key=itemgetter(0), reverse=True)
        #print sorted_l
        print "\n\nLEADERBOARD:"
        print "===================="
        print "Name", "\t\t\t", "Wins"
        for i,j in sorted_l:
            print j, "\t\t", i

        # Remove unwanted keys from dictionary
        #Remove the 1,2,3 keys
        for i in xrange(len(stats1['Players'])):
            #print i+1
            del stats1[i+1]

        #Remove the player name keys
        for i in stats1['Players']:
            #print i+1
            del stats1[i]

        # Remove player names
        del stats1['Players']
        del stats1['Player Wins']


        print "\n\nFINAL STATS:"

        for k, v in sorted(stats1.iteritems()):
            print "%s : %s" % (k, v)



def printUsage():
    """
    This function displays the usage instructions to run the script with example arguments
    """
    print 'Python Tournament Runner and post Tournament Statistics generator usage:'
    print
    print 'python tournamentRunner.py bot1name, bot2name, bot2name'
    print

# TODO:

# This is used when the script must only calculate statistics, will possibly crash beacuse timings are now not done
#def main(args, skipTournament=True, tournaments_to_play=3, wait_for_user_input=False):

# This is used when the script must run a tournament
# TODO: Issue #6, Add some of the arguments of this function to the arguments passed into the main script from the command line
def main(args, skipTournament=False, tournaments_to_play=5, wait_for_user_input=True):
    if not skipTournament:
        bot_paths = []
        # test if all bot directories are correct
        # FIXME: Issue #7, Possible bug, the following part assumes that the directories to access is relative to the root path, the root being the testharness folder
        for dirname in args:
            if os.access(dirname, os.F_OK):
                path = dirname + '/' + "run.bat"
                #print "%s can be accessed" % dirname
                if os.access(path, os.R_OK):
                    print "%s can be accessed" % (path)
                    bot_paths.append(dirname)
            else:
                print "%s can NOT be accessed and is excluded from the tournament" % dirname

        # TODO: Issue #2, Check that if there is only one valid bot remaining that can be accessed then cancel the tournament

        print "Bots and play order that will take part in tournament"
        print bot_paths

        game_nr = 0
        for a, b in itertools.combinations(bot_paths, 2):
            game_nr += 1
            print "Game nr [%d]: %s vs. %s" % (game_nr, a, b)

        if wait_for_user_input:
            s = raw_input('press ENTER to continue')

        tournament_times = []

        for tournament_nr in xrange(tournaments_to_play):
            # TODO: Issue #3, Implement timing to calculate statistics about  how long each game took, average time

            # FIXME: Bug at sdfdkfjdkfjdkfj

            # BUG: sdasdsdsdsd



            # Let bots play round robin tournament
            for p1, p2 in itertools.combinations(bot_paths, 2):
                #print "Game nr [%d]: %s vs. %s" % (game_nr, a, b)

                starttime = time.time()

                #command = ['SpaceInvadersDuel', '-o', 'player1', '-t', 'player2']
                command = ['SpaceInvadersDuel', '-o', p1, '-t', p2]

                prc = subprocess.Popen(command)

                # Wait for process to terminate
                while prc.poll() == None:
                    pass

                # save time of how long the current gamed took to play and finish
                tournament_times.append(time.time() - starttime)

        # display tournament times
        print tournament_times

    pleaseExit = False

    if pleaseExit:
        exit(0)

    calculateStats(tournament_times)


# Check if this script is called as the main module
if __name__ == '__main__':

    # TODO: Issue #1, Implement better argument handling and usage display

    # Test number of arguments provided from the shell
    if (len(sys.argv) < 2):
        # Arguments given less than 2
        # print usage information to console
        printUsage()
    else:
        # Correct number of arguments provided
        # Call main function
        #print "Arguments provided:"
        #for a in sys.argv:
        #    print a
        main(sys.argv)


#program that finds the number of conflicts for a players in a position for an entire nhl season

from urllib.request import urlopen, URLError, HTTPError
from bs4 import BeautifulSoup
import socket
import itertools
import os.path
from pathlib import Path

team_abreviations = {
'ANA':  'anaheim-ducks',
'BOS': 	'boston-bruins',
'BUF': 	'buffalo-sabres',
'CAR': 	'carolina-hurricanes',
'CLB': 	'columbus-blue-jackets',
'CGY': 	'calgary-flames',
'CHI': 	'chicago-blackhawks',
'COL': 	'colorado-avalanche',
'DAL': 	'dallas-stars',
'DET': 	'detroit-red-wings',
'EDM': 	'edmonton-oilers',
'FLA': 	'florida-panthers',
'LA' :	'los-angeles-kings',
'MIN': 	'minnesota-wild',
'MON': 	'montreal-canadiens',
'NSH': 	'nashville-predators',
'NJ' :	'new-jersey-devils',
'NYI': 	'new-york-islanders',
'NYR': 	'new-york-rangers',
'OTT': 	'ottawa-senators',
'PHI': 	'philadelphia-flyers',
'ARI': 	'arizona-coyotes',
'PIT': 	'pittsburgh-penguins',
'SJ' :	'san-jose-sharks',
'STL': 	'st-louis-blues',
'TB' :	'tampa-bay-lightning',
'TOR': 	'toronto-maple-leafs',
'VAN': 	'vancouver-canucks',
'WPG': 	'winnipeg-jets',
'WAS': 	'washington-capitals',
'LV':	'vegas-golden-knights'
}

def compare_teams(player_conflicts_list = None):
	number_of_teams = int(input("Enter number of teams less than 4: "))

	while 3 < number_of_teams or number_of_teams < 0:
		number_of_teams = int(input("Invalid number of teams: please re-enter: "))
	roster = []

	for x in range(number_of_teams):
		roster_input = input("Enter team: ")
		roster.append(files[roster_input])

	if player_conflicts_list == None:
		compared_team = input("Enter team to compare: ")
		compared_player = files[compared_team]	
		player_conflicts = schedule_conflicts(roster, compared_player)

	else:
		player_conflicts = schedule_conflicts(roster, player_conflicts_list)

	return player_conflicts


def schedule_conflicts(roster_schedule_list, player_schedule_list):

	conflict_games_list = []
	available_games_list =[]
	full_roster_dates = []
	master_schedule = set() 
	for x in range(len(roster_schedule_list)):
		master_schedule.update(roster_schedule_list[x])

	empty_elements = 3 - len(roster_schedule_list)
	for x in range(empty_elements):
		roster_schedule_list.append([None])

	for player1, player2, player3 in itertools.combinations(roster_schedule_list, 3):
		print(str(player1) + '\n')
		print(str(player2) + '\n')
		print(str(player3) + '\n')
		for game_date in master_schedule:

			print(game_date in player1 and game_date in player2)
			print(game_date in player2 and game_date in player3)
			print(game_date in player1 and game_date in player3)
			
			if game_date in player1 and game_date in player2:
				full_roster_dates.append(game_date)
				print("adding " + game_date + " to full roster schedule\n")

			elif game_date in player2 and game_date in player3:
				full_roster_dates.append(game_date)
				print("adding " + game_date + " to full roster schedule\n")

			elif game_date in player1 and game_date in player3:
				full_roster_dates.append(game_date)
				print("adding " + game_date + " to full roster schedule \n")
			else:
				print(game_date + " available\n")

	for compared_player_game_date in player_schedule_list:
		if compared_player_game_date in full_roster_dates:
			print("adding " + compared_player_game_date + " to conflict schedule")
			conflict_games_list.append(compared_player_game_date)

		else:
			available_games_list.append(compared_player_game_date)
			print("adding " + compared_player_game_date + " to available schedule")

	print("conflicting games : " + str(conflict_games_list) + '\n')
	print("total conflicting games: " + str(len(conflict_games_list)) + '\n')
	print("available games : " + str(available_games_list) + '\n')
	print("total available games: " + str(len(available_games_list)) + '\n')

	return conflict_games_list

def get_files():

	schedule = None
	games_dict = {}
	print("Reading schedule files...")
	for x in team_abreviations:
		if os.path.isfile('nhlschedules/' + team_abreviations[x] + '.txt'):
			try:
				file = open('nhlschedules/' + team_abreviations[x] + '.txt', "r")

			except OSError as e:
				print('File ' + team_abreviations[x] + 'could not be found.' + str(e))

		else :
			try:
				print('File ' + team_abreviations[x] + 'could not be found, creating new file.')
				file = open('nhlschedules/' + team_abreviations[x] + '.txt', "w+")

				if schedule is None:
					schedule = get_schedule()
				file.write(x + '\n')

				for y in schedule[x]:
					file.write(y + '\n')

				file.close()

			except OSError as e:
				print('File ' + team_abreviations[x] + 'could not be created.' + str(e))

		file = open('nhlschedules/' + team_abreviations[x] + '.txt', "r")

		if file.mode == 'r':
			games_dict.update({file.readline().strip(): parsed_newlines(file.readlines())})

	return games_dict


def parsed_newlines(list):
	parsed_list = []

	for x in list:
		parsed_list.append(x.strip())

	return parsed_list


def get_schedule():
	url= 'https://www.cbssports.com/nhl/teams/'
	teams = {}

	for key in team_abreviations:

		team_game_dates = []

		complete_url = url + str(key) + '/' + str(team_abreviations[key]) + '/schedule'
		http_response_object = connect_website(complete_url)
		print('Downloading ' + team_abreviations[key] + ' schedule \n')
		page_soup = BeautifulSoup(http_response_object, 'html.parser')

		for date in page_soup.findAll('span', {'class': 'CellGameDate'}):
			team_game_dates.append(date.contents[0].strip())
		
		teams.update({key: team_game_dates})

	return teams

def connect_website(website):
	print('Connecting with '+ website + '...')
	socket.setdefaulttimeout( 23 )  # timeout in seconds

	try :
	    response = urlopen(website)

	except HTTPError as e:
		
	    print ('The server couldn\'t fulfill the request. Reason:', str(e.code) + '\n')

	except URLError as e:
	    print ('We failed to reach a server. Reason:', str(e.reason) + '\n')

	else :
	    html = response.read()
	    print ('Connection established!' + '\n')
	    response.close()
	    
	    return html


files = get_files()
position_one_conflicts = compare_teams()
position_two_conflicts = compare_teams(position_one_conflicts)
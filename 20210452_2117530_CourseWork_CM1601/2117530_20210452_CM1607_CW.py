import csv
import random
import time

#team names as dictionary
teamnum = {'1': 'England.csv', '2': 'Pakistan.csv', '3': 'India.csv', '4': 'NewZealand.csv',
           '5': 'SouthAfrica.csv','6': 'Australia.csv', '7': 'SriLanka.csv', '8': 'Bangladesh.csv'}
team_names = {'1': 'England', '2': 'Pakistan', '3': 'India', '4': 'NewZealand', '5': 'SouthAfrica','6': 'Australia', '7': 'SriLanka', '8': 'Bangladesh'}

#Used at the point of editing
detailnum = {'1':'PLAYER _NAME', '2':'MATCHES', '3':'ROLE', '4':'RUNS', '5':'STRIKE_RATE', '6':'AVERAGE', '7':'WICKETS', '8':'ECONOMY'}

#Used in the process of generating the matches
team_names_A = {1:'England',2:'Pakistan',3:'India',4:'NewZealand'}
team_names_B = {1:'SouthAfrica',2:'Australia',3:'SriLanka',4:'Bangladesh'}
schedule_A = []
schedule_B = []
list1 = [1,2,3,4]

tournament_standings = {"A": {}, "B": {}}
play_offs = {}
final = {}

#dismissal types
dismissal = ['Bowled','Caught','Leg before wicket','Stumped']

summary = {}
player_summary = {}

def init():
    # generate player stats for tournament
    for team in teamnum:
        with open(teamnum[team], 'r', encoding='utf-8-sig') as player_details:
            csv_reader = csv.reader(player_details, delimiter=',')
            headers = next(csv_reader)[1:]
            player_summary[team_names[team]] = {}
            for row in csv_reader:
                 player_summary[team_names[team]][row[0]] = {"PLAYER_NAME": row[0], "ROLE": row[2], "MATCHES": 0, "RUNS": 0, "WICKETS": 0, "COUNTRY": team_names[team]}

    write_player_stats()


def introduction():
    txt = "ICC Men's T20 WORLD CUP 2021"
    underline = "--------------------------------"
    x = txt.center(150)
    y = underline.center(150)
    print(x)
    print(y)
    print("GROUP A"'\n'
        "1 - England""\n""2 - Pakistan""\n""3 - India""\n""4 - New Zealand""\n"
        "GROUP B"'\n'
        "5 - South Africa""\n""6 - Australia""\n""7 - Sri Lanka""\n""8 - Bangladesh")

    print("Welcome to ICC Men's T20 World Cup!!!")

 # printing and editing player details and team details
def instructions():

    print("Read the following instructions and follow accordingly.")
    print("-----------------------------------------------------------------------")
    res = input("Do you like to watch team the information? (yes/no) : ")
    while res == 'yes':
            team = input("England - 1""\n""Pakistan - 2""\n""India - 3""\n""New Zealand - 4""\n""South Africa - 5""\n""Australia - 6""\n""Sri Lanka - 7""\n""Bangladesh - 8""\n"
                "Select the team (Please enter the corresponding number): ")

            # opening the required team player details
            with open(teamnum[team], 'r') as player_details:
                csv_reader = csv.reader(player_details, delimiter=',')
                for row in csv_reader:
                    print(row)
            res = input("Do you like to watch team the information? (yes/no) : ")
    edit_player()


# directing the users to editing process
def edit_player():
    res1 = input("Do you need to do any changes in player details? (yes/no) : ")

    while res1 == 'yes':
        dict = {}
        print('Please select the team name and the player', "\t")
        sel_team = input("Enter the team number : ")

        with open(teamnum[sel_team], 'r',encoding='utf-8-sig') as data:  # encoding is given to remove the extra symbol
            for line in csv.DictReader(data):
                dict[line['PLAYER _NAME']] = line
                print(line['PLAYER _NAME'])
        sel_player = input("Enter the player name : ")
        print(dict[sel_player])

        res3 = input("What detail you would like to change?"'\n'
              "1 - Player Name\n2 - Role\n""Enter the corresponding number to be changed : ")
        change = input("Enter the changing value : ")
        col_name = detailnum[res3]
        print(col_name)
        dict[sel_player][col_name] = change
        print(dict[sel_player])
        res1 = input("Do you need to do any changes in player details again? (yes/no) : ")


def generate_schedule():
    for i in range(len(list1)):
        for j in range(len(list1[i + 1:])):
            pairing = (list1[i], list1[j + i + 1]) #the matches are orderly printed as tuple type
            schedule_A.append(pairing) # appending or joining the tuples into a list
            schedule_B.append(pairing)
    random.shuffle(schedule_A) # shuffling and generating different matches
    random.shuffle(schedule_B)

    # generate tournament standings
    for team in team_names_A:
        tournament_standings["A"][team_names_A[team]] = {"name": team_names_A[team], "M": 0, "W": 0, "L": 0, "NRR": 0, "Pts": 0 }

    for team in team_names_B:
        tournament_standings["B"][team_names_B[team]] = {"name": team_names_B[team], "M": 0, "W": 0, "L": 0, "NRR": 0, "Pts": 0 }

def generate_playoffs(group):
    maxScore = 0
    maxTeam1 = None
    for team in tournament_standings[group]:
        if tournament_standings[group][team]["Pts"] > maxScore:
            maxScore = tournament_standings[group][team]["Pts"]
            maxTeam1 = team

    secondMaxScore = 0
    maxTeam2 = None
    for team in tournament_standings[group]:
        if tournament_standings[group][team]["Pts"] != maxScore and tournament_standings[group][team]["Pts"] > secondMaxScore:
            secondMaxScore = tournament_standings[group][team]["Pts"]
            maxTeam2 = team

    return  maxTeam1, maxTeam2

def start_tournament():
    txt = '<<<<<<<<<<<<<<<The game starts now!!!!>>>>>>>>>>>>>>>'
    x = txt.center(100)
    print(x)
    print('\t')

    # print group A matches are being played
    play_matches(schedule_A, team_names_A, "A")

    ## print group b matches
    play_matches(schedule_B, team_names_B, "B")

    ## get top two teams from a, get top two teams from b
    maxTeamA1, maxTeamA2 = generate_playoffs("A")
    maxTeamB1, maxTeamB2 = generate_playoffs("B")

    play_offs['Semi Final 1'] = {"team1": maxTeamA1, "team2": maxTeamB2}
    play_offs['Semi Final 2'] = {"team1": maxTeamA2, "team2": maxTeamB1}
    print(play_offs)

    semiFinal1Winner, semiFinal2Winner = play_semi_finals()
    play_offs['Semi Final 1']['winner'] = semiFinal1Winner
    play_offs['Semi Final 2']['winner'] = semiFinal2Winner
    print('Teams',semiFinal1Winner,'and', semiFinal2Winner,'are qualified for the final')

    play_offs['Final'] = {"team1": semiFinal1Winner, "team2": semiFinal2Winner, "winner": None}
    winner = play_final(semiFinal1Winner, semiFinal2Winner)
    play_offs['Final']['winner'] = winner
    print(play_offs)
    print('\t')
    print("Team",winner,"has won the ICC Men's T20 WORLD CUP 2021 !!!!!")






def play_matches(schedule, team_names, group):

    for match in schedule:
        time.sleep(2)
        team_one = match[0]
        team_two = match[1]
        print("--------The match is between", team_names[team_one], "and", team_names[team_two], "--------")
        play_single_match(team_names[team_one], team_names[team_two], group)
        # get input from user, to view sumary again, view tournament standings, to continue


def play_single_match(team1, team2, group):
    # toss
    firstBattingTeam = toss(team1, team2)
    secondBattingTeam = team1 if firstBattingTeam==team2 else team2

    print('\t')
    print("********First innings has started********")
    # play first innings
    player_runs1 = 0
    # time.sleep(1)
    runs1 = random.randint(50,275)
    print('The runs scored by',firstBattingTeam,'is',runs1)
    wicket_1 = random.randint(0,10)
    print('Wickets taken by',secondBattingTeam,'is',wicket_1)
    print('\t')

    print("********Second innings has started********")

    # play second innings
    player_runs2 = 0
    runs2 = random.randint(50,runs1+6)
    print('The runs scored by', secondBattingTeam, 'is', runs2)
    wicket_2 = random.randint(0, 10)
    print('Wickets taken by', firstBattingTeam, 'is', wicket_2)
    print("\t")





    # player stats
    team1Players = random.sample(list(player_summary[team1].keys()), 11)
    team2Players = random.sample(list(player_summary[team2].keys()), 11)

    match_summary = {}
    for player in team1Players:
        runs = random.randint(0,runs1)
        runs1 -= runs
        wicket = random.randint(0,wicket_1)
        wicket_1 -= wicket
        player_summary[team1][player]["MATCHES"] += 1
        match_summary[player] = {"PLAYER_NAME": player, "RUNS": runs, "WICKETS": wicket}

    for player in team2Players:
        runs = random.randint(0, runs2)
        runs2 -= runs
        wicket = random.randint(0, wicket_2)
        wicket_2 -= wicket
        player_summary[team2][player]["MATCHES"] += 1
        match_summary[player] = {"PLAYER_NAME": player, "RUNS": runs2, "WICKETS": wicket}

    winning_team = firstBattingTeam if runs1 > runs2 else secondBattingTeam
    print('\t')
    print("Team",winning_team, 'won the match')
    print('\t')


    write_player_stats()

    # update tournament dictionary
    winningTeam = team1 if random.randint(0,1) > 0.5 else team2
    loosingTeam = team1 if winningTeam == team2 else team2

    tournament_standings[group][winningTeam]["W"] += 1
    tournament_standings[group][winningTeam]["M"] += 1
    tournament_standings[group][winningTeam]["Pts"] += 2
    tournament_standings[group][winningTeam]["NRR"] += random.randint(0,1)

    tournament_standings[group][loosingTeam]["L"] += 1
    tournament_standings[group][loosingTeam]["M"] += 1
    tournament_standings[group][loosingTeam]["NRR"] -= random.randint(0,1)

    write_tournament_standings(group)
    # print summary
    summary[f"Group Stages : {team1} vs {team2}"] = {"match": f"Group Stages : {team1} vs {team2}", "team1": team1, "team2": team2, "firstBatting": firstBattingTeam, "winner": winningTeam}
    write_summary()
    write_match(match_summary, team1, team2, "Group Stages")

def play_semi_finals():
    # play seminals
    semiFinal1Winner = play_offs['Semi Final 1']['team1']
    semiFinal2Winner = play_offs['Semi Final 2']['team1']
    return semiFinal1Winner, semiFinal2Winner

def play_final(team1, team2):
    winner = team1
    return winner

def write_tournament_standings(group):
    filename = f"Group{group}Standings.csv"
    with open(filename, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        fieldnames = ['name', 'M', 'W', 'L', 'NRR', 'Pts']
        writer = csv.DictWriter(csv_file, fieldnames)
        writer.writeheader()
        for key, value in tournament_standings[group].items():
            writer.writerow(value)


def write_player_stats():
    with open("Player_Stats.csv", 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        fieldnames = ['PLAYER_NAME', 'ROLE', 'MATCHES', 'RUNS', 'WICKETS', 'COUNTRY']
        writer = csv.DictWriter(csv_file, fieldnames)
        writer.writeheader()

        for team in player_summary:
            for key, value in player_summary[team].items():
                writer.writerow(value)


def write_summary():
    with open("Summary.csv", 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        fieldnames = ['match', 'team1', 'team2', 'firstBatting', 'winner']
        writer = csv.DictWriter(csv_file, fieldnames)
        writer.writeheader()
        for key, value in summary.items():
            writer.writerow(value)

def write_match(match, team1, team2, league):
    with open(f"{league} {team1} vs {team2}.csv", 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        fieldnames = ['PLAYER_NAME', 'RUNS', 'WICKETS']
        writer = csv.DictWriter(csv_file, fieldnames)
        writer.writeheader()
        for key, value in match.items():
            writer.writerow(value)

def toss(team1,team2):
    coin = ['head', 'tail']
    choices = ['bat', 'field']
    toss_guess = random.choice(coin)
    toss = random.choice(coin)
    choose = random.choice(choices)
    print("The coin tossed a",toss)
    if toss_guess==toss:
        # print(team_one)
        print(team1 ,'won the toss and choose to',choose,'first')
        return team1 if choose == "bat" else team2
    else:
        # print(team_two)
        print(team2,'won the toss and choose to',choose,'first')
        return team2 if choose == "bat" else team1




#Calling the functions in order
init()
introduction()

print("----------------LET'S EXPLORE THE TEAM DETAILS---------------")

instructions()
generate_schedule()
start_tournament()

res3 = input('Do you like to watch the match status (yes/no: ')
while res3 == 'yes':
    print("1 - GroupAStandings",'\n',
    '2 - GroupBStandings','\n',
    "3 - end_summary",'\n',
    "4 - Player_Stats")

    res4 = input('Please enter the corresponding file number : ')
    if res4 == "1":
        with open('GroupAStandings.csv', 'r') as GroupAStandings:
            csv_reader = csv.reader(GroupAStandings, delimiter=',')
            for row in csv_reader:
                print(row)

    elif res4 == '2':
        with open('GroupBStandings.csv', 'r') as GroupBStandings:
            csv_reader = csv.reader(GroupBStandings, delimiter=',')
            for row in csv_reader:
                print(row)

    elif res4 =="3":
        with open('Summary.csv', 'r') as end_summary:
            csv_reader = csv.reader(end_summary, delimiter=',')
            for row in csv_reader:
                print(row)
    elif res4 == '4':
        with open('Player_Stats.csv','r') as Player_Stats:
            csv_reader = csv.reader(Player_Stats, delimiter=',')
            for row in csv_reader:
                print(row)
    res3 = input('Do you like to watch the match status (yes/no): ')




print("*******ICC Men's T20 WORLD CUP 2021 has come to an end*******",'\n','Thank You for staying with us!!!!')







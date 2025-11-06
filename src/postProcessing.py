import sqlite3
from typing import List, Dict, Any, Optional, Tuple
import matplotlib.pyplot as plt

def rows_to_dicts(db_path: str, query: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
    """
    Execute `query` against SQLite DB at `db_path` and return all rows as a list of dicts.
    Example:
      rows = rows_to_dicts('data.db', 'SELECT * FROM mytable WHERE foo = ?', (42,))
    """
    params = params or ()
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row  # makes rows behave like mappings
        cur = conn.execute(query, params)
        rows = cur.fetchall()
        return [dict(row) for row in rows]

def makeSimplifiedMatchObj(data):
    matches = []
    #The timestamp value will help determine the order that matches were submitted.
    #It helps with replay matches and duplicates, since the later match has to be taken.
    timestampCounter = 0
    for item in data:
        timestampCounter += 1
        match = {
            "matchNum": item["match_id"],
            "team": item["Zteam"],
            "totalScore": item["ZtotalScore"],
            "timestamp": timestampCounter
        }

        matches.append(match)
    return matches

#This function returns the index of the first element in an array of dictionaries where the dictionary with the key "key" has the value of "value"
def indexOf(arr, key, value):
    index = 0
    for element in arr:
        #See if the key matches
        if(element[key] == value):
            return index
        index += 1
    #If no element is found, return -1
    return -1

#This function returns a list of all of a teams scores, with replay matches replacing their earlier matches
def getValidMatches(team):
    global matches
    matchesOfTeam = []

    for match in matches:
        if match["team"] == team:
            matchesOfTeam.append(match)

    #Validate matches

    #This array stores the numbers for each of the matches played. 
    #It is used to see if the match has the same match number as a previous match, meaning it was a replay 
    validatedMatches = []
    for match in matchesOfTeam:
        #See if it is a replay
        
        #Try to get the index where a match with the same match number is located
        index = indexOf(validatedMatches, "matchNum", match["matchNum"])
        #if a match is found
        if index != -1:
            #replace the match
            validatedMatches[index] = match
        else:
            #If it isn't found in the list, add it to the list
            validatedMatches.append(match)

    return validatedMatches

def getTeamScores(team):
    global matches
    #Get valid matches
    teamMatches = getValidMatches(team)
    scores = []
    #Loop though the team's matches and add the scores to a list
    for match in teamMatches:
        scores.append(int(match["totalScore"]))
    return scores

def getAllScores():
    global matches, teams
    allScores = {}
    for team in teams:
        scores = getTeamScores(team)
        allScores[team] = scores
    return allScores

def average(arr):
    total = 0
    for item in arr:
        total += int(item)
    average = total/len(arr)
    return average

def getTeamAverage(team):
    global allScores
    scores = allScores[team]
    return average(scores)

def getAllTeamAverages():
    global teams
    teamAverages = {}
    for team in teams:
        avg = getTeamAverage(team)
        teamAverages[team] = avg
    return teamAverages


#This function returns a list of all the teams at an event
def getTeams():
    global matches

    teams = []
    for match in matches:
        team = match["team"]
        #see if the team is not already listed
        if(not team in teams ):
            #add the team to the teamlist
            teams.append(team)
    teams.sort()
    return teams

def printDict(dict):
    for key in dict:
        print(key + ": " + str(dict[key]))

def printArr(arr):
    index = 0
    for item in arr:
        print(str(index) + ": " + str(item))
        index += 1

def rankByAverage(averages):
    #Averages should be a dictionary with one key-value pair per team

    rankedTeams = []

    for team in averages:
        #Create a tiny dictionary to store the team's name and average
        teamAvg = averages[team]
        teamData = [team, teamAvg]

        #loop through all the ranked teams
        #once you get to a team smaller than you, insert your team right before it

        #Catch the case where it is an empty list
        if len(rankedTeams) == 0:
            #add the team to the list
            rankedTeams.append(teamData)

        for index in range(len(rankedTeams)):
            rankedTeam = rankedTeams[index]
            rankedAvg = rankedTeam[1]

            #If the team has a higher score than the selected team
            if teamAvg > rankedAvg:
                #Add the team before it
                rankedTeams.insert(index, teamData)
                break

    return rankedTeams

def getHighScoreOfTeam(team):
    global allScores
    scores = allScores[team]

    highScore = 0
    for score in scores:
        if score > highScore:
            highScore = score
    return highScore
def getTopGun():
    global teams
    highestTeam = teams[0]
    for team in teams:
        if getHighScoreOfTeam(team) > getHighScoreOfTeam(highestTeam):
            highestTeam = team
    return [highestTeam, getHighScoreOfTeam(highestTeam)]

def getTeamScoresInPoints(team):
    scores = getTeamScores(team)

    points = []
    for i in range(len(scores)):
        points.append((i + 1, scores[i]))
    return points

def getAllTeamGraphs():
    global teams

    graphs = []

    for team in teams:
        points = getTeamScoresInPoints(team)
        graphs.append((team, points))

    return graphs





data = rows_to_dicts("scorecard.db", "SELECT * FROM scoress")
matches = makeSimplifiedMatchObj(data)
teams = getTeams()
allScores = getAllScores()
#printDict(allScores)
teamAverages = getAllTeamAverages()
leaderboard = rankByAverage(teamAverages)

print("Leaderboard:")
printArr(leaderboard[0:3])

print("Top Gun: " + str(getTopGun()))

def plot_points_xy(lines: List[Tuple[List[Tuple[float, float]]]],
                   title="My Plot",
                   xlabel="x",
                   ylabel="y",
                   save_path: str | None = None):
    
    plt.figure(figsize=(8, 5))
    # Unpack
    for line in lines:
        title = line[0]
        points = line[1]
        xs, ys = zip(*points) if points else ([], [])
        plt.plot(xs, ys, linestyle='-', marker='o', label=title)  # line + markers
        #plt.scatter(xs, ys, color='red', label='points')  # explicit scatter
    
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150)
        print(f"Saved plot to {save_path}")
    plt.show()


sample = [(0, 1), (1, 3), (2, 2.5), (3, 5), (4, 4.5)]
sample = getTeamScoresInPoints("Spring Branch Middle School")
lines = getAllTeamGraphs()
#print(lines)
plot_points_xy(lines, title="Scores")

printArr(getValidMatches("Navarro High School"))



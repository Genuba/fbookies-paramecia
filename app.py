import difflib

from pymongo_get_database import get_database

db = get_database()
betsByDate = db["betsByDate"]

docData = betsByDate.find({})


def getBetsByTeamName(n):
    betBookieName_dic = {}
    for bet in n["bets"]:
        key = bet["bookie"]

        if not key in betBookieName_dic:
            betBookieName_dic[key] = {}

        index = bet["teamA"]["name"] + " vs " + bet["teamB"]["name"]

        betBookieName_dic[key][index] = bet
    return betBookieName_dic


def getClosestMatchComparison(matchX, matchY):
    print("matchX: " + matchX + " matchY: " + matchY)
    matchListX = matchX.split(" vs ")
    matchListY = matchY.split(" vs ")

    # comparation by team name in the match: A B = C D
    # A C -> A D
    # B C -> B D

    closest_matches = [
        difflib.get_close_matches(matchX, matchListY) for matchX in matchListX
    ]
    return closest_matches


def groupBetsByTeamMatch(n):
    bookie_stop_dic = {}
    match_stop_dic = {}
    match_dic = {}
    for bookieX in n.keys():
        for matchX in n[bookieX].keys():
            for bookieY in n.keys():
                if bookieY == bookieX and not bookieX in bookie_stop_dic:
                    break
                if not bookieY in match_stop_dic:
                    match_stop_dic[bookieY] = {}
                for matchY in n[bookieY].keys():
                    if matchY in match_stop_dic[bookieY]:
                        break
                    closest_matches = getClosestMatchComparison(matchX, matchY)
                    print(closest_matches)
                    if len(closest_matches) > 0:
                        if not matchX in match_dic:
                            match_dic[matchX] = {}
                            match_dic[matchX][bookieX] = n[bookieX][matchX]

                        match_dic[matchX][bookieY] = n[bookieY][matchY]

                        # stop cycling matchY
                        match_stop_dic[bookieY][matchY] = 1

                    # score = difflib.SequenceMatcher(None, matchX, matchY).ratio()
                    # print(
                    #    "score for: " + matchX + " ----- " + matchY + " = " + str(score)
                    # )
        # stop cycling bookieX
        bookie_stop_dic[bookieX] = 1


for rowBet in docData:
    print("------------- " + rowBet["timestamp"] + " ---------------")
    betBookieName_dic = getBetsByTeamName(rowBet)
    groupBetsByTeamMatch(betBookieName_dic)

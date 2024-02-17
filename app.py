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


def getClossestMatchComparison(matchX, matchY):
    print("matchX: " + matchX + " matchY: " + matchY)
    matchListX = matchX.split(" vs ")
    matchListY = matchY.split(" vs ")

    # comparation by team name in the match: A B = C D
    # A C -> A D
    # B C -> B D

    closest_matches = [
        difflib.get_close_matches(matchNameX, matchListY) for matchNameX in matchListX
    ]
    return closest_matches


def groupBetsByTeamMatch(n):
    bookie_dic = {}
    for bookieX in n.keys():
        for matchX in n[bookieX].keys():
            for bookieY in n.keys():
                if bookieY == bookieX and not bookieX in bookie_dic:
                    break
                for matchY in n[bookieY].keys():
                    closest_matches = getClossestMatchComparison(matchX, matchY)
                    print(closest_matches)

                    # score = difflib.SequenceMatcher(None, matchX, matchY).ratio()
                    # print(
                    #    "score for: " + matchX + " ----- " + matchY + " = " + str(score)
                    # )

        bookie_dic[bookieX] = 1


for rowBet in docData:
    print("------------- " + rowBet["timestamp"] + " ---------------")
    betBookieName_dic = getBetsByTeamName(rowBet)
    groupBetsByTeamMatch(betBookieName_dic)

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

        index = (
            bet["teamA"]["name"]
            + " vs "
            + bet["teamB"]["name"]
            + "----"
            + bet["teamB"]["name"]
            + " vs "
            + bet["teamA"]["name"]
        )

        betBookieName_dic[key][index] = bet
    return betBookieName_dic


def groupBetsByTeamMatch(n):
    print(n)


#    keysList = list(n.keys())
#    print(keysList)
#
#    for betMatch in n.keys():
#        keysList.remove(betMatch)
#        for key in keysList:
#            if len(keysList):
#                score = difflib.SequenceMatcher(None, betMatch, key).ratio()
#                print("score for: " + betMatch + " ----- " + key + " = " + str(score))
#

for rowBet in docData:
    print("------------- " + rowBet["timestamp"] + " ---------------")
    betBookieName_dic = getBetsByTeamName(rowBet)
    groupBetsByTeamMatch(betBookieName_dic)

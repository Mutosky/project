import requests
import numpy as np
from datetime import date, timedelta


today = date.today()
today = today - timedelta(days=1)
api_key = "5218e35066bd174fcc60095f853f4a3e8bf62785177f49e61af1f888c01e10ba"


def pad_list(lst, max_length):
    return lst + [np.nan] * (max_length - len(lst))


def remove_lower_than_10(numbers):
    return [num for num in numbers if int(num) >= 10]

def replace(data):
    for i in range(len(data)):
        if data[i] == '':
            data[i] = 0
    return data



def getTestData(teamid, teamid2):

    score = []
    place = []
    possession = []
    shotinsidebox = []
    dangerousattacks = []
    accuracy = []
    On_target = []
    Corners = []
    Attacks = []

    score2 = []
    place2 = []
    possession2 = []
    shotinsidebox2 = []
    dangerousattacks2 = []
    accuracy2 = []
    On_target2 = []
    Corners2 = []
    Attacks2 = []


    outcome = []
    team1 = []
    team2 = []
    event_date = []
    away = 1
    home = 2

    ballpos = 'Ball Possession'
    passaccu = 'Passes Accurate'
    shotinside = 'Shots Inside Box'
    dangerous = 'Dangerous Attacks'
    target = 'On Target'
    Corner = 'Corners'
    Attack = 'Attacks'

    url = f'https://apiv2.allsportsapi.com/football/?met=H2H&APIkey={
        api_key}&firstTeamId={teamid}&secondTeamId={teamid2}'

    responed = requests.get(url=url)
    if responed.status_code == 200:
        data = responed.json()['result']['H2H']

        for key in data:
            event_key = key['event_key']
            featureurl = f'https://apiv2.allsportsapi.com/football/?met=Fixtures&APIkey={api_key}&from=2023-01-01&to={today}&matchId={event_key}'

            featurerespond = requests.get(url=featureurl)
            if featurerespond.status_code == 200:
                if 'result' in featurerespond.json():
                    featuredata = featurerespond.json()['result'][:3]
                    for match in featuredata:
                        homeid = match['home_team_key']
                        awayid = match['away_team_key']
                        homename = match['event_home_team']
                        awayname = match['event_away_team']
                        goals = match['event_final_result']
                        event_date.append(match['event_date'])
                        stat = match['statistics']

                        if goals == '-':
                            if teamid == homeid:
                                place.append(home)
                                place2.append(away)
                                team1.append(homename)
                                team2.append(awayname)
                                score.append(0)
                                score2.append(0)
                                outcome.append('Draw')
                            elif teamid == awayid:
                                place.append(away)
                                place2.append(home)
                                score.append(0)
                                score2.append(0)
                                outcome.append('Draw')
                        else:
                            homescores = goals[0]
                            awayscores = goals[4]

                            if homeid == teamid:
                                place.append(home)
                                place2.append(away)
                                team1.append(homename)
                                team2.append(awayname)
                                score.append(homescores)
                                score2.append(awayscores)
                                if homescores > awayscores:
                                    outcome.append('TeamOne')
                                elif awayscores > homescores:
                                    outcome.append('TeamTwo')
                                else:
                                    outcome.append('Draw')

                                for statis in stat:
                                    if statis['type'] == ballpos:
                                        inputData3 = statis['away'].replace('%', '')
                                        inputData4 = statis['home'].replace('%', '')
                                        data3 = 0 if inputData3 == '' else inputData3
                                        data4 = 0 if inputData4 == '' else inputData4
                                        print(data3, data4)
                                        possession.append(data3)
                                        possession2.append(data4)
                                    if statis['type'] == passaccu:
                                        inputdata = statis['away']
                                        inputData2 = statis['home']
                                        inputdata = 0 if inputdata == '' else inputdata
                                        inputData2 = 0 if inputData2 == '' else inputData2
                                        print(inputdata, inputData2)
                                        accuracy.append(inputdata)
                                        accuracy2.append(inputData2)
                                    if statis['type'] == shotinside:
                                        inputdata = statis['away']
                                        inputData2 = statis['home']
                                        inputdata = 0 if inputdata == '' else inputdata
                                        inputData2 = 0 if inputData2 == '' else inputData2
                                        print(inputdata, inputData2)
                                        shotinsidebox.append(inputdata)
                                        shotinsidebox2.append(inputData2)
                                    if statis['type'] == dangerous:
                                        inputdata = statis['away']
                                        inputData2 = statis['home']
                                        inputdata = 0 if inputdata == '' else inputdata
                                        inputData2 = 0 if inputData2 == '' else inputData2
                                        print(inputdata, inputData2)
                                        dangerousattacks.append(inputdata)
                                        dangerousattacks2.append(inputData2)
                                    if statis['type'] == target:
                                        inputdata = statis['away']
                                        inputData2 = statis['home']
                                        inputdata = 0 if inputdata == '' else inputdata
                                        inputData2 = 0 if inputData2 == '' else inputData2
                                        print(inputdata, inputData2)
                                        On_target.append(inputdata)
                                        On_target2.append(inputData2)
                                    if statis['type'] == Corner:
                                        inputdata = statis['away']
                                        inputData2 = statis['home']
                                        inputdata = 0 if inputdata == '' else inputdata
                                        inputData2 = 0 if inputData2 == '' else inputData2
                                        print(inputdata, inputData2)
                                        Corners.append(inputdata)
                                        Corners2.append(inputData2)
                                    if statis['type'] == Attack:
                                        inputdata = statis['away']
                                        inputData2 = statis['home']
                                        inputdata = 0 if inputdata == '' else inputdata
                                        inputData2 = 0 if inputData2 == '' else inputData2
                                        print(inputdata, inputData2)
                                        Attacks.append(inputdata)
                                        Attacks2.append(inputData2)

                            elif awayid == teamid:
                                team1.append(awayname)
                                team2.append(homename)
                                place.append(away)
                                place2.append(home)
                                score.append(awayscores)
                                score2.append(homescores)
                                if awayscores > homescores:
                                    outcome.append('TeamOne')
                                elif homescores > awayscores:
                                    outcome.append('TeamTwo')
                                else:
                                    outcome.append('Draw')

                                for statis in stat:
                                    if statis['type'] == ballpos:
                                        inputData3 = statis['away'].replace('%', '')
                                        inputData4 = statis['home'].replace('%', '')
                                        data3 = 0 if inputData3 == '' else inputData3
                                        data4 = 0 if inputData4 == '' else inputData4
                                        print(data3, data4)
                                        possession.append(data3)
                                        possession2.append(data4)
                                    if statis['type'] == passaccu:
                                        inputdata = statis['away']
                                        inputData2 = statis['home']
                                        inputdata = 0 if inputdata == '' else inputdata
                                        inputData2 = 0 if inputData2 == '' else inputData2
                                        print(inputdata, inputData2)
                                        accuracy.append(inputdata)
                                        accuracy2.append(inputData2)
                                    if statis['type'] == shotinside:
                                        inputdata = statis['away']
                                        inputData2 = statis['home']
                                        inputdata = 0 if inputdata == '' else inputdata
                                        inputData2 = 0 if inputData2 == '' else inputData2
                                        print(inputdata, inputData2)
                                        shotinsidebox.append(inputdata)
                                        shotinsidebox2.append(inputData2)
                                    if statis['type'] == dangerous:
                                        inputdata = statis['away']
                                        inputData2 = statis['home']
                                        inputdata = 0 if inputdata == '' else inputdata
                                        inputData2 = 0 if inputData2 == '' else inputData2
                                        print(inputdata, inputData2)
                                        dangerousattacks.append(inputdata)
                                        dangerousattacks2.append(inputData2)
                                    if statis['type'] == target:
                                        inputdata = statis['away']
                                        inputData2 = statis['home']
                                        inputdata = 0 if inputdata == '' else inputdata
                                        inputData2 = 0 if inputData2 == '' else inputData2
                                        print(inputdata, inputData2)
                                        On_target.append(inputdata)
                                        On_target2.append(inputData2)
                                    if statis['type'] == Corner:
                                        inputdata = statis['away']
                                        inputData2 = statis['home']
                                        inputdata = 0 if inputdata == '' else inputdata
                                        inputData2 = 0 if inputData2 == '' else inputData2
                                        print(inputdata, inputData2)
                                        Corners.append(inputdata)
                                        Corners2.append(inputData2)
                                    if statis['type'] == Attack:
                                        inputdata = statis['away']
                                        inputData2 = statis['home']
                                        inputdata = 0 if inputdata == '' else inputdata
                                        inputData2 = 0 if inputData2 == '' else inputData2
                                        print(inputdata, inputData2)
                                        Attacks.append(inputdata)
                                        Attacks2.append(inputData2)

        max_length = max(len(event_date), len(outcome))
        possession = pad_list(possession, max_length)
        dangerousattacks = pad_list(dangerousattacks, max_length)
        accuracy = pad_list(accuracy, max_length)
        On_target =  pad_list(On_target, max_length)
        shotinsidebox = pad_list(shotinsidebox, max_length)
        Corners = pad_list(Corners, max_length)
        Attacks = pad_list(Attacks, max_length)
        
        possession2 = pad_list(possession2, max_length)
        dangerousattacks2 = pad_list(dangerousattacks2, max_length)
        accuracy2 = pad_list(accuracy2, max_length)
        On_target2 = pad_list(On_target2, max_length)
        shotinsidebox2 = pad_list(shotinsidebox2, max_length)
        Corners2 = pad_list(Corners2, max_length)
        Attacks2 = pad_list(Attacks2, max_length)



        print(len(outcome), len(event_date), len(team1), len(score), len(place), len(possession), len(dangerousattacks), len(accuracy), len(On_target), len(shotinsidebox), len(Corners), len(
            Attacks), len(team2), len(score2), len(place2), len(possession2), len(dangerousattacks2), len(accuracy2), len(On_target2), len(shotinsidebox2), len(Corners2), len(Attacks2))


        return outcome, event_date, team1, score, place, possession, dangerousattacks, accuracy, On_target, shotinsidebox, Corners, Attacks, team2, score2, place2, possession2, dangerousattacks2, accuracy2, On_target2, shotinsidebox2, Corners2, Attacks
    else:
        print(responed.status_code)



def getpastfivematch(teamid=80, trainData=False):

    score = []
    place = []
    possession = []
    shotinsidebox = []
    dangerousattacks = []
    accuracy = []
    On_target = []
    Corners = []
    Attacks = []

    score2 = []
    place2 = []
    possession2 = []
    shotinsidebox2 = []
    dangerousattacks2 = []
    accuracy2 = []
    On_target2 = []
    Corners2 = []
    Attacks2 = []
    team2id = []

    outcome = []
    team1 = []
    team2 = []
    event_date = []
    away = 1
    home = 2

    ballpos = 'Ball Possession'
    passaccu = 'Passes Accurate'
    shotinside = 'Shots Inside Box'
    dangerous = 'Dangerous Attacks'
    target = 'On Target'
    Corner = 'Corners'
    Attack = 'Attacks'


    url = f'https://apiv2.allsportsapi.com/football/?met=Fixtures&APIkey={api_key}&from=2024-04-01&to={today}&teamId={teamid}'

    respond  = requests.get(url=url)
    if respond.status_code ==  200:
        if 'result' in respond.json():
            featuredata = respond.json()['result']
            print(featuredata)
            for match in featuredata:
                homeid = match['home_team_key']
                awayid = match['away_team_key']
                homename = match['event_home_team']
                awayname = match['event_away_team']
                goals = match['event_final_result']
                event_date.append(match['event_date'])
                stat = match['statistics']

                if goals == '-':
                    if teamid == homeid:
                        team1.append(teamid)
                        team2.append(awayname)
                        team2id.append(awayid)
                        place.append(home)
                        place2.append(away)
                        score.append(0)
                        score2.append(0)
                        outcome.append('Draw')
                    elif teamid == awayid:
                        team1.append(teamid)
                        team2.append(homename)
                        team2id.append(homeid)
                        place.append(away)
                        place2.append(home)
                        score.append(0)
                        score2.append(0)
                        outcome.append('Draw')
                else:
                    homescores = goals[0]
                    awayscores = goals[4]
                    if homeid == teamid:
                        team1.append(teamid)
                        team2.append(awayname)
                        team2id.append(awayid)
                        place.append(home)
                        place2.append(away)
                        score.append(homescores)
                        score2.append(awayscores)
                        if trainData == True:
                            if homescores > awayscores:
                                outcome.append('TeamOne')
                            elif awayscores > homescores:
                                outcome.append('TeamTwo')
                            else:
                                outcome.append('Draw')
                        else:
                            if homescores > awayscores:
                                outcome.append('Win')
                            elif awayscores > homescores:
                                outcome.append('Loss')
                            else:
                                outcome.append('Draw')

                        for statis in stat:
                            if statis['type'] == ballpos:
                                inputData = statis['home'].replace('%', '')
                                inputData2 = statis['away'].replace('%', '')
                                data = 0 if inputData == '' else inputData
                                data2 = 0 if inputData2 == '' else inputData2
                                print(data, data2)
                                possession.append(data)
                                possession2.append(data2)
                            if statis['type'] == passaccu:
                                inputData = statis['home'].replace('%', '')
                                inputData2 = statis['away'].replace('%', '')
                                data = 0 if inputData == '' else inputData
                                data2 = 0 if inputData2 == '' else inputData2
                                print(data, data2)
                                accuracy.append(data)
                                accuracy2.append(data2)
                            if statis['type'] == shotinside:
                                inputData = statis['home'].replace('%', '')
                                inputData2 = statis['away'].replace('%', '')
                                data = 0 if inputData == '' else inputData
                                data2 = 0 if inputData2 == '' else inputData2
                                print(data, data2)
                                shotinsidebox.append(data)
                                shotinsidebox2.append(data2)
                            if statis['type'] == dangerous:
                                inputData = statis['home'].replace('%', '')
                                inputData2 = statis['away'].replace('%', '')
                                data = 0 if inputData == '' else inputData
                                data2 = 0 if inputData2 == '' else inputData2
                                print(data, data2)
                                dangerousattacks.append(data)
                                dangerousattacks2.append(data2)
                            if statis['type'] == target:
                                inputData = statis['home'].replace('%', '')
                                inputData2 = statis['away'].replace('%', '')
                                data = 0 if inputData == '' else inputData
                                data2 = 0 if inputData2 == '' else inputData2
                                print(data, data2)
                                On_target.append(data)
                                On_target2.append(data2)
                            if statis['type'] == Corner:
                                inputData = statis['home'].replace('%', '')
                                inputData2 = statis['away'].replace('%', '')
                                data = 0 if inputData == '' else inputData
                                data2 = 0 if inputData2 == '' else inputData2
                                print(data, data2)
                                Corners.append(data)
                                Corners2.append(data2)
                            if statis['type'] == Attack:
                                inputData = statis['home'].replace('%', '')
                                inputData2 = statis['away'].replace('%', '')
                                data = 0 if inputData == '' else inputData
                                data2 = 0 if inputData2 == '' else inputData2
                                print(data, data2)
                                Attacks.append(data)
                                Attacks2.append(data2)

                    elif awayid == teamid:
                        team1.append(teamid)
                        team2.append(homename)
                        team2id.append(homeid)
                        place.append(away)
                        place2.append(home)
                        score.append(awayscores)
                        score2.append(homescores)
                        if trainData == True:
                            if homescores > awayscores:
                                outcome.append('TeamOne')
                            elif awayscores > homescores:
                                outcome.append('TeamTwo')
                            else:
                                outcome.append('Draw')
                        else:
                            if homescores > awayscores:
                                outcome.append('Win')
                            elif awayscores > homescores:
                                outcome.append('Loss')
                            else:
                                outcome.append('Draw')

                        for statis in stat:
                            if statis['type'] == ballpos:
                                inputData3 = statis['away'].replace('%', '')
                                inputData4 = statis['home'].replace('%', '')
                                data3 = 0 if inputData3 == '' else inputData3
                                data4 = 0 if inputData4 == '' else inputData4
                                print(data3, data4)
                                possession.append(data3)
                                possession2.append(data4)
                            if statis['type'] == passaccu:
                                inputdata = statis['away']
                                inputData2 = statis['home']
                                inputdata = 0 if inputdata == '' else inputdata
                                inputData2 = 0 if inputData2 == '' else inputData2
                                print(inputdata, inputData2)
                                accuracy.append(inputdata)
                                accuracy2.append(inputData2)
                            if statis['type'] == shotinside:
                                inputdata = statis['away']
                                inputData2 = statis['home']
                                inputdata = 0 if inputdata == '' else inputdata
                                inputData2 = 0 if inputData2 == '' else inputData2
                                print(inputdata, inputData2)
                                shotinsidebox.append(inputdata)
                                shotinsidebox2.append(inputData2)
                            if statis['type'] == dangerous:
                                inputdata = statis['away']
                                inputData2 = statis['home']
                                inputdata = 0 if inputdata == '' else inputdata
                                inputData2 = 0 if inputData2 == '' else inputData2
                                print(inputdata, inputData2)
                                dangerousattacks.append(inputdata)
                                dangerousattacks2.append(inputData2)
                            if statis['type'] == target:
                                inputdata = statis['away']
                                inputData2 = statis['home']
                                inputdata = 0 if inputdata == '' else inputdata
                                inputData2 = 0 if inputData2 == '' else inputData2
                                print(inputdata, inputData2)
                                On_target.append(inputdata)
                                On_target2.append(inputData2)
                            if statis['type'] == Corner:
                                inputdata = statis['away']
                                inputData2 = statis['home']
                                inputdata = 0 if inputdata == '' else inputdata
                                inputData2 = 0 if inputData2 == '' else inputData2
                                print(inputdata, inputData2)
                                Corners.append(inputdata)
                                Corners2.append(inputData2)
                            if statis['type'] == Attack:
                                inputdata = statis['away']
                                inputData2 = statis['home']
                                inputdata = 0 if inputdata == '' else inputdata
                                inputData2 = 0 if inputData2 == '' else inputData2
                                print(inputdata, inputData2)
                                Attacks.append(inputdata)
                                Attacks2.append(inputData2)


        lowerdangerousattacks = remove_lower_than_10(dangerousattacks)
        lowerdangerousattacks2 = remove_lower_than_10(dangerousattacks)
        lowerAttacks = remove_lower_than_10(Attacks)
        lowerAttacks2 = remove_lower_than_10(Attacks2)

        max_length = max(len(event_date), len(outcome))
        possession = pad_list(possession, max_length)
        lowerdangerousattacks = pad_list(lowerdangerousattacks, max_length)
        accuracy = pad_list(accuracy, max_length)
        On_target =  pad_list(On_target, max_length)
        shotinsidebox = pad_list(shotinsidebox, max_length)
        Corners = pad_list(Corners, max_length)
        lowerAttacks = pad_list(lowerAttacks, max_length)
        possession2 = pad_list(possession2, max_length)
        lowerdangerousattacks2 = pad_list(lowerdangerousattacks2, max_length)
        accuracy2 = pad_list(accuracy2, max_length)
        On_target2 = pad_list(On_target2, max_length)
        shotinsidebox2 = pad_list(shotinsidebox2, max_length)
        Corners2 = pad_list(Corners2, max_length)
        lowerAttacks2 = pad_list(lowerAttacks2, max_length)

        

        print(len(outcome), len(event_date), len(team1), len(score), len(place), len(possession), len(lowerdangerousattacks), len(accuracy), len(On_target), len(shotinsidebox), len(Corners), len(
            lowerAttacks), len(team2), len(score2), len(place2), len(possession2), len(lowerdangerousattacks2), len(accuracy2), len(On_target2), len(shotinsidebox2), len(Corners2), len(lowerAttacks2), len(team2id))



        return outcome, event_date, team1, score, place, possession, lowerdangerousattacks, accuracy, On_target, shotinsidebox, Corners, lowerAttacks, team2, score2, place2, possession2, lowerdangerousattacks2, accuracy2, On_target2, shotinsidebox2, Corners2, lowerAttacks2, team2id

    else: print(respond.status_code)

      




def getneededteamid(teamid):
    url = f'https://apiv2.allsportsapi.com/football/?met=Fixtures&APIkey={api_key}&from=2023-01-01&to=2024-03-2&teamId={teamid}'
    
    respond =  requests.get(url=url)
    if respond.status_code == 200:
        data = respond.json()['result']
        for match in data:
            homeid = match['home_team_key']
            awayid = match['away_team_key']
            homename = match['event_home_team']
            awayname = match['event_away_team']
            if teamid == homeid:
                print(f'the id passed in the function is the home team id team name : {homename} ')
                print(f'opponent id : {awayid}  opponent name : {awayname}')
                print('\n\n\n')
            elif teamid == awayid:
                print(f'the id passed in the function is the away team id away name {awayname} ')
                print(f'opponent id : {homeid}  opponent name : {homename}')
                print('\n\n\n')



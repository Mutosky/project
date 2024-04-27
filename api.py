import requests
import numpy as np
from datetime import date


today = date.today()
api_key = "c0bbeb584e5287c7d142f75486275a19f48090969411a85d6b5721ed35e090bd"


def pad_list(lst, max_length):
    return lst + [np.nan] * (max_length - len(lst))


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
                    featuredata = featurerespond.json()['result'][:1]
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
                                        possession.append(
                                            statis['home'].replace('%', ''))
                                        possession2.append(
                                            statis['away'].replace('%', ''))
                                    if statis['type'] == passaccu:
                                        accuracy.append(statis['home'])
                                        accuracy2.append(statis['away'])
                                    if statis['type'] == shotinside:
                                        shotinsidebox.append(statis['home'])
                                        shotinsidebox2.append(statis['away'])
                                    if statis['type'] == dangerous:
                                        dangerousattacks.append(statis['home'])
                                        dangerousattacks2.append(
                                            statis['away'])
                                    if statis['type'] == target:
                                        On_target.append(statis['home'])
                                        On_target2.append(statis['away'])
                                    if statis['type'] == Corner:
                                        Corners.append(statis['home'])
                                        Corners2.append(statis['away'])
                                    if statis['type'] == Attack:
                                        Attacks.append(statis['home'])
                                        Attacks2.append(statis['away'])

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
                                        possession.append(
                                            statis['away'].replace('%', ''))
                                        possession2.append(
                                            statis['home'].replace('%', ''))
                                    if statis['type'] == passaccu:
                                        accuracy.append(statis['away'])
                                        accuracy2.append(statis['home'])
                                    if statis['type'] == shotinside:
                                        shotinsidebox.append(statis['away'])
                                        shotinsidebox2.append(statis['home'])
                                    if statis['type'] == dangerous:
                                        dangerousattacks.append(statis['away'])
                                        dangerousattacks2.append(
                                            statis['home'])
                                    if statis['type'] == target:
                                        On_target.append(statis['away'])
                                        On_target2.append(statis['home'])
                                    if statis['type'] == Corner:
                                        Corners.append(statis['away'])
                                        Corners2.append(statis['home'])
                                    if statis['type'] == Attack:
                                        Attacks.append(statis['away'])
                                        Attacks2.append(statis['home'])

        max_length = max(len(score), len(outcome))
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


        return outcome, event_date, team1, score, place, possession, dangerousattacks, accuracy, On_target, shotinsidebox, Corners, Attacks, team2, score2, place2, possession2, dangerousattacks2, accuracy2, On_target2, shotinsidebox2, Corners2, Attacks2
    else:
        print(responed.status_code)


def getpastfivematch(teamid= 80, trainData =False):

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


    url = f'https://apiv2.allsportsapi.com/football/?met=Fixtures&APIkey={api_key}&from=2023-09-01&to={today}&teamId={teamid}'

    respond  = requests.get(url=url)
    if respond.status_code ==  200:
        if 'result' in respond.json():
            featuredata = respond.json()['result']
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
                                possession.append(
                                    statis['home'].replace('%', ''))
                                possession2.append(
                                    statis['away'].replace('%', ''))
                            if statis['type'] == passaccu:
                                accuracy.append(statis['home'])
                                accuracy2.append(statis['away'])
                            if statis['type'] == shotinside:
                                shotinsidebox.append(statis['home'])
                                shotinsidebox2.append(statis['away'])
                            if statis['type'] == dangerous:
                                dangerousattacks.append(statis['home'])
                                dangerousattacks2.append(
                                    statis['away'])
                            if statis['type'] == target:
                                On_target.append(statis['home'])
                                On_target2.append(statis['away'])
                            if statis['type'] == Corner:
                                Corners.append(statis['home'])
                                Corners2.append(statis['away'])
                            if statis['type'] == Attack:
                                Attacks.append(statis['home'])
                                Attacks2.append(statis['away'])

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
                                possession.append(
                                    statis['away'].replace('%', ''))
                                possession2.append(
                                    statis['home'].replace('%', ''))
                            if statis['type'] == passaccu:
                                accuracy.append(statis['away'])
                                accuracy2.append(statis['home'])
                            if statis['type'] == shotinside:
                                shotinsidebox.append(statis['away'])
                                shotinsidebox2.append(statis['home'])
                            if statis['type'] == dangerous:
                                dangerousattacks.append(statis['away'])
                                dangerousattacks2.append(
                                    statis['home'])
                            if statis['type'] == target:
                                On_target.append(statis['away'])
                                On_target2.append(statis['home'])
                            if statis['type'] == Corner:
                                Corners.append(statis['away'])
                                Corners2.append(statis['home'])
                            if statis['type'] == Attack:
                                Attacks.append(statis['away'])
                                Attacks2.append(statis['home'])


        max_length = max(len(score), len(outcome))
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

        return outcome, event_date, team1, score, place, possession, dangerousattacks, accuracy, On_target, shotinsidebox, Corners, Attacks, team2, score2, place2, possession2, dangerousattacks2, accuracy2, On_target2, shotinsidebox2, Corners2, Attacks2, team2id

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



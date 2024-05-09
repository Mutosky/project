from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import pandas as pd
from api import getTestData, getpastfivematch


def loop(data):
    itemList = []
    for dat in data:
        itemList.append(dat)
    return itemList


def put_in_list(data):
    win = []
    loss = []
    draw = []
    for proba in data:
        draw.append(proba[0])
        loss.append(proba[1])
        win.append(proba[2])

    return win, loss, draw


def needData(data, data2):
    team1OpponentName = []
    team1MatchDate = []
    team1MatchOutcome = []
    team2OpponentName = []
    team2MatchDate = []
    team2MatchOutcome = []

    for dat in data['team2_id']:
        team1OpponentName.append(dat)
    for dat in data['event_date']:
        team1MatchDate.append(dat)
    for dat in data['match_outcome']:
        team1MatchOutcome.append(dat)
    for dat in data2['team2_id']:
        team2OpponentName.append(dat)
    for dat in data2['event_date']:
        team2MatchDate.append(dat)
    for dat in data2['match_outcome']:
        team2MatchOutcome.append(dat)

    return team1OpponentName, team1MatchDate, team1MatchOutcome, team2OpponentName, team2MatchDate, team2MatchOutcome


def datas(teamid=80, team2id=141, Head2Head=False):
    if Head2Head == True:
        outcome, event_date, team1, score, place, possession, dangerousattacks, accuracies, On_target, shotinsidebox, Corners, Attacks, team2, score2, place2, possession2, dangerousattacks2, accuracies2, On_target2, shotinsidebox2, Corners2, Attacks2 = getTestData(
            teamid=teamid, teamid2=team2id)
    else:
        outcome, event_date, team1, score, place, possession, dangerousattacks, accuracies, On_target, shotinsidebox, Corners, Attacks, team2, score2, place2, possession2, dangerousattacks2, accuracies2, On_target2, shotinsidebox2, Corners2, Attacks2, _ = getpastfivematch(
            teamid=teamid)

    data = pd.DataFrame({
        'event_date': event_date,
        'match_outcome': outcome,
        'team1_id': team1,
        'team1_possession': possession,
        'team1_accuracy': accuracies,
        'team1_shotinsidebox': shotinsidebox,
        'team1_dangerousattacks': dangerousattacks,
        'team1_place': place,
        'team1_scores': score,
        'team1_on_target': On_target,
        'team1_corners': Corners,
        'team1_attacks': Attacks,
        'team2_id': team2,
        'team2_possession': possession2,
        'team2_accuracy': accuracies2,
        'team2_shotinsidebox': shotinsidebox2,
        'team2_dangerousattacks': dangerousattacks2,
        'team2_place': place2,
        'team2_scores': score2,
        'team2_on_target': On_target2,
        'team2_corners': Corners2,
        'team2_attacks': Attacks2
    })

    return data


def test_data(data=pd.DataFrame({}), oneData=False, home=False):
    outcome_mapping = {'Loss': 0, 'Win': 2, 'Draw': 1}
    data['numerical_outcome'] = data['match_outcome'].map(outcome_mapping)

    if oneData == True:
        neededData = data[['match_outcome', 'event_date', 'team2_id', 'team1_id']]
        testData = data.head(n=1)
        testData = testData.drop(
            columns=['event_date', 'match_outcome', 'team1_id', 'team2_id'])
    else:
        if home == True:
            data = data[data['team1_place'] == 2]
            data = data.fillna(data.mode().iloc[0])
            data = data.sort_values(by='event_date', ascending=False)
            testData = data.head(n=5)
            neededData = testData[['match_outcome',
                                   'event_date', 'team2_id', 'team1_place']]
            testData = testData.drop(
                columns=['event_date', 'match_outcome', 'team1_id', 'team2_id'])
        else:
            data = data.fillna(data.mode().iloc[0])
            data = data.sort_values(by='event_date', ascending=False)
            testData = data.head(n=5)
            neededData = testData[['match_outcome', 'event_date', 'team2_id']]
            testData = testData.drop(
                columns=['event_date', 'match_outcome', 'team1_id', 'team2_id'])

    return testData, neededData


def modeltraining(data=pd.DataFrame({})):
    outcome_mapping = {'Loss': 0, 'Win': 2, 'Draw': 1}
    data['numerical_outcome'] = data['match_outcome'].map(outcome_mapping)
    data = data.fillna(data.mode().iloc[0])
    data = data.sort_values(by='event_date', ascending=True)

    feature = data.drop(
        columns=['match_outcome', 'event_date', 'team1_id', 'team2_id'])

    encoder = LabelEncoder()
    label = data[['match_outcome']]
    encodedLabel = encoder.fit_transform(label)

    X_trian, _, Y_trian, _ = train_test_split(
        feature, encodedLabel, random_state=42, test_size=0.1)

    model = RandomForestClassifier(n_estimators=20, random_state=1)
    model.fit(X=X_trian, y=Y_trian)

    return model


def pastfivematch(teamid):
    data = datas(teamid=teamid)
    model = modeltraining(data=data)
    X_test, neededData = test_data(data=data)
    prediction = model.predict_proba(X=X_test)
    return prediction, neededData


def Head2Head(teamid, team2id):
    trainData = datas(teamid=teamid)
    model = modeltraining(data=trainData)
    data = datas(teamid=teamid, team2id=team2id, Head2Head=True)
    X_test, neededData = test_data(data=data, oneData=True)
    prediction = model.predict_proba(X=X_test)

    prediction_list = []
    for matchs in prediction:
        for proba in matchs:
            prediction_list.append(proba)

    return prediction_list, neededData


def homeAdvantage(teamid):
    Data = datas(teamid=teamid)
    model = modeltraining(data=Data)
    X_test, neededData = test_data(data=Data, home=True)
    prediction = model.predict_proba(X_test)
    return prediction, neededData

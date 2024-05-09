from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import pandas as pd
from api import getTestData, getpastfivematch



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

    for dat in data['team1_opponentname']:
        team1OpponentName.append(dat)
    for dat in data['team1_match_date']:
        team1MatchDate.append(dat)
    for dat in data['team1_Outcome']:
        team1MatchOutcome.append(dat)
    for dat in data2['team2_opponentname']:
        team2OpponentName.append(dat)
    for dat in data2['team2_match_date']:
        team2MatchDate.append(dat)
    for dat in data2['team2_Outcome']:
        team2MatchOutcome.append(dat)

    return team1OpponentName, team1MatchDate, team1MatchOutcome, team2OpponentName, team2MatchDate, team2MatchOutcome


def predictionalgorithm(team1id, team2id):
    outcome, event_date, team1, score, place, possession, dangerousattacks, accuracies, On_target, shotinsidebox, Corners, Attacks, team2, score2, place2, possession2, dangerousattacks2, accuracies2, On_target2, shotinsidebox2, Corners2, Attacks2 = getTestData(
        teamid=team1id, teamid2=team2id)
    outcomeB, event_dateB, team1B, scoreB, placeB, possessionB, dangerousattacksB, accuraciesB, On_targetB, shotinsideboxB, CornersB, AttacksB, team2B, score2B, place2B, possession2B, dangerousattacks2B, accuracies2B, On_target2B, shotinsidebox2B, Corners2B, Attacks2B, team2ids = getpastfivematch(
        trainData=True)

    testdata = pd.DataFrame({
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

    traindata = pd.DataFrame({
        'event_date': event_dateB,
        'match_outcome': outcomeB,
        'team1_id': team1B,
        'team1_possession': possessionB,
        'team1_accuracy': accuraciesB,
        'team1_shotinsidebox': shotinsideboxB,
        'team1_dangerousattacks': dangerousattacksB,
        'team1_place': placeB,
        'team1_scores': scoreB,
        'team1_on_target': On_targetB,
        'team1_corners': CornersB,
        'team1_attacks': AttacksB,
        'team2_id': team2B,
        'team2_possession': possession2B,
        'team2_accuracy': accuracies2B,
        'team2_shotinsidebox': shotinsidebox2B,
        'team2_dangerousattacks': dangerousattacks2B,
        'team2_place': place2B,
        'team2_scores': score2B,
        'team2_on_target': On_target2B,
        'team2_corners': Corners2B,
        'team2_attacks': Attacks2B
    })

    traindata = traindata.fillna(traindata.mode().iloc[0])
    traindata = traindata.sort_values(by='event_date', ascending=True)
    testdata = testdata.sort_values(by='event_date', ascending=False)

    features = traindata.drop(
        columns=['event_date', 'match_outcome', 'team2_id', 'team1_id'])

    # label encoding
    labels = traindata['match_outcome']
    encoded_label = LabelEncoder().fit_transform(labels)

    # model trainig
    X_train, _, Y_train, _ = train_test_split(
        features, encoded_label, test_size=0.1, random_state=50)
    model = RandomForestClassifier(n_estimators=20, random_state=1)
    model.fit(X=X_train, y=Y_train)

    # testdata
    X_test = testdata.head(n=1)
    X_test = X_test.drop(
        columns=['event_date', 'match_outcome', 'team1_id', 'team2_id'])

    # prediction
    probability = model.predict_proba(X_test)

    # needed data for displaying

    teamData = testdata[['event_date',
                         'match_outcome', 'team1_id', 'team2_id']]
    probability_list = []

   # changed to list because nparry can be passed in json to frontend javascript
    for matchs in probability:
        for proba in matchs:
            probability_list.append(proba)
    return probability_list, teamData


def predictionalgorithm2(team1id, team2id):
    outcome, event_date, team1, score, place, possession, dangerousattacks, accuracies, On_target, shotinsidebox, Corners, Attacks, team2, score2, place2, possession2, dangerousattacks2, accuracies2, On_target2, shotinsidebox2, Corners2, Attacks2, team2ids = getpastfivematch(
        teamid=team1id)
    outcomeB, event_dateB, team1B, scoreB, placeB, possessionB, dangerousattacksB, accuraciesB, On_targetB, shotinsideboxB, CornersB, AttacksB, team2B, score2B, place2B, possession2B, dangerousattacks2B, accuracies2B, On_target2B, shotinsidebox2B, Corners2B, Attacks2B, team2idsB = getpastfivematch(
        teamid=team2id)

    dataA = pd.DataFrame({
        'team1_Outcome': outcome,
        'team1_match_date': event_date,
        'team1id': team1,
        'team1_opponentname': team2,
        'team1_opponentid': team2ids,
        'team1_scores': score,
        'team1_opponent_scores': score2,
        'team1_place': place,
        'team1_opponent_place': place2,
        'team1_possession': possession,
        'team1_opponent_possession': possession2,
        'team1_dangerousattacks': dangerousattacks,
        'team1_opponent_dangerousattacks': dangerousattacks2,
        'team1_accuracy': accuracies,
        'team1_opponent_accuracy': accuracies2,
        'team1_on_target': On_target,
        'team1_opponent_on_target': On_target2,
        'team1_shotinsidebox': shotinsidebox,
        'team1_opponent_shotinsidebox': shotinsidebox2,
        'team1_corner': Corners,
        'team1_opponent_corner': Corners2,
        'team1_attacks': Attacks,
        'team1_opponent_atttacks': Attacks2
    })

    dataB = pd.DataFrame({
        'team2_Outcome': outcomeB,
        'team2_match_date': event_dateB,
        'team2id': team1B,
        'team2_opponentname': team2B,
        'team2_opponentid': team2idsB,
        'team2_scores': scoreB,
        'team2_opponent_scores': score2B,
        'team2_place': placeB,
        'team2_opponent_place': place2B,
        'team2_possession': possessionB,
        'team2_opponent_possession': possession2B,
        'team2_dangerousattacks': dangerousattacksB,
        'team2_opponent_dangerousattacks': dangerousattacks2B,
        'team2_accuracy': accuraciesB,
        'team2_opponent_accuracy': accuracies2B,
        'team2_on_target': On_targetB,
        'team2_opponent_on_target': On_target2B,
        'team2_shotinsidebox': shotinsideboxB,
        'team2_opponent_shotinsidebox': shotinsidebox2B,
        'team2_corner': CornersB,
        'team2_opponent_corner': Corners2B,
        'team2_attacks': AttacksB,
        'team2_opponent_atttacks': Attacks2B
    })

    outcome_mapping = {'Loss': 0, 'Win': 2, 'Draw': 1}

    dataA['numerical_outcome'] = dataA['team1_Outcome'].map(outcome_mapping)
    dataB['numerical_outcome'] = dataB['team2_Outcome'].map(outcome_mapping)
    dataA = dataA.fillna(dataA.mode().iloc[0])
    dataB = dataB.fillna(dataB.mode().iloc[0])
    dataA = dataA.sort_values(by='team1_match_date', ascending=True)
    dataB = dataB.sort_values(by='team2_match_date', ascending=True)

    features1 = dataA.drop(
        columns=['team1_Outcome', 'team1_match_date', 'team1id', 'team1_opponentname'])
    features2 = dataB.drop(
        columns=['team2_Outcome', 'team2_match_date', 'team2id', 'team2_opponentname'])

    label1 = dataA['team1_Outcome']
    encoded_labelteam1 = LabelEncoder().fit_transform(label1)
    label2 = dataB['team2_Outcome']
    encoded_labelteam2 = LabelEncoder().fit_transform(label2)

    X_train, _, Y_train, _ = train_test_split(
        features1, encoded_labelteam1, test_size=0.1, random_state=42)
    X_trainT, _, Y_trainT, _ = train_test_split(
        features2, encoded_labelteam2, test_size=0.1, random_state=42)

    model1 = RandomForestClassifier(n_estimators=20, random_state=1)
    model2 = RandomForestClassifier(n_estimators=20, random_state=1)

    model1.fit(X=X_train, y=Y_train)
    model2.fit(X=X_trainT, y=Y_trainT)

    label_encoder1 = LabelEncoder()
    label_encoder2 = LabelEncoder()
    label_encoder1.fit(dataA['team1_Outcome'])
    label_encoder2.fit(dataB['team2_Outcome'])

    dataA = dataA.sort_values(by='team1_match_date', ascending=False)
    dataB = dataB.sort_values(by='team2_match_date', ascending=False)

    X_test1 = dataA.head(n=5)
    team1outcome = X_test1[['team1_Outcome',
                            'team1_match_date', 'team1_opponentname']]
    X_test1 = X_test1.drop(
        columns=['team1_Outcome', 'team1_match_date', 'team1id', 'team1_opponentname'])

    X_test2 = dataB.head(n=5)
    team2outcome = X_test2[['team2_Outcome',
                            'team2_match_date', 'team2_opponentname']]
    X_test2 = X_test2.drop(
        columns=['team2_Outcome', 'team2_match_date', 'team2id', 'team2_opponentname'])

    Team1_probability = model1.predict_proba(X=X_test1)
    Team2_probability = model2.predict_proba(X=X_test2)

    return Team1_probability, team1outcome, Team2_probability, team2outcome


def advanges(team1id):
    outcome, event_date, team1, score, place, possession, dangerousattacks, accuracies, On_target, shotinsidebox, Corners, Attacks, team2, score2, place2, possession2, dangerousattacks2, accuracies2, On_target2, shotinsidebox2, Corners2, Attacks2, team2ids = getpastfivematch(
        teamid=team1id)

    data = pd.DataFrame({
        'team1_Outcome': outcome,
        'team1_match_date': event_date,
        'team1id': team1,
        'team1_opponentname': team2,
        'team1_opponentid': team2ids,
        'team1_scores': score,
        'team1_opponent_scores': score2,
        'team1_place': place,
        'team1_opponent_place': place2,
        'team1_possession': possession,
        'team1_opponent_possession': possession2,
        'team1_dangerousattacks': dangerousattacks,
        'team1_opponent_dangerousattacks': dangerousattacks2,
        'team1_accuracy': accuracies,
        'team1_opponent_accuracy': accuracies2,
        'team1_on_target': On_target,
        'team1_opponent_on_target': On_target2,
        'team1_shotinsidebox': shotinsidebox,
        'team1_opponent_shotinsidebox': shotinsidebox2,
        'team1_corner': Corners,
        'team1_opponent_corner': Corners2,
        'team1_attacks': Attacks,
        'team1_opponent_atttacks': Attacks2
    })
    print(data['team1_place'])

    outcome_mapping = {'Loss': 0, 'Win': 2, 'Draw': 1}

    dataA['numerical_outcome'] = dataA['team1_Outcome'].map(outcome_mapping)
    dataA = dataA.fillna(dataA.mode().iloc[0])
    dataA = dataA.sort_values(by='team1_match_date', ascending=True)

    features1 = dataA.drop(
        columns=['team1_Outcome', 'team1_match_date', 'team1id', 'team1_opponentname'])

    label1 = dataA['team1_Outcome']
    encoded_labelteam1 = LabelEncoder().fit_transform(label1)

    X_train, _, Y_train, _ = train_test_split(
        features1, encoded_labelteam1, test_size=0.1, random_state=42)

    model1 = RandomForestClassifier(n_estimators=20, random_state=1)

    model1.fit(X=X_train, y=Y_train)

    label_encoder1 = LabelEncoder()
    label_encoder1.fit(dataA['team1_Outcome'])

    dataA = dataA.sort_values(by='team1_match_date', ascending=False)

    X_test1 = dataA.head(n=5)
    team1outcome = X_test1[['team1_Outcome',
                            'team1_match_date', 'team1_opponentname']]
    X_test1 = X_test1.drop(
        columns=['team1_Outcome', 'team1_match_date', 'team1id', 'team1_opponentname'])

    Team1_probability = model1.predict_proba(X=X_test1)

    return Team1_probability, team1outcome


teamid = 80
team2id = 100
Team1_probability, team1outcome, Team2_probability, team2outcome = predictionalgorithm2(
    team1id=teamid, team2id=team2id)
print(Team1_probability)
print(team1outcome)
print(Team2_probability)
print(team2outcome)

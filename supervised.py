from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score
from sklearn.metrics import classification_report
from scipy.stats import norm
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from api import getdata, getpastfivematch

class algorithms():

    def predictionalgorithm(team1id, team2id):
        outcome, event_date, team1, score, place, possession, dangerousattacks, accuracies, On_target, shotinsidebox, Corners, Attacks, team2, score2, place2, possession2, dangerousattacks2, accuracies2, On_target2, shotinsidebox2, Corners2, Attacks2 = getdata(
            teamid=team1id, teamid2=team2id)
        
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


        data = data.fillna(data.mode().iloc[0])
        data = data.sort_values(by='event_date', ascending=True)


        features = data.drop(columns=['event_date', 'match_outcome', 'team1_id', 'team2_id'])
        
        labels = data['match_outcome']
        encoded_label = LabelEncoder().fit_transform(labels)
        needed_data = data[['match_outcome', 'event_date', 'team1_scores', 'team2_scores']]
        print('\n', needed_data, '\n')

        
        X_train, _, Y_train, _ = train_test_split(features, encoded_label, test_size=0.1, random_state=50)

        model = RandomForestClassifier(n_estimators=20, random_state=1)


        model.fit(X=X_train, y=Y_train)

        # Predict
        matchdrawn = data[data['match_outcome'] == 'Draw']
        if matchdrawn.empty:
            print('empty')
        else: matchdrawn = matchdrawn.sample(n=1)

        matchteamone = data[data['match_outcome'] == 'TeamOne']
        if matchteamone.empty:
            print('empty')
        else: matchteamone = matchteamone.sample(n=1)

        matchteamtwo = data[data['match_outcome'] == 'TeamTwo']
        if matchteamtwo.empty:
            print('empty')
        else: matchteamtwo = matchteamtwo.sample(n=1)
        print('\n')

        X_test = pd.concat([matchdrawn, matchteamone, matchteamtwo])
        X_test = X_test.drop(columns=['event_date', 'match_outcome', 'team1_id', 'team2_id'])


        y_pred = model.predict(X_test)

        labels_encoder = LabelEncoder()
        labels_encoder.fit(data['match_outcome'])

        predicted_label = labels_encoder.inverse_transform(y_pred)
        print(predicted_label)

        probability = f'H2H probability \n {model.predict_proba(X_test)}'

        return probability










    def predictionalgorithm2(team1id, team2id):
        outcome, event_date, team1, score, place, possession, dangerousattacks, accuracies, On_target, shotinsidebox, Corners, Attacks, team2, score2, place2, possession2, dangerousattacks2, accuracies2, On_target2, shotinsidebox2, Corners2, Attacks2 = getpastfivematch(
            teamid=team1id)
        outcomeB, event_dateB, team1B, scoreB, placeB, possessionB, dangerousattacksB, accuraciesB, On_targetB, shotinsideboxB, CornersB, AttacksB, team2B, score2B, place2B, possession2B, dangerousattacks2B, accuracies2B, On_target2B, shotinsidebox2B, Corners2B, Attacks2B= getpastfivematch(
            teamid=team2id)
        

        dataA = pd.DataFrame({
            'team1_Outcome': outcome,
            'team1_match_date': event_date,
            'team1id': team1,
            'team1_opponentid': team2,
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
            'team2_opponentid': team2B,
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



        features1 = dataA.drop(columns=['team1_Outcome', 'team1_match_date', 'team1id', 'team1_opponentid'])
        features2 = dataB.drop(columns=['team2_Outcome', 'team2_match_date', 'team2id', 'team2_opponentid'])

        label1 = dataA['team1_Outcome']
        encoded_labelteam1 = LabelEncoder().fit_transform(label1)
        label2 = dataB['team2_Outcome']
        encoded_labelteam2 = LabelEncoder().fit_transform(label2)

        X_train, _, Y_train, _ = train_test_split(features1, encoded_labelteam1, test_size=0.1, random_state=42)
        X_trainT, _, Y_trainT, _ = train_test_split(features2, encoded_labelteam2, test_size=0.1, random_state=42)

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

        matchdrawn = dataA[dataA['team1_Outcome'] == 'Draw']
        if matchdrawn.empty:
            print('empty')
        else:
            matchdrawn = matchdrawn.head(n=1)

        matchwon = dataA[dataA['team1_Outcome'] == 'Win']
        if matchwon.empty:
            print('empty')
        else:
            matchwon = matchwon.head(n=1)

        matchloss = dataA[dataA['team1_Outcome'] == 'Loss']
        if matchloss.empty:
            print('empty')
        else:
            matchloss = matchloss.head(n=1)



        matchdrawn2 = dataB[dataB['team2_Outcome'] == 'Draw']
        if matchdrawn2.empty:
            print('empty')
        else:
            matchdrawn2 = matchdrawn2.head(n=1)

        matchwon2 = dataB[dataB['team2_Outcome'] == 'Win']
        if matchwon2.empty:
            print('empty')
        else:
            matchwon2 = matchwon2.head(n=1)

        matchloss2 = dataB[dataB['team2_Outcome'] == 'Loss']
        if matchloss2.empty:
            print('empty')
        else:
            matchloss2 = matchloss2.head(n=1)

        X_test1 = pd.concat([matchdrawn, matchloss, matchwon])
        needed_data1 = X_test1[['team1_Outcome', 'team1_opponentid', 'team1_match_date', 'numerical_outcome']]
        print(f'team1 data : \n {needed_data1}')
        X_test1 = X_test1.drop(columns=['team1_match_date', 'team1_Outcome', 'team1id', 'team1_opponentid'])
        
        X_test2 = pd.concat([matchdrawn2, matchloss2, matchwon2])
        needed_data2 = X_test2[['team2_Outcome', 'team2_opponentid', 'team2_match_date', 'numerical_outcome']]
        print(f'team2 data : \n {needed_data2}')
        X_test2 = X_test2.drop(columns=['team2_match_date', 'team2_Outcome', 'team2id', 'team2_opponentid'])
        
        

        Y_pred1 = model1.predict(X=X_test1)
        Y_pred2 = model2.predict(X=X_test2)

        predicted_label1 = label_encoder1.inverse_transform(Y_pred1)
        predicted_label2 = label_encoder2.inverse_transform(Y_pred2)


        Team1_probability = model1.predict_proba(X=X_test1)
        Team2_probability = model2.predict_proba(X=X_test2)


        return Team1_probability, Team2_probability, predicted_label1, predicted_label2


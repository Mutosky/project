from supervised import predictionalgorithm, predictionalgorithm2, put_in_list, needData
from flask import request, jsonify, render_template, redirect
from init import flaskinit, teams, add_user, Users
import os

app = flaskinit()

@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        data = request.get_json()
        if data:
            if "team1" and "team2" in data:                
                team1id = int(teams[data['team1']])
                team2id = int(teams[data['team2']])

                probability, match_data = predictionalgorithm(
                    team1id=team1id,
                    team2id=team2id
                )

                outcome = []
                date = []
                team1 = []
                team2 = []

                for dat in match_data['match_outcome']:
                    outcome.append(dat)
                for dat in match_data['event_date']:
                    date.append(dat)
                for dat in match_date['team1_id']:
                    team1.append(dat)
                for dat in match_data['team2_id']:
                    team2.append(dat)

                Team1_probability, team1outcome, Team2_probability, team2outcome = predictionalgorithm2(
                    team1id=team1id,
                    team2id=team2id 
                )

                team1OpponentName, team1MatchDate, team1MatchOutcome, team2OpponentName, team2MatchDate, team2MatchOutcome = needData(
                    data=team1outcome,
                    data2=team2outcome
                )

                win1, loss1, draw1 = put_in_list(data=Team1_probability)
                win2, loss2, draw2 = put_in_list(data=Team2_probability)

                return jsonify({'H2H_data': {'last_match_probability': probability, 'outcome': outcome, 'date': date, 'team1': team1, 'team2': team2}, 
                                'Lastfivematchdata': {'HomeTeam': {'win': win1, 'loss': loss1, 'draw': draw1, 'opponent': team1OpponentName, 'Outcome': team1MatchOutcome, 'date': team1MatchDate}, 
                                                      'AwayTeam': {'win': win2, 'loss': loss2, 'draw': draw2, 'opponent': team2OpponentName, 'Outcome': team2MatchOutcome, 'date': team2MatchDate}}})
        else:
            return jsonify({'error': 'not data found'})
                
    return render_template('home.html')




@app.route('/payment', methods=['GET', 'POST'])
def payment():
    return render_template('payment.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userData = request.get_json()
        if userData:
            username = userData['name']
            password = userData['pass']
            print(f'{username} : {password} for signIn')
    return render_template('register.html')






@app.route('/signup', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        userData = request.get_json()
        if userData:
            username = userData['name']
            password = userData['pass']
            outCome = add_user(userData=Users(name=username, password=password))
            
    return render_template('register.html')





if __name__ == "__main__":
    app.run(debug=True)
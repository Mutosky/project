from supervised import predictionalgorithm, predictionalgorithm2, put_in_list, needData
from flask import request, jsonify, render_template, redirect
from init import flaskinit, teams, add_user, Users, login_users, Session
from datetime import date
import os

app = flaskinit()

def loop(data):
    itemList = []
    for dat in data:
        itemList.append(dat)
    return itemList


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

                

                outcome = loop(data=match_data['match_outcome'])
                date = loop(data=match_data['event_date'])
                team1 = loop(data=match_data['team1_id'])
                team2 = loop(data=match_data['team2_id'])

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



@app.route('/')
@app.route('/services')
def services():
    return render_template('services.html')





@app.route('/login', methods=['GET', 'POST'])
def login():
    error = 'Error this account is not active make payment in payment page or if payment has already been made wait for confirmation'
    if request.method == 'POST':
        userData = request.get_json()
        if userData:
            username = userData['name']
            password = userData['pass']
            code = login_users( username=username, password=password)
            if code == 'invalid':
                return jsonify({'error': 'user not found'})
            else:
                status = code.status
                if status == 'active':
                    return redirect('/home', code=304)
                else: return jsonify({'error': error})
    return render_template('register.html')




@app.route('/signup', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        userData = request.get_json()
        if userData:
            username = userData['name']
            password = userData['pass']
            status = 'deactivated'
            dates = date.today()
            code = add_user(username=username, password=password, status=status, dates=dates)
            if code == 'successful':
                return redirect('/payment', code=304)
            else:
                return jsonify({'error': 'internal error try again later'})
    return render_template('register.html')




@app.route('/get_users', methods=['GET', 'POST'])
def get_users():
    session = Session()
    users = session.query(Users).all()
    data = []
    for user in users:
        data.append({'name': user.name, 'status': user.status})
    session.close()
    return jsonify({'users': data})


@app.route('/updateUsers', methods=['GET', 'POST'])
def upadate():
    session = Session()
    if request.method == 'POST':
        data = request.get_json()
        print(data)





username = 'omotomiwa'
@app.route(f'/admin/{username}')
def admin():
    return render_template('admin.html')




@app.route('/payment', methods=['GET', 'POST'])
def payment():
    return render_template('payment.html')


if __name__ == "__main__":
    app.run(debug=True)
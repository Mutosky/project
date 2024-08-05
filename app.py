from init import app, teams, login_users, get_allusers, get_user, addGame, checkAvalibleGames, clearGames, finallyProbability
from flask import request, jsonify, render_template, redirect, url_for
from flask_login import login_required, login_user, logout_user, UserMixin, LoginManager
import requests
from datetime import date


login_manager = LoginManager()
login_manager.init_app(app=app)


class User(UserMixin):
    def __init__(self, id):
        self.id = id


@login_manager.user_loader
def load_user(user_id):
    user = User(user_id)
    return user


@app.route('/footballanalysis', methods=['GET'])
def footballanalysis():
    return render_template('footballanalysis.html')


@app.route('/regionalAnalysis', methods=['GET'])
def regionalAnalysis():
    return render_template('footballAnalysis2.html')


@app.route('/Analysis', methods=['GET'])
def Analysis():
    return jsonify({'redirect': url_for('teamAnalysis')})

@app.route('/teamAnalysis', methods=['GET'])
def teamAnalysis():
    return render_template('teamAnalysis.html')

@app.route('/head2head', methods=['GET', 'POST'])
def Head_to_Head():
    if request.method == 'POST':
        data = request.get_json()
        team1 = int(teams[data['team1']])
        team2 = int(teams[data['team2']])

        url = 'http://fpsapi.pythonanywhere.com/Head2Head'
        json = {'team1': team1, 'team2': team2}
        try:
            responds = requests.post(url=url, json=json, timeout=6)
            if responds.status_code == 200:
                return responds.json()
        except Exception as e:
            if e:
                return jsonify({'status': 500})


@app.route('/similaropponent', methods=['GET', 'POST'])
def similarOpponent():
    if request.method == 'POST':
        data = request.get_json()
        team1 = int(teams[data['team1']])
        team2 = int(teams[data['team2']])

        url = 'http://fpsapi.pythonanywhere.com/similaropponent'
        json = {'team1': team1, 'team2': team2}
        try:
            responds = requests.post(url=url, json=json, timeout=10)
            if responds.status_code == 200:
                data = responds.json()
                if 'status' in data:
                    return data['message']
                else: return data
        except Exception as e:
            if e:
                return jsonify({'status': 500})


@app.route('/pastFiveMatch', methods=['GET', 'POST'])
def pastFiveMatch():
    if request.method == 'POST':
        data = request.get_json()
        team = int(teams[data['team1']])

        url = 'http://fpsapi.pythonanywhere.com/pastfivematch'
        json = {'team1': team}
        try:
            responds = requests.post(url=url, json=json, timeout=10)
            if responds.status_code == 200:
                data =  responds.json()
                if 'status' in data:
                    return data['message']
                else:
                    return data
            else: print(responds.status_code)
        except Exception as e:
            if e:
                return jsonify({'status': 500})


@app.route('/homeAdvantages', methods=['GET', 'POST'])
def homeAdvantages():
    if request.method == 'POST':
        data = request.get_json()
        homeTeam = int(teams[data['team1']])

        url = 'http://fpsapi.pythonanywhere.com/homeadvantage'
        json = {'team1': homeTeam}
        try:
            responds = requests.post(url=url, json=json, timeout=10)
            if responds.status_code == 200:
                data = responds.json()
                if 'status' in data:
                    return data['message']
                else: return data
        except Exception as e:
            if e:
                return jsonify({'status': 500})
            

@app.route('/awayadvantage', methods = ['GET', 'POST'])
def awayAdvantages():
    if request.method == 'POST':
        data = request.get_json()
        awayTeam = int(teams[data['team2']])

        url = 'http://fpsapi.pythonanywhere.com/awayadvantage'
        json ={'team2': awayTeam}
        try:
            respond = requests.post(url=url, json=json, timeout=10)
            if respond.status_code == 200:
                data = respond.json()
                if 'status' in data:
                    return data['message']
                else: return data
        except Exception as e:
            if e:
             return jsonify({'status': 500})
            
@app.route('/teamfinalP', methods=['GET', 'POST'])
def teamProbability():
    if request.method == 'POST':
        data = request.get_json()
        Team1 = int(teams[data['team1']])
        Team2 = int(teams[data['team2']])

        try:
            team1FinalP, team2FinalP, eventOutcomeP = finallyProbability(team1=Team1, team2=Team2)
            return jsonify({'team1FP': team1FinalP, 'team2FP': team2FinalP, 'final_result': eventOutcomeP})
        except Exception as e:
            print(e)
             




@app.route('/')
@app.route('/home')
def home():
    return render_template('services.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userData = request.get_json()
        if userData:
            username = userData['name']
            print(username)
            password = userData['pass']
            code = login_users(username=username, password=password)
            if code == 'invalid':
                return jsonify({'error': 'user not found'})
            else:
                status = code.status
                if status == 'Admin':
                    user = User(username)
                    login_user(user=user)
                    return jsonify({'redirect': url_for('admins')})
                else:
                    return jsonify({'redirect': url_for('home'), 'alert': 'user is not active'})
    return render_template('register.html')




@app.route('/get_users', methods=['GET'])
@login_required
def get_users():
    users = get_allusers()
    data = []
    for user in users:
        data.append({'name': user.name, 'status': user.status})
    adminData = get_user(admin=True)
    adminName = adminData.name
    return jsonify({'users': data, 'admin': adminName})





@app.route('/admins', methods=['GET', 'POST'])
@login_required
def admins():
    return render_template('admin.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))






@app.route('/addGames', methods=['POST'])
@login_required
def control_games():
    if request.method == 'POST':
        data = request.get_json()

        team1 = data['team1']
        team2 = data['team2']
        try: 
            Poutcome = finallyProbability(team1=team1, team2=team2)
            status = addGame(homeTeam=team1, awayTeam=team2, date=date.today(), predictedOutcome=Poutcome)
        except Exception as e:
            print(e)
        

        if status == 'successful':
            return jsonify({'status': 'successfully added game'})
        elif status == 'already added':
            return jsonify({'status': 'Game as already been added'})
        else:
            print(status)
            return jsonify({'status': 'error adding games'})


@app.route('/getAllGames', methods=['GET'])
def getAllGames():
    data = checkAvalibleGames()
    match_data = []
    if data:
        for games in data:
            match_data.append({'homeTeam': games.HomeTeam, 'awayTeam': games.AwayTeam, 'predictedOutcome': games.PreGames, 'outcome': games.Outcome})
        print(match_data)
        return jsonify({'data': match_data})
    else: 
        return jsonify({'error': 'No Match Yet'})
    

    
@app.route('/deleteGame', methods=['GET'])
@login_required
def deleteGames():
    respond = clearGames()
    return jsonify({'alert': respond})



if __name__ == "__main__":
    app.run(debug=True)

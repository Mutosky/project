from init import app, teams, add_user, login_users, get_allusers, get_user, updateUser, authAdmin, addGame, checkAvalibleGames, clearGames
from flask import request, jsonify, render_template, redirect, url_for
from flask_login import login_required, login_user, logout_user, UserMixin, LoginManager, current_user
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
                    print(data)
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


'''@app.route('/signup', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        userData = request.get_json()
        if userData:
            username = userData['name']
            password = userData['pass']
            dates = date.today()
            code = add_user(username=username, password=password, dates=dates)
            if code == 'successful':
                user = User(username)
                print(user)
                login_user(user=user)
                return jsonify({'redirect': url_for('home')})
            else:
                return jsonify({'error': 'internal error try again later'})
    return render_template('register.html')'''


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


@app.route('/updateUsers', methods=['GET', 'POST'])
@login_required
def upadate():
    if request.method == 'POST':
        data = request.get_json()
        username = data['name']
        status = data['status']
        update = updateUser(username=username, status=status)
        if update == 'successful':
            return jsonify({'status': 'users status has been changed successfully'})
        else:
            return jsonify({'status': 'user not found'})


'''@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if request.method == 'POST':
        data = request.get_json()
        username = data['name']
        password = data['password']
        respond = authAdmin(name=username, password=password)
        if respond == 'successful':
            user = User(username)
            login_user(user=user)
            return jsonify({'redirect': url_for('admins')})
        elif respond == None:
            return 'error user not found', 404
    return render_template('adminLogin.html')'''


@app.route('/admins', methods=['GET', 'POST'])
@login_required
def admins():
    return render_template('admin.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/deleteUser', methods=['GET', 'DELETE'])
@login_required
def delete():
    if request.method == 'DELETE':
        username = request.get_json()['name']
        status = updateUser(username=username, delete=True)
        if status == 'successful':
            return jsonify({'status': 'user deleted successful'})
        elif status == 'unable to delete admin':
            return jsonify({'status': status})
        else:
            return jsonify({'status': 'not a user'})



@app.route('/addGames', methods=['POST'])
@login_required
def control_games():
    if request.method == 'POST':
        data = request.get_json()
        if 'odds' in data:
            team1 = data['team1']
            team2 = data['team2']
            odds= data['odds']
            numberOdds = data['numberOdds']
            status = addGame(HomeTeam=team1, AwayTeam=team2, InputOdds=numberOdds,  odds=odds, predictedOutcome='home or draw')
        else:
            team1 = data['team1']
            team2 = data['team2']
            numberOdds = data['numberOdds']
            status = addGame(HomeTeam=team1, AwayTeam=team2, InputOdds=numberOdds, predictedOutcome='')

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
    for games in data:
        match_data.append({'homeTeam': games.homeTeam, 'awayTeam': games.awayTeam,
                          'odds': games.odds, 'GameOdds': games.inputodds, 'predictedOutcome': games.oddscolume})
    print(match_data)
    return jsonify({'data': match_data})


@app.route('/deleteGame', methods=['GET'])
@login_required
def deleteGames():
    respond = clearGames()
    return jsonify({'alert': respond})


if __name__ == "__main__":
    app.run(debug=True)

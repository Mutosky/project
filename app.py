from init import app, teams, add_user, login_users, get_allusers, get_user, updateUser, authAdmin
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



def geetin(data):
    data1= []
    data2= []
    data3= []
    data4= []
    for dat in data['match_outcome']:
        data1.append(dat)
    for dat in data['team2_id']:
        data2.append(dat)
    for dat in data['event_date']:
        data3.append(dat)
    for dat in data['team1_place']:
        data4.append(dat)
    
    return data1, data2, data3, data4




@app.route('/footballanalysis', methods=['GET', 'POST'])
@login_required
def footballanalysis():
    if request.method == 'POST':
        data = request.get_json()
        if "team1" and "team2" in data:                
            team1id = int(teams[data['team1']])
            team2id = int(teams[data['team2']])
            json = {'team1': team1id, 'team2': team2id}
            json2 = {'team1': team2id}

            try: 
                url = 'http://fpsapi.pythonanywhere.com/pastfivematch'
                PFMdata = requests.post(url=url, json=json, timeout=10)
                if PFMdata.status_code == 200:
                    win1 = PFMdata.json()['win']
                    loss1 = PFMdata.json()['loss']
                    draw1 = PFMdata.json()['draw']
                    team1OpponentName = PFMdata.json()['opponent']
                    team1MatchOutcome = PFMdata.json()['outcome']
                    team1MatchDate = PFMdata.json()['date']
                else:
                    print(PFMdata.status_code)
            except TimeoutError as e:
                print(e)

            try:
                url2 = 'http://fpsapi.pythonanywhere.com/similaropponent'
                SMOdata = requests.post(url=url2, json=json, timeout=10)
                if SMOdata.status_code == 200:
                    print(SMOdata.json())

                    win3 = SMOdata.json()['team1']['win']
                    loss3 = SMOdata.json()['team1']['loss']
                    draw3 = SMOdata.json()['team1']['draw']
                    win4 = SMOdata.json()['team2']['win']
                    loss4 = SMOdata.json()['team2']['loss']
                    draw4 = SMOdata.json()['team2']['draw']
                    datalist = SMOdata.json()['opponent']['data']
                else:
                    print(SMOdata.status_code)
            except TimeoutError as e:
                print(e)
            
            try:
                url3 = 'http://fpsapi.pythonanywhere.com/homeadvantage'
                HAGdata = requests.post(url=url3, json=json, timeout=10)
                if HAGdata.status_code == 200:
                    print(HAGdata.json())

                    homeWin = HAGdata.json()['win']
                    homeLoss = HAGdata.json()['loss']
                    homeDraw = HAGdata.json()['draw']
                    eventDate = HAGdata.json()['date']
                    homeOutcome = HAGdata.json()['outcome']
                    opponent = HAGdata.json()['opponent']
                else:
                    print(HAGdata.status_code)
            except TimeoutError as e:
                print(e)
            
            try:
                url = 'http://fpsapi.pythonanywhere.com/pastfivematch'
                PFM2data = requests.post(url=url, json=json2, timeout=10)
                if PFM2data.status_code == 200:
                    print(PFM2data.json())

                    win2 = PFM2data.json()['win']
                    loss2 = PFM2data.json()['loss']
                    draw2 = PFM2data.json()['draw']
                    team2OpponentName = PFM2data.json()['opponent']
                    team2MatchOutcome = PFM2data.json()['outcome']
                    team2MatchDate = PFM2data.json()['date']
                else:
                    print(PFMdata.status_code)
            except TimeoutError as e:
                print(e)

            try:
                url = 'http://fpsapi.pythonanywhere.com/Head2Head'
                H2Hdata = requests.post(url=url, json=json, timeout=10)
                if H2Hdata.status_code == 200:
                    print(H2Hdata.json())

                    probability = H2Hdata.json()['datalist']
                    outcome = H2Hdata.json()['match_outcome']
                    dates = H2Hdata.json()['event_date']
                    team1 = H2Hdata.json()['team1_id']
                    team2 = H2Hdata.json()['team2_id']
                else:
                    print(H2Hdata.status_code)
            except Exception as e:
                if e:
                    print('error')
                    probability = 'None'
                    outcome = 'None'
                    dates = 'None'
                    team1 = 'None'
                    team2 = 'None'
                

                

                


            return jsonify({'H2H_data': {'last_match_probability': probability, 'outcome': outcome, 'date': dates, 'team1': team1, 'team2': team2},
                            'Lastfivematchdata': {'HomeTeam': {'win': win1, 'loss': loss1, 'draw': draw1, 'opponent': team1OpponentName, 'Outcome': team1MatchOutcome, 'date': team1MatchDate},
                                                'AwayTeam': {'win': win2, 'loss': loss2, 'draw': draw2, 'opponent': team2OpponentName, 'Outcome': team2MatchOutcome, 'date': team2MatchDate}},
                            'homeAdvange': {'win': homeWin, 'loss': homeLoss, 'draw': homeDraw, 'date': eventDate, 'match_outcome': homeOutcome, 'opponent': opponent},
                            'similarOpponent': {'teamOne': {'win': win3, 'loss': loss3, 'draw': draw3},
                                                'teamTwo': {'win': win4, 'loss': loss4, 'draw': draw4},
                                                'opponents': {'data': datalist}}
                            })
        else:
            return jsonify({'error': 'not data found'})
    return render_template('footballanalysis.html')







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
            password = userData['pass']
            code = login_users( username=username, password=password)
            if code == 'invalid':
                return jsonify({'error': 'user not found'})
            else:
                status = code.status
                if status == 'active':
                    user = User(username)
                    print(user)
                    login_user(user=user)
                    return jsonify({'redirect': url_for('home')})
                elif status == 'Admin': return jsonify({'redirect': url_for('admin')})
                else: return jsonify({'redirect': url_for('payment')})
    return render_template('register.html')




@app.route('/signup', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        userData = request.get_json()
        if userData:
            username = userData['name']
            password = userData['pass']
            dates = date.today()
            code = add_user(username=username, password=password, dates=dates)
            if code == 'successful':
                user= User(username)
                login_user(user=user)
                return jsonify({'redirect': url_for('home')})
            else:
                return jsonify({'error': 'internal error try again later'})
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
        else: return jsonify({'status': 'user not found'})
    



@app.route('/admin', methods=['GET', 'POST'])
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
    return render_template('adminLogin.html')


@app.route('/admins', methods=['GET', 'POST'])
@login_required
def admins():
    return render_template('admin.html')


@app.route('/logout')
@login_required
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


@app.route('/payment', methods=['GET', 'POST'])
@login_required
def payment():
    return render_template('payment.html')




if __name__ == "__main__":
    app.run(debug=True)
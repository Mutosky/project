from init import flaskinit, teams, add_user, login_users, get_allusers, get_user, updateUser, authAdmin
from flask import request, jsonify, render_template, redirect, url_for
from flask_login import login_required, login_user, logout_user, UserMixin, LoginManager
import requests
from datetime import date

app = flaskinit()

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
    urlPastFiveMatch = 'http://fpsapi.pythonanywhere.com/pastfivematch'
    urlHead2Head = 'http://fpsapi.pythonanywhere.com/Head2Head'
    urlSimilarOpponent = 'http://fpsapi.pythonanywhere.com/similaropponent'
    urlHomeAdvantages = 'http://fpsapi.pythonanywhere.com/homeadvantage'
    if request.method == 'POST':
        data = request.get_json()
        if "team1" and "team2" in data:                
            team1id = int(teams[data['team1']])
            team2id = int(teams[data['team2']])
            json = {'team1': team1id, 'team2': team2id}

            H2Hdata = requests.post(url=urlHead2Head, json=json, timeout=30)
            PFMdata = requests.post(url=urlPastFiveMatch, json=json, timeout=30)
            PFM2data = requests.post(url=urlPastFiveMatch, json=json, timeout=30)
            SMOdata = requests.post(url=urlSimilarOpponent, json=json, timeout=30 )
            HAGdata = requests.post(url=urlHomeAdvantages, json=json, timeout=30)

            probability = H2Hdata.json()['datalist']
            outcome = H2Hdata.json()['match_outcome']
            dates = H2Hdata.json()['event_date']
            team1 = H2Hdata.json()['team1_id']
            team2 = H2Hdata.json()['team2_id']

            win1 = PFMdata.json()['win']
            loss1 = PFMdata.json()['loss']
            draw1 = PFMdata.json()['draw']
            team1OpponentName = PFMdata.json()['opponent']
            team1MatchOutcome = PFMdata.json()['outcome']
            team1MatchDate = PFMdata.json()['date']
            win2 = PFM2data.json()['win']
            loss2 = PFM2data.json()['loss']
            draw2 = PFM2data.json()['draw']
            team2OpponentName = PFM2data.json()['opponent']
            team2MatchOutcome = PFM2data.json()['outcome']
            team2MatchDate = PFM2data.json()['date']

            win3 = SMOdata.json()['team1']['win']
            loss3 = SMOdata.json()['team1']['loss']
            draw3 = SMOdata.json()['team1']['draw']
            win4 = SMOdata.json()['team2']['win']
            loss4 = SMOdata.json()['team2']['loss']
            draw4 = SMOdata.json()['team2']['draw']
            similarTeams = SMOdata.json()['opponent']['name']
            datalist = SMOdata.json()['opponent']['date']

            homeWin = HAGdata.json()['win']
            homeLoss = HAGdata.json()['loss']
            homeDraw = HAGdata.json()['draw']
            eventDate = HAGdata.json()['date']
            homeOutcome = HAGdata.json()['outcome']
            opponent = HAGdata.json()['date']


            return jsonify({'H2H_data': {'last_match_probability': probability, 'outcome': outcome, 'date': dates, 'team1': team1, 'team2': team2},
                            'Lastfivematchdata': {'HomeTeam': {'win': win1, 'loss': loss1, 'draw': draw1, 'opponent': team1OpponentName, 'Outcome': team1MatchOutcome, 'date': team1MatchDate},
                                                  'AwayTeam': {'win': win2, 'loss': loss2, 'draw': draw2, 'opponent': team2OpponentName, 'Outcome': team2MatchOutcome, 'date': team2MatchDate}},
                            'homeAdvange': {'win': homeWin, 'loss': homeLoss, 'draw': homeDraw, 'date': eventDate, 'match_outcome': homeOutcome, 'opponent': opponent},
                            'similarOpponent': {'teamOne': {'win': win3, 'loss': loss3, 'draw': draw3},
                                                'teamTwo': {'win': win4, 'loss': loss4, 'draw': draw4},
                                                'opponents': {'name': similarTeams, 'data': datalist}}
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
                    return redirect(url_for('home'))
                elif status == 'Admin': return redirect(url_for('admin'))
                else: return redirect(url_for('payment'))
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
                return redirect(url_for('payment'))
            else:
                return jsonify({'error': 'internal error try again later'})
    return render_template('register.html')



@app.route('/get_users', methods=['GET'])
def get_users():
    users = get_allusers()
    data = []
    for user in users:
        data.append({'name': user.name, 'status': user.status})
    adminData = get_user(admin=True)
    adminName = adminData.name
    return jsonify({'users': data, 'admin': adminName})


@app.route('/updateUsers', methods=['GET', 'POST'])
def upadate():
    if request.method == 'POST':
        data = request.get_json()
        username = data['name']
        status = data['status']
        update = updateUser(username=username, status=status)
        if update == 'succesful':
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
            return render_template('admin.html')
        elif respond == None:
            return 'error user not found', 404
    return render_template('adminLogin.html')


@app.route('/admins', methods=['GET', 'POST'])
def admins():
    return render_template('admin.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/payment', methods=['GET', 'POST'])
def payment():
    return render_template('payment.html')




if __name__ == "__main__":
    app.run(debug=True)
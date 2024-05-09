from init import flaskinit, teams, add_user, login_users, get_allusers, get_user, updateUser
from supervised import pastfivematch, Head2Head, put_in_list, needData, loop, homeAdvantage
from flask import request, jsonify, render_template, redirect, url_for
from flask_login import login_required, login_user, logout_user, UserMixin,LoginManager
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
    if request.method == 'POST':
        data = request.get_json()
        if data:
            if "team1" and "team2" in data:                
                team1id = int(teams[data['team1']])
                team2id = int(teams[data['team2']])

                probability, match_data = Head2Head(
                    teamid=team1id,
                    team2id=team2id
                )
                Team1_probability, team1outcome = pastfivematch(
                    teamid=team1id
                )
                Team2_probability, team2outcome = pastfivematch(
                    teamid=team2id
                )
                homeProbability, neededData = homeAdvantage(
                    teamid=team1id
                )
                team1OpponentName, team1MatchDate, team1MatchOutcome, team2OpponentName, team2MatchDate, team2MatchOutcome = needData(
                    data=team1outcome,
                    data2=team2outcome
                )

                homeOutcome, _, eventDate, _ = geetin(data=neededData)

                outcome = loop(data=match_data['match_outcome'])
                date = loop(data=match_data['event_date'])
                team1 = loop(data=match_data['team1_id'])
                team2 = loop(data=match_data['team2_id'])
                
                win1, loss1, draw1 = put_in_list(data=Team1_probability)
                win2, loss2, draw2 = put_in_list(data=Team2_probability)
                homeWin, homeLoss, homeDraw = put_in_list(data=homeProbability)

                return jsonify({'H2H_data': {'last_match_probability': probability, 'outcome': outcome, 'date': date, 'team1': team1, 'team2': team2}, 
                                'Lastfivematchdata': {'HomeTeam': {'win': win1, 'loss': loss1, 'draw': draw1, 'opponent': team1OpponentName, 'Outcome': team1MatchOutcome, 'date': team1MatchDate}, 
                                                    'AwayTeam': {'win': win2, 'loss': loss2, 'draw': draw2, 'opponent': team2OpponentName, 'Outcome': team2MatchOutcome, 'date': team2MatchDate}},
                                'homeAdvange': {'win': homeWin, 'loss': homeLoss, 'draw': homeDraw, 'date': eventDate, 'match_outcome': homeOutcome},
                                'similarOpponent': {}
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
                    user = User(username)
                    login_user(user=user)
                    return redirect(url_for('home'))
                elif status == 'Admin': return redirect('/admin')
                else: return jsonify({'error': error})
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
    




@app.route('/admin', methods = ['GET'])
def admin():
    return render_template('admin.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/payment', methods=['GET', 'POST'])
def payment():
    return render_template('payment.html')


@app.route('/throbber', methods=['GET', 'POST'])
def example():
    return render_template('example.html')


if __name__ == "__main__":
    app.run(debug=True)
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





@app.route('/footballanalysis', methods=['GET'])
@login_required
def footballanalysis():
    return render_template('footballanalysis.html')



@app.route('/head2head', methods=['GET','POST'])
@login_required
def Head_to_Head():
    if request.method == 'POST':
        data = request.get_json()
        team1 = int(teams[data['team1']])
        team2 = int(teams[data['team2']])

        url = 'http://fpsapi.pythonanywhere.com/Head2Head'
        json = {'team1': team1, 'team2': team2}
        try:
            responds = requests.post(url=url, json=json, timeout=10)
            if responds.status_code == 200:
                return responds.json()
        except Exception as e:
            if e:
                return jsonify({'status': 500})





@app.route('/similaropponent', methods=['GET', 'POST'])
@login_required
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
                return responds.json()
        except Exception as e:
            if e:
                return jsonify({'status': 500})


@app.route('/pastFiveMatch', methods=['GET', 'POST'])
@login_required
def pastFiveMatch():
    if request.method == 'POST':
        data = request.get_json()
        team = int(teams[data['team1']])

        url = 'http://fpsapi.pythonanywhere.com/pastfivematch'
        json = {'team1': team}
        try:
            responds = requests.post(url=url, json=json, timeout=10)
            if responds.status_code == 200:
                return responds.json()
        except Exception as e:
            if e:
                return jsonify({'status': 500})


@app.route('/homeAdvantages', methods=['GET', 'POST'])
@login_required
def homeAdvantages():
    if request.method == 'POST':
        data = request.get_json()
        homeTeam = int(teams[data['team1']])

        url = 'http://fpsapi.pythonanywhere.com/homeadvantage'
        json = {'team1': homeTeam}
        try:
            responds = requests.post(url=url, json=json, timeout=10)
            if responds.status_code == 200:
                return responds.json()
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
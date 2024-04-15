from supervised import predictionalgorithm, predictionalgorithm2
from flask import request, jsonify, render_template
from init import flaskinit, teams
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

                probability, event_date = predictionalgorithm(
                    team1id=team1id,
                    team2id=team2id
                )


                return jsonify({'H2H_data':{'last_match_probability': probability, '': event_date}, 
                                'Last_five_match_data':{}})
        else:
            return jsonify({'error': 'not data found'})
                
    return render_template('home.html')



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
            username = userData['email']
            password = userData['password']
            print(f'{username} : {password} for signUp')
    return render_template('register.html')


@app.route('/payment', methods=['GET', 'POST'])
def payment():
    return render_template('payment.html')




if __name__ == "__main__":
    app.run(debug=True)




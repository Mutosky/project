from sqlalchemy import create_engine, Column, Float, String, Integer, Date, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask import jsonify
import requests
from datetime import date

import os
from dotenv import load_dotenv
from flask import Flask

load_dotenv()


teams = {"Udinese": " 4984", "FC Porto": "81", "Inter Milan": "79", "Newcastle United": "3100",
         "Sheffield United": "3074", "Lens": "3821", "AFC Bournemouth": "3071", "Tottenham Hotspur": "164", "Everton": "3073", "Monaco": "3817",
         "MLS All-Stars": "23795", "Nürnberg": "3924", "Southampton": "3072", "Leeds United": "3103", "Leicester City": "155", "Aston Villa": "3088",
         "Oxford United": "3113", "Lyon": "3815", "Zürich": "7410", "Bodø / Glimt": "215", "Orlando City": "7959", "Ipswich": "3121",
         "West Ham United": "3081", "Empoli": "4979", "Nottingham Forest": "3089", "Brighton & Hove Albion": "3079", "PSV": "150", "Luton Town": "3091",
         "Wolverhampton Wanderers": "3077", "Lens": "3821", "Brentford": "3086", "Crystal Palace": "3429", "Burnley": "3075", "Fulham": "3085", "Lecce": "5010",
         "Sassuolo": "4975", "Frosinone": "5000", "Salernitana": "5012", "Roma": "139", "Genoa": "4986", "Napoli": "152", "Monza": "4990", "Cagliari": "4981",
         "Fiorentina": "4974", "Verona": "4982", "AC Milan": "159", "Torino": "4973", "Atalanta": "85", "Lazio": "93", "Bologna": "4983", "Real Madrid": "76",
         "Barcelona": "97", "Sevilla": "89", "Cremonese": "4998", "Sporting Lisbon": "177", "Freiburg": "3962", "Sampdoria": "4985", "Spezia": "4977", "Nantes": "3820",
         "Standard Liège": "148", "Rijeka": "154", "Arsenal": "141", "Benfica": "147", "Maccabi Haifa": "185", "PSG": "100", "Atletico Madrid": "73", "Guadalajara": "5355",
         "Venezia": "5007", "Villareal": "162", "Manchester City": "80", "Chelsea": "88", "RB Leipzig": "101", "Girona": "7263", "Getafe": "7288", "Las Palmas": "7289",
         "Almeria": "7260", "Arandina": "7105", "Mallorca": "7285", "Alaves": "7275", "Union Berlin": "3936", "Real Betis": "7261", "Granada": "151", "Cadiz": "7277",
         "Sporting Braga": "156", "Valencia": "7272", "Rayo Vallecano": "7264", "Osasuna": "7269", "Real Sociedad": "153", "Celta Vigo": "7290", "Athletic Bilbao": "7258",
         "Juventus": "96", "Manchester United": "102", "Real Valladolid": "7262", "Liverpool": "84", "Espanyol": "7268", "Elche": "7274", "Al Hilal": "366", "Al Ahly": "585",
         "Cacereño": "6805", "Celtic": "127", "Shakhtar Donetsk": "78", "Eintracht Frankfurt": "3945", "América": "284", "Levante": "7259", "Alcoyano": "7249",
         "Bayern Munich": "72", "Italy": "3", "England": "16", "Denmark": "7", "Spain": "19", "Czech Republic": "13", "Ukraine": "12", "Belgium": "6", "Switzerland": "2", 
         "Germany": "21", "Sweden": "17", "Ukraine": "12", "Croatia": "14", "France": "22", "Netherlands": "10", "Portugal": "23", "Wales": "4", "Austria": "9", "Poland": "18",
        "Slovakia": "20", "Hungary": "24", "Scotland": "15", "North Macedonia": "11", "Russia": "5", "Finland": "8", "Turkey": "1"}

dbPassword = os.getenv('PASSWORD')
secretKey = os.getenv('SECRET_KEY')

app = Flask(__name__)
app.config['SECRET_KEY'] = secretKey


engine = create_engine(f'postgresql://default:{dbPassword}@ep-wispy-waterfall-a4h1vshm.us-east-1.aws.neon.tech:5432/verceldb?sslmode=require')

Session = sessionmaker(autoflush=False, bind=engine)
Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    password = Column(String)
    status = Column(String, nullable=True)
    dates = Column(Date)


class Games(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True)
    HomeTeam = Column(String, nullable=False)
    AwayTeam = Column(String, nullable=False)
    PreGames = Column(String, nullable=True)
    Outcome = Column(String, nullable=True)
    Dates = Column(Date, nullable=False) 
    



Base.metadata.create_all(engine)


def checkAvalibleGames():
    session = Session()
    try:
        allGames = session.query(Games).all()
        return allGames
    except Exception as e:
        return e
    finally:
        session.close()
    

def clearGames():
    session = Session()
    try:
        all_games = session.query(Games).all()
        if all_games:
            for game in all_games:
                homeTeam = game.HomeTeam
                awayTeam = game.AwayTeam
                game_to_delete = session.query(Games).filter_by(HomeTeam=homeTeam, AwayTeam=awayTeam).first()
                if game_to_delete:
                    session.delete(game_to_delete)
                    session.commit()
            return 'game deleted successfully'
        else: return 'no games to delete'
    except Exception as e:
        return e
    finally:
        session.close()



        
def addGame(homeTeam, awayTeam, predictedOutcome, date, outcome='ongoing'):
    session = Session()
    try:
        game = session.query(Games).filter_by(HomeTeam=homeTeam, AwayTeam=awayTeam).first()
        if game:
            return 'already added'
        else:
            session.add(Games(HomeTeam=homeTeam, AwayTeam=awayTeam, PreGames=predictedOutcome, Outcome=outcome, Dates=date))
            session.commit()
            return 'successful'   
    except Exception as e:
        return e
    finally:
        session.close()





def add_user(username, password, dates, status='deactivated'):
    if username and password:
        try:
            session = Session()
            session.add(Users(name=username, password=password, status=status, dates=dates))
            session.commit()
            return 'successful'
        except Exception as e:
            session.rollback()
            return f'error {e}'
        finally:
            session.close()
    else: return 'no data found'


def get_user(username='unknown', admin=False):
    session = Session()
    try:
        if admin == True:
            status='Admin'
            userData = session.query(Users).filter_by(status=status).first()
        else:
            userData = session.query(Users).filter_by(name=username).first()
        return userData
    except Exception as e:
        return e
    finally: session.close()
    

def get_allusers():
    session = Session()
    try:
        alldata = session.query(Users).all()
        return alldata
    except Exception as e:
        return e
    finally: session.close()
    

def updateUser(username, status='', delete=False):
    session = Session()
    if delete == True:
        user_to_delete = session.query(Users).filter_by(name=username).first()
        if user_to_delete:
            if user_to_delete.status == 'Admin':
                return 'unable to delete admin'
            else:
                session.delete(user_to_delete)
                session.commit()
                return 'successful'
        else:
            return 'user not found'
    elif delete == False:
        newStatus = 'active' if status == 'deactivated' else 'deactivated'
        try: 
            userData = session.query(Users).filter_by(name=username).first()
            if userData:
                userData.status = newStatus
                session.commit()
                return 'successful'
        except Exception as e:
            return e
    session.close()



def login_users(username, password):
    if username and password:
        try: 
            session = Session()
            user = session.query(Users).filter_by(name=username, password=password).first()
            if user:
                return user
            else: return 'invalid'
        except Exception as e:
            return f'error {e}'
        finally: session.close()

def authAdmin(name, password):
    if name and password:
        try:
            session = Session()
            user = session.query(Users).filter_by(name=name, password=password).first()
            print(user.name, user.status)
            if user:
                if user.status == 'Admin':
                    return 'successful'
            else: return None
        except Exception as e:
            print(f'error in try{e}')
            return f'error {e}'
        finally: session.close()


def similarOpponent(team1, team2):
    url = 'http://fpsapi.pythonanywhere.com/similaropponent'
    json = {'team1': team1, 'team2': team2}
    try:
        responds = requests.post(url=url, json=json, timeout=10)
        if responds.status_code == 200:
            data = responds.json()
            if 'status' in data:
                return data['message']
            else:
                return data
    except Exception as e:
        if e:
            return jsonify({'status': 500})


def pastFiveMatch(team):
    url = 'http://fpsapi.pythonanywhere.com/pastfivematch'
    json = {'team1': team}
    try:
        responds = requests.post(url=url, json=json, timeout=10)
        if responds.status_code == 200:
            data = responds.json()
            if 'status' in data:
                return data['message']
            else:
                return data
        else:
            print(responds.status_code)
    except Exception as e:
        if e:
            return jsonify({'status': 500})


def homeAdvantages(team1):
    url = 'http://fpsapi.pythonanywhere.com/homeadvantage'
    json = {'team1': team1}
    try:
        responds = requests.post(url=url, json=json, timeout=10)
        if responds.status_code == 200:
            data = responds.json()
            if 'status' in data:
                return data['message']
            else:
                return data
    except Exception as e:
        if e:
            return jsonify({'status': 500})


def awayAdvantages(team2):
    url = 'http://fpsapi.pythonanywhere.com/awayadvantage'
    json = {'team2': team2}
    try:
        respond = requests.post(url=url, json=json, timeout=10)
        if respond.status_code == 200:
            data = respond.json()
            if 'status' in data:
                return data['message']
            else:
                return data
    except Exception as e:
        if e:
            return jsonify({'status': 500})


def finallyProbability(team1, team2):
    SOD = similarOpponent(team1=team1, team2=team2)
    PFMDTeam1 = pastFiveMatch(team=team1)
    HAD = homeAdvantages(team1=team1)
    PFMDTeam2 = pastFiveMatch(team=team2)
    AAD = awayAdvantages(team2=team2)
    weight = {
        "similaropponent": 1.00,
        "advantages": 1.00,
        "pastfivematch": 1.00
    }
    team1Data = {
        "similaropponent": SOD['team1'],
        "advantages": HAD,
        "pastfivematch": PFMDTeam1
    }
    team2Data = {
        "similaropponent": SOD['team2'],
        "advantages": AAD,
        "pastfivematch": PFMDTeam2
    }
    team1FinalP = calculatefinallyprobability(
        probability=team1Data, weights=weight)

    team2FinalP = calculatefinallyprobability(
        probability=team2Data, weights=weight)
    
    eventOutcomeP = eventProbability(team1FP=team1FinalP, team2FP=team2FinalP)

    return team1FinalP, team2FinalP, eventOutcomeP


def calculatefinallyprobability(probability, weights):
    final_probs = {'win': 0.0, 'draw': 0.0, 'loss': 0.0}

    for name, weight in weights.items():
        for match_probs in probability[name]['win']:
            final_probs['win'] = final_probs['win']+weight*match_probs
        for match_probs in probability[name]['draw']:
            final_probs['draw'] = final_probs['draw']+weight*match_probs
        for match_probs in probability[name]['loss']:
            final_probs['loss'] = final_probs['loss']+weight*match_probs

    total = final_probs['win']+final_probs['loss']+final_probs['draw']

    ScalingFactor = 100/total

    win = final_probs['win']*ScalingFactor
    loss = final_probs['loss']*ScalingFactor
    draw = final_probs['draw']*ScalingFactor

    final_probs['win'] = win/100
    final_probs['loss'] = loss/100
    final_probs['draw'] = draw/100

    return final_probs


def eventProbability(team1FP, team2FP):
    eventprob = {'homeTeam': 0.0, 'draw': 0.0, 'awayTeam': 0.0}

    team1win = team1FP['win']
    team2win = team2FP['win']

    draw = team1FP['draw']+team2FP['draw']

    Sum = team1win+team2win+draw
    scalingFactor = 100/Sum

    team1win = team1win*scalingFactor
    team2win = team2win*scalingFactor
    draw = draw*scalingFactor

    eventprob['homeTeam'] = team1win/100
    eventprob['awayTeam'] = team2win/100
    eventprob['draw'] = draw/100

    return eventprob

from sqlalchemy import create_engine, Column, Float, String, Integer, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
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
         "Bayern Munich": "72"}

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

Base.metadata.create_all(engine)


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
                
    
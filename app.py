from googletrans import Translator
import time
from firebase_admin import credentials, firestore, initialize_app
import json
from flask import Flask, request,session #import main Flask class and request object
import requests
import pandas as pd
app = Flask(__name__) #create the Flask app
app.secret_key = "Revhack"
texts = {}
# import matplotlib.pyplot as plt
# import seaborn as sns

from nltk.stem import PorterStemmer
ps =PorterStemmer()


config = {
  "type": "service_account",
  "project_id": "user-app-6afb2",
  "private_key_id": "ce9b7b227d17668447acd43a93985a4c170815be",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCnkzdFVKzjvW1d\nQD1MSWOMmZI5QohUqjfj5uNwaLo07TRUmwGLxpMpYL+fggCgzHUuAs/hv/s3G6SI\nMh+cEQ9ch2BIPVtEeFtHQKRU0aLby3El6MSXgNths71f4iblBFgIefKWzi2n0xRd\nOP/sjsL/5EqcdKxPvESbkn2ppPa13mZ2ii1zKgB2kqvaNGgzNMdEGZ9OIUa2xmss\nSMQQNVj7O70r6ozrkyBJiaPne6FHiZjvR/31avjFk7QIwWdsaTijRAcUnTi2Z08o\nesh+X+tduTqgbatuW75HWYDNf3E9nX6vG5XP3beUhNQMEUkjqV2h5cW/HwZ3KNBT\noD81+xUpAgMBAAECggEAAmaBWBE7chrPiz0xxyWjwU5k90RYYZffDxV1RiO4IOW8\ngrhps8/efjta41iZRl8OgcOqGm/bBbWeqLxXEnboGKXFkWp0B3S5dY7UtnSMhh1D\nX1QzQSqLstZ5STQ3j/gLLshYaV1GC7SbH0st11H5Fxwt8lDnUFAx+SyGlBHbpYVC\n2oXDxNt6zGsZguaGaNXgqcfiQDCwpaulzoWWq5SvENMaPIER497ttPY2EERQOcyZ\nJKnTuj1ddL8VUcNhKpm2Gmq6XBTYYFsZWPqqtirQAWfWCLJpp6dgGCoxp9b/WECV\ng5gwubhH7QI9gQi4GDjTchXWzrpaD6wm/k1jJ3NKpQKBgQDmdc57vjkVfRM8AKhW\nnMuV/38J4ircxDHKQYtNxYyC3CaHLTDeengwjaaQQVzYSj5VNqwhlfbbbqoXLWsR\nh0ZjzU6qDj7aexyKuSP6T9FtZHKcvK4vP53FV4ajo11LkFEBvdNEwe2ymFgVVZgL\nuzoGFy+q7cAUfleOLULK+HoYcwKBgQC6JVkcdsJpQpuasXN4z3JzBSD7wMlu6MYo\nw4QFxh/EaLmo4GcozqDiXxonfGLTFChQjq64wLhHyfbGaKzj0rePsBHQm89pYzfh\neIQQ8kyx9/xiawEMTISnZ7sY92pzsMW4IRWwnPL+mpC26WBb90IDg/ABg8LHXUMv\nPYA8DHqg8wKBgFgvwEGNut5ELDYLsl7iRO0zBXPMvcYYtUzF4/5wl6IDiCK14jtf\n9dnuekw9FsAVOOD2uMtpTTsOj7uqv4vHjeHm0DE2nkqQTY2v5tqD7InFpC3h7W1b\nFI5NPdIkUzD1GmpmLw/ifYiXzyzqwfHLRRrLiIwJyjSNXAelvidZCa+NAoGAQ/xg\nD4VQfCFXs6gcBIO/yUKWSVygNWHO/hRqo7E46QNWy9cp1j2hhQw3ATTs4yr5jnKO\nXewFYjLhbpXMj2jmohQsbYR6vIMAZdkeYxIb8OQhydBLEbLgwEOikfvLZXWqwRVU\nVqz8EwFg2W1jRDOKaL5HakY1XZsybo6Hx2bHYwECgYEAsnSFFwl4ZJ2RH2KX/ZjX\n7i29HJ8MM/nbPVzUxvvZ2VtSy3EghEvQDsoeeDu09+bD0/0Ub0x+4Vbzdh1qRw7z\nqcxi9IK5ql2Q8YczCiuYLfpIETYucL7YlLWjGzWPsMBUGRaPR04zQfzqvKJ7BzfD\nj0HuDQaYmZ01G57bwDMjkZ0=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-iy8dz@user-app-6afb2.iam.gserviceaccount.com",
  "client_id": "113514663679555066158",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-iy8dz%40user-app-6afb2.iam.gserviceaccount.com"
}

cred = credentials.Certificate(config)
default_app = initialize_app(cred)
db = firestore.client()
tOrders = db.collection('TransOrders')
SDetails = db.collection('SaleDetails')
@app.route('/')
def hello_world(): 
    return '<h1>Welcome to Rev Hack</h1>'

@app.route('/query-example')

def query_example():
   
    def translatekaro(stringd,lang):
        api_url = 'https://hackapi.reverieinc.com/nmt'
        create_row_data = {'data':[stringd],
        'tgt':lang,
        'src':'en'}
        print("hi"+str(create_row_data))
        r = requests.post(url=api_url,headers={'Content-Type':'application/json','token' : '35352f14ab2403b1b1ca50bb0a65d9930a9a98ba'}, json=create_row_data)
        listemp = json.loads(r.text)['data']['result'][0][0]
        print(listemp)
        return listemp 
        

    docs = db.collection(u'Orders').get()
    session.clear()
    list1 = []
    list2 = []
    list3 = []
    for doc in docs:
        # print(u'{} => {}'.format(doc.id, doc.to_dict()))
        
        texts = doc.to_dict()['userOrder']
        
        
        
        print("1"+str(texts))
        
        dummy = {}
        dummyvalue = 0
        
       
        for key,value in texts.items():
            
            if "kg" in value.lower():
                dummyvalue = float(value.split()[0])
            if "gram" in value.lower():
                dummyvalue = round(float(value.split()[0])/1000,2)
                texts[key] = value
            elif "pound" in value.lower():
                dummyvalue = round(float(value.split()[0])/2.205,2)
                texts[key] = value
            
            key= ps.stem(key.lower())
                
             
            dummy[key] = dummyvalue
            
        texts = dummy
        print(texts)
        database = {'sugar':30,'rice':20,'kurkure':5,'tomato':39,'onion':100,'wheat':40,'potato':15,'appl':110,'banana':40,'mango':90,'orange':40,'orang':40,'bananas':40}
        remaining = {'sugar':10,'rice':8,'kurkure':10,'tomato':7,'onion':9,'wheat':13,'potato':10,'appl':10,'banana':7,'mango':5,'orange':8,'orang':6,'bananas':8}
        
        try:
            for key,value in texts.items():
            
                list1.append(texts[key])
                list2.append(database[key])
                list3.append(key)
        
        except KeyError:
            print("not in list")

        
        
        for key,value in texts.items():
            if key in session:
                session[key] = int(session[key])+int(texts[key])
            else:
                session[key] = int(texts[key])
       
        
        translator = Translator()
        translated = {}
        userPrice = {}
        
       
        
        try: 
            for key, value in texts.items():

                translated[translatekaro(stringd=key,lang="hi")]=value
                time.sleep(1.5)
                remaining[key] = remaining[key]- texts[key]
                time.sleep(1.5)
                userPrice[translatekaro(stringd=key,lang="hi")] = database[key]
        except KeyError:
            print("not found")
        # for key, value in  texts.items():
        #     texts[translator.translate(key, dest='en').text]=value
        
        print("last"+str(texts))
            
        cost = 0
        try:

            for key,value in texts.items():
                cost = cost + int(texts[key])*database[key]

        except KeyError:
            print("not found")
        
        data = {'cost':cost,'userOrder':translated,'userPrice':userPrice}
        
        tOrders.document(doc.id).set(data)
        print()
        print()
    
    data = {'item':list3,'count': list1, 'cost': list2}
    df = pd.DataFrame.from_dict(data)
    df.to_csv('file1.csv',index=True,index_label='Time')
   
    
    total = {}
    for key in session:
        total[key] = session[key]
    stocks = {'banana': '20-01-2020', 'appl': '21-01-2020', 'sugar': '22-01-2020', 'wheat': '23-01-2020', 'rice': '21-01-2020', 'tomato': '20-01-2020', 'potato': '22-01-2020', 'mango': '19-01-2020'}    
    data2 = {'Daily Expense':total,'remaining':remaining,'stocks':stocks}
    SDetails.document("katabook").set(data2)
    return "Aise taise kara lo"



    
if __name__ == '__main__':
    app.run(debug=True, port=5000) #run app in debug mode on port 5000
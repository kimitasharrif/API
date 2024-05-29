# Apllication programing Interface
from flask import *
import pymysql
connection=pymysql.connect(host="localhost",user="root", database="bookings_db",password="")
app=Flask(__name__)
# routes
@app.route("/signup",methods=['POST','GET'])
def Signup():
    connection=pymysql.connect(host="localhost",user="root", database="bookings_db",password="")
    # Get data  from the user using the api
    json=request.json
    username=json['username']
    email=json['email']
    phone=json['phone']
    password=json['password']
    confirm_password=json['confirm_password']
    #Validadition
    if not username or not email or not phone or not password or not confirm_password:
        response =jsonify({"meassge":"Please provide all the required data"})
        response.status_code=401
        return response
    if password != confirm_password:
       response =jsonify({"meassge":"Password do not match"})
       response.status_code=402
       return response
    sql_save='insert into users (username,email,phone ,password) values(%s,%s,%s,%s)'
    values=(username,email,phone,password)
    
    cursor_save=connection.cursor()
    cursor_save.execute(sql_save,values)
    connection.commit()
    response =jsonify({"message":"Signup successifully"})
    response.status_code=200
    return response

    
@app.route("/signin",methods=['POST','GET'])
def Signin():
    connection=pymysql.connect(host="localhost",user="root", database="bookings_db",password="")
    json=request.json
    username=json['username']
    password=json['password']
    sql='select * from users where username=%s and password =%s'
    cursor=connection.cursor()
    cursor.execute(sql,(username,password))
    if cursor.rowcount ==0:
        response = jsonify({"message": "Username does not exist"})
        response.status_code = 405
        return response
    else:
        response = jsonify({"message": "Signin Successful"})
        response.status_code = 201
        return response



@app.route("/getrooms",methods=['POST','GET'])
def GetConferenceRooms():
    connection=pymysql.connect(host="localhost",user="root", database="bookings_db",password="")
    sql='select * from rooms'
    cursor=connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql)
    if cursor.rowcount ==0:
        response = jsonify({"message": "No room to display"})
        response.status_code = 406
        return response
    else:
        rooms=cursor.fetchall()
        response=jsonify(rooms)
        response.status_code=203
        return response
        return response

# Mpesa integration route

# mpesa integration route
import requests
import base64
import datetime
from requests.auth import HTTPBasicAuth
@app.route("/mpesa_payment",methods=['POST','GET'])
def mpesa_payment():
        connection=pymysql.connect(host="localhost",user="root", database="bookings_db",password="")
        json=request.json
        phone = json['phone']
        amount = json['amount']
        # GENERATING THE ACCESS TOKEN
        # create an account on safaricom daraja
        consumer_key = "GTWADFxIpUfDoNikNGqq1C3023evM6UH"
        consumer_secret = "amFbAoUByPV2rM5A"

        api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"  # AUTH URL
        r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))

        data = r.json()
        access_token = "Bearer" + ' ' + data['access_token']

        #  GETTING THE PASSWORD
        timestamp = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
        passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
        business_short_code = "174379" #test paybil
        data = business_short_code + passkey + timestamp
        encoded = base64.b64encode(data.encode())
        password = encoded.decode('utf-8')
        # BODY OR PAYLOAD
        payload = {
            "BusinessShortCode": "174379",
            "Password": "{}".format(password),
            "Timestamp": "{}".format(timestamp),
            "TransactionType": "CustomerPayBillOnline",
            "Amount":amount,  # use 1 when testing
            "PartyA": phone,  # change to your number
            "PartyB": "174379",
            "PhoneNumber": phone,
            "CallBackURL": "https://modcom.co.ke/job/confirmation.php",
            "AccountReference": "account",
            "TransactionDesc": "account"
        }

        # POPULAING THE HTTP HEADER
        headers = {
            "Authorization": access_token,
            "Content-Type": "application/json"
        }

        url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"  # C2B URL

        response = requests.post(url, json=payload, headers=headers)
        print(response.text)
        response=jsonify({"Success":"Paid {}".format(phone,amount)})
        response.status_code=204
        return response

app.run(debug=True)





@app.route("/getroom")
def Getroom():
    
import os
import pyodbc
from flask import (Flask, redirect, render_template, request,send_from_directory, url_for,jsonify,session,send_file)
from dotenv import load_dotenv
from io import BytesIO

app = Flask(__name__)


load_dotenv()

server = os.getenv("SQL_SERVER")
database = os.getenv("SQL_DATABASE")
username = os.getenv("SQL_USERNAME")
password = os.getenv("SQL_PASSWORD")
driver = '{ODBC Driver 18 for SQL Server}'

connection_string = f'Driver={driver};Server={server};Database={database};Uid={username};Pwd={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'


conn = pyodbc.connect(connection_string)

@app.route('/')
def index():

    conn=pyodbc.connect(connection_string)
    cursor=conn.cursor()
    query="Select ImgID,Imagedata,Imagetype,Name from [Cloths.Data]"
    cursor.execute(query)
    Images=cursor.fetchall()

    return render_template('index.html',Images=Images)

@app.route('/admin')
def admin():
    conn=pyodbc.connect(connection_string)
    cursor=conn.cursor()
    query="Select ImgID,Imagedata,Imagetype,Name from [Cloths.Data]"
    cursor.execute(query)
    Images=cursor.fetchall()
    return render_template('admin/dashboard.html',Images=Images)

@app.route('/upload', methods=['POST'])
def upload():
    file=request.files['image']
    if file:
        image_data=file.read()
        conn=pyodbc.connect(connection_string)
        cursor=conn.cursor()
        query="Insert into [Cloths.Data](Name,ClothType,Imagetype,Imagedata) Values (?,?,?,?)"
        cursor.execute(query,(file.filename,file.filename,file.content_type, image_data,))
        conn.commit()
    return redirect('admin')

@app.route('/image/<int:image_id>')
def image(image_id):
    conn=pyodbc.connect(connection_string)
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM [Cloths.data] WHERE ImgId = ?", image_id)
    row = cursor.fetchone()
    if row:
        return send_file(BytesIO(row.Imagedata), mimetype=row.Imagetype)
    return "Image not found", 404


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/authentication',methods=['POST'])
def auth():
    email=request.form.get('email')
    password=request.form.get('password')
    if email and password:
        print(email,password)
    else:
        print("Not working")
    return render_template('index.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')   

@app.route('/usercreation', methods=['POST'])
def usercreation():
    return render_template('index.html')


if __name__=='__main__':
    app.run(debug=True,port=3000)
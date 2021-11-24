from datetime import datetime
from os import name
from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///sample_login.db"
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)

class SampleLogin(db.Model):
    sno = db.Column(db.Integer,primary_key = True )
    txt_name = db.Column(db.String(200),nullable = False )
    txt_password = db.Column(db.String(200),nullable = False )
    date_created = db.Column(db.DateTime,default = datetime.utcnow)


    def __repr__(self) -> str:
        return f"{self.sno} - {self.txt_name} - {self.txt_password}"


@app.route("/", methods = ['GET','POST'])
def hello_world():
    if request.method =='POST':
        txt_name = request.form['txt_name']
        txt_password = request.form['txt_password']  
        sample_login = SampleLogin(txt_name = txt_name, txt_password = txt_password)
        db.session.add(sample_login)
        db.session.commit()
    alldata = SampleLogin.query.all()
    
    print(alldata)

    return render_template('index.html' , alldata = alldata)
     # return "<p>Hello, World!</p>"

@app.route("/show")
def about():
    alldata = SampleLogin.query.all()
    print(alldata)
    return render_template('index.html' , alldata = alldata)

@app.route('/update/<int:sno>' , methods = ['GET','POST'])
def update(sno):
    if request.method == 'POST':
        txt_name = request.form['txt_name']
        txt_password = request.form['txt_password']  
        alldata = SampleLogin.query.filter_by(sno=sno).first()
        alldata.txt_name = txt_name
        alldata.txt_password = txt_password
        db.session.add(alldata)
        db.session.commit()
        return redirect("/")
    alldata = SampleLogin.query.filter_by(sno=sno).first()
    return render_template('update.html' , alldata = alldata)
   

@app.route('/delete/<int:sno>', methods = ['GET','POST'])
def delete(sno):
    alldata = SampleLogin.query.filter_by(sno=sno).first()
    db.session.delete(alldata)
    db.session.commit()
    return redirect("/")
    
 
if __name__=="__main__":
    app.run(debug=True)
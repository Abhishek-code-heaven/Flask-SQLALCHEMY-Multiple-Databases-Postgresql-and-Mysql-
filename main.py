from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from flask import request, redirect, render_template

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost/mydatabase'
app.config['SQLALCHEMY_BINDS'] = {'two' : 'mysql://root:123@localhost/mydatabase'}
app.config['SQLALCHEMY TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

class Postgresql(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique = True)
  email = db.Column(db.String(120), unique = True)

  def __init__(self,username,email):
    self.username = username
    self.email = email

  def __repr__(self):
    return '<User %r>' % self.username

class Mysql(db.Model):
  __bind_key__ = 'two'
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique = True)
  email = db.Column(db.String(120), unique = True)

  def __init__(self,username,email):
    self.username = username
    self.email = email

  def __repr__(self):
    return '<User %r>' % self.username

@app.route('/PostgreSQL')
def indexpostgres():
  return render_template('postgres_template.html')

@app.route('/MySQL')
def indexsql():
  return render_template('mysql_user.html')

@app.route('/postgres_user', methods = ['POST'])
def postgres_user():
  user = Postgresql(request.form['username'], request.form['email'])
  db.session.add(user)
  db.session.commit()
  return redirect(url_for('indexpostgres'))

@app.route('/mysql_user', methods = ['POST'])
def sql_user():
  user = Mysql(request.form['username'], request.form['email'])
  db.session.add(user)
  db.session.commit()
  return redirect(url_for('indexsql'))



if __name__=="__main__":
  app.run(debug=True)
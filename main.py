# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing


# configuration
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = '1234'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

#app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql',mode = 'r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def show_entries():
    cur = g.db.execute('select player_name, hand, age, gender, rank from players order by id desc')
    players = [dict(player_name=row[0], hand=row[1], age = row[2], \
gender = row[3], rank =row[4]) for row in cur.fetchall()]
    return render_template('show_entries.html', players=players)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into players (player_name, hand, age, gender, rank) values (?,?,?,?,?)',[request.form['player_name'], request.form['hand'], request.form['age'], request.form['gender'], request.form['rank']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/test', methods=['POST'])
def test():
    if not session.get('logged_in'):
        abort(401)
    cont = request.form['cont_radio'];    
    p = request.form['player_radio'];
    if cont == '1':
        cur = g.db.execute('select * from shots WHERE player_name = "%s"' %p)
    elif cont == '2':
        cur = g.db.execute('select * from shots WHERE player_name = "%s" AND receiver_score>=3 AND receiver_score>server_score' %p)
    elif cont == '3':
        cur = g.db.execute('select * from shots WHERE player_name = "%s" AND server_score>=3 AND server_score>receiver_score' %p)
    else:
        cur = g.db.execute('select * from shots WHERE player_name = "%s"' %p)
    
    shots = [dict(player_name=row[0],speed = row[2],x=row[6],y=row[7],score_s=row[11], score_r=row[12],tournament=row[10],start_x=row[3],start_y=row[4], serve_class=row[1]) for row in cur.fetchall()]
    
    cur2 = g.db.execute('select * from players order by id desc')
    players = [dict(player_name=row[1],hand=row[2],age=row[3],gender=row[4],rank=row[5]) for row in cur2.fetchall()]
    num = len(shots)
    return render_template('show_shots.html',players = players,shots=shots, p = p, num = num, cont=cont)

@app.route('/select_para', methods=['GET', 'POST'])
def select_para():
    if not session.get('logged_in'):
        abort(401)
    return render_template('select_para.html')

@app.route('/serve_pred', methods=['GET', 'POST'])
def serve_pred():
    if not session.get('logged_in'):
        abort(401)
    return render_template('serve_pred.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

@app.route('/plot')
def plot():
    return render_template('plot_serve.html')


if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000)


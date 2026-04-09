from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
import os
import time

app = Flask(__name__)
application = app
app.secret_key = 'super_secret_classified_key'

DB_HOST = os.getenv("DB_HOST", "db")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "Ehtisham@2004")
DB_NAME = os.getenv("DB_NAME", "flask_app_db")

def get_db_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

def init_db():
    retries = 10
    while retries > 0:
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS vips (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    alibi TEXT NOT NULL
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS fixers (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(255) NOT NULL,
                    password VARCHAR(255) NOT NULL
                )
            ''')

            cursor.execute('SELECT COUNT(*) AS count FROM vips')
            vips_count = cursor.fetchone()['count']
            if vips_count < 10:
                cursor.execute('DELETE FROM vips')
                dummy_vips = [
                    ('Prince Andrew', 'Never Met Him'),
                    ('Bill Clinton', 'Philanthropy Meeting'),
                    ('Bill Gates', 'Getting Financial Advice'),
                    ('Stephen Hawking', 'Checking the island\'s Wi-Fi'),
                    ('Kevin Spacey', 'My PR Team Was Hacked'),
                    ('Les Wexner', 'Pleaded the 5th'),
                    ('David Copperfield', 'Making the evidence disappear'),
                    ('Alan Dershowitz', 'Kept my underwear on'),
                    ('Jes Staley', 'Thought it was a Disney cruise'),
                    ('Leon Black', 'Tax write-off purposes'),
                    ('John Doe (Redacted)', 'Looking for the bathroom'),
                    ('Anonymous Tech CEO', 'I was hacked'),
                    ('That One Guy From The 90s', 'It was my evil twin'),
                    ('A Very Sweaty Prince', 'I thought it was Epstein\'s brother, Jeff'),
                    ('Definitely Not A Politician', 'Just there for the snorkeling'),
                    ('Mr. Monopoly', 'Philanthropy Meeting'),
                    ('Bruce Wayne', 'Getting Financial Advice'),
                    ('Tony Stark', 'Never Met Him'),
                    ('Lex Luthor', 'My PR Team Was Hacked'),
                    ('Dr. Evil', 'Pleaded the 5th'),
                    ('Mr. Burns', 'Looking for the bathroom'),
                    ('Scrooge McDuck', 'Thought it was a Disney cruise'),
                    ('Rich Uncle Pennybags', 'Researching a movie role'),
                    ('Gordon Gekko', 'Checking the island\'s Wi-Fi'),
                    ('Jordan Belfort', 'I was hacked'),
                    ('Patrick Bateman', 'It was my evil twin'),
                    ('Montgomery Burns', 'I thought it was Epstein\'s brother, Jeff'),
                    ('Carter Pewterschmidt', 'Just there for the snorkeling'),
                    ('Arthur Fortune', 'Tax write-off purposes'),
                    ('Tyrell Wellick', 'Making the evidence disappear'),
                    ('Eldon Tyrell', 'Kept my underwear on'),
                    ('Niander Wallace', 'Philanthropy Meeting'),
                    ('Ozymandias', 'Getting Financial Advice'),
                    ('Lucius Malfoy', 'Never Met Him'),
                    ('Tom Riddle', 'My PR Team Was Hacked'),
                    ('Voldemort', 'Pleaded the 5th'),
                    ('Sauron', 'Looking for the bathroom'),
                    ('Saruman', 'Thought it was a Disney cruise'),
                    ('Darth Vader', 'Researching a movie role'),
                    ('Emperor Palpatine', 'Checking the island\'s Wi-Fi'),
                    ('Jabba the Hutt', 'I was hacked'),
                    ('Boba Fett', 'It was my evil twin'),
                    ('Thanos', 'I thought it was Epstein\'s brother, Jeff'),
                    ('Loki', 'Just there for the snorkeling'),
                    ('Ultron', 'Tax write-off purposes'),
                    ('Green Goblin', 'Making the evidence disappear'),
                    ('Doctor Octopus', 'Kept my underwear on'),
                    ('Venom', 'Philanthropy Meeting'),
                    ('Carnage', 'Getting Financial Advice'),
                    ('Kingpin', 'Never Met Him')
                ]
                cursor.executemany('INSERT INTO vips (name, alibi) VALUES (%s, %s)', dummy_vips)

            conn.commit()
            cursor.close()
            conn.close()

            print("Database initialized successfully")
            return

        except Exception as e:
            print(f"Waiting for MySQL... ({e})")
            retries -= 1
            time.sleep(3)

    raise Exception("Could not connect to MySQL after retries")

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check hardcoded guest admin
        if username == 'guest_admin' and password == 'i_plead_the_5th':
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
            
        # Check database for fixers
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM fixers WHERE username = %s AND password = %s', (username, password))
        fixer = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if fixer:
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            flash('Access Denied. This incident will be reported.')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM vips')
    vips = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('dashboard.html', vips=vips)

# --- VIP CRUD ---
@app.route('/vips')
def vips():
    if not session.get('logged_in'): return redirect(url_for('login'))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM vips')
    vips = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('vips.html', vips=vips)

@app.route('/vips/add', methods=('GET', 'POST'))
def add_vip():
    if not session.get('logged_in'): return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form['name']
        alibi = request.form['alibi']
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('INSERT INTO vips (name, alibi) VALUES (%s, %s)', (name, alibi))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('vips'))
    return render_template('vip_form.html', action='Add')

@app.route('/vips/edit/<int:id>', methods=('GET', 'POST'))
def edit_vip(id):
    if not session.get('logged_in'): return redirect(url_for('login'))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM vips WHERE id = %s', (id,))
    vip = cursor.fetchone()
    if request.method == 'POST':
        name = request.form['name']
        alibi = request.form['alibi']
        cursor.execute('UPDATE vips SET name = %s, alibi = %s WHERE id = %s', (name, alibi, id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('vips'))
    cursor.close()
    conn.close()
    return render_template('vip_form.html', action='Edit', vip=vip)

@app.route('/vips/delete/<int:id>', methods=('POST',))
def delete_vip(id):
    if not session.get('logged_in'): return redirect(url_for('login'))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('DELETE FROM vips WHERE id = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('vips'))

# --- Fixer CRUD ---
@app.route('/fixers')
def fixers():
    if not session.get('logged_in'): return redirect(url_for('login'))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM fixers')
    fixers = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('fixers.html', fixers=fixers)

@app.route('/fixers/add', methods=('GET', 'POST'))
def add_fixer():
    if not session.get('logged_in'): return redirect(url_for('login'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('INSERT INTO fixers (username, password) VALUES (%s, %s)', (username, password))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('fixers'))
    return render_template('fixer_form.html', action='Add')

@app.route('/fixers/edit/<int:id>', methods=('GET', 'POST'))
def edit_fixer(id):
    if not session.get('logged_in'): return redirect(url_for('login'))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM fixers WHERE id = %s', (id,))
    fixer = cursor.fetchone()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor.execute('UPDATE fixers SET username = %s, password = %s WHERE id = %s', (username, password, id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('fixers'))
    cursor.close()
    conn.close()
    return render_template('fixer_form.html', action='Edit', fixer=fixer)

@app.route('/fixers/delete/<int:id>', methods=('POST',))
def delete_fixer(id):
    if not session.get('logged_in'): return redirect(url_for('login'))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('DELETE FROM fixers WHERE id = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('fixers'))

# Run DB initialization for both Gunicorn and local Flask execution.
init_db()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    application.run(host="0.0.0.0", port=port)

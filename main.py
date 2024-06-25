from flask import Flask, render_template, request, redirect, url_for, session, g, jsonify
import MySQLdb, random

app = Flask(__name__)
app.secret_key = '_5#y2L"F4Q8z-n-xec]/'

def random_sifra(length=4):
    r1 = ['1', '2', '3', 'A']
    r2 = ['4', '5', '6', 'B']
    r3 = ['7', '8', '9', 'C']
    r4 = ['*', '0', 'D', '#']

    slova = r1 + r2 + r3 + r4
    password = ''.join(random.choice(slova) for _ in range(length))
    
    return password

@app.before_request
def before_request_func():
    g.connection = MySQLdb.connect(host="localhost", user="app", passwd="1234", db="purs")
    g.cursor = g.connection.cursor()

    if request.path in ['/login', '/register', '/provjera_sifre'] or request.path.startswith('/static'):
        return
        
    if session.get('username') is None:
        return redirect(url_for('login'))
        
@app.after_request
def after_request_func(response):
    g.connection.commit()
    g.connection.close()
    return response

@app.get('/')
def index():
    user_id = session.get('id')
    ovlasti = session.get('ovlasti')
    id = request.args.get('id', '1')
    ormaric_id = request.args.get('ormaric_id')
    sifra = request.args.get('sifra')
    poruka = request.args.get('poruka')

    if id == '1':
        if user_id is not None:
            getOr = render_template('getOrmaric.sql')
            g.cursor.execute(getOr)
            ormarici = g.cursor.fetchall()
            response = render_template('index.html', naslov='Početna stranica', username=session.get('username'), data=ormarici, ovlasti=ovlasti, id=id, poruka=poruka)
            return response, 200

    elif id == '2':
        if user_id is not None:
            getAk = render_template('getAktivnosti.sql')
            g.cursor.execute(getAk)
            aktivnosti = g.cursor.fetchall()
            print(aktivnosti)
            response = render_template('index.html', naslov='Registrirani korisnici', username=session.get('username'), data=aktivnosti, ovlasti=ovlasti, id=id, poruka=poruka)
            return response, 200   

    elif id == '3':
        if user_id is not None:
            response = render_template('index.html', naslov='Iznajmi ormarić', username=session.get('username'), ovlasti=ovlasti, id=id, id_ormarica=ormaric_id, sifra=sifra, poruka=poruka)
            return response, 200
        
    elif id == '4':
        if user_id is not None:
            getAktivnosti = render_template('getAktivnostiTab.sql')
            g.cursor.execute(getAktivnosti)
            aktivnosti = g.cursor.fetchall()
            response = render_template('index.html', naslov='Sve aktivnosti', username=session.get('username'), data=aktivnosti, ovlasti=ovlasti, id=id)
            return response, 200

    return redirect(url_for('login'))

@app.post('/insert_ormaric')
def insert_ormaric():
    g.cursor.execute(render_template('insertOrmaric.sql'))
    g.connection.commit()  
    return redirect(url_for('index'))

@app.post('/toggle_ormaric/<int:id>')
def toggle_ormaric(id):
    g.cursor.execute(render_template('toggleOrmaric.sql'), (id,))
    g.connection.commit()
    return redirect(url_for('index'))

@app.post('/delete_ormaric/<int:id>')
def delete_ormaric(id):
    if id == 1:
        return redirect(url_for('index', id=1, poruka="Nije moguće obrisati ovaj ormarić!"))
    g.cursor.execute(render_template('deleteOrmaric.sql'), (id,))
    g.connection.commit()
    return redirect(url_for('index', id=1, poruka="Ormarić je uspješno obrisan."))

@app.post('/delete_korisnik/<int:id>')
def delete_korisnik(id):
    g.cursor.execute(render_template('deleteKorisnik.sql'), (id,))

    if g.cursor.rowcount > 0:
        g.connection.commit()
        poruka = "Korisnik uspješno obrisan."
    else:
        poruka = "Brisanje neuspješno. Nije moguće obrisati administratora."
    return redirect(url_for('index', id = 2, poruka=poruka))

@app.get('/iznajmi_ormaric')
def iznajmi_get():
    user_id = session.get('id')
    if user_id is None:
        return redirect(url_for('login'))
    
    ovlasti = session.get('ovlasti')
    id = '3'
    
    g.cursor.execute(render_template('checkOrmKor.sql'), (user_id,))
    result = g.cursor.fetchone()

    if result:
        ormaric_id, sifra = result
        return render_template('index.html', naslov='Iznajmi ormarić', username=session.get('username'), ovlasti=ovlasti, id=id, id_ormarica=ormaric_id, sifra=sifra)
    else:
        return render_template('index.html', naslov='Iznajmi ormarić', username=session.get('username'), ovlasti=ovlasti, id=id)

@app.post('/vrati_ormaric')
def vrati_ormaric():
    user_id = session.get('id')
    if user_id is None:
        return redirect(url_for('login'))
    
    ormaric_id = request.form.get('ormaric_id')
    if ormaric_id:
        g.cursor.execute(render_template('returnOrmaric.sql'), (ormaric_id,))
        g.cursor.execute(render_template('deleteOrmKor.sql'), (ormaric_id, user_id))
        g.cursor.execute(render_template('addAktivnost.sql'), (user_id, ormaric_id, 'Vraćen ormarić'))
        g.connection.commit()
        
        return redirect(url_for('index', id=3, poruka="Ormarić je uspješno vraćen."))
    else:
        return redirect(url_for('index', id=3, poruka="Došlo je do greške prilikom vraćanja ormarića."))

@app.post('/iznajmi_ormaric')
def iznajmi_post():
    user_id = session.get('id')

    if user_id is None:
        return redirect(url_for('login'))
    
    g.cursor.execute(render_template('checkOrmKor.sql'), (user_id,))
    result = g.cursor.fetchone()

    if result:
        ormaric_id, sifra = result
        return redirect(url_for('index', id=3, ormaric_id=ormaric_id, sifra=sifra, poruka="Već imate iznajmljen ormarić."))
    
    sifra = random_sifra()

    g.cursor.execute(render_template('slobOrmaric.sql'))
    result = g.cursor.fetchone()
    print(result)

    if result:
        ormaric_id = result[0]
        g.cursor.execute(render_template('updateOrmaric.sql'), (ormaric_id,))
        g.cursor.execute(render_template('addOrmKor.sql'), (user_id, ormaric_id, sifra))
        g.cursor.execute(render_template('addAktivnost.sql'), (user_id, ormaric_id, 'Iznajmljen ormarić'))
        g.connection.commit()
        return redirect(url_for('index', id=3, ormaric_id=ormaric_id, sifra=sifra, poruka="Uspješno ste iznajmili ormarić."))
    else:
        return redirect(url_for('index', id=3, poruka="Nema slobodnih ormarića."))

@app.post('/register')
def register_korisnik():
    ime = request.form['ime']
    prezime = request.form['prezime']
    username = request.form['username']
    password = request.form['password']

    g.cursor.execute(render_template('checkUsername.sql'), (username,))
    result = g.cursor.fetchone()

    if result[0] > 0:
        return render_template('login.html', poruka='Korisničko ime već postoji. Molimo odaberite drugo.')
    
    g.cursor.execute(render_template('registerKorisnik.sql'), (ime, prezime, username, password, 2))
    g.connection.commit()
    return render_template('login.html', poruka='Uspješna registracija!')

@app.get('/login')
def login():
    response = render_template('login.html', naslov='Stranica za prijavu')
    return response, 200

@app.post('/login')
def check():
    username = request.form.get('username')
    password = request.form.get('password')

    getUser = render_template('getUser.sql')
    g.cursor.execute(getUser, (username, password))
    user = g.cursor.fetchone()

    if user:
        session['id'] = user[0]
        session['username'] = user[1]
        session['ovlasti'] = user[2]
        getLogin = render_template('addLogin.sql')
        g.cursor.execute(getLogin, (user[0],))
        g.connection.commit()
        return redirect(url_for('index', id=3))
                    
    else:
        return render_template('login.html', poruka='Uneseni su pogresni podaci')    
    
@app.post('/provjera_sifre')
def provjera_sifre():
    data = request.get_json()
    sifra = data.get('sifra')
   
    g.cursor.execute(render_template('checkSifra.sql'), (sifra,))
    result = g.cursor.fetchone()

    if result:
        return jsonify({'ormaric_sifra': True}), 200
    else:
        return jsonify({'ormaric_sifra': False}), 200


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

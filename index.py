from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

# MYSQL CONNECTION
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'easydrinks'
mysql = MySQL(app)


# SETTINGS
app.secret_key = 'mysecretkey'

@app.route('/')
def home():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()
    return render_template('home.html', contacts = data)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO contacts (fullname, phone, email) VALUES (%s, %s, %s)', 
        (fullname, phone, email))
        mysql.connection.commit()
        flash('Los datos se han cargado correctamente')
        return redirect(url_for('home'))

@app.route('/edit/<id>')
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE id = %s', [id])
    data = cur.fetchall()
    return render_template('edit-contact.html', contact = data[0])

@app.route('/update/<id>', methods = ['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        phone = request.form['phone']
    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE contacts
        SET fullname = %s,
            email = %s,
            phone = %s
        WHERE id = %s
     """, (fullname, email, phone, id))
    mysql.connection.commit()
    flash('Contacto actualizado correctamente')
    return redirect(url_for('home'))

@app.route('/delete/<string:id>')
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('El contacto se ha eliminado correctamente')
    return redirect(url_for('home'))
       
# AUTOMATIC REFRESH
if  __name__ == '__main__':
    app.run(port=3000, debug=True)


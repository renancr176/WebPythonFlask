"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, jsonify, request
from flask_mysqldb import MySQL
from WebPythonFlask import app

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'faculdade'

mysql = MySQL(app)

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

# ---------------------------- PAGINAS ----------------------

@app.route('/funcionarios', methods=['GET'])
def funcionarios():
    return render_template(
        'funcionarios.html',
        title='Funcionarios'
    )

@app.route('/funcionarios/<int:funcionarioId>/pontos', methods=['GET'])
def pontos(funcionarioId):
    return render_template(
        'pontos.html',
        title='Pontos'
    )

# ---------------------- API ENDPOINTS ----------------------

@app.route('/api', methods=['GET'])
def api():
    return jsonify({"versao":"1.0"}), 200


@app.route('/api/funcionarios', methods=['GET', 'POST'])
def api_funcionarios():
    if (request.method == 'POST'):
        if(request.form['nome']):
            cur = mysql.connection.cursor()
            sql = "INSERT INTO funcionarios (nome) VALUES ('"+request.form['nome']+"')"
            cur.execute(sql)
            mysql.connection.commit()
            cur.close()
            return jsonify({"result": "ok"}), 202
        else:
            return null, 400
    else:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM funcionarios")
        funcionarios = []
        result = cur.fetchall()
        for f in result:
            funcionarios.append({"id":f[0], "nome":f[1]})
        cur.close()
        return jsonify(funcionarios), 200

@app.route('/api/pontos/<int:funcionarioId>', methods=['GET', 'POST'])
def api_pontos(funcionarioId):
    if (request.method == 'POST'):
        cur = mysql.connection.cursor()
        sql = "INSERT INTO funcionariopontos (funcionarioId, dataPonto) VALUES ('"+str(funcionarioId)+"', NOW())"
        cur.execute(sql)
        mysql.connection.commit()
        cur.close()
        return jsonify({"result": "ok"}), 202
    else:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM funcionariopontos")
        pontos = []
        result = cur.fetchall()
        for f in result:
            pontos.append({"id":f[0], "funcionarioId": f[1], "dataPonto":f[2]})
        cur.close()
        return jsonify(pontos), 200
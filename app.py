from flask import Flask, render_template, request, session, redirect, url_for, flash
import mysql.connector, os, hashlib
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)

conexao = mysql.connector.connect(
    host='localhost',
    user = 'root',
    password='root',
    database = 'atividade' )


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        data_nasc = request.form['data_nasc']
        telefone = request.form['telefone']
        apelido = request.form['apelido']
        senha = request.form['senha']

        cursor = conexao.cursor()

        try:        
            comando_insert = f"INSERT INTO usuario (nome, email, data_nasc, telefone, apelido, senha) VALUES ('{nome}', '{email}', '{data_nasc}', '{telefone}', '{apelido}', SHA2('{senha}', 256))"
            cursor.execute(comando_insert)
            conexao.commit()

            cursor.close()

            flash('registro concluido!')
            return redirect(url_for('index'))
        except mysql.connector.IntegrityError as e:
            conexao.rollback()
            cursor.close()
            flash('Erro: Email ou apelido já cadastrado. Escolha outros.')

    return render_template('registro.html')

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        email = request.form['login']
        apelido = request.form['login']
        senha = request.form['senha']

        cursor = conexao.cursor()
        comando_select = f"SELECT nome, email, data_nasc, telefone, apelido, senha FROM usuario WHERE email = '{email}' OR apelido = '{apelido}'"
        cursor.execute(comando_select)

        usuario = cursor.fetchone()

        if usuario and hashlib.sha256(senha.encode()).hexdigest() == usuario[5]:
            session['usuario'] = usuario
            return redirect(url_for('dashboard'))
        else:
            flash('Erro: Usuário ou senha incorretos. Tente novamente.')
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if 'usuario' in session:
        usuario = session['usuario']

        if isinstance(usuario[2], str):
            try:
                usuario_data_nasc = datetime.strptime(usuario[2], '%a, %d %b %Y %H:%M:%S GMT')
            except ValueError:
                usuario_data_nasc = datetime.strptime(usuario[2], "%Y-%m-%d").date()
        else:
            usuario_data_nasc = usuario[2]

        return render_template('dashboard.html', usuario = usuario, usuario_data_nasc=usuario_data_nasc)
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
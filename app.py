#importação das bibliotecas
from flask import Flask, render_template, request, session, redirect, url_for, flash
import mysql.connector, os, hashlib
from datetime import datetime

#inicia o flask
app = Flask(__name__)

#configurando uma chave secreta forte para aumentar a segurança da aplicação Flask.
app.secret_key = os.urandom(24)

# Conecta com mysql
conexao = mysql.connector.connect(
    host='localhost',
    user = 'root',
    password='root',
    database = 'atividade' )

# Rota do index
@app.route('/')
def index():
    return render_template('index.html')

#rota do registro
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        #coleta dados do formulário de registro
        nome = request.form['nome']
        email = request.form['email']
        data_nasc = request.form['data_nasc']
        telefone = request.form['telefone']
        apelido = request.form['apelido']
        senha = request.form['senha']

        cursor = conexao.cursor()

        try:   
            #tenta registrar no banco de dados, os dados do usuario     
            comando_insert = f"INSERT INTO usuario (nome, email, data_nasc, telefone, apelido, senha) VALUES ('{nome}', '{email}', '{data_nasc}', '{telefone}', '{apelido}', SHA2('{senha}', 256))"
            cursor.execute(comando_insert)
            conexao.commit()

            cursor.close()

            flash('registro concluido!')
            return redirect(url_for('index'))

        except mysql.connector.IntegrityError as e:
            #Verifica se ja existe esse usuario
            conexao.rollback()
            cursor.close()
            flash('Erro: Email ou apelido já cadastrado. Escolha outros.')

    return render_template('registro.html')

#Rota do login
@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        #coleta dados do formulário de login
        email = request.form['login']
        apelido = request.form['login']
        senha = request.form['senha']

        cursor = conexao.cursor()
        comando_select = f"SELECT id, nome, email, data_nasc, telefone, apelido, senha FROM usuario WHERE email = '{email}' OR apelido = '{apelido}'"
        cursor.execute(comando_select)

        usuario = cursor.fetchone()

        if usuario and hashlib.sha256(senha.encode()).hexdigest() == usuario[6]:
            #autentica o usuario se as credenciais estiverem corretas
            session['usuario'] = usuario
            return redirect(url_for('dashboard'))
        else:
            flash('Erro: Usuário ou senha incorretos. Tente novamente.')
    return render_template('login.html')


#Rota do dashboard
@app.route('/dashboard')
def dashboard():
    if 'usuario' in session:
        usuario = session['usuario']

        if isinstance(usuario[3], str): #formatar a data do banco
            try:
                usuario_data_nasc = datetime.strptime(usuario[3], '%a, %d %b %Y %H:%M:%S GMT')
            except ValueError:
                usuario_data_nasc = datetime.strptime(usuario[3], "%Y-%m-%d").date()
        else:
            usuario_data_nasc = usuario[3]

        return render_template('dashboard.html', usuario = usuario, usuario_data_nasc=usuario_data_nasc)
    return redirect(url_for('login'))

# Rota de logout
@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

#Rota da exclusão da conta
@app.route('/excluir_conta', methods=['POST', 'GET'])
def excluir_conta():
    if 'usuario' in session:
        usuario = session['usuario']
        if request.method == 'POST':
            senha = request.form['senha']

            cursor = conexao.cursor()
            comando_select = f"SELECT nome, email, data_nasc, telefone, apelido, senha FROM usuario WHERE id = {usuario[0]}"
            cursor.execute(comando_select)
            usuario_db = cursor.fetchone()

            if usuario_db and hashlib.sha256(senha.encode()).hexdigest() == usuario[6]: 
                #verifica a senha e exclui a conta
                comando_delete = f"DELETE FROM usuario WHERE id = {usuario[0]}"
                cursor.execute(comando_delete)
                conexao.commit()
                
                cursor.close()
                session.pop('usuario', None)
                flash('Conta excluida com sucesso!')
                return redirect(url_for('index'))
        
            else:
                flash('Erro: Senha incorreta. Tente novamente.')
            
            return redirect(url_for('dashboard'))
 
    return redirect(url_for('login'))

#executa o aplicativo flask
if __name__ == '__main__':
    app.run(debug=True)
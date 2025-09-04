from flask import Flask, render_template, request, redirect, session, flash, url_for

class livro:
    def __init__(self, nome, autor, nota):
        self.nome = nome
        self.autor = autor
        self.nota = nota

livro1 = livro('VBA do Basico ao Avançado', 'Tadeu Carmona', '8.2')
livro2 = livro('Storytelling com dados', 'Cole Nussbaumer Knaflic', '9.0')
livro3 = livro('Machine Learning – Guia De Referência Rápida', 'Matt Harrison', '7.0')
lista = [livro1, livro2, livro3]

class Usuario:
    def __init__(self, nome, nickname, senha):
        self.nome = nome
        self.nickname = nickname
        self.senha = senha

usuario1 = Usuario("Matheus Volpini", "MV", "matheus")
usuario2 = Usuario("Luciana Veras", "Lu", "Luzinha")
usuario3 = Usuario("Maria Luiza", "Malu", "testando")

usuarios = { usuario1.nickname : usuario1,
             usuario2.nickname : usuario2,
             usuario3.nickname : usuario3 }

app = Flask(__name__)
app.secret_key = 'Volpini'

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Novo Livro')

@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    autor = request.form['autor']
    nota = request.form['nota']
    livro_obj = livro(nome, autor, nota)
    lista.append(livro_obj)
    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)


@app.route('/autenticar', methods=['POST', ])
def autenticar():
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname + ' logado com sucesso!')
            proxima_pagina = request.form.get('proxima')
            if not proxima_pagina or proxima_pagina == 'None':
                proxima_pagina = url_for('index')
            return redirect(proxima_pagina)
    flash('Usuário não logado.')
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('index'))

app.run(debug=True)
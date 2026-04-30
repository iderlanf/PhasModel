import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

# Configurações de Upload
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# URL da sua API FastAPI
API_URL = "http://localhost:8000/modelos"

# Garante que a pasta de uploads exista
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    tipo = request.args.get("filtro_tipo")   # ex: 'pele'
    valor = request.args.get("filtro_valor") # ex: 'branca'
    
    filtros = {}
    if tipo and valor:
        # Cria o dicionário dinâmico, ex: {"pele": "branca"}
        filtros[tipo] = valor 
    
    try:
        # Envia os filtros para a FastAPI: http://localhost:8000/modelos?pele=branca
        response = requests.get(API_URL, params=filtros)
        modelos = response.json() if response.status_code == 200 else []
    except Exception as e:
        print(f"Erro ao conectar na API: {e}")
        modelos = []
        
    return render_template('index.html', modelos=modelos)

@app.route('/modelo/<int:id>')
def detalhes(id):
    """Exibe detalhes de uma modelo específica"""
    try:
        response = requests.get(f"http://localhost:8000/modelo/{id}")
        if response.status_code == 200:
            modelo = response.json()
            return render_template('detalhes.html', modelo=modelo)
    except requests.exceptions.ConnectionError:
        print("Erro de conexão com a API.")
    return "Modelo não encontrada", 404

@app.route('/adicionar', methods=['POST'])
def adicionar():
    """Recebe o formulário, salva a imagem e envia os dados para a API"""
    file = request.files.get('foto_arquivo')
    filename = "default.png"
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    dados = {
        "nome": request.form.get("nome"),
        "idade": int(request.form.get("idade")),
        "peso": int(request.form.get("peso")),
        "altura": float(request.form.get("altura")),
        "cabelo": request.form.get("cabelo"), # Atualizado
        "pele": request.form.get("pele"),     # Atualizado
        "olhos": request.form.get("olhos"),   # Atualizado
        "busto": float(request.form.get("busto")),
        "cintura": float(request.form.get("cintura")),
        "quadril": float(request.form.get("quadril")),
        "evento_participado": request.form.get("evento_participado"),
        "foto_url": filename
    }

    try:
        requests.post(API_URL, json=dados)
    except requests.exceptions.ConnectionError:
        print("Erro: Não foi possível enviar os dados para a API.")
        
    return redirect(url_for('index'))

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    if request.method == 'GET':
        try:
            response = requests.get(f"http://localhost:8000/modelo/{id}")
            if response.status_code == 200:
                modelo = response.json()
                return render_template('editar.html', modelo=modelo)
        except requests.exceptions.ConnectionError:
            print("Erro de conexão com a API.")
        return "Modelo não encontrada", 404

    # Se for POST, envia a atualização para a API
    dados = {
        "nome": request.form.get("nome"),
        "idade": int(request.form.get("idade")),
        "peso": int(request.form.get("peso")),
        "altura": float(request.form.get("altura")),
        "cabelo": request.form.get("cabelo"), # Atualizado
        "pele": request.form.get("pele"),     # Atualizado
        "olhos": request.form.get("olhos"),   # Atualizado
        "busto": float(request.form.get("busto")),
        "cintura": float(request.form.get("cintura")),
        "quadril": float(request.form.get("quadril")),
        "evento_participado": request.form.get("evento_participado"),
        "foto_url": request.form.get("foto_url")
    }
    
    try:
        requests.put(f"http://localhost:8000/modelos/{id}", json=dados)
    except requests.exceptions.ConnectionError:
        print("Erro de conexão com a API ao tentar editar.")

    return redirect(url_for('index'))

@app.route('/excluir/<int:id>')
def excluir(id):
    """Solicita a exclusão para a API"""
    try:
        response = requests.delete(f"{API_URL}/{id}")
        if response.status_code == 200:
            print(f"Modelo {id} excluída com sucesso.")
        else:
            print(f"Erro ao excluir: {response.text}")
    except requests.exceptions.ConnectionError:
        print("Erro de conexão com a API.")
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(port=5000, debug=True)

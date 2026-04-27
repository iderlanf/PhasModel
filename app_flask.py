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
    """Lista todas as modelos consumindo a API"""
    try:
        response = requests.get(API_URL)
        modelos = response.json() if response.status_code == 200 else []
    except requests.exceptions.ConnectionError:
        modelos = []
        print("Erro: A API FastAPI não está rodando na porta 8000")
    
    return render_template('index.html', modelos=modelos)

@app.route('/modelo/<int:id>')
def detalhes(id):
    """Exibe detalhes de uma modelo específica"""
    response = requests.get(f"http://localhost:8000/modelo/{id}")
    if response.status_code == 200:
        modelo = response.json()
        return render_template('detalhes.html', modelo=modelo)
    return "Modelo não encontrada", 404

@app.route('/adicionar', methods=['POST'])
def adicionar():
    """Recebe o formulário, salva a imagem e envia os dados para a API"""
    # 1. Trata o arquivo de imagem
    file = request.files.get('foto_arquivo')
    filename = "default.png" 
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    # 2. Coleta os dados do formulário
    dados = {
        "nome": request.form.get("nome"),
        "idade": int(request.form.get("idade")),
        "peso": int(request.form.get("peso")),
        "altura": float(request.form.get("altura")),
        "cor": request.form.get("cor"),
        "busto": float(request.form.get("busto")),
        "cintura": float(request.form.get("cintura")),
        "quadril": float(request.form.get("quadril")),
        "evento_participado": request.form.get("evento_participado"),
        "foto_url": filename
    }

    # 3. Envia para a API (FastAPI)
    try:
        requests.post(API_URL, json=dados)
    except requests.exceptions.ConnectionError:
        print("Erro: Não foi possível enviar os dados para a API.")

    return redirect(url_for('index'))

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    if request.method == 'GET':
        # Busca os dados atuais para preencher o formulário
        response = requests.get(f"http://localhost:8000/modelo/{id}")
        if response.status_code == 200:
            modelo = response.json()
            return render_template('editar.html', modelo=modelo)
        return "Modelo não encontrada", 404

    # Se for POST, envia a atualização para a API
    dados = {
        "nome": request.form.get("nome"),
        "idade": int(request.form.get("idade")),
        "peso": int(request.form.get("peso")),
        "altura": float(request.form.get("altura")),
        "cor": request.form.get("cor"),
        "busto": float(request.form.get("busto")),
        "cintura": float(request.form.get("cintura")),
        "quadril": float(request.form.get("quadril")),
        "evento_participado": request.form.get("evento_participado"),
        "foto_url": request.form.get("foto_url") # Mantém a foto atual por simplificação
    }
    requests.put(f"http://localhost:8000/modelos/{id}", json=dados)
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
    # O Flask roda na porta 5000
    app.run(port=5000, debug=True)

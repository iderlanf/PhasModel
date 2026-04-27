import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)
API_URL = "http://localhost:8000/modelos"

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    # Consome o endpoint GET do FastAPI
    response = requests.get(API_URL)
    modelos = response.json() if response.status_code == 200 else []
    return render_template('index.html', modelos=modelos)

@app.route('/modelo/<int:id>')
def detalhes(id):
    # Consome o endpoint GET /modelo/{id} do FastAPI
    response = requests.get(f"http://localhost:8000/modelo/{id}")
    if response.status_code == 200:
        modelo = response.json()
        return render_template('detalhes.html', modelo=modelo)
    return "Modelo não encontrada", 404

@app.route('/adicionar', methods=['POST'])
def adicionar():
    # 1. Trata o arquivo
    file = request.files.get('foto_arquivo')
    filename = "default.png" # Foto padrão caso não envie nenhuma

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    # 2. Coleta os outros dados
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
        "foto_url": filename  # Enviamos apenas o nome do arquivo para o banco
    }
    
    requests.post("http://localhost:8000/modelos", json=dados)
    return redirect(url_for('index'))

@app.route('/excluir/<int:id>')
def excluir(id):
    # Chama o endpoint DELETE do FastAPI passando o ID na URL
    response = requests.delete(f"http://localhost:8000/modelos/{id}")
    
    if response.status_code == 200:
        print(f"Modelo {id} excluída com sucesso.")
    else:
        print(f"Erro ao excluir: {response.text}")
        
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(port=5000, debug=True)
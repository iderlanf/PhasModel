from typing import Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import mysql.connector
from typing import List

app = FastAPI(title="API de Modelos")

# Configuração do Banco de Dados
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "0510", # Insira sua senha aqui
    "database": "biblioteca"
}

# Modelo Pydantic para validação
class ModeloSchema(BaseModel):
    nome: str
    idade: int
    peso: int
    altura: float
    cor: str
    busto: float
    cintura: float
    quadril: float
    evento_participado: str
    foto_url: Optional[str] = "default.png"

class ModeloDB(ModeloSchema):
    id: int

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.get("/modelos", response_model=List[ModeloDB])
def listar_modelos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM modelos")
    resultados = cursor.fetchall()
    conn.close()
    return resultados

@app.post("/modelos", status_code=status.HTTP_201_CREATED)
def criar_modelo(modelo: ModeloSchema):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """INSERT INTO modelos (nome, idade, peso, altura, cor, busto, cintura, quadril, evento_participado, foto_url) 
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    values = (modelo.nome, modelo.idade, modelo.peso, modelo.altura, modelo.cor, 
        modelo.busto, modelo.cintura, modelo.quadril, modelo.evento_participado,
        modelo.foto_url)
    cursor.execute(query, values)
    conn.commit()
    conn.close()
    return {"message": "Modelo cadastrada com sucesso"}

@app.get("/modelo/{id}", response_model=ModeloDB)
def buscar_modelo(id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM modelos WHERE id = %s", (id,))
    item = cursor.fetchone()
    conn.close()
    if not item:
        raise HTTPException(status_code=404, detail="Modelo não encontrada")
    return item

@app.delete("/modelos/{id}")
def excluir_modelo(id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM modelos WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    return {"message": "Modelo excluída"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

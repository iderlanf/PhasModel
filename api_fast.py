from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, field_validator
import mysql.connector
from typing import List, Optional, Any

app = FastAPI(title="API de Modelos Phas Models")

# Configuração do Banco de Dados
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "0510",
    "database": "biblioteca"
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

# Schema para entrada de dados (POST/PUT)
class ModeloSchema(BaseModel):
    nome: str
    idade: int
    peso: int
    altura: float
    cabelo: str
    pele: str
    olhos: str
    busto: float
    cintura: float
    quadril: float
    evento_participado: str
    foto_url: Optional[str] = "default.png"

# Schema para saída de dados (inclui o ID e trata Decimais do MySQL)
class ModeloDB(ModeloSchema):
    id: int

    # Este validador garante que os números vindos do MySQL (Decimal) 
    # sejam convertidos para float, corrigindo o erro de campos vazios no HTML.
    @field_validator('altura', 'busto', 'cintura', 'quadril', mode='before')
    @classmethod
    def convert_decimal(cls, v: Any) -> float:
        if v is None:
            return 0.0
        return float(v)

@app.get("/modelos", response_model=List[ModeloDB])
def listar_modelos(
    idade: Optional[int] = None,
    peso: Optional[int] = None,
    altura: Optional[float] = None,
    cabelo: Optional[str] = None,
    pele: Optional[str] = None,
    olhos: Optional[str] = None,
    busto: Optional[float] = None,
    cintura: Optional[float] = None,
    quadril: Optional[float] = None
):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = "SELECT * FROM modelos WHERE 1=1"
    params = []

    # Mapeamento dinâmico simples
    if idade: query += " AND idade = %s"; params.append(idade)
    if peso: query += " AND peso = %s"; params.append(peso)
    if altura: query += " AND altura = %s"; params.append(altura)
    if cabelo: query += " AND cabelo LIKE %s"; params.append(f"%{cabelo}%")
    if pele: query += " AND pele LIKE %s"; params.append(f"%{pele}%")
    if olhos: query += " AND olhos LIKE %s"; params.append(f"%{olhos}%")
    if busto: query += " AND busto = %s"; params.append(busto)
    if cintura: query += " AND cintura = %s"; params.append(cintura)
    if quadril: query += " AND quadril = %s"; params.append(quadril)

    cursor.execute(query, tuple(params))
    resultados = cursor.fetchall()
    conn.close()
    return resultados

@app.post("/modelos", status_code=status.HTTP_201_CREATED)
def criar_modelo(modelo: ModeloSchema):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """INSERT INTO modelos 
               (nome, idade, peso, altura, cabelo, pele, olhos, busto, cintura, quadril, evento_participado, foto_url) 
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    values = (
        modelo.nome, modelo.idade, modelo.peso, modelo.altura, 
        modelo.cabelo, modelo.pele, modelo.olhos, 
        modelo.busto, modelo.cintura, modelo.quadril, 
        modelo.evento_participado, modelo.foto_url
    )
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

@app.put("/modelos/{id}")
def atualizar_modelo(id: int, modelo: ModeloSchema):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """UPDATE modelos SET 
               nome=%s, idade=%s, peso=%s, altura=%s, cabelo=%s, pele=%s, olhos=%s, 
               busto=%s, cintura=%s, quadril=%s, evento_participado=%s, foto_url=%s 
               WHERE id=%s"""
    values = (
        modelo.nome, modelo.idade, modelo.peso, modelo.altura, 
        modelo.cabelo, modelo.pele, modelo.olhos, 
        modelo.busto, modelo.cintura, modelo.quadril, 
        modelo.evento_participado, modelo.foto_url, id
    )
    cursor.execute(query, values)
    conn.commit()
    conn.close()
    return {"message": "Modelo atualizada com sucesso"}

@app.delete("/modelos/{id}")
def excluir_modelo(id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM modelos WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    return {"message": "Modelo excluída com sucesso"}

if __name__ == "__main__":
    import uvicorn
    # Inicia o servidor na porta 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)

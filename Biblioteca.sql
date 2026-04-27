CREATE DATABASE IF NOT EXISTS biblioteca;
USE biblioteca;

CREATE TABLE IF NOT EXISTS modelos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    idade INT,
    peso INT,
    altura DECIMAL(5,2),
    cor VARCHAR(50),
    busto DECIMAL(5,2),
    cintura DECIMAL(5,2),
    quadril DECIMAL(5,2),
    evento_participado TEXT
    foto_url VARCHAR(255) DEFAULT 'default.png'
);
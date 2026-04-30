CREATE DATABASE biblioteca;
USE biblioteca;

CREATE TABLE modelos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    idade INT,
    peso INT,
    altura DECIMAL(5,2),
    cabelo VARCHAR(50),
    pele VARCHAR(50),
    olhos VARCHAR(50),
    busto DECIMAL(5,2),
    cintura DECIMAL(5,2),
    quadril DECIMAL(5,2),
    evento_participado TEXT,
    foto_url VARCHAR(255) DEFAULT 'default.png'
);
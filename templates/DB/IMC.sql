CREATE DATABASE imc;

USE imc;

CREATE TABLE pacientes (
    id INT AUTO_INCREMENT PRIMARY KEY,       -- Identificador único para cada paciente
    nome VARCHAR(255) NOT NULL,              -- Nome do paciente
    peso FLOAT NOT NULL,                     -- Peso em quilogramas
    altura FLOAT NOT NULL,                   -- Altura em metros
    imc FLOAT NOT NULL,                      -- IMC calculado
    classificacao VARCHAR(255) NOT NULL,     -- Classificação com base no IMC
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Registro da data de criação
);

SELECT * FROM pacientes;












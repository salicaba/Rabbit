-- Script de inicialización de la Base de Datos

CREATE DATABASE IF NOT EXISTS empresa_db;
USE empresa_db;

CREATE TABLE IF NOT EXISTS accesos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    empleado VARCHAR(255) NOT NULL,
    area VARCHAR(255) NOT NULL,
    hora VARCHAR(255) NOT NULL
);

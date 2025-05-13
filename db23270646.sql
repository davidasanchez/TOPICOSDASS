CREATE DATABASE IF NOT EXISTS waldos;
USE waldos;

CREATE TABLE IF NOT EXISTS categorias (
    id_categoria INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS clientes (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    direccion VARCHAR(200) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    email VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS empleados (
    id_empleado INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    cargo VARCHAR(100) NOT NULL,
    salario DECIMAL(10, 2) NOT NULL
);

CREATE TABLE IF NOT EXISTS proveedores (
    id_proveedor INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    direccion VARCHAR(200) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    email VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS unidades (
    id_unidad INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

INSERT INTO categorias (nombre) VALUES 
('Electrónicos'),
('Ropa'),
('Alimentos'),
('Hogar'),
('Juguetes');

INSERT INTO clientes (nombre, direccion, telefono, email) VALUES 
('Juan Pérez', 'Calle 123, Ciudad', '555-1234', 'juan@example.com'),
('María López', 'Avenida 456, Ciudad', '555-5678', 'maria@example.com'),
('Carlos Gómez', 'Boulevard 789, Ciudad', '555-9012', 'carlos@example.com');

INSERT INTO empleados (nombre, cargo, salario) VALUES 
('Pedro Ramírez', 'Gerente', 25000.00),
('Ana Martínez', 'Vendedor', 15000.00),
('Luisa Fernández', 'Almacenista', 12000.00);

INSERT INTO proveedores (nombre, direccion, telefono, email) VALUES 
('Distribuidora ABC', 'Calle Falsa 123, Ciudad', '555-1111', 'abc@example.com'),
('Suministros XYZ', 'Avenida Siempre Viva 456', '555-2222', 'xyz@example.com'),
('Importaciones QRS', 'Boulevard Industrial 789', '555-3333', 'qrs@example.com');

INSERT INTO unidades (nombre) VALUES 
('Pieza'),
('Kilogramo'),
('Litro'),
('Metro'),
('Caja');
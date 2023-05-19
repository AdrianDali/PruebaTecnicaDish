CREATE DATABASE `pruebatecnicadish` ;
use pruebatecnicadish;

CREATE TABLE `pruebatecnicadish`.`cliente` (
  `nombre` VARCHAR(40) NOT NULL,
  `apellido` VARCHAR(45) NOT NULL,
  `telefono` INT NOT NULL,
  `edad` INT NOT NULL,
  PRIMARY KEY (`telefono`));

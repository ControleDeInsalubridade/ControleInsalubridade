-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`Funcionário`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`Funcionário` ;

CREATE TABLE IF NOT EXISTS `mydb`.`Funcionário` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `Nome` VARCHAR(256) NOT NULL,
  `Sobrenome` VARCHAR(256) NOT NULL,
  `CPF` VARCHAR(256) NOT NULL,
  `RG` VARCHAR(256) NOT NULL,
  `DataNascimento` DATE NOT NULL,
  `Endereço` VARCHAR(256) NOT NULL,
  `Sexo` VARCHAR(256) NOT NULL,
  `data_admissão` DATE NOT NULL,
  `data_demissão` DATE NULL,
  PRIMARY KEY (`ID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Sala`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`Sala` ;

CREATE TABLE IF NOT EXISTS `mydb`.`Sala` (`ID`,`Nome`,`Ativo`)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Bancada`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`Bancada` ;

CREATE TABLE IF NOT EXISTS `mydb`.`Bancada` (
  `ID` INT NOT NULL,
  `Tipo` VARCHAR(45) NOT NULL,
  `Sala_ID` INT NOT NULL,
  `Ativo` TINYINT NOT NULL,
  PRIMARY KEY (`ID`, `Sala_ID`),
  INDEX `fk_Bancada_Sala1_idx` (`Sala_ID` ASC),
  CONSTRAINT `fk_Bancada_Sala1`
    FOREIGN KEY (`Sala_ID`)
    REFERENCES `mydb`.`Sala` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Utiliza`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`Utiliza` ;

CREATE TABLE IF NOT EXISTS `mydb`.`Utiliza` (
  `ID` INT NOT NULL,
  `Hora_inicio` DATETIME NOT NULL,
  `Hora_fim` DATETIME NULL,
  `Funcionário_ID` INT NOT NULL,
  `Bancada_ID` INT NOT NULL,
  `Bancada_Sala_ID` INT NOT NULL,
  PRIMARY KEY (`ID`),
  INDEX `fk_Utiliza_Funcionário1_idx` (`Funcionário_ID` ASC),
  INDEX `fk_Utiliza_Bancada1_idx` (`Bancada_ID` ASC, `Bancada_Sala_ID` ASC),
  CONSTRAINT `fk_Utiliza_Funcionário1`
    FOREIGN KEY (`Funcionário_ID`)
    REFERENCES `mydb`.`Funcionário` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Utiliza_Bancada1`
    FOREIGN KEY (`Bancada_ID` , `Bancada_Sala_ID`)
    REFERENCES `mydb`.`Bancada` (`ID` , `Sala_ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Camera`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`Camera` ;

CREATE TABLE IF NOT EXISTS `mydb`.`Camera` (
  `ID` INT NOT NULL,
  `IP` VARCHAR(45) NOT NULL,
  `Modelo` VARCHAR(45) NOT NULL,
  `Marca` VARCHAR(45) NOT NULL,
  `Datasheet` VARCHAR(45) NULL,
  `Sala_ID` INT NOT NULL,
  PRIMARY KEY (`ID`, `Sala_ID`),
  INDEX `fk_Camera_Sala1_idx` (`Sala_ID` ASC),
  CONSTRAINT `fk_Camera_Sala1`
    FOREIGN KEY (`Sala_ID`)
    REFERENCES `mydb`.`Sala` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Acessa`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`Acessa` ;

CREATE TABLE IF NOT EXISTS `mydb`.`Acessa` (
  `Acesso_ID` INT NOT NULL AUTO_INCREMENT,
  `Hora_entrada` DATETIME NOT NULL,
  `Hora_saída` DATETIME NULL,
  `Funcionário_ID` INT NOT NULL,
  `Sala_ID` INT NOT NULL,
  INDEX `fk_Acessa_Sala1_idx` (`Sala_ID` ASC),
  PRIMARY KEY (`Acesso_ID`),
  CONSTRAINT `fk_Acessa_Funcionário1`
    FOREIGN KEY (`Funcionário_ID`)
    REFERENCES `mydb`.`Funcionário` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Acessa_Sala1`
    FOREIGN KEY (`Sala_ID`)
    REFERENCES `mydb`.`Sala` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Administrador`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`Administrador` ;

CREATE TABLE IF NOT EXISTS `mydb`.`Administrador` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `CPF` VARCHAR(45) NOT NULL,
  `Senha` VARCHAR(45) NOT NULL,
  `Funcionário_ID` INT NULL,
  PRIMARY KEY (`ID`),
  INDEX `fk_Administrador_Funcionário1_idx` (`Funcionário_ID` ASC),
  CONSTRAINT `fk_Administrador_Funcionário1`
    FOREIGN KEY (`Funcionário_ID`)
    REFERENCES `mydb`.`Funcionário` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

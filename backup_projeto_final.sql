-- MySQL dump 10.13  Distrib 5.7.22, for Linux (x86_64)
--
-- Host: localhost    Database: mydb
-- ------------------------------------------------------
-- Server version	5.7.22-0ubuntu0.16.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Acessa`
--

DROP TABLE IF EXISTS `Acessa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Acessa` (
  `Acesso_ID` int(11) NOT NULL AUTO_INCREMENT,
  `Hora_entrada` datetime NOT NULL,
  `Hora_saida` datetime DEFAULT NULL,
  `Funcionario_ID` int(11) NOT NULL,
  `Sala_ID` int(11) NOT NULL,
  PRIMARY KEY (`Acesso_ID`),
  KEY `fk_Acessa_Sala1_idx` (`Sala_ID`),
  KEY `fk_Acessa_Funcionário1` (`Funcionario_ID`),
  CONSTRAINT `fk_Acessa_Funcionário1` FOREIGN KEY (`Funcionario_ID`) REFERENCES `Funcionario` (`ID`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_Acessa_Sala1` FOREIGN KEY (`Sala_ID`) REFERENCES `Sala` (`ID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Acessa`
--

LOCK TABLES `Acessa` WRITE;
/*!40000 ALTER TABLE `Acessa` DISABLE KEYS */;
/*!40000 ALTER TABLE `Acessa` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Administrador`
--

DROP TABLE IF EXISTS `Administrador`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Administrador` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `CPF` varchar(45) NOT NULL,
  `Senha` varchar(45) NOT NULL,
  `Funcionario_ID` int(11) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  KEY `fk_Administrador_Funcionário1_idx` (`Funcionario_ID`),
  CONSTRAINT `fk_Administrador_Funcionário1` FOREIGN KEY (`Funcionario_ID`) REFERENCES `Funcionario` (`ID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Administrador`
--

LOCK TABLES `Administrador` WRITE;
/*!40000 ALTER TABLE `Administrador` DISABLE KEYS */;
/*!40000 ALTER TABLE `Administrador` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Bancada`
--

DROP TABLE IF EXISTS `Bancada`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Bancada` (
  `ID` int(11) NOT NULL,
  `Tipo` varchar(45) NOT NULL,
  `Sala_ID` int(11) NOT NULL,
  `Ativo` tinyint(4) NOT NULL,
  PRIMARY KEY (`ID`,`Sala_ID`),
  KEY `fk_Bancada_Sala1_idx` (`Sala_ID`),
  CONSTRAINT `fk_Bancada_Sala1` FOREIGN KEY (`Sala_ID`) REFERENCES `Sala` (`ID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Bancada`
--

LOCK TABLES `Bancada` WRITE;
/*!40000 ALTER TABLE `Bancada` DISABLE KEYS */;
/*!40000 ALTER TABLE `Bancada` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Camera`
--

DROP TABLE IF EXISTS `Camera`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Camera` (
  `ID` int(11) NOT NULL,
  `IP` varchar(45) NOT NULL,
  `Modelo` varchar(45) NOT NULL,
  `Marca` varchar(45) NOT NULL,
  `Datasheet` varchar(45) DEFAULT NULL,
  `Sala_ID` int(11) NOT NULL,
  PRIMARY KEY (`ID`,`Sala_ID`),
  KEY `fk_Camera_Sala1_idx` (`Sala_ID`),
  CONSTRAINT `fk_Camera_Sala1` FOREIGN KEY (`Sala_ID`) REFERENCES `Sala` (`ID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Camera`
--

LOCK TABLES `Camera` WRITE;
/*!40000 ALTER TABLE `Camera` DISABLE KEYS */;
/*!40000 ALTER TABLE `Camera` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Funcionario`
--

DROP TABLE IF EXISTS `Funcionario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Funcionario` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Nome` varchar(256) NOT NULL,
  `Sobrenome` varchar(256) NOT NULL,
  `CPF` varchar(256) NOT NULL,
  `RG` varchar(256) NOT NULL,
  `DataNascimento` date NOT NULL,
  `Endereco` varchar(256) NOT NULL,
  `Sexo` varchar(256) NOT NULL,
  `data_admissao` date NOT NULL,
  `data_demissao` date DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Funcionario`
--

LOCK TABLES `Funcionario` WRITE;
/*!40000 ALTER TABLE `Funcionario` DISABLE KEYS */;
INSERT INTO `Funcionario` VALUES (1,'Leticia','Coelho','000','000','0001-02-01','R. Manoel duarte','fem','0555-05-22',NULL),(2,'Fernando','Muller','085.599.878.47','2.555.888','8854-12-20','Rua manoel duarte','Feminino','0055-01-20',NULL),(3,'José','Silva','888.888.888-88','5.555-55','5555-08-20','T. bfpspdasfmpf 2255','Feminino','2015-05-05',NULL),(4,'José','Silveira','025.346.642.21','4.236-952','1976-02-23','venida das Maracanãs  324 	Pedra Branca 	Palhoça/SC	88137-200','Masculino','1999-04-06',NULL),(5,'João','Figueiredo','069.348.285-12','7.348-964','1984-12-01','Avenida Gentil Reinaldo Cordioli 198	Passa Vinte 	Palhoça/SC	88133-300','Masculino','2001-04-01',NULL),(6,'Maria ','Soares','874.364.821.23','4.236-248','1989-12-23','Avenida Nelson Baltazar Schütz 347	Aririú 	Palhoça/SC	88135-202','Feminino','2004-08-05',NULL),(7,'Alda','Martins','651.348.341.66','5.348-679','1983-09-25','Rua Acendino Pedro da Silva 	Barra do Aririú 287	Palhoça/SC	88134-468','Feminino','1998-07-21','2018-12-20'),(8,'Antônio','Souza','478.348.218.08','5.975-612','1969-07-29','Rua Angra do Heroísmo 	São Sebastião 398	Palhoça/SC	88136-505','Masculino','1995-12-04',NULL),(9,'Maria ','Bernadete','214.367.975-75','9.247-621','1992-03-18','Rua Ariena 35	Passa Vinte 	Palhoça/SC	88132-276','Feminino','2016-03-03',NULL),(10,'Julia ','Santos','4875.3248.975-32','6.214-325','1991-09-12','Rua Bernardino Jacob May 347	Centro 	Palhoça/SC	88130-060','Feminino','2005-03-17',NULL),(11,'Caetano','Medeiros','842.397.324.95','3.785-642','1975-06-09','Rua Cândido Izidoro da Silva 348	Guarda do Cubatão 	Palhoça/SC	88135-353','Masculino','1990-04-12',NULL),(12,'Pedro','Carrara','876.321.875-92','9.475-324','1984-07-01','Rua Capri 83	Pagani 	Palhoça/SC	88132-229','Masculino','2002-05-01',NULL),(13,'Carlos','Dutra','034.675.314.22','9.178-314','1989-07-25','Rua Centáurea 384	Jardim Eldorado 	Palhoça/SC	88133-760','Masculino','2007-04-03',NULL),(14,'Cristian','Jacques','9875.247.632-66','6.247-612','1983-07-06','Rua Colégio Nossa Senhora de Fátima 278	Alto Aririú 	Palhoça/SC	88135-623','Masculino','2008-09-22',NULL),(15,'Carolina','Coelho','497.324.785-66','4.248-751','1994-04-23','Rua das Canelas 38	Madri 	Palhoça/SC	88136-310','Feminino','2014-04-25',NULL),(16,'Salete','Gomes','478.214.963-24','5.278-214','1987-04-22','Rua Capitão Euclides de Castro 38	Coqueiros 	Florianópolis/SC	88080-010','Feminino','2013-07-02',NULL),(17,'çç','ll','lll','ll','0021-02-21','oo','Masculino','0058-05-11',NULL);
/*!40000 ALTER TABLE `Funcionario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Sala`
--

DROP TABLE IF EXISTS `Sala`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Sala` (
  `ID` int(11) NOT NULL,
  `Nome` varchar(45) NOT NULL,
  `Ativo` tinyint(4) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Sala`
--

LOCK TABLES `Sala` WRITE;
/*!40000 ALTER TABLE `Sala` DISABLE KEYS */;
INSERT INTO `Sala` VALUES (211,'Sala um',1);
/*!40000 ALTER TABLE `Sala` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Utiliza`
--

DROP TABLE IF EXISTS `Utiliza`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Utiliza` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Hora_inicio` datetime NOT NULL,
  `Hora_fim` datetime DEFAULT NULL,
  `Funcionario_ID` int(11) NOT NULL,
  `Bancada_ID` int(11) NOT NULL,
  `Bancada_Sala_ID` int(11) NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `fk_Utiliza_Funcionário1_idx` (`Funcionario_ID`),
  KEY `fk_Utiliza_Bancada1_idx` (`Bancada_ID`,`Bancada_Sala_ID`),
  CONSTRAINT `fk_Utiliza_Bancada1` FOREIGN KEY (`Bancada_ID`, `Bancada_Sala_ID`) REFERENCES `Bancada` (`ID`, `Sala_ID`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_Utiliza_Funcionário1` FOREIGN KEY (`Funcionario_ID`) REFERENCES `Funcionario` (`ID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Utiliza`
--

LOCK TABLES `Utiliza` WRITE;
/*!40000 ALTER TABLE `Utiliza` DISABLE KEYS */;
/*!40000 ALTER TABLE `Utiliza` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-07-03 19:44:09

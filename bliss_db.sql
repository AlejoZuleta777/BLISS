-- MySQL dump 10.13  Distrib 8.0.46, for Win64 (x86_64)
--
-- Host: localhost    Database: bliss_db
-- ------------------------------------------------------
-- Server version	8.0.46

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `alerts`
--

DROP TABLE IF EXISTS `alerts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alerts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `unit_id` int NOT NULL,
  `lot_id` int DEFAULT NULL,
  `alert_type` varchar(80) COLLATE utf8mb4_unicode_ci NOT NULL,
  `title` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `message` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `alert_date` datetime NOT NULL,
  `status` enum('PENDIENTE','ATENDIDA') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'PENDIENTE',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `unit_id` (`unit_id`),
  KEY `lot_id` (`lot_id`),
  CONSTRAINT `alerts_ibfk_1` FOREIGN KEY (`unit_id`) REFERENCES `production_units` (`id`) ON DELETE CASCADE,
  CONSTRAINT `alerts_ibfk_2` FOREIGN KEY (`lot_id`) REFERENCES `animal_lots` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alerts`
--

LOCK TABLES `alerts` WRITE;
/*!40000 ALTER TABLE `alerts` DISABLE KEYS */;
/*!40000 ALTER TABLE `alerts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `animal_lots`
--

DROP TABLE IF EXISTS `animal_lots`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `animal_lots` (
  `id` int NOT NULL AUTO_INCREMENT,
  `unit_id` int NOT NULL,
  `species_id` int NOT NULL,
  `name` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `quantity` int NOT NULL DEFAULT '0',
  `entry_date` date NOT NULL,
  `status` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'ACTIVO',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `unit_id` (`unit_id`),
  KEY `species_id` (`species_id`),
  CONSTRAINT `animal_lots_ibfk_1` FOREIGN KEY (`unit_id`) REFERENCES `production_units` (`id`) ON DELETE CASCADE,
  CONSTRAINT `animal_lots_ibfk_2` FOREIGN KEY (`species_id`) REFERENCES `species` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `animal_lots`
--

LOCK TABLES `animal_lots` WRITE;
/*!40000 ALTER TABLE `animal_lots` DISABLE KEYS */;
INSERT INTO `animal_lots` VALUES (1,1,1,'Lote ebejico1',115,'2025-01-11','ACTIVO','2026-11-03 02:58:52'),(2,3,2,'Galpon #1',2000,'2026-10-01','ACTIVO','2026-11-18 23:46:38');
/*!40000 ALTER TABLE `animal_lots` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `expenses`
--

DROP TABLE IF EXISTS `expenses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `expenses` (
  `id` int NOT NULL AUTO_INCREMENT,
  `unit_id` int NOT NULL,
  `lot_id` int DEFAULT NULL,
  `concept` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `category` varchar(80) COLLATE utf8mb4_unicode_ci NOT NULL,
  `amount` decimal(14,2) NOT NULL,
  `expense_date` date NOT NULL,
  `description` text COLLATE utf8mb4_unicode_ci,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `unit_id` (`unit_id`),
  KEY `lot_id` (`lot_id`),
  CONSTRAINT `expenses_ibfk_1` FOREIGN KEY (`unit_id`) REFERENCES `production_units` (`id`) ON DELETE CASCADE,
  CONSTRAINT `expenses_ibfk_2` FOREIGN KEY (`lot_id`) REFERENCES `animal_lots` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `expenses`
--

LOCK TABLES `expenses` WRITE;
/*!40000 ALTER TABLE `expenses` DISABLE KEYS */;
INSERT INTO `expenses` VALUES (1,1,1,'Compra de vacunas ','Salud animal',3500000.00,'2026-10-28','Compras necesarias de medicamentos para la sostenibilidad de los animales ','2026-11-19 00:25:18');
/*!40000 ALTER TABLE `expenses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `feeding_records`
--

DROP TABLE IF EXISTS `feeding_records`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `feeding_records` (
  `id` int NOT NULL AUTO_INCREMENT,
  `lot_id` int NOT NULL,
  `feed_name` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `quantity` decimal(12,2) NOT NULL,
  `measurement_unit` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'kg',
  `unit_price` decimal(12,2) NOT NULL DEFAULT '0.00',
  `total_cost` decimal(12,2) NOT NULL DEFAULT '0.00',
  `feeding_date` date NOT NULL,
  `notes` text COLLATE utf8mb4_unicode_ci,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `lot_id` (`lot_id`),
  CONSTRAINT `feeding_records_ibfk_1` FOREIGN KEY (`lot_id`) REFERENCES `animal_lots` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `feeding_records`
--

LOCK TABLES `feeding_records` WRITE;
/*!40000 ALTER TABLE `feeding_records` DISABLE KEYS */;
INSERT INTO `feeding_records` VALUES (1,1,'Concentrado Bovino',20.00,'kg',4500.00,90000.00,'2026-11-11','Alimentación de prueba','2026-11-11 18:29:50'),(2,2,'Ponedoras',40.00,'kg',97000.00,3880000.00,'2026-10-01','Alimentación de la mañana','2026-11-18 23:54:41');
/*!40000 ALTER TABLE `feeding_records` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `health_events`
--

DROP TABLE IF EXISTS `health_events`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `health_events` (
  `id` int NOT NULL AUTO_INCREMENT,
  `lot_id` int NOT NULL,
  `event_type` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `product_used` varchar(120) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `event_date` date NOT NULL,
  `description` text COLLATE utf8mb4_unicode_ci,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `lot_id` (`lot_id`),
  CONSTRAINT `health_events_ibfk_1` FOREIGN KEY (`lot_id`) REFERENCES `animal_lots` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `health_events`
--

LOCK TABLES `health_events` WRITE;
/*!40000 ALTER TABLE `health_events` DISABLE KEYS */;
/*!40000 ALTER TABLE `health_events` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `incomes`
--

DROP TABLE IF EXISTS `incomes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `incomes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `unit_id` int NOT NULL,
  `lot_id` int DEFAULT NULL,
  `concept` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `amount` decimal(14,2) NOT NULL,
  `income_date` date NOT NULL,
  `description` text COLLATE utf8mb4_unicode_ci,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `unit_id` (`unit_id`),
  KEY `lot_id` (`lot_id`),
  CONSTRAINT `incomes_ibfk_1` FOREIGN KEY (`unit_id`) REFERENCES `production_units` (`id`) ON DELETE CASCADE,
  CONSTRAINT `incomes_ibfk_2` FOREIGN KEY (`lot_id`) REFERENCES `animal_lots` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `incomes`
--

LOCK TABLES `incomes` WRITE;
/*!40000 ALTER TABLE `incomes` DISABLE KEYS */;
INSERT INTO `incomes` VALUES (1,1,1,'Venta de huevos ',10000000.00,'2026-10-28','Venta en 2 semanas de producción ','2026-11-19 00:26:33'),(2,2,NULL,'venta de gallinas ',4000000.00,'2026-11-17','asdasda','2026-11-19 01:47:18');
/*!40000 ALTER TABLE `incomes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventory_items`
--

DROP TABLE IF EXISTS `inventory_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inventory_items` (
  `id` int NOT NULL AUTO_INCREMENT,
  `unit_id` int NOT NULL,
  `name` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `category` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'OTRO',
  `quantity` decimal(12,2) NOT NULL DEFAULT '0.00',
  `measurement_unit` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'unidad',
  `minimum_quantity` decimal(12,2) NOT NULL DEFAULT '0.00',
  `unit_cost` decimal(12,2) NOT NULL DEFAULT '0.00',
  `expiration_date` date DEFAULT NULL,
  `notes` text COLLATE utf8mb4_unicode_ci,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `unit_id` (`unit_id`),
  CONSTRAINT `inventory_items_ibfk_1` FOREIGN KEY (`unit_id`) REFERENCES `production_units` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventory_items`
--

LOCK TABLES `inventory_items` WRITE;
/*!40000 ALTER TABLE `inventory_items` DISABLE KEYS */;
INSERT INTO `inventory_items` VALUES (1,3,'Ponedoras','ALIMENTO',0.00,'kg',32.00,97.00,'2026-10-01',NULL,'2026-11-18 23:53:35'),(2,3,'Polinizador','ALIMENTO',60.00,'kg',34.00,10000.00,'2026-11-16',NULL,'2026-11-19 01:51:45');
/*!40000 ALTER TABLE `inventory_items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventory_movements`
--

DROP TABLE IF EXISTS `inventory_movements`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inventory_movements` (
  `id` int NOT NULL AUTO_INCREMENT,
  `item_id` int NOT NULL,
  `movement_type` enum('ENTRADA','SALIDA') COLLATE utf8mb4_unicode_ci NOT NULL,
  `quantity` decimal(12,2) NOT NULL,
  `notes` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `movement_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `item_id` (`item_id`),
  CONSTRAINT `inventory_movements_ibfk_1` FOREIGN KEY (`item_id`) REFERENCES `inventory_items` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventory_movements`
--

LOCK TABLES `inventory_movements` WRITE;
/*!40000 ALTER TABLE `inventory_movements` DISABLE KEYS */;
INSERT INTO `inventory_movements` VALUES (1,1,'SALIDA',40.00,'Consumo de alimentación - Lote: Galpon #1','2026-11-18 23:54:41');
/*!40000 ALTER TABLE `inventory_movements` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mortality_records`
--

DROP TABLE IF EXISTS `mortality_records`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mortality_records` (
  `id` int NOT NULL AUTO_INCREMENT,
  `lot_id` int NOT NULL,
  `quantity` int NOT NULL,
  `mortality_date` date NOT NULL,
  `reason` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `notes` text COLLATE utf8mb4_unicode_ci,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `lot_id` (`lot_id`),
  CONSTRAINT `mortality_records_ibfk_1` FOREIGN KEY (`lot_id`) REFERENCES `animal_lots` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mortality_records`
--

LOCK TABLES `mortality_records` WRITE;
/*!40000 ALTER TABLE `mortality_records` DISABLE KEYS */;
/*!40000 ALTER TABLE `mortality_records` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `production_records`
--

DROP TABLE IF EXISTS `production_records`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `production_records` (
  `id` int NOT NULL AUTO_INCREMENT,
  `lot_id` int NOT NULL,
  `quantity` decimal(12,2) NOT NULL,
  `measurement_unit` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'unidad',
  `production_date` date NOT NULL,
  `notes` text COLLATE utf8mb4_unicode_ci,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `lot_id` (`lot_id`),
  CONSTRAINT `production_records_ibfk_1` FOREIGN KEY (`lot_id`) REFERENCES `animal_lots` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `production_records`
--

LOCK TABLES `production_records` WRITE;
/*!40000 ALTER TABLE `production_records` DISABLE KEYS */;
INSERT INTO `production_records` VALUES (1,2,2000.00,'kg','2026-10-01','Producción de la mañana ','2026-11-18 23:56:20');
/*!40000 ALTER TABLE `production_records` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `production_units`
--

DROP TABLE IF EXISTS `production_units`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `production_units` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `name` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `production_type` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `location` varchar(180) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `production_units_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `production_units`
--

LOCK TABLES `production_units` WRITE;
/*!40000 ALTER TABLE `production_units` DISABLE KEYS */;
INSERT INTO `production_units` VALUES (1,1,'Finca BLISS Demo','GANADERIA','Medellín, Antioquia','2026-11-03 02:41:04'),(2,2,'Finca Productor B','AVICULTURA','ebejico','2026-11-03 03:22:46'),(3,4,'La clara','AVICULTURA','Ebejico,Antioquia','2026-11-18 23:44:53');
/*!40000 ALTER TABLE `production_units` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `scheduled_events`
--

DROP TABLE IF EXISTS `scheduled_events`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `scheduled_events` (
  `id` int NOT NULL AUTO_INCREMENT,
  `lot_id` int NOT NULL,
  `event_type` varchar(80) COLLATE utf8mb4_unicode_ci NOT NULL,
  `scheduled_date` date NOT NULL,
  `description` text COLLATE utf8mb4_unicode_ci,
  `status` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'PENDIENTE',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `lot_id` (`lot_id`),
  CONSTRAINT `scheduled_events_ibfk_1` FOREIGN KEY (`lot_id`) REFERENCES `animal_lots` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `scheduled_events`
--

LOCK TABLES `scheduled_events` WRITE;
/*!40000 ALTER TABLE `scheduled_events` DISABLE KEYS */;
/*!40000 ALTER TABLE `scheduled_events` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `species`
--

DROP TABLE IF EXISTS `species`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `species` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `production_type` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `species`
--

LOCK TABLES `species` WRITE;
/*!40000 ALTER TABLE `species` DISABLE KEYS */;
INSERT INTO `species` VALUES (1,'Bovinos','GANADERIA'),(2,'Aves','AVICULTURA'),(3,'Porcinos','PORCICULTURA'),(4,'Peces','PISCICULTURA'),(5,'Equinos','EQUINOS');
/*!40000 ALTER TABLE `species` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `full_name` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password_hash` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Alejandro zuleta','m.alejosz31@gmail.com','scrypt:32768:8:1$XGR9LEW8jYtlp3Fw$ecda0f74dccdedb983492be5d6e76b664ffdf02750b99dacb6a6e341ba39d48698b4773cfb930ef0c78f0713a4aec97d239c74676c409aaccd31f42aacccb14e','3015875308','2026-11-03 02:35:51'),(2,'Sebastian Rodriguez','sebas.r12@yahoo.com','scrypt:32768:8:1$pa34aoAw0rcnAm0u$feb9c5ebc51f5e36590d77230b8918e99cd59fa3e593026933537366bb65023f7720fc6bc447fccb73eaeab4b6d8646992d5b62ccac9a96400548869a6bcb108','3103523156','2026-11-03 03:20:30'),(3,'Alejandro Sanchez','m.alejosz311@gmail.com','scrypt:32768:8:1$e1gRmPQKQaXvOIIJ$76a67d283fff858ffe1ca31aef7a6fdf964adcaada69ac018772e21a85d650886482a34d5d42fa75799df3546f29bb41c4c47c3cb7ce9a44eb5af9537040e361','+573015875309','2026-11-18 23:40:00'),(4,'Sergio Ordoñez','sergioordo12@hotmail.com','scrypt:32768:8:1$evQeRKjfD4TPyiCe$503c9f0a6eab9dd600233179cc34c9efbff7665e3745d7568ea6d6017c1f3dea23f9cc1b14e852fea0d9bd095f4cff695706817469751ba95a98a73321d479eb','3147565789','2026-11-18 23:43:53'),(5,'Maicol sanchez','m.alejosz3112@gmail.com','scrypt:32768:8:1$q6EChR4aOD6iCQLb$e01ef984079d22ff20d182b4c25a0544bb4086b1d5abe5dc7de90286e96cef348e24137e1bcf4ea9a19b2f8715207373dc02be9a09e1e25ec08fdb748c0ab7ca','3147565789','2026-11-19 01:48:47');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-11-19 20:41:19

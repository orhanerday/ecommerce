-- Active: 1759683453608@@127.0.0.1@3306@ecommerce
-- MySQL dump 10.13  Distrib 9.4.0, for macos26.0 (arm64)
--
-- Host: 127.0.0.1    Database: ecommerce
-- ------------------------------------------------------
-- Server version	8.0.43

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
-- Table structure for table `customers`
--

DROP TABLE IF EXISTS `customers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customers` (
  `customer_id` char(36) NOT NULL,
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `wallet_balance` decimal(10,2) DEFAULT '5000.00',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`customer_id`),
  KEY `idx_customer_id` (`customer_id`),
  CONSTRAINT `check_wallet_balance_non_negative` CHECK ((`wallet_balance` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customers`
--

/*!40000 ALTER TABLE `customers` DISABLE KEYS */;
INSERT INTO `customers` VALUES ('43e8ff2f-5d48-498f-a569-ca2cf9f7fae3','string',99450.00,'2025-10-06 13:19:07','2025-10-06 14:05:31');
/*!40000 ALTER TABLE `customers` ENABLE KEYS */;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders` (
  `order_id` char(36) NOT NULL,
  `customer_id` char(36) NOT NULL,
  `product_id` char(36) NOT NULL,
  `price_paid` decimal(10,2) NOT NULL DEFAULT '0.00',
  `status` enum('PENDING','COMPLETED','FAILED','CANCELLED') DEFAULT 'PENDING',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`order_id`),
  KEY `idx_order_id` (`order_id`),
  KEY `customer_id` (`customer_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`customer_id`) ON DELETE RESTRICT,
  CONSTRAINT `orders_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
INSERT INTO `orders` VALUES ('02bbfb9e-ed60-4aaf-9c4a-738c4116ed39','43e8ff2f-5d48-498f-a569-ca2cf9f7fae3','a1b2c3d4-e5f6-7890-1234-567890abcdef',150.00,'FAILED','2025-10-06 13:45:53','2025-10-06 13:45:53'),('08dc9306-7a9a-48fd-9fc8-dce6571fd86b','43e8ff2f-5d48-498f-a569-ca2cf9f7fae3','a1b2c3d4-e5f6-7890-1234-567890abcdef',150.00,'FAILED','2025-10-06 13:46:53','2025-10-06 13:46:53'),('0f0df382-7f6b-4e18-b831-e645e7dd8254','43e8ff2f-5d48-498f-a569-ca2cf9f7fae3','a1b2c3d4-e5f6-7890-1234-567890abcdef',150.00,'FAILED','2025-10-06 13:46:53','2025-10-06 13:46:53'),('1c0adbc2-8350-45aa-a01d-cfeb31b85c28','43e8ff2f-5d48-498f-a569-ca2cf9f7fae3','a1b2c3d4-e5f6-7890-1234-567890abcdef',150.00,'FAILED','2025-10-06 13:46:53','2025-10-06 13:46:53'),('1cd5d377-3e75-4901-834b-3c4f84c1a731','43e8ff2f-5d48-498f-a569-ca2cf9f7fae3','a1b2c3d4-e5f6-7890-1234-567890abcdef',150.00,'CANCELLED','2025-10-06 13:47:26','2025-10-06 13:47:44'),('1eaa43ec-b1ef-4231-b4c2-b812882ceca1','43e8ff2f-5d48-498f-a569-ca2cf9f7fae3','a1b2c3d4-e5f6-7890-1234-567890abcdef',150.00,'FAILED','2025-10-06 13:46:53','2025-10-06 13:46:53'),('2a8ad668-6afe-47c5-bcb1-e48046dec281','43e8ff2f-5d48-498f-a569-ca2cf9f7fae3','a1b2c3d4-e5f6-7890-1234-567890abcdef',150.00,'COMPLETED','2025-10-06 13:45:53','2025-10-06 13:45:53'),('3ad9ef0d-bdff-44f7-be96-bc4e5dfec2ec','43e8ff2f-5d48-498f-a569-ca2cf9f7fae3','a1b2c3d4-e5f6-7890-1234-567890abcdef',150.00,'FAILED','2025-10-06 13:46:53','2025-10-06 13:46:53'),('3fa2906e-170d-4aec-a867-7566b7ff644a','43e8ff2f-5d48-498f-a569-ca2cf9f7fae3','a1b2c3d4-e5f6-7890-1234-567890abcdef',150.00,'CANCELLED','2025-10-06 13:47:59','2025-10-06 13:48:10'),('41a25c2b-b565-44cf-9d35-70cbac30398e','43e8ff2f-5d48-498f-a569-ca2cf9f7fae3','a1b2c3d4-e5f6-7890-1234-567890abcdef',150.00,'FAILED','2025-10-06 13:45:53','2025-10-06 13:45:53'),('4f5b8780-f8e6-4101-8156-7e10d72cffe0','43e8ff2f-5d48-498f-a569-ca2cf9f7fae3','a1b2c3d4-e5f6-7890-1234-567890abcdef',150.00,'CANCELLED','2025-10-06 14:05:43','2025-10-06 14:05:48'),('508164c0-5b4b-49e8-91b5-1bd30c63619a','43e8ff2f-5d48-498f-a569-ca2cf9f7fae3','a1b2c3d4-e5f6-7890-1234-567890abcdef',150.00,'FAILED','2025-10-06 13:45:53','2025-10-06 13:45:53'),('53bee918-9bbc-41c0-b567-9ee901d7cbcd','43e8ff2f-5d48-498f-a569-ca2cf9f7fae3','a1b2c3d4-e5f6-7890-1234-567890abcdef',150.00,'FAILED','2025-10-06 13:45:53','2025-10-06 13:45:53'),('57d9eee7-c7f1-4d14-b203-7de1d5485619','43e8ff2f-5d48-498f-a569-ca2cf9f7fae3','a1b2c3d4-e5f6-7890-1234-567890abcdef',150.00,'FAILED','2025-10-06 13:45:53','2025-10-06 13:45:53'),('71c88c73-0d01-4259-a6ba-b96807d65852','43e8ff2f-5d48-498f-a569-ca2cf9f7fae3','a1b2c3d4-e5f6-7890-1234-567890abcdef',150.00,'FAILED','2025-10-06 13:46:53','2025-10-06 13:46:53'),('751280f8-2905-4728-b78e-377781aaba54','43e8ff2f-5d48-498f-a569-ca2cf9f7fae3','a1b2c3d4-e5f6-7890-1234-567890abcdef',150.00,'FAILED','2025-10-06 13:46:53','2025-10-06 13:46:53'),('758d9e6f-90da-4d79-b90e-b905030dfd4e','43e8ff2f-5d48-498f-a569-ca2cf9f7fae3','a1b2c3d4-e5f6-7890-1234-567890abcdef',150.00,'FAILED','2025-10-06 13:45:53','2025-10-06 13:45:53'),('8554fe91-4def-48a1-bf33-ae918c98941d','43e8ff2f-5d48-498f-a569-ca2cf9f7fae3','a1b2c3d4-e5f6-7890-1234-567890abcdef',150.00,'FAILED','2025-10-06 13:45:53','2025-10-06 13:45:53'),('96161988-4a9b-4b8f-9515-e2c576237381','43e8ff2f-5d48-498f-a569-ca2cf9f7fae3','a1b2c3d4-e5f6-7890-1234-567890abcdef',150.00,'FAILED','2025-10-06 13:45:53','2025-10-06 13:45:53'),('9b4de64b-a94b-465e-befa-185c86aaad98','43e8ff2f-5d48-498f-a569-ca2cf9f7fae3','a1b2c3d4-e5f6-7890-1234-567890abcdef',150.00,'FAILED','2025-10-06 13:45:53','2025-10-06 13:45:53'),('9b619057-ded8-4c2c-bd5a-33d71fe89bdc','43e8ff2f-5d48-498f-a569-ca2cf9f7fae3','a1b2c3d4-e5f6-7890-1234-567890abcdef',150.00,'FAILED','2025-10-06 13:45:53','2025-10-06 13:45:53'),('a9b31279-a663-4af3-8006-4ccda4c1a846','43e8ff2f-5d48-498f-a569-ca2cf9f7fae3','a1b2c3d4-e5f6-7890-1234-567890abcdef',150.00,'FAILED','2025-10-06 13:46:53','2025-10-06 13:46:53'),('b0528574-8d4b-4835-89de-d45f35bb741e','43e8ff2f-5d48-498f-a569-ca2cf9f7fae3','a1b2c3d4-e5f6-7890-1234-567890abcdef',150.00,'FAILED','2025-10-06 13:46:53','2025-10-06 13:46:53'),('b260862c-3836-4735-b8f8-cc2efae850b1','43e8ff2f-5d48-498f-a569-ca2cf9f7fae3','a1b2c3d4-e5f6-7890-1234-567890abcdef',150.00,'FAILED','2025-10-06 13:45:53','2025-10-06 13:45:53'),('b4e77cb2-cb05-4490-944c-ff963c7133c2','43e8ff2f-5d48-498f-a569-ca2cf9f7fae3','a1b2c3d4-e5f6-7890-1234-567890abcdef',150.00,'FAILED','2025-10-06 13:46:53','2025-10-06 13:46:53'),('b7df13dd-4ad0-4b1b-a231-b4901e45de5e','43e8ff2f-5d48-498f-a569-ca2cf9f7fae3','a1b2c3d4-e5f6-7890-1234-567890abcdef',150.00,'FAILED','2025-10-06 13:46:53','2025-10-06 13:46:53'),('b840b103-08a2-4ceb-88e6-04f4aadcc465','43e8ff2f-5d48-498f-a569-ca2cf9f7fae3','a1b2c3d4-e5f6-7890-1234-567890abcdef',150.00,'FAILED','2025-10-06 13:46:53','2025-10-06 13:46:53'),('bedd299a-9ac7-46aa-b926-8f36c6632d10','43e8ff2f-5d48-498f-a569-ca2cf9f7fae3','a1b2c3d4-e5f6-7890-1234-567890abcdef',150.00,'FAILED','2025-10-06 13:45:53','2025-10-06 13:45:53'),('c37c5ae7-355a-4310-a6fc-b6ef46153c78','43e8ff2f-5d48-498f-a569-ca2cf9f7fae3','a1b2c3d4-e5f6-7890-1234-567890abcdef',150.00,'FAILED','2025-10-06 13:46:53','2025-10-06 13:46:53'),('cbca4dc2-480f-4e75-836f-be7319167d4a','43e8ff2f-5d48-498f-a569-ca2cf9f7fae3','a1b2c3d4-e5f6-7890-1234-567890abcdef',150.00,'FAILED','2025-10-06 13:45:53','2025-10-06 13:45:53'),('cea2f3de-8679-4d95-b43d-e1c090a789e1','43e8ff2f-5d48-498f-a569-ca2cf9f7fae3','a1b2c3d4-e5f6-7890-1234-567890abcdef',150.00,'FAILED','2025-10-06 13:45:53','2025-10-06 13:45:53'),('cfe03b59-34ca-4f91-8ba7-f135601a51c1','43e8ff2f-5d48-498f-a569-ca2cf9f7fae3','a1b2c3d4-e5f6-7890-1234-567890abcdef',150.00,'FAILED','2025-10-06 13:46:53','2025-10-06 13:46:53'),('d28e315c-ee63-4c8c-b492-05aaaeb1e56c','43e8ff2f-5d48-498f-a569-ca2cf9f7fae3','a1b2c3d4-e5f6-7890-1234-567890abcdef',150.00,'FAILED','2025-10-06 13:46:53','2025-10-06 13:46:53'),('d7d3b375-e239-4cc8-b2c5-24f11d242a4d','43e8ff2f-5d48-498f-a569-ca2cf9f7fae3','a1b2c3d4-e5f6-7890-1234-567890abcdef',150.00,'FAILED','2025-10-06 13:46:53','2025-10-06 13:46:53'),('ea01b887-cd3c-4a07-87f5-3ba6d2572d5f','43e8ff2f-5d48-498f-a569-ca2cf9f7fae3','a1b2c3d4-e5f6-7890-1234-567890abcdef',150.00,'FAILED','2025-10-06 13:46:53','2025-10-06 13:46:53'),('f334a3c8-d101-47cc-b7f2-fd4b41d6b071','43e8ff2f-5d48-498f-a569-ca2cf9f7fae3','a1b2c3d4-e5f6-7890-1234-567890abcdef',150.00,'FAILED','2025-10-06 13:45:53','2025-10-06 13:45:53'),('fba024a6-a50d-4b32-a1ae-e24f3c79159c','43e8ff2f-5d48-498f-a569-ca2cf9f7fae3','a1b2c3d4-e5f6-7890-1234-567890abcdef',150.00,'FAILED','2025-10-06 13:46:53','2025-10-06 13:46:53'),('fba58d90-dc29-4355-83d9-83d56b0bce61','43e8ff2f-5d48-498f-a569-ca2cf9f7fae3','a1b2c3d4-e5f6-7890-1234-567890abcdef',150.00,'FAILED','2025-10-06 13:46:53','2025-10-06 13:46:53');
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products` (
  `product_id` char(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `name` varchar(255) NOT NULL,
  `description` text,
  `base_price` decimal(10,2) NOT NULL,
  `stock` int NOT NULL DEFAULT '0',
  `initial_stock` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`product_id`),
  KEY `idx_product_id` (`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES ('a1b2c3d4-e5f6-7890-1234-567890abcdef','Quantum Laptop','A sleek, powerful laptop for all your computing needs.',100.00,1,100),('b2c3d4e5-f6a7-8901-2345-67890abcdef1','Galactic Smartphone','The latest smartphone with a stunning display and cosmic speed.',800.00,150,150),('c3d4e5f6-a7b8-9012-3456-7890abcdef12','Nebula Noise-Cancelling Headphones','Immerse yourself in sound. Blocks out distractions.',250.00,200,200),('d4e5f6a7-b8c9-0123-4567-890abcdef123','Ergonomic Starship Keyboard','Type comfortably for lightyears.',95.00,75,75);
/*!40000 ALTER TABLE `products` ENABLE KEYS */;

--
-- Dumping routines for database 'ecommerce'
--
--
-- WARNING: can't read the INFORMATION_SCHEMA.libraries table. It's most probably an old server 8.0.43.
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-10-06 17:15:35

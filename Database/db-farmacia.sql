-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1:3306
-- Tiempo de generación: 24-10-2024 a las 19:21:27
-- Versión del servidor: 8.3.0
-- Versión de PHP: 8.2.18

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `db-farmacia`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `buys`
--

DROP TABLE IF EXISTS `buys`;
CREATE TABLE IF NOT EXISTS `buys` (
  `folio` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `user_id` int NOT NULL,
  `iup_supplier` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `total` decimal(18,2) NOT NULL,
  `date` varchar(20) NOT NULL,
  PRIMARY KEY (`folio`),
  KEY `fk_users` (`user_id`),
  KEY `fk_supliers` (`iup_supplier`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `buys`
--

INSERT INTO `buys` (`folio`, `user_id`, `iup_supplier`, `total`, `date`) VALUES
('527119940474', 2, 'FGSIAAHBGYPEY01L', 13920.00, '23-10-2024'),
('661482946774', 2, '6GKE5AABJY6ACOMF', 5800.00, '23-10-2024');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `buy_register`
--

DROP TABLE IF EXISTS `buy_register`;
CREATE TABLE IF NOT EXISTS `buy_register` (
  `id` int NOT NULL AUTO_INCREMENT,
  `buy_suppliers_folio` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `upc_product` varchar(12) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `quantity` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_buy_suppliers` (`buy_suppliers_folio`),
  KEY `fk_products` (`upc_product`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `buy_register`
--

INSERT INTO `buy_register` (`id`, `buy_suppliers_folio`, `upc_product`, `quantity`) VALUES
(3, '527119940474', '225746509504', 12),
(4, '661482946774', '362921249708', 1000);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `clients`
--

DROP TABLE IF EXISTS `clients`;
CREATE TABLE IF NOT EXISTS `clients` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `email` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `points` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `clients`
--

INSERT INTO `clients` (`id`, `name`, `phone`, `email`, `points`) VALUES
(1, 'Jorge Alberto', '33 1262 8080', 'hola', 0),
(2, 'Lola', '3312628080', 'holamundogmail.com', 0),
(3, 'Puto negro', '+52 1234567890', 'puto@negro.nigga', 6);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `products`
--

DROP TABLE IF EXISTS `products`;
CREATE TABLE IF NOT EXISTS `products` (
  `upc` varchar(12) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `stock` int NOT NULL,
  `description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `price` decimal(18,2) NOT NULL,
  PRIMARY KEY (`upc`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `products`
--

INSERT INTO `products` (`upc`, `name`, `stock`, `description`, `price`) VALUES
('225746509504', 'Chilito', 12, 'ta chiquito', 1000.00),
('228128318951', 'Chachitos', 50, 'Cereal de arroz inflado', 15.00),
('362921249708', 'Halls', 0, 'Pastillas de caramelo', 5.00),
('533406192047', 'Chiles Jalapeños', 23, 'Chiles en escabeche', 2.00),
('628452046737', 'Pelon Pelo', 0, 'Dulce de tamarindo', 20.00);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `sales`
--

DROP TABLE IF EXISTS `sales`;
CREATE TABLE IF NOT EXISTS `sales` (
  `folio` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `client_id` int NOT NULL,
  `user_id` int NOT NULL,
  `date` varchar(20) NOT NULL,
  `total` decimal(18,2) NOT NULL,
  PRIMARY KEY (`folio`),
  KEY `client_fk` (`client_id`),
  KEY `user_fk` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `sales`
--

INSERT INTO `sales` (`folio`, `client_id`, `user_id`, `date`, `total`) VALUES
('933425819047', 3, 2, '23-10-2024', 5800.00),
('972747688449', 2, 2, '0000-00-00 00:00:00', 348.00);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `sales_register`
--

DROP TABLE IF EXISTS `sales_register`;
CREATE TABLE IF NOT EXISTS `sales_register` (
  `id` int NOT NULL AUTO_INCREMENT,
  `folio_venta` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `upc_product` varchar(12) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `quantity` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `sale_fk` (`folio_venta`),
  KEY `product_fk` (`upc_product`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `sales_register`
--

INSERT INTO `sales_register` (`id`, `folio_venta`, `upc_product`, `quantity`) VALUES
(2, '933425819047', '362921249708', 1000);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `suppliers`
--

DROP TABLE IF EXISTS `suppliers`;
CREATE TABLE IF NOT EXISTS `suppliers` (
  `iup` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `companyName` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`iup`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `suppliers`
--

INSERT INTO `suppliers` (`iup`, `companyName`) VALUES
('6GKE5AABJY6ACOMF', 'A la chingada'),
('FGSIAAHBGYPEY01L', 'Gorditas Calientes'),
('HL0TMSEFU40VDZLN', 'Cannel\'s');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `username` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `password` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `profile` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `users`
--

INSERT INTO `users` (`id`, `name`, `username`, `password`, `profile`) VALUES
(2, 'Pedro', 'pedrito', '1234', 'Admin'),
(3, 'Jose', 'pato', 'MareaAlta5', 'Cajero'),
(4, 'Bocchi la piedra', 'bocchi', 'Bocchi69@', 'Cajero');

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `buys`
--
ALTER TABLE `buys`
  ADD CONSTRAINT `fk_buy_suppliers_suppliers` FOREIGN KEY (`iup_supplier`) REFERENCES `suppliers` (`iup`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_buy_suppliers_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `buy_register`
--
ALTER TABLE `buy_register`
  ADD CONSTRAINT `buy_register_ibfk_1` FOREIGN KEY (`upc_product`) REFERENCES `products` (`upc`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_buy_register_buy_suppliers` FOREIGN KEY (`buy_suppliers_folio`) REFERENCES `buys` (`folio`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `sales`
--
ALTER TABLE `sales`
  ADD CONSTRAINT `fk_sale_client` FOREIGN KEY (`client_id`) REFERENCES `clients` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_sale_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `sales_register`
--
ALTER TABLE `sales_register`
  ADD CONSTRAINT `fk_sales_register_products` FOREIGN KEY (`upc_product`) REFERENCES `products` (`upc`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_sales_register_sales` FOREIGN KEY (`folio_venta`) REFERENCES `sales` (`folio`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

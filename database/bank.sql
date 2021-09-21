-- phpMyAdmin SQL Dump
-- version 5.1.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Aug 20, 2021 at 08:33 PM
-- Server version: 10.4.18-MariaDB
-- PHP Version: 7.3.27

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `esport_shop`
--

-- --------------------------------------------------------

--
-- Table structure for table `bank`
--

CREATE TABLE `bank` (
  `id` bigint(20) NOT NULL,
  `bank_name` varchar(255) NOT NULL,
  `bank_name_account` varchar(255) NOT NULL,
  `bank_number` varchar(255) NOT NULL,
  `bank_telephone` varchar(255) NOT NULL,
  `bank_image` varchar(100) DEFAULT NULL,
  `active` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `bank`
--

INSERT INTO `bank` (`id`, `bank_name`, `bank_name_account`, `bank_number`, `bank_telephone`, `bank_image`, `active`) VALUES
(1, 'ธนาคารกรสิกรไทย', 'นายพัชรพล ฟองสมุทร์', 'xxxx-xxxxx-xxxxx', '-', 'bank/kbank.png', 0),
(2, 'ธนาคารไทยพาณิชย์', 'นายพัชรพล ฟองสมุทร์', 'xxxx-xxxxx-xxxxx', '-', 'bank/scb.png', 0),
(3, 'ทรูมันนี่วอเล็ต', 'นายพัชรพล ฟองสมุทร์', '-', '098-585-6195', 'bank/truemoney.png', 0);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `bank`
--
ALTER TABLE `bank`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `bank`
--
ALTER TABLE `bank`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

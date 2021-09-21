-- phpMyAdmin SQL Dump
-- version 5.1.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Aug 20, 2021 at 08:35 PM
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
-- Table structure for table `store_provinces`
--

CREATE TABLE `store_provinces` (
  `id` bigint(20) NOT NULL,
  `code` varchar(4) NOT NULL,
  `name_th` varchar(150) NOT NULL,
  `name_en` varchar(150) NOT NULL,
  `geography_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `store_provinces`
--

INSERT INTO `store_provinces` (`id`, `code`, `name_th`, `name_en`, `geography_id`) VALUES
(1, '10', 'กรุงเทพมหานคร', 'Bangkok', 2),
(2, '11', 'สมุทรปราการ', 'Samut Prakan', 2),
(3, '12', 'นนทบุรี', 'Nonthaburi', 2),
(4, '13', 'ปทุมธานี', 'Pathum Thani', 2),
(5, '14', 'พระนครศรีอยุธยา', 'Phra Nakhon Si Ayutthaya', 2),
(6, '15', 'อ่างทอง', 'Ang Thong', 2),
(7, '16', 'ลพบุรี', 'Loburi', 2),
(8, '17', 'สิงห์บุรี', 'Sing Buri', 2),
(9, '18', 'ชัยนาท', 'Chai Nat', 2),
(10, '19', 'สระบุรี', 'Saraburi', 2),
(11, '20', 'ชลบุรี', 'Chon Buri', 5),
(12, '21', 'ระยอง', 'Rayong', 5),
(13, '22', 'จันทบุรี', 'Chanthaburi', 5),
(14, '23', 'ตราด', 'Trat', 5),
(15, '24', 'ฉะเชิงเทรา', 'Chachoengsao', 5),
(16, '25', 'ปราจีนบุรี', 'Prachin Buri', 5),
(17, '26', 'นครนายก', 'Nakhon Nayok', 2),
(18, '27', 'สระแก้ว', 'Sa Kaeo', 5),
(19, '30', 'นครราชสีมา', 'Nakhon Ratchasima', 3),
(20, '31', 'บุรีรัมย์', 'Buri Ram', 3),
(21, '32', 'สุรินทร์', 'Surin', 3),
(22, '33', 'ศรีสะเกษ', 'Si Sa Ket', 3),
(23, '34', 'อุบลราชธานี', 'Ubon Ratchathani', 3),
(24, '35', 'ยโสธร', 'Yasothon', 3),
(25, '36', 'ชัยภูมิ', 'Chaiyaphum', 3),
(26, '37', 'อำนาจเจริญ', 'Amnat Charoen', 3),
(27, '39', 'หนองบัวลำภู', 'Nong Bua Lam Phu', 3),
(28, '40', 'ขอนแก่น', 'Khon Kaen', 3),
(29, '41', 'อุดรธานี', 'Udon Thani', 3),
(30, '42', 'เลย', 'Loei', 3),
(31, '43', 'หนองคาย', 'Nong Khai', 3),
(32, '44', 'มหาสารคาม', 'Maha Sarakham', 3),
(33, '45', 'ร้อยเอ็ด', 'Roi Et', 3),
(34, '46', 'กาฬสินธุ์', 'Kalasin', 3),
(35, '47', 'สกลนคร', 'Sakon Nakhon', 3),
(36, '48', 'นครพนม', 'Nakhon Phanom', 3),
(37, '49', 'มุกดาหาร', 'Mukdahan', 3),
(38, '50', 'เชียงใหม่', 'Chiang Mai', 1),
(39, '51', 'ลำพูน', 'Lamphun', 1),
(40, '52', 'ลำปาง', 'Lampang', 1),
(41, '53', 'อุตรดิตถ์', 'Uttaradit', 1),
(42, '54', 'แพร่', 'Phrae', 1),
(43, '55', 'น่าน', 'Nan', 1),
(44, '56', 'พะเยา', 'Phayao', 1),
(45, '57', 'เชียงราย', 'Chiang Rai', 1),
(46, '58', 'แม่ฮ่องสอน', 'Mae Hong Son', 1),
(47, '60', 'นครสวรรค์', 'Nakhon Sawan', 2),
(48, '61', 'อุทัยธานี', 'Uthai Thani', 2),
(49, '62', 'กำแพงเพชร', 'Kamphaeng Phet', 2),
(50, '63', 'ตาก', 'Tak', 4),
(51, '64', 'สุโขทัย', 'Sukhothai', 2),
(52, '65', 'พิษณุโลก', 'Phitsanulok', 2),
(53, '66', 'พิจิตร', 'Phichit', 2),
(54, '67', 'เพชรบูรณ์', 'Phetchabun', 2),
(55, '70', 'ราชบุรี', 'Ratchaburi', 4),
(56, '71', 'กาญจนบุรี', 'Kanchanaburi', 4),
(57, '72', 'สุพรรณบุรี', 'Suphan Buri', 2),
(58, '73', 'นครปฐม', 'Nakhon Pathom', 2),
(59, '74', 'สมุทรสาคร', 'Samut Sakhon', 2),
(60, '75', 'สมุทรสงคราม', 'Samut Songkhram', 2),
(61, '76', 'เพชรบุรี', 'Phetchaburi', 4),
(62, '77', 'ประจวบคีรีขันธ์', 'Prachuap Khiri Khan', 4),
(63, '80', 'นครศรีธรรมราช', 'Nakhon Si Thammarat', 6),
(64, '81', 'กระบี่', 'Krabi', 6),
(65, '82', 'พังงา', 'Phangnga', 6),
(66, '83', 'ภูเก็ต', 'Phuket', 6),
(67, '84', 'สุราษฎร์ธานี', 'Surat Thani', 6),
(68, '85', 'ระนอง', 'Ranong', 6),
(69, '86', 'ชุมพร', 'Chumphon', 6),
(70, '90', 'สงขลา', 'Songkhla', 6),
(71, '91', 'สตูล', 'Satun', 6),
(72, '92', 'ตรัง', 'Trang', 6),
(73, '93', 'พัทลุง', 'Phatthalung', 6),
(74, '94', 'ปัตตานี', 'Pattani', 6),
(75, '95', 'ยะลา', 'Yala', 6),
(76, '96', 'นราธิวาส', 'Narathiwat', 6),
(77, '97', 'บึงกาฬ', 'buogkan', 3);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `store_provinces`
--
ALTER TABLE `store_provinces`
  ADD PRIMARY KEY (`id`),
  ADD KEY `store_provinces_geography_id_7ac91159_fk_store_geographies_id` (`geography_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `store_provinces`
--
ALTER TABLE `store_provinces`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=78;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `store_provinces`
--
ALTER TABLE `store_provinces`
  ADD CONSTRAINT `store_provinces_geography_id_7ac91159_fk_store_geographies_id` FOREIGN KEY (`geography_id`) REFERENCES `store_geographies` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

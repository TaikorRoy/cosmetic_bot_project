-- phpMyAdmin SQL Dump
-- version 4.3.11
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: 2015-06-10 12:36:32
-- 服务器版本： 5.6.24
-- PHP Version: 5.5.24

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `sku`
--

-- --------------------------------------------------------

--
-- 表的结构 `sku`
--

CREATE TABLE IF NOT EXISTS `sku` (
  `sku` char(11) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `sku_name` char(80) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `product_name` char(80) CHARACTER SET utf8 NOT NULL,
  `product_category` int(2) NOT NULL,
  `brand` char(50) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `size` char(20) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- 转存表中的数据 `sku`
--

INSERT INTO `sku` (`sku`, `sku_name`, `product_name`, `product_category`, `brand`, `size`) VALUES
('aa', '娇兰水合青春活能精华露', '娇兰水合青春活能精华露', 1, '娇兰', '0'),
('aaa', '娇兰赋妍紧致修复精华油(黄金复原蜜)', '娇兰赋妍紧致修复精华油(黄金复原蜜)', 1, '娇兰', '0');

-- --------------------------------------------------------

--
-- 表的结构 `skuprice`
--

CREATE TABLE IF NOT EXISTS `skuprice` (
  `sku_name` char(80) COLLATE utf8_unicode_ci NOT NULL,
  `B2C_platform` int(2) NOT NULL,
  `vendor_url` char(255) COLLATE utf8_unicode_ci NOT NULL,
  `scrapping_time` int(11) NOT NULL,
  `source_name` char(80) COLLATE utf8_unicode_ci NOT NULL,
  `price` int(6) NOT NULL,
  `sales_volume` int(6) NOT NULL,
  `comments` int(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- 转存表中的数据 `skuprice`
--

INSERT INTO `skuprice` (`sku_name`, `B2C_platform`, `vendor_url`, `scrapping_time`, `source_name`, `price`, `sales_volume`, `comments`) VALUES
('aaa', 1, 'aaa', 1, 'aaa', 1, 1, 1),
('娇兰水合青春活能精华露', 0, 'http://item.jd.com/1178120570.html', 1433756419, 'Guerlain娇兰水合青春活能精华露5ml', 65, -999, 0),
('娇兰赋妍紧致修复精华油(黄金复原蜜)', 1, 'http://item.jd.com/1543334729.html', 1433756419, '娇兰(Guerlain)赋妍紧致修复精华油(黄金复原蜜)28ML', 880, -999, 0);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `sku`
--
ALTER TABLE `sku`
  ADD PRIMARY KEY (`sku_name`);

--
-- Indexes for table `skuprice`
--
ALTER TABLE `skuprice`
  ADD PRIMARY KEY (`sku_name`,`B2C_platform`,`vendor_url`,`scrapping_time`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

# ************************************************************
# Sequel Pro SQL dump
# Version 4541
#
# http://www.sequelpro.com/
# https://github.com/sequelpro/sequelpro
#
# Host: 127.0.0.1 (MySQL 5.5.37-0ubuntu0.12.10.1)
# Database: cardData
# Generation Time: 2017-01-10 17:02:14 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table blacklist
# ------------------------------------------------------------

DROP TABLE IF EXISTS `blacklist`;

CREATE TABLE `blacklist` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `studentID` varchar(15) NOT NULL DEFAULT '',
  `chapterID` int(11) DEFAULT NULL,
  `time_stamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `blacklisted` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_to_chapter` (`studentID`,`chapterID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



# Dump of table chapters
# ------------------------------------------------------------

DROP TABLE IF EXISTS `chapters`;

CREATE TABLE `chapters` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` text,
  `short_name` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



# Dump of table dataList
# ------------------------------------------------------------

DROP TABLE IF EXISTS `dataList`;

CREATE TABLE `dataList` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` text,
  `studentID` text,
  `card_text` text,
  `time_stamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `userID` int(11) DEFAULT '0',
  `chapterID` int(11) DEFAULT '9',
  `eventID` int(11) DEFAULT '9',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



# Dump of table events
# ------------------------------------------------------------

DROP TABLE IF EXISTS `events`;

CREATE TABLE `events` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` text NOT NULL,
  `chapterID` int(11) NOT NULL,
  `time_stamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



# Dump of table users
# ------------------------------------------------------------

DROP TABLE IF EXISTS `users`;

CREATE TABLE `users` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `email` text,
  `password` text,
  `chapterID` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;




/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

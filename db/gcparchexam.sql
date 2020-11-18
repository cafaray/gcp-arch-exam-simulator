DROP DATABASE IF EXISTS `gcparchexam`;
CREATE DATABASE `gcparchexam` DEFAULT CHARACTER SET 'utf8';
USE `gcparchexam`

CREATE TABLE `topics` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `description` varchar(200) NOT NULL,
  `file` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;

CREATE TABLE `questions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `question` varchar(2000) NOT NULL,
  `explanation` varchar(2000) DEFAULT '',
  `idtopic` int(11) NOT NULL,
  `used` int(11) DEFAULT '0',
  PRIMARY KEY (`id`),
  FOREIGN KEY (idtopic) REFERENCES topics(id)
) ENGINE=InnoDB AUTO_INCREMENT=1259 DEFAULT CHARSET=utf8;

CREATE TABLE `options` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `idquestion` int(11) NOT NULL,
  `qoption` varchar(1) NOT NULL,
  `description` varchar(2000) NOT NULL,
  `is_right` int(11) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `idquestion` (`idquestion`),
  CONSTRAINT `options_ibfk_1` FOREIGN KEY (`idquestion`) REFERENCES `questions` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=866 DEFAULT CHARSET=utf8;

CREATE TABLE `simulations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `result` int(11) DEFAULT NULL,
  `startAt` datetime NOT NULL,
  `endAt` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8;

CREATE TABLE `simulation` (
  `idsimulation` int(11) NOT NULL,
  `idquestion` int(11) NOT NULL,
  `selected1` varchar(1) DEFAULT NULL,
  `selected2` varchar(1) DEFAULT NULL,
  `selected3` varchar(1) DEFAULT NULL,
  `selected4` varchar(1) DEFAULT NULL,
  `evaluation` int(11) DEFAULT '0',
  PRIMARY KEY (`idsimulation`,`idquestion`),
  KEY `idquestion` (`idquestion`),
  CONSTRAINT `simulation_ibfk_1` FOREIGN KEY (`idsimulation`) REFERENCES `simulations` (`id`),
  CONSTRAINT `simulation_ibfk_2` FOREIGN KEY (`idquestion`) REFERENCES `questions` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


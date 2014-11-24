CREATE DATABASE bookstore;
USE bookstore;

--
-- Table structure for table `achat`
--
drop table achat;
CREATE TABLE IF NOT EXISTS `achat` (
  `UserID` int(11) DEFAULT NULL,
  `LivreID` int(11) DEFAULT NULL,
  `DateAchat` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  KEY `UserID` (`UserID`),
  KEY `LivreID` (`LivreID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `emprunt`
--
drop table emprunt;
CREATE TABLE IF NOT EXISTS `emprunt` (
  `UserID` int(11) NOT NULL,
  `LivreID` int(11) NOT NULL,
  `DateEmprunt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `DateRetour` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  KEY `UserID` (`UserID`),
  KEY `LivreID` (`LivreID`)
);

--
-- Table structure for table `livre`
--
drop table livre;
CREATE TABLE IF NOT EXISTS `livre` (
  `ISBN` varchar(255) NOT NULL UNIQUE,
  `titre` varchar(255) NOT NULL,
  `auteur` varchar(255) NOT NULL,
  `nombrePage` int(11) NOT NULL,
  `prix` int(11) NOT NULL,
  `categorie` varchar(255) NOT NULL,
  `rating` int(11) NOT NULL,
  `datePublication` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`ISBN`)
);

INSERT INTO livre (ISBN,titre,auteur,nombrePage,prix,categorie,rating,datePublication)
VALUES(
  'SWAG69',
  'Kappa',
  'Twitchchat',
  69,
  666,
  'autism',
  9,
  '2005-10-30 T 10:45'
);

INSERT INTO livre (ISBN,titre,auteur,nombrePage,prix,categorie,rating,datePublication)
VALUES(
  'SWAG67',
  'Kappafdf',
  'Twitchdddt',
  6978,
  '623',
  'aurore',
  2,
  '2005-10-30 T 10:45'
);

-- --------------------------------------------------------

-- --------------------------------------------------------

--
-- Table structure for table `reservation`
--
drop table reservation;
CREATE TABLE IF NOT EXISTS `reservation` (
  `Type` varchar(255) NOT NULL,
  `UserID` int(11) NOT NULL,
  `LivreID` int(11) NOT NULL,
  KEY `UserID` (`UserID`),
  KEY `LivreID` (`LivreID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

-- --------------------------------------------------------

--
-- Table structure for table `reservation`
--
drop table reservation;
CREATE TABLE IF NOT EXISTS `reservation` (
  `Type` varchar(255) NOT NULL,
  `UserID` int(11) NOT NULL,
  `LivreID` int(11) NOT NULL,
  KEY `UserID` (`UserID`),
  KEY `LivreID` (`LivreID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `user`
--
drop table user;
CREATE TABLE IF NOT EXISTS `user` (
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `nom` varchar(255) NOT NULL,
  `prenom` varchar(255) NOT NULL,
  `courriel` varchar(255) NOT NULL,
  `codePostal` varchar(255) NOT NULL,
  `adresse` varchar(255) NOT NULL,
  `permission` int(11) NOT NULL,
  `dette` double NOT NULL,
  PRIMARY KEY (`username`)
);

INSERT INTO user (username,password,nom,prenom,courriel,codePostal,adresse,permission,dette)
VALUES(
  'bob',
  'bob',
  'Bobe',
  'PrenomBob',
  'bob@bob.bob',
  'B0Bbb0',
  '123 bob rue bob',
  1,
  0
);

INSERT INTO user (username,password,nom,prenom,courriel,codePostal,adresse,permission,dette)
VALUES(
  'mich888',
  'chelmi',
  'Dufous',
  'Michel',
  'michel@everest.com',
  'MSMSMSMDF',
  '123 rue michel',
  1,
  0
);

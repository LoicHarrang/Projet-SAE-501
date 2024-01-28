CREATE TABLE `comptes` (
  `login` varchar(17) DEFAULT NULL,
  `password` varchar(7) DEFAULT NULL,
  `statut` varchar(14) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `comptes` VALUES ('mathys@admin.fr','mathys','administrateur'),('quentin@admin.fr','quentin','administrateur'),('jean@client.fr','jean','utilisateur'),('abigail@client.fr','abigail','utilisateur'),('loic@client.fr','loic','administrateur'),('damien@client.fr','damien','utilisateur'),('leo@client.fr','leo','utilisateur'),('astrid@client.fr','astrid','utilisateur');
UNLOCK TABLES;
-- Insert data into Fournisseur table
INSERT INTO Fournisseur (NomFournisseur, AdresseFournisseur) VALUES
  ('Poufsouffle', '10 Rue de la Gerbe, Lyon'),
  ('Hedwige', '46 Rue de La Paix'),
  ('Harry Potté', '14 Rue Au Pays Des Bisounours'),
  ('Sparta-300', '17 Rue des eaux profondes'),
  ('La taverne', '17 Rue de Poudlard'),
  ('Retour vers le passé', '78 Rue de Belle Avenue'),
  ('Guns n'' computers', '45 Avenue de l''Inde'),
  ('Panterré', '27 Rue Ferme d''Eden'),
  ('Froidjeu', '44 Avenue de Gotham City'),
  ('Harry Potté', '14 Rue Au Pays Des Bisounours'),
  ('Shrekous', '10 Rue des zabeilles');

-- Insert data into Materiel table
INSERT INTO Materiel (Type_mat, Marque, Description, Image) VALUES
  ('serveur', 'CDiscout', 'Gros serveur pour les petites randos', 'ciscout.png'),
  ('serveur', 'HPé', 'Gros serveur for vos petits services', 'serveur_hpe.png'),
  ('portable', 'ArubatMan', 'Un câble qui vous aidera dans vos sorties nocturnes', 'arubatman.png'),
  ('écran', 'Zamzung', 'Un zuber écran pour vou zaccombagner', 'zamzung_ecran.png'),
  ('accessoire', 'Leroy Merlin l''enchanté', 'Une lumière pour émerveiller vos nuits', 'kaamelott.png'),
  ('portable', 'SAcer Aqua', 'SAcer Taylor Swift 3, PC puissant, pas cher', 'taylor_swift.png'),
  ('portable', 'Lenoveau', 'Un pc portable pour tous vos besoins à la ferme', 'lenoveau.png'),
  ('portable', 'DellPhine', 'Belle machine avec une caméra haute définition pour vos besoins de création', 'belle_delphine.png'),
  ('serveur', 'Apache', 'Une relique du monde ancien des Indiens d''Amérique', 'apache.png'),
  ('portable', 'Dell', 'Dell Latitude 5290 - Windows 10', 'dell.png'),
  ('serveur', 'Haribou', 'Pour les grands et les petits', 'image.png'),
  ('serveur', 'Haribou', 'Pour tout le monde', 'image.png');

-- Insert data into Propose table
INSERT INTO Propose (NoMateriel, NoFournisseur, Prix) VALUES
  (2, 3, 650.0),
  (3, 2, 3.5),
  (4, 11, 150.0),
  (6, 4, 450.0),
  (5, 9, 2.0),
  (8, 6, 500.0),
  (9, 7, 545.0),
  (7, 8, 750.0),
  (10, 6, 685.0),
  (1, 9, 273.0),
  (11, 4, 72.0),
  (12, 3, 72.0);

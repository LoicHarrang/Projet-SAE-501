CREATE TABLE Fournisseur (
  NoFournisseur SERIAL PRIMARY KEY,
  NomFournisseur TEXT NOT NULL,
  AdresseFournisseur TEXT NOT NULL
);

CREATE TABLE Materiel (
  NoMateriel SERIAL PRIMARY KEY,
  Type_mat TEXT NOT NULL CHECK (Type_mat IN ('portable', 'serveur', 'accessoire', 'station', 'écran')),
  Marque TEXT NOT NULL,
  Description TEXT NOT NULL,
  Image TEXT NOT NULL
);

CREATE TABLE Propose (
  NoMateriel INTEGER NOT NULL,
  NoFournisseur INTEGER NOT NULL,
  Prix NUMERIC NOT NULL,
  PRIMARY KEY (NoMateriel, NoFournisseur),
  FOREIGN KEY (NoMateriel) REFERENCES Materiel(NoMateriel) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (NoFournisseur) REFERENCES Fournisseur(NoFournisseur) ON DELETE CASCADE ON UPDATE CASCADE
);

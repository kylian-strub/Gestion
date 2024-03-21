-- Suppression des tables --
# sujet 7 : reparation / type_reparation          **
DROP TABLE IF EXISTS Type_reparation;
DROP TABLE IF EXISTS Reparation;


CREATE TABLE Type_reparation(
    id_type INT AUTO_INCREMENT,
    libelle_type VARCHAR(50),
    logo VARCHAR(100),
    PRIMARY KEY(id_type)
);

CREATE TABLE Reparation(
    id_reparation INT AUTO_INCREMENT,
    libelle_reparation VARCHAR(50),
    immat_voiture VARCHAR(50),
    prix_reparation NUMERIC(8,2),
    date_reparation DATE,
    type_reparation_id  INT NOT NULL,
    photo VARCHAR(50),
    PRIMARY KEY(id_reparation),
    FOREIGN KEY(type_reparation_id) REFERENCES type_reparation(id_type) ON DELETE CASCADE);

# sujet 7 : reparation / type_reparation          **

INSERT INTO Type_reparation(id_type, libelle_type, logo) VALUES
 (NULL, 'entretien', 'logo_entretien.png'),
 (NULL, 'carrosserie', 'logo_entretien.png'),
 (NULL, 'mecanique', 'logo_entretien.png'),
 (NULL, 'autre', 'logo_autre.png');

INSERT INTO Reparation(id_reparation,libelle_reparation,immat_voiture,prix_reparation,date_reparation,type_reparation_id,photo) VALUES
(NULL,'Vidange','RP-456-ZF','50','2014-10-15',1,'intervention_1.png'),
(NULL,'Vidange','HK-856-SN','89','2005-05-06',1,'intervention_1.png'),
(NULL,'Vidange','SD-479-EG','57','2007-08-08',1,'intervention_1.png'),
(NULL,'Vidange','KU-458-VX','68','2007-04-13',1,'intervention_1.png'),
(NULL,'Remplac. pare brise','LY-228-EY','250.00','2003-12-30',2,'intervention_2.png'),
(NULL,'Remplac. pare brise','DS-865-KT','175.65','2011-05-06',2,'intervention_2.png'),
(NULL,'révision','XG-554-DD','100','2010-03-01',1,'intervention_3.png'),
(NULL,'révision','JK-103-DG','90','2001-05-06',1,'intervention_3.png'),
(NULL,'Changement pneus','KU-458-VX','30.54','2007-04-13',1,'intervention_4.png'),
(NULL,'Changement pneus','LY-228-EY','224.21','2009-12-30',1,'intervention_4.png'),
(NULL,'Changement pneus','DS-865-KT','227.00','2011-05-06',1,'intervention_4.png'),
(NULL,'Remplacement plaq. de frein','XG-554-DD','150','2010-03-01',1,'intervention_5.png'),
(NULL,'Tambour freins arr.','CD-665-GZ','180','2012-05-06',3,'intervention_6.png'),
(NULL,'Remplacement plaq. de frein','KU-458-VX','100','2007-04-13',1,'intervention_5.png'),
(NULL,'Changement des cardans','LY-228-EY','1300','2009-12-30',3,'intervention_6.png'),
(NULL,'Changement boite de vitesse','DS-865-KT','1400','2011-05-06',3,'intervention_7.png'),
(NULL,'Remplac. courroie distribution','XG-554-DD','440','2010-03-01',3,'intervention_8.png'),
(NULL,'Remplac. courroie distribution','JK-103-DG','460','2001-05-06',3,'intervention_9.png');

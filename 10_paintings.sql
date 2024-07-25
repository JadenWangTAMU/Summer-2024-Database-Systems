-- insert the museum as a user
-- INSERT INTO "user" (user_fname, user_lname, email, password, role) VALUES('The', 'Museum', 'N/A', 'password', 'A');

INSERT INTO "user" (user_fname, user_lname, email, password, role) VALUES('Blake', 'Dejohn', 'unknowingly@tamu.edu', 'password', 'A');

INSERT INTO "user" (user_fname, user_lname, email, password, role) VALUES('Jaden', 'Wang', 'jcwtexasanm@tamu.edu
', 'password', 'A');

INSERT INTO "user" (user_fname, user_lname, email, password, role) VALUES('Adam', 'Burhanpurwala', 'adam.burri@tamu.edu', 'password', 'A');

INSERT INTO "user" (user_fname, user_lname, email, password, role) VALUES('Kyle', 'Easton', 'kyleeaston@tamu.edu', 'password', 'A');


-- -- insert 10 creators
-- INSERT INTO creator(creator_fname, creator_lname, birth_country, birth_date, death_date) VALUES('Johannes', 'Vermeer', 'Netherlands', '1632-10-31', '1675-12-15');

-- INSERT INTO creator(creator_fname, creator_lname, birth_country, birth_date, death_date) VALUES('Leonardo', 'da Vinci', 'Italy', '1452-04-15', '1519-05-02');

-- INSERT INTO creator(creator_fname, creator_lname, birth_country, birth_date, death_date) VALUES('Vincent', 'van Gogh', 'Netherlands', '1853-03-30', '1890-07-29');

-- INSERT INTO creator(creator_fname, creator_lname, birth_country, birth_date, death_date) VALUES('Edvard', 'Munch', 'Norway', '1863-12-12', '1944-01-23');

-- INSERT INTO creator(creator_fname, creator_lname, birth_country, birth_date, death_date) VALUES('Salvador', 'Dali', 'Spain', '1904-05-11', '1989-01-23');

-- INSERT INTO creator(creator_fname, creator_lname, birth_country, birth_date, death_date) VALUES('Caspar', 'David Friedrich', 'Germany', '1774-09-05', '1840-05-07');

-- INSERT INTO creator(creator_fname, creator_lname, birth_country, birth_date, death_date) VALUES('Luke', 'Fildes', 'England', '1843-10-23', '1927-02-28');

-- INSERT INTO creator(creator_fname, creator_lname, birth_country, birth_date, death_date) VALUES('Gustave', 'Dore', 'France', '1832-01-06', '1883-01-23');

-- INSERT INTO creator(creator_fname, creator_lname, birth_country, birth_date, death_date) VALUES('Winslow', 'Homer', 'United States', '1836-02-24', '1910-09-29');

-- INSERT INTO creator(creator_fname, creator_lname, birth_country, birth_date, death_date) VALUES('Ilya', 'Repin', 'Russia', '1844-08-05', '1930-09-29');

-- --insert 10 of their paintings
-- INSERT INTO art_piece(creator_id, owner_id, title, year_finished, cost, description, photo_link, sellable, viewable) VALUES(1, 1, 'Girl with a Pearl Earring', 1665, 1000000, 'Dutch Golden Age painting','https://en.wikipedia.org/wiki/Girl_with_a_Pearl_Earring#/media/File:1665_Girl_with_a_Pearl_Earring.jpg', FALSE, TRUE);

-- INSERT INTO art_piece(creator_id, owner_id, title, year_finished, cost, description, photo_link, sellable, viewable) VALUES(2, 1, 'Mona Lisa', 1503, 1000000, 'Italian Renaissance painting','https://en.wikipedia.org/wiki/Mona_Lisa#/media/File:Mona_Lisa,_by_Leonardo_da_Vinci,_from_C2RMF_retouched.jpg', FALSE, TRUE);

-- INSERT INTO art_piece(creator_id, owner_id, title, year_finished, cost, description, photo_link, sellable, viewable) VALUES(3, 1, 'The Starry Night', 1889, 1000000, 'Post-Impressionist painting','https://en.wikipedia.org/wiki/The_Starry_Night#/media/File:Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg', FALSE, TRUE);

-- INSERT INTO art_piece(creator_id, owner_id, title, year_finished, cost, description, photo_link, sellable, viewable) VALUES(4, 1, 'The Scream', 1893, 1000000, 'Expressionist painting','https://en.wikipedia.org/wiki/The_Scream#/media/File:The_Scream.jpg', FALSE, TRUE);

-- INSERT INTO art_piece(creator_id, owner_id, title, year_finished, cost, description, photo_link, sellable, viewable) VALUES(5, 1, 'The Persistence of Memory', 1931, 1000000, 'Surrealist painting','https://en.wikipedia.org/wiki/The_Persistence_of_Memory#/media/File:The_Persistence_of_Memory.jpg', FALSE, TRUE);

-- INSERT INTO art_piece(creator_id, owner_id, title, year_finished, cost, description, photo_link, sellable, viewable) VALUES(6, 1, 'Wanderer above the Sea of Fog', 1818, 1000000, 'Romantic painting','https://en.wikipedia.org/wiki/Wanderer_above_the_Sea_of_Fog#/media/File:Caspar_David_Friedrich_-_Wanderer_above_the_sea_of_fog.jpg', FALSE, TRUE);

-- INSERT INTO art_piece(creator_id, owner_id, title, year_finished, cost, description, photo_link, sellable, viewable) VALUES(7, 1, 'The Doctor', 1891, 1000000, 'Victorian painting','https://en.wikipedia.org/wiki/Luke_Fildes#/media/File:Luke_Fildes_The_Doctor.jpg', FALSE, TRUE);

-- INSERT INTO art_piece(creator_id, owner_id, title, year_finished, cost, description, photo_link, sellable, viewable) VALUES(8, 1, 'Destruction of Leviathan', 1865, 1000000, 'Romantic painting','https://en.wikipedia.org/wiki/Gustave_Dor%C3%A9#/media/File:Destruction_of_Leviathan.png', FALSE, TRUE);

-- INSERT INTO art_piece(creator_id, owner_id, title, year_finished, cost, description, photo_link, sellable, viewable) VALUES(9, 1, 'Breezing Up (A Fair Wind)', 1876, 1000000, 'Realist painting','https://en.wikipedia.org/wiki/Winslow_Homer#/media/File:Winslow_Homer_-_Breezing_Up_(A_Fair_Wind)_-_Google_Art_Project.jpg', FALSE, TRUE);

-- INSERT INTO art_piece(creator_id, owner_id, title, year_finished, cost, description, photo_link, sellable, viewable) VALUES(10, 1, 'Ivan the Terrible and His Son Ivan', 1885, 1000000, 'Realist painting','https://en.wikipedia.org/wiki/Ivan_the_Terrible_and_His_Son_Ivan#/media/File:Iv%C3%A1n_el_Terrible_y_su_hijo,_por_Ili%C3%A1_Repin.jpg', FALSE, TRUE);
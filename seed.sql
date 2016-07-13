INSERT INTO competitors (itf_id, first_name, last_name, sex, birthdate, level, team_id)
VALUES (510317, 'Jiří', 'Beneš', 'Muž', '2.Kup', '7. February 2004', 1);
INSERT INTO competitors (itf_id, first_name, last_name, sex, birthdate, level, team_id)
VALUES (507192, 'Lucie', 'Bohatá', 'Žena', 'I.Dan', '14. February 2001', 1);
INSERT INTO competitors (itf_id, first_name, last_name, sex, birthdate, level, team_id)
VALUES (510313, 'Mikuláš', 'Hupcej', 'Muž', '7.Kup', '9. September 2003', 1);
INSERT INTO competitors (itf_id, first_name, last_name, sex, birthdate, level, team_id)
VALUES (509634, 'Eliška', 'Hupcejová', 'Žena', '4.Kup', '1. September 2001', 1);
INSERT INTO competitors (itf_id, first_name, last_name, sex, birthdate, level, team_id)
VALUES (510314, 'Jakub', 'Kalous', 'Muž', '4.Kup', '21. October 2002', 1);
INSERT INTO competitors (itf_id, first_name, last_name, sex, birthdate, level, team_id)
VALUES (510387, 'Erik', 'Kudrjavcev', 'Muž', '8.Kup', '21. March 2003', 1);
INSERT INTO competitors (itf_id, first_name, last_name, sex, birthdate, level, team_id)
VALUES (510394, 'Zdeněk', 'Lhotka', 'Muž', '1.Kup', '28. September 2003', 1);
INSERT INTO competitors (itf_id, first_name, last_name, sex, birthdate, level, team_id)
VALUES (510391, 'Patricia', 'Oginčuková', 'Žena', '8.Kup', '5. September 2005', 1);
INSERT INTO competitors (itf_id, first_name, last_name, sex, birthdate, level, team_id)
VALUES (507195, 'Natáli', 'Podskalníková', 'Žena', '1.Kup', '19. May 2003', 1);
INSERT INTO competitors (itf_id, first_name, last_name, sex, birthdate, level, team_id)
VALUES (507191, 'Sára', 'Podskalníková', 'Žena', 'I.Dan', '13. June 2000', 1);
INSERT INTO competitors (itf_id, first_name, last_name, sex, birthdate, level, team_id)
VALUES (507196, 'Patricie', 'Pokorná', 'Žena', '1.Kup', '2. December 2002', 2);
INSERT INTO competitors (itf_id, first_name, last_name, sex, birthdate, level, team_id)
VALUES (510380, 'Antonín', 'Pokorný', 'Muž', '6.Kup', '14. December 2006', 2);
INSERT INTO competitors (itf_id, first_name, last_name, sex, birthdate, level, team_id)
VALUES (509636, 'Daniela', 'Richterová', 'Žena', '3.Kup', '2. April 2004', 2);
INSERT INTO competitors (itf_id, first_name, last_name, sex, birthdate, level, team_id)
VALUES (510384, 'Davil', 'Roubal', 'Muž', '4.Kup', '17. July 1998', 2);
INSERT INTO competitors (itf_id, first_name, last_name, sex, birthdate, level, team_id)
VALUES (500822, 'Jakub', 'Roubal', 'Muž', 'I.Dan', '11. January 2000', 2);

INSERT INTO teams (name) VALUES ('Sparring');
INSERT INTO teams (name) VALUES ('Stránčice');

INSERT INTO users (first_name, last_name, email, pw_hash, team_id, is_admin) VALUES ('AdminF', 'AdminL', 'admin', 'admin', 1, 1);
INSERT INTO users (first_name, last_name, email, pw_hash, team_id, is_admin) VALUES ('UserF', 'UserL', 'user', 'user', 2, 0);
INSERT INTO users (first_name, last_name, email, pw_hash, team_id, is_admin) VALUES ('Robert', 'Pokorny','administrator@taekwondocz.com', 'robert', 1, 1);

INSERT INTO competition (name, location, date, deadline, fee, instructions_url, langlong) VALUES ('Světový pohár 2016', 'Budapešť', '12. října - 16. října 2016', '30. srpna 2016', '200.- Kč', 'http://taekwondocz.com/files/PROPOZICE%20MR%202016.pdf', '50.289, 14.830');

INSERT INTO member_competition (member_id, competition_id) VALUES (1, 1);
INSERT INTO member_competition (member_id, competition_id) VALUES (2, 1);
INSERT INTO member_competition (member_id, competition_id) VALUES (3, 1);
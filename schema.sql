DROP TABLE IF EXISTS competitors;
CREATE TABLE competitors (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  itf_id     INTEGER NOT NULL,
  first_name TEXT    NOT NULL,
  last_name  TEXT    NOT NULL,
  sex        string  NOT NULL,
  birthdate  string,
  weight     INTEGER,
  level      string,
  team_id    string
);

DROP TABLE IF EXISTS teams;
CREATE TABLE teams (
  id   INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL
);

DROP TABLE IF EXISTS users;
CREATE TABLE users (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  first_name  TEXT    NOT NULL,
  last_name   TEXT    NOT NULL,
  email       TEXT    NOT NULL,
  pw_hash     TEXT    NOT NULL,
  team_id     INTEGER NOT NULL,
  is_admin    INTEGER NOT NULL
);

DROP TABLE IF EXISTS competition;
CREATE TABLE competition (
  id                INTEGER PRIMARY KEY AUTOINCREMENT,
  name              TEXT    NOT NULL,
  location          TEXT    NOT NULL,
  date              TEXT    NOT NULL,
  deadline          TEXT    NOT NULL,
  fee               TEXT    NOT NULL,
  instructions_url  TEXT    NOT NULL,
  langlong          TEXT
);

DROP TABLE IF EXISTS member_competition;
CREATE TABLE member_competition (
  id                INTEGER PRIMARY KEY AUTOINCREMENT,
  member_id         INTEGER    NOT NULL,
  competition_id    INTEGER    NOT NULL
);

DROP TABLE IF EXISTS member_competition_levels;
CREATE TABLE member_competition (
  id                INTEGER PRIMARY KEY AUTOINCREMENT,
  member_id         INTEGER    NOT NULL,
  competition_id    INTEGER    NOT NULL
);
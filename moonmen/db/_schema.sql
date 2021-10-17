DROP TABLE IF EXISTS instances;
DROP TABLE IF EXISTS tasks;
DROP TABLE IF EXISTS notes;
DROP TABLE IF EXISTS files;

CREATE TABLE instances (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    description TEXT,
    repository TEXT
);

CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    instance_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    status INTEGER NOT NULL,
    FOREIGN KEY (instance_id) REFERENCES instances (id)
);

CREATE TABLE notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    instance_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    content TEXT,
    FOREIGN KEY (instance_id) REFERENCES instances (id)
);

CREATE TABLE files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    instance_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    path TEXT UNIQUE NOT NULL,
    FOREIGN KEY (instance_id) REFERENCES instances (id)
);

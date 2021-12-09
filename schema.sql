CREATE TABLE IF NOT EXISTS Users (
    person_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    phone TEXT NOT NULL UNIQUE,
    email TEXT UNIQUE NOT NULL,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL DEFAULT 'password',
    active INTEGER DEFAULT 1,
    date_created TEXT,
    hire_date TEXT,
    user_type TEXT DEFAULT 'User'
);
CREATE TABLE IF NOT EXISTS Competencies (
    comp_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    date_created TEXT
);
CREATE TABLE IF NOT EXISTS Assessments (
    assessment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    comp_id INTEGER,
    FOREIGN KEY (comp_id)
        REFERENCES Competencies (comp_id)
);
CREATE TABLE IF NOT EXISTS competency_results (
    comp_id INTEGER,
    person_id INTEGER,
    level INTEGER,
    report TEXT,
    FOREIGN KEY (comp_id)
        REFERENCES Competencies (comp_id)
);
CREATE TABLE IF NOT EXISTS assessment_results (
    asess_result_id INTEGER PRIMARY KEY AUTOINCREMENT,
    assessment_id INTEGER,
    person_id INTEGER,
    score TEXT,
    feedback TEXT,
    completed_date TEXT,
    FOREIGN KEY (assessment_id)
        REFERENCES Assessments (assessment_id),
    FOREIGN KEY (person_id)
        REFERENCES Users (person_id)
);

INSERT INTO Users (first_name, last_name, phone, email, username, password, date_created, hire_date, user_type)
VALUES ('Tony', 'Stark', '123-444-2432','tony@stark.com', 'ironman', '$2b$12$hXV7K881YN/7dmizgNoyL.Sa8H8KEOqQsUZRk0IlOgZMutHwu6tlm', '12/2/2021','02/23/2005', 'Manager'),
('Pepper', 'Pots', '123-222-2432','pepper@pots.com', 'Pots24', '$2b$12$hXV7K881YN/7dmizgNoyL.jOthHRIAcE6STckBKiNy3mVwLCKe0E2','04/15/2005','02/2/2021', 'User'),
('Natasha', 'Romanoff', '332-222-2432','natasha@romanoff.com', 'blackwidow','$2b$12$hXV7K881YN/7dmizgNoyL.k/MaJPGbPWEBbQZ7ia3SXy6HlxQx6Yi', '12/2/2021','07/15/2010', 'User');

INSERT INTO Competencies (name, date_created)
Values ('Data Types', '12/2/2021'),
('Variables', '12/2/2021'),
('Functions', '12/2/2021'),
('Boolean Logic', '12/2/2021'),
('Conditionals', '12/2/2021'),
('Loops', '12/2/2021'),
('Data Structures', '12/2/2021'),
('Lists', '12/2/2021'),
('Dictionaries', '12/2/2021'),
('Working with Files', '12/2/2021'),
('Exception Handling', '12/2/2021'),
('Quality Assurance (QA)', '12/2/2021'),
('Object-Oriented-Programming', '12/2/2021'),
('Recursion', '12/2/2021'),
('Databases', '12/2/2021');

INSERT INTO Assessments (name, description, comp_id)
VALUES ('For loop assessment', 'Nested for loops, loop through lists, use for loop range', 6),
('While loop assessment', 'can use a while loop in the right situations.', 6),
('data type assessment', 'quiz on all the different data types', 1),
('dictionaries assessment', 'tests on all the different dictionary methods', 9);

INSERT INTO competency_results (comp_id, person_id, level, report)
VALUES (1, 1, 4,'This is a report of how well a user is doing on this competency'),
(2, 1, 4,'This is a report of how well a user is doing on this competency.'),
(3, 1, 4,'This is a report of how well a user is doing on this competency.'),
(4, 1, 4,'This is a report of how well a user is doing on this competency.'),
(5, 1, 4,'This is a report of how well a user is doing on this competency.'),
(1, 2, 2,'This is a report of how well a user is doing on this competency.'),
(2, 2, 3,'This is a report of how well a user is doing on this competency.'),
(3, 2, 1,'This is a report of how well a user is doing on this competency.'),
(1, 1, 4,'This is a report of how well a user is doing on this competency.');

INSERT INTO assessment_results (assessment_id, person_id, score, feedback, completed_date)
VALUES (1, 1, '10/10','this is where we give feedback on the particular assessment','03-01-2020'),
(2, 1, '15/15','this is where we give feedback on the particular assessment','03-01-2020'),
(3, 1, '30/30','this is where we give feedback on the particular assessment','03-01-2020'),
(4, 1, '8/8','this is where we give feedback on the particular assessment','03-01-2020'),
(1, 2, '6/10','this is where we give feedback on the particular assessment','03-01-2020'),
(2, 2, '10/15','this is where we give feedback on the particular assessment','03-01-2020'),
(3, 2, '20/30','this is where we give feedback on the particular assessment','03-01-2020');










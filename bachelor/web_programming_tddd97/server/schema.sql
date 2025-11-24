DROP TABLE IF EXISTS tw_users;
DROP TABLE IF EXISTS tw_logged_in;
DROP TABLE IF EXISTS tw_messages;

SELECT 'Creating tables' AS 'Message';

CREATE TABLE tw_users (
    fname VARCHAR(50) NOT NULL,
    lname VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    country VARCHAR(50) NOT NULL,
    city VARCHAR(50) NOT NULL,
    gender VARCHAR(10) NOT NULL,
    password VARCHAR(50) NOT NULL,
    CONSTRAINT pk_tw_users PRIMARY KEY(email)
);

CREATE TABLE tw_logged_in (
    email VARCHAR(50) NOT NULL,
    token VARCHAR(36),
    CONSTRAINT pk_tw_logged_in PRIMARY KEY(email),
    CONSTRAINT fk_logged_user FOREIGN KEY (email) REFERENCES tw_users(email) ON DELETE SET NULL
);

CREATE TABLE tw_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    from_id VARCHAR(50) NOT NULL,
    to_id VARCHAR(50) NOT NULL,
    msg VARCHAR(128) NOT NULL,
    CONSTRAINT fk_from_messages FOREIGN KEY (from_id) REFERENCES tw_users(email),
    CONSTRAINT fk_to_messages FOREIGN KEY (to_id) REFERENCES tw_users(email)
);
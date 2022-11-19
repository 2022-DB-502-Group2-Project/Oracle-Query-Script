-- Member Table
-- use id as uuid
-- use pw as one-way-encrypt for security
CREATE TABLE member(
    id VARCHAR(100) NOT NULL PRIMARY KEY,
    username VARCHAR2(30) NOT NULL,
    password VARCHAR2(1000) NOT NULL,
    email VARCHAR2(1000) NOT NULL
);
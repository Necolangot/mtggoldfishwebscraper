CREATE TABLE CARDS(
name    CHAR(255) NOT NULL PRIMARY KEY,
date    date,
colors  char(255),
type    char(255),
power   char(10),
tough   char(10),
otext   text,
price   decimal(10,3),
loyalty int,
flip    char(255)
);
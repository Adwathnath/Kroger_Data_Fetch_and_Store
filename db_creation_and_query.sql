/* db queries i used to create and manipulate db and tables*/

create database KrogerData;
use KrogerData;

create table products (
product_id varchar(20),   
upc varchar(20),
page_uri varchar(300),
brand varchar(20),
categories varchar(30),
countryOrigin varchar(25),
descriptn varchar(100),
Date varchar(50)
);


create table images (
product_id varchar(20),   
perspective varchar(30),
image_size varchar(30),
url varchar(300),
Date varchar(50)
);

create table items (
product_id varchar(20),   
item_id varchar(20),
size varchar(30),
curbside varchar(20),
delivery varchar(20),
in_store varchar(20),
ship_to_home varchar(20),
Date varchar(50)
);

create table validation_info (
url_format varchar(30),
url_reach varchar(30),
Date varchar(30)
);

create table delete_info (
message varchar(30) default 'Data.json deleted on',
Date    varchar(50)
);
#show databases;
create database spe_proj;
use spe_proj;

create table admins(
	username varchar(50),
    password varchar(15),
    email_id varchar(50),
    primary key (username)
    );

insert into admins values('rvarma', 'rv123','varma.richavarma@gmail.com');

create table violation_db(
	created_at datetime,
    no_of_violations numeric,
    primary key (created_at)
    );
    



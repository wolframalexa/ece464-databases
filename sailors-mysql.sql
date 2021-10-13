/*
SQL queries to populate a Sailors and Boats dataset
*/
create table sailors(
    sid int PRIMARY KEY,
    sname varchar(30),
    rating int,
    age int
);

create table reserves(
    sid int,
    bid int,
    day date,
    amount_paid decimal,
	PRIMARY KEY (sid, bid, day)
);

create table boats(
    bid int PRIMARY KEY,
	bname char(20),
	color char(10),
	length int
);

create table expenses(
    eid int PRIMARY KEY,
    type int,
    recipient_id int,
    day date,
    amount decimal
);

insert into sailors values (22,'dusting',7,45);
insert into sailors values (29,'brutus',1,33);
insert into sailors values (31,'lubber',8,55);
insert into sailors values (32,'andy',8,25);
insert into sailors values (58,'rusty',10,35);
insert into sailors values (64,'horatio',7,16);
insert into sailors values (71,'zorba',10,35);
insert into sailors values (74,'horatio',9,25);
insert into sailors values (85,'art',3,25);
insert into sailors values (95,'bob',3,63);
insert into sailors values (23,'emilio',7,45);
insert into sailors values (24,'scruntus',1,33);
insert into sailors values (35,'figaro',8,55);
insert into sailors values (59,'stum',8,25);
insert into sailors values (60,'jit',10,35);
insert into sailors values (61,'ossola',7,16);
insert into sailors values (62,'shaun',10,35);
insert into sailors values (88,'dan',9,25);
insert into sailors values (89,'dye',3,25);
insert into sailors values (90,'vin',3,63);

insert into reserves values (23,104,'1998/10/10', 148.52);
insert into reserves values (24,104,'1998/10/10', 100.00);
insert into reserves values (35,104,'1998/8/10', 100.00);
insert into reserves values (59,105,'1998/7/10', 4929.30);
insert into reserves values (23,105,'1998/11/10', 402.21);
insert into reserves values (35,105,'1998/11/6', 2840.12);
insert into reserves values (59,106,'1998/11/12', 133.43);
insert into reserves values (60,106,'1998/9/5', 511.01);
insert into reserves values (60,106,'1998/9/8', 749.23);
insert into reserves values (88,107,'1998/9/8', 473.12);
insert into reserves values (89,108,'1998/10/10', 45.12);
insert into reserves values (90,109,'1998/10/10', 36.33);
insert into reserves values (89,109,'1998/8/10', 43.12);
insert into reserves values (60,109,'1998/7/10', 23.23);
insert into reserves values (59,109,'1998/11/10', 45.12);
insert into reserves values (62,110,'1998/11/6', 145.22);
insert into reserves values (88,110,'1998/11/12', 145.23);
insert into reserves values (88,110,'1998/9/5', 488.89);
insert into reserves values (88,111,'1998/9/8', 488.56);
insert into reserves values (61,112,'1998/9/8', 46.34);
insert into reserves values (22,101,'1998/10/10', 46.12);
insert into reserves values (22,102,'1998/10/10', 36.27);
insert into reserves values (22,103,'1998/8/10', 144.36);
insert into reserves values (22,104,'1998/7/10', 364.12);
insert into reserves values (31,102,'1998/11/10', 5628.44);
insert into reserves values (31,103,'1998/11/6', 4512.11);
insert into reserves values (31,104,'1998/11/12', 57.47);
insert into reserves values (64,101,'1998/9/5', 3764.34);
insert into reserves values (64,102,'1998/9/8', 34.34);
insert into reserves values (74,103,'1998/9/8', 23.23);

insert into boats values (101,'Interlake','blue', 45);
insert into boats values (102,'Interlake','red', 45);
insert into boats values (103,'Clipper','green', 40);
insert into boats values (104,'Clipper','red', 40);
insert into boats values (105,'Marine','red', 35);
insert into boats values (106,'Marine','green', 35);
insert into boats values (107,'Marine','blue', 35);
insert into boats values (108,'Driftwood','red', 35);
insert into boats values (109,'Driftwood','blue', 35);
insert into boats values (110,'Klapser','red', 30);
insert into boats values (111,'Sooney','green', 28);
insert into boats values (112,'Sooney','red', 28);


insert into expenses values (13, 2, 41, 1998-06-08, 137.45)
insert into expenses values (16, 4, 32, 1990-06-14, 10000)
insert into expenses values (44, 1, 45, 1998-06-14, 800)
insert into expenses values (20, 0, 2, 1995-07-26, 1000)
insert into expenses values (45, 1, 45, 1998-06-21, 800)
insert into expenses values (66, 5, 21, 2001-02-02, 1456.73)

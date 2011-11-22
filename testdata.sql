insert into student (username, name) values ('mjb0321', 'Michael Ballantyne'),('djt0231', 'Daniel Tanner'),('zym0210', 'Zachary Morin');

insert into semester (name,active) values ('Fall 2010','false'),('Spring 2011','true'),('Fall 2011','true'),('Spring 2012','false');

insert into student_semester (student, semester) values (1,1),(1,2),(2,3);

insert into organization (name, contact_name, contact_phone) values ('BSA', 'Bill Milner', '801-483-1444');

insert into hours_entry (student, semester, event_date, hours, organization) values (1,1,'Oct-08-2011',5,1),(1,1,'Oct-23-2011',3,1);

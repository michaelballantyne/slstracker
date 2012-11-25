create table if not exists semester (
    id serial primary key,
    name varchar(50) unique not null,
    active boolean not null
);

create table if not exists final_project (
    id serial primary key,
    body bytea not null
); 

create table if not exists student (
    id serial primary key,
    username varchar(50) unique not null,
    name varchar(50) not null,
    starting_hours int,
    final_project int references final_project(id)
);

create table if not exists student_semester (
    semester int references semester(id),
    student int references student(id),
    reflection text,
    primary key (semester, student)
);

create table if not exists organization (
    id serial primary key,
    name varchar(50) unique not null,
    contact_name varchar(50) not null,
    contact_phone varchar(50) not null
);

create table if not exists hours_entry (
    id serial primary key,
    student int not null,
    semester int not null,
    event_date date not null,
    hours int not null,
    organization int not null references organization(id),
    foreign key (student, semester) references student_semester(student, semester),
    activity text not null
);

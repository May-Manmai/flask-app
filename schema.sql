create table users (
    id SERIAL NOT null primary key,
    name VARCHAR(100) not null,
    email TEXT not null unique,
    password VARCHAR(255) not null
);

create table ingredients (
    id SERIAL NOT null primary key,
    user_id int,
    purchased_date date not null,
    expiry_date date not null, 
    name VARCHAR(100) not null,
    CONSTRAINT fk_user FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);




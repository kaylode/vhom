# PostgreSQL Database
- This repo uses PostgreSQL as Database server
- Follow these guide for simple database setup, or look into [this cheatsheet](https://gist.github.com/Kartones/dd3ff5ec5ea238d4c546) for more info

## **Download and setup PostgreSQL**
- Download and install postgresql from https://www.postgresql.org/download/

## **Initialize database**

- Connect to PostgreSQL server:
```
psql -U <username>;
```

- Create database: 
```
create database <tablename>;
```

- Create table: 
```
\c <tablename> # connect to database
create table waterlevel;
```

- Check if table exists:
```
\dt
```

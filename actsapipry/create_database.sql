-- Database: true_home

-- DROP DATABASE true_home;

CREATE DATABASE true_home
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'Spanish_Mexico.1252'
    LC_CTYPE = 'Spanish_Mexico.1252'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;

COMMENT ON DATABASE true_home
    IS 'Base de datos para apps de TrueHome';

GRANT ALL ON DATABASE true_home TO postgres;

GRANT TEMPORARY ON DATABASE true_home TO usr_true_home;

GRANT TEMPORARY, CONNECT ON DATABASE true_home TO PUBLIC;
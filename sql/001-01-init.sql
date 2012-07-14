--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

--
-- Name: famoso_reports; Type: DATABASE; Schema: -; Owner: -
--

CREATE DATABASE famoso_reports WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'en_US.UTF-8' LC_CTYPE = 'en_US.UTF-8';


\connect famoso_reports

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

--
-- Name: plpgsql; Type: PROCEDURAL LANGUAGE; Schema: -; Owner: -
--

CREATE OR REPLACE PROCEDURAL LANGUAGE plpgsql;


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: appusers; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE appusers (
    id integer NOT NULL,
    username character varying(20) NOT NULL,
    password character varying(80) NOT NULL,
    first_name character varying(64) NOT NULL,
    last_name character varying(64) NOT NULL,
    email character varying(256) NOT NULL,
    admin boolean NOT NULL
);


--
-- Name: appusers_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE appusers_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: appusers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE appusers_id_seq OWNED BY appusers.id;


--
-- Name: report; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE report (
    id integer NOT NULL,
    name character varying(256) NOT NULL,
    report_group_id integer NOT NULL
);


--
-- Name: report_group_users; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE report_group_users (
    report_group_id integer NOT NULL,
    user_id integer NOT NULL
);


--
-- Name: report_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE report_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: report_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE report_id_seq OWNED BY report.id;


--
-- Name: report_report_type; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE report_report_type (
    report_id integer NOT NULL,
    report_type_id integer NOT NULL
);


--
-- Name: report_type; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE report_type (
    id integer NOT NULL,
    extension character varying(8) NOT NULL
);


--
-- Name: report_type_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE report_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: report_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE report_type_id_seq OWNED BY report_type.id;


--
-- Name: reportgroups; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE reportgroups (
    id integer NOT NULL,
    name character varying(256) NOT NULL,
    displayname character varying(256) NOT NULL
);


--
-- Name: reportgroups_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE reportgroups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: reportgroups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE reportgroups_id_seq OWNED BY reportgroups.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE appusers ALTER COLUMN id SET DEFAULT nextval('appusers_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE report ALTER COLUMN id SET DEFAULT nextval('report_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE report_type ALTER COLUMN id SET DEFAULT nextval('report_type_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE reportgroups ALTER COLUMN id SET DEFAULT nextval('reportgroups_id_seq'::regclass);


--
-- Name: appusers_email_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY appusers
    ADD CONSTRAINT appusers_email_key UNIQUE (email);


--
-- Name: appusers_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY appusers
    ADD CONSTRAINT appusers_pkey PRIMARY KEY (id);


--
-- Name: appusers_username_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY appusers
    ADD CONSTRAINT appusers_username_key UNIQUE (username);


--
-- Name: name_group_uc; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY report
    ADD CONSTRAINT name_group_uc UNIQUE (name, report_group_id);


--
-- Name: report_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY report
    ADD CONSTRAINT report_pkey PRIMARY KEY (id);


--
-- Name: report_report_type_uc; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY report_report_type
    ADD CONSTRAINT report_report_type_uc UNIQUE (report_id, report_type_id);


--
-- Name: report_type_extension_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY report_type
    ADD CONSTRAINT report_type_extension_key UNIQUE (extension);


--
-- Name: report_type_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY report_type
    ADD CONSTRAINT report_type_pkey PRIMARY KEY (id);


--
-- Name: reportgroups_displayname_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY reportgroups
    ADD CONSTRAINT reportgroups_displayname_key UNIQUE (displayname);


--
-- Name: reportgroups_name_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY reportgroups
    ADD CONSTRAINT reportgroups_name_key UNIQUE (name);


--
-- Name: reportgroups_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY reportgroups
    ADD CONSTRAINT reportgroups_pkey PRIMARY KEY (id);


--
-- Name: user_report_uc; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY report_group_users
    ADD CONSTRAINT user_report_uc UNIQUE (report_group_id, user_id);


--
-- Name: report_group_users_report_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY report_group_users
    ADD CONSTRAINT report_group_users_report_group_id_fkey FOREIGN KEY (report_group_id) REFERENCES reportgroups(id);


--
-- Name: report_group_users_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY report_group_users
    ADD CONSTRAINT report_group_users_user_id_fkey FOREIGN KEY (user_id) REFERENCES appusers(id);


--
-- Name: report_report_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY report
    ADD CONSTRAINT report_report_group_id_fkey FOREIGN KEY (report_group_id) REFERENCES reportgroups(id);


--
-- Name: report_report_type_report_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY report_report_type
    ADD CONSTRAINT report_report_type_report_id_fkey FOREIGN KEY (report_id) REFERENCES report(id);


--
-- Name: report_report_type_report_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY report_report_type
    ADD CONSTRAINT report_report_type_report_type_id_fkey FOREIGN KEY (report_type_id) REFERENCES report_type(id);


--
-- Name: public; Type: ACL; Schema: -; Owner: -
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--


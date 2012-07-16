-- Create attribute table for using in filter reports

CREATE TABLE report_attribute (
    id integer NOT NULL,    
	report_id integer NOT NULL,
    name character varying(256) NOT NULL,
    value character varying(256) NOT NULL
);

CREATE SEQUENCE report_attribute_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;                                    

ALTER SEQUENCE report_attribute_id_seq OWNED BY appusers.id;

ALTER TABLE report_attribute ALTER COLUMN id SET DEFAULT nextval('report_attribute_id_seq'::regclass);

ALTER TABLE ONLY report_attribute
    ADD CONSTRAINT report_attribute_pkey PRIMARY KEY (id);
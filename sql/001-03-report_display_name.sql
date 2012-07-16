-- add a displayname for report, so it's better on the eyes!

alter table report add column displayname character varying(256);
update report set displayname = name;
alter table report alter column displayname set not null;

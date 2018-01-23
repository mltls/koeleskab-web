drop table if exists koeleskab;
create table koeleskab (
       id integer primary key autoincrement,
       time float not null,
       temperature float not null
)

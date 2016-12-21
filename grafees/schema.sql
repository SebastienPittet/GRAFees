

drop table if exists STATIONS;
create table STATIONS (
    Id integer primary key autoincrement,
    Long real,
    Lat real,
    Location text
);

drop table if exists UNITS;
create table UNITS (
    Id integer primary key autoincrement,
    Unit text unique,
    Description text
);

drop table if exists MEASURES;
create table MEASURES (
  Id integer primary key autoincrement,
  Epoch integer,
  Value real,
  Unit integer,
  Station integer,
  foreign key (Unit) references UNITS(Id),
  foreign key (Station) references STATIONS(Id)
);

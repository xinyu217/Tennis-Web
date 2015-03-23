drop table if exists players;
create table players (
  id integer primary key autoincrement,
  player_name text not null,
  hand text not null,
  age integer not null,
  gender text not null,
  rank integer not null
);

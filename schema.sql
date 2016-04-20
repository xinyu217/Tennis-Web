drop table if exists players;
create table players (
  id integer primary key autoincrement,
  player_name text not null,
  hand text not null,
  age integer not null,
  gender text not null,
  rank integer not null
);
drop table if exists shots;
create table shots (
  player_name text not null,
  serve_class integer not null,
  speed double not null,
  start_x double not null,
  start_y double not null,
  start_z double not null,
  end_x double not null,
  end_y double not null,  
  end_z double not null,
  serve_type integer not null,
  match_type text not null,
  server_score integer not null,
  receiver_score integer not null
);

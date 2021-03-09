-- Your SQL goes here
CREATE TABLE matches(team_1 VARCHAR(100), team_2 VARCHAR(100), team_1_winner_odds decimal, team_2_winner_odds decimal, draw_odds decimal, bet_type varchar(100), scrape_time integer, match_time integer, tournament_name varchar(100), source varchar(100), primary key(team_1, team_2, scrape_time, match_time, source));

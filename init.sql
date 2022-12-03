DROP TABLE member;
DROP TABLE team_info;
DROP TABLE team_homeground;
DROP TABLE player_prev_league;
DROP TABLE player_info;
DROP TABLE previous_league;

-- Member Table
-- use id as uuid
-- use pw as one-way-encrypt for security
CREATE TABLE member(
    id VARCHAR(100) NOT NULL PRIMARY KEY,
    username VARCHAR2(30) NOT NULL,
    password VARCHAR2(1000) NOT NULL,
    email VARCHAR2(1000) NOT NULL
);

-- Team information
-- all of information of team informations should not be null
CREATE TABLE team_info(
    teamid VARCHAR2(1000) NOT NULL PRIMARY KEY,
    teamname VARCHAR2(50) NOT NULL,
    leaguetype VARCHAR2(30) NOT NULL,
    totalgamecount VARCHAR2(20) NOT NULL,
    winingpoint VARCHAR2(20)  NOT NULL,
    win VARCHAR2(20)  NOT NULL,
    draw VARCHAR2(20)  NOT NULL,
    lose VARCHAR2(20)  NOT NULL,
    score VARCHAR2(20)  NOT NULL,
    losspoint VARCHAR2(20)  NOT NULL
);

-- Homeground information of teams
-- primary key teamid references team table's teamid : if team deleted -> stadium deleted
CREATE TABLE team_homeground(
    teamid VARCHAR2(1000) NOT NULL PRIMARY KEY,
    stadiumname VARCHAR2(50) NOT NULL,
    CONSTRAINT fk_team FOREIGN KEY (teamid) REFERENCES team_info(teamid) ON DELETE CASCADE
);

-- Player information
-- primary key playerid references team table's teamid
CREATE TABLE player_info(
    playerid VARCHAR2(1000) NOT NULL PRIMARY KEY,
    playername VARCHAR2(50) NOT NULL,
    teamid VARCHAR2(1000),
    leaguetype VARCHAR2(30) NOT NULL,
    position VARCHAR2(30),
    backnumber VARCHAR2(20) ,
    height VARCHAR2(20) ,
    weight VARCHAR2(20) ,
    birth DATE,
    imgurl VARCHAR(1500)
);

-- previous leageu datas
CREATE TABLE previous_league( 
    leaguename VARCHAR2(60) NOT NULL PRIMARY KEY,
    year VARCHAR2(20) NOT NULL
);

-- connection table between player_info and previous_league (m : n)
CREATE TABLE player_prev_league(
    playerid VARCHAR2(1000) NOT NULL,
    leagueid VARCHAR2(1000) NOT NULL,
    teamid VARCHAR2(1000) NOT NULL,
    participant VARCHAR2(20) ,
    winningpoint VARCHAR2(20) ,
    assist VARCHAR2(20) ,
    goalkick VARCHAR2(20) ,
    cornerkick VARCHAR2(20) ,
    offside VARCHAR2(20) ,
    shooting VARCHAR2(20) ,
    foul VARCHAR2(20) ,
    losspoint VARCHAR2(20) ,
    warning VARCHAR2(20) ,
    left VARCHAR2(20) ,
    -- CONSTRAINT prev_connector_pk PRIMARY KEY (playerid,leagueid),
    CONSTRAINT prev_player_league_pk PRIMARY KEY (playerid, leagueid),
    CONSTRAINT fk_player FOREIGN KEY (playerid) REFERENCES player_info(playerid) ON DELETE CASCADE,
    CONSTRAINT fk_prevleague FOREIGN KEY (leagueid) REFERENCES previous_league(leagueid) ON DELETE CASCADE
);

-- These queries is for testing
insert into player_info (playerid, playername, leaguetype) values ('id1','name1','league1');
insert into player_info (playerid, playername, leaguetype) values ('id2','name2','league1');
insert into player_info (playerid, playername, leaguetype) values ('id3','name3','league1');
insert into previous_league values ('lid1','lname1',2022);
insert into previous_league values ('lid2','lname2',2022);
insert into previous_league values ('lid3','lname3',2022);

insert into player_prev_league (playerid, leagueid, teamname) values ('id1','lid1','t1');
insert into player_prev_league (playerid, leagueid, teamname) values ('id2','lid2','t1');
insert into player_prev_league (playerid, leagueid, teamname) values ('id1','lid3','t1');



-- commit queries
commit;


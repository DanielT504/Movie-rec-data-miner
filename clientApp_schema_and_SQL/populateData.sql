drop table BoxOfficeMojoDaily;
drop table BoxOfficeMojoReleases;
drop table Credits;
drop table HSXMoviePrices;
drop table HSXMovieMaster;
drop table DomesticAvgMovieTicketPrices;
drop table Keywords;
drop table Ratings;
drop table Links;
drop table MojoBudgetUpdate;
drop table Movies;

-- Movies Table
CREATE TABLE Movies (
    imdb_id VARCHAR(20),
    metadata_id INT,
    title VARCHAR(255) NOT NULL,
    release_date VARCHAR(20),
    genres VARCHAR(5000),
    runtime INT,
    tagline VARCHAR(255),
    overview TEXT,
    PRIMARY KEY(imdb_id, title)
);

create index MoviesMetadata on Movies(metadata_id);
create index MoviesTitle on Movies(title);

-- BoxOfficeMojoReleases Table
CREATE TABLE BoxOfficeMojoReleases (
    bo_id VARCHAR(25) PRIMARY KEY,
    imdb_id VARCHAR(20),
    distributor_name VARCHAR(255),
    domestic_gross DECIMAL(15, 2),
    release_date VARCHAR(20),
    running_time VARCHAR(20),
    updated_at TEXT,
    FOREIGN KEY (imdb_id) REFERENCES Movies(imdb_id)
);

-- BoxOfficeMojoDaily Table
CREATE TABLE BoxOfficeMojoDaily (
    bo_date TEXT,
    bo_id VARCHAR(25) PRIMARY KEY,
    daily_domestic_gross DECIMAL(15, 2),
    daily_theater_count INT,
    retrieved_at TEXT,
    inserted_at TEXT,
    FOREIGN KEY (bo_id) REFERENCES BoxOfficeMojoReleases(bo_id)
);

CREATE TABLE Credits (
    cast TEXT,
    crew TEXT,
    id INT PRIMARY KEY,
    FOREIGN KEY (id) REFERENCES Movies(metadata_id)
);

-- DomesticAvgMovieTicketPrices Table
CREATE TABLE DomesticAvgMovieTicketPrices (
    year INT PRIMARY KEY,
    avg_movie_ticket_price_usd DECIMAL(5, 2)
);

-- HSXMovieMaster Table
CREATE TABLE HSXMovieMaster (
    hsx_id INT,
    title VARCHAR(255) NOT NULL,
    synopsis TEXT,
    ipo_date TEXT,
    delist_date TEXT,
    theaters INT,
    distributor VARCHAR(255),
    release_pattern VARCHAR(50),
    updated_at TEXT,
    PRIMARY KEY (hsx_id, title),
    FOREIGN KEY (title) REFERENCES Movies(title)
);

-- HSXMoviePrices Table
CREATE TABLE HSXMoviePrices (
    hsx_id INT PRIMARY KEY,
    price DECIMAL(10, 2),
    shares_long INT,
    shares_short INT,
    trading_vol INT,
    retrieved_at TEXT,
    inserted_at TEXT,
    FOREIGN KEY (hsx_id) REFERENCES HSXMovieMaster(hsx_id)
);

-- Keywords Table
CREATE TABLE Keywords (
    metadata_id INT PRIMARY KEY,
    keyword_value TEXT,
    FOREIGN KEY (metadata_id) REFERENCES Movies(metadata_id)
);

-- Links Table
CREATE TABLE Links (
    movie_id INT PRIMARY KEY,
    imdb_id VARCHAR(20),
    metadata_id INT
);

-- MojoBudgetUpdate Table
CREATE TABLE MojoBudgetUpdate (
    imdb_id VARCHAR(20) PRIMARY KEY,
    title TEXT,
    year INT,
    trivia TEXT,
    mpaa VARCHAR(10),
    release_date VARCHAR(20),
    run_time INT,
    distributor VARCHAR(255),
    director VARCHAR(255),
    writer VARCHAR(255),
    producer VARCHAR(255),
    composer VARCHAR(255),
    cinematographer VARCHAR(255),
    main_actor_1 VARCHAR(255),
    main_actor_2 VARCHAR(255),
    main_actor_3 VARCHAR(255),
    main_actor_4 VARCHAR(255),
    budget DECIMAL(15, 2),
    domestic DECIMAL(15, 2),
    international DECIMAL(15, 2),
    worldwide DECIMAL(15, 2),
    genre_1 VARCHAR(50),
    genre_2 VARCHAR(50),
    genre_3 VARCHAR(50),
    genre_4 VARCHAR(50),
    HTML TEXT,
    FOREIGN KEY (imdb_id) REFERENCES Movies(imdb_id)
);

-- Ratings Table
CREATE TABLE Ratings (
    user_id INT,
    movie_id INT,
    rating DECIMAL(3, 1),
    FOREIGN KEY (movie_id) REFERENCES Links(movie_id)
);

-- Load data into Movies table
LOAD DATA INFILE '/var/lib/mysql-files/03-Movies/movies_metadata.csv'
IGNORE INTO TABLE Movies
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(@col1, @col2, @col3, @col4, @col5, @col6, @col7, @col8, @col9, @col10, @col11, @col12, @col13, @col14, @col15, @col16, @col17, @col18, @col19, @col20, @col21, @col22, @col23, @col24) 
set genres=@col4, imdb_id=@col7, metadata_id=@col6, title=@col21, release_date=@col15, runtime= IFNULL(NULLIF(@col17, ''), 0), tagline=@col20, overview=@col10;

-- Load data into BoxOfficeMojoDaily table
LOAD DATA INFILE '/var/lib/mysql-files/03-Movies/hsx_bomojo_data/boxofficemojo_daily_boxoffice.csv'
IGNORE INTO TABLE BoxOfficeMojoDaily
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- Load data into BoxOfficeMojoReleases table
LOAD DATA INFILE '/var/lib/mysql-files/03-Movies/hsx_bomojo_data/boxofficemojo_releases.csv'
IGNORE INTO TABLE BoxOfficeMojoReleases
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(@col1, @col2, @col3, @col4, @col5, @col6, @col7, @col8, @col9, @col10, @col11, @col12, @col13, @col14, @col15, @col16, @col17, @col18, @col19, @col20, @col21) 
set bo_id=@col1, imdb_id=@col4, distributor_name=@col7, domestic_gross=@col8, release_date=@col12, running_time=@col17, updated_at=@col21;

-- Load data into Cast table
LOAD DATA INFILE '/var/lib/mysql-files/03-Movies/credits.csv'
IGNORE INTO TABLE Credits
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- Load data into DomesticAvgMovieTicketPrices table
LOAD DATA INFILE '/var/lib/mysql-files/03-Movies/domestic_avg_movie_ticket_prices.csv'
IGNORE INTO TABLE DomesticAvgMovieTicketPrices
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(@col1, @col2, @col3) 
set year=@col1, avg_movie_ticket_price_usd=@col2;

-- Load data into HSXMovieMaster table
LOAD DATA INFILE '/var/lib/mysql-files/03-Movies/hsx_bomojo_data/hsx_movie_master.csv'
IGNORE INTO TABLE HSXMovieMaster
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(@col1, @col2, @col3, @col4, @col5, @col6, @col7, @col8, @col9, @col10, @col11, @col12, @col13, @col14, @col15, @col16) 
set hsx_id=@col1, title=@col2, synopsis=@col3, ipo_date=@col8, delist_date=@col10, theaters=@col12, distributor=@col13, release_pattern=@col14, updated_at=@col16;

-- Load data into HSXMoviePrices table
LOAD DATA INFILE '/var/lib/mysql-files/03-Movies/hsx_bomojo_data/hsx_movie_prices.csv'
IGNORE INTO TABLE HSXMoviePrices
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- Load data into Keywords table
LOAD DATA INFILE '/var/lib/mysql-files/03-Movies/keywords.csv'
IGNORE INTO TABLE Keywords
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- Load data into Links table
LOAD DATA INFILE '/var/lib/mysql-files/03-Movies/links_small.csv'
INTO TABLE Links
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(@col1, @col2, @col3)
set movie_id=@col1, imdb_id=@col2, metadata_id=IFNULL(NULLIF(@col3, ''), 0);
UPDATE Links SET imdb_id = CONCAT('tt', imdb_id);

-- Load data into MojoBudgetUpdate table
LOAD DATA INFILE '/var/lib/mysql-files/03-Movies/Mojo_budget_update.csv'
IGNORE INTO TABLE MojoBudgetUpdate
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- Load data into Ratings table
LOAD DATA INFILE '/var/lib/mysql-files/03-Movies/ratings_small.csv'
IGNORE INTO TABLE Ratings
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(@col1, @col2, @col3, @col4) set user_id=@col1, movie_id=@col2, rating=@col3;



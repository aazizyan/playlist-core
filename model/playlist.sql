CREATE TABLE users(
	user_id SERIAL PRIMARY KEY,
	username varchar(50) NOT NULL UNIQUE,
	password BYTEA NOT NULL,
	name varchar(30) NOT NULL,
	is_admin BOOLEAN NOT NULL DEFAULT FALSE,
	token CHAR(32),
	token_date REAL DEFAULT EXTRACT(EPOCH FROM now())
);

CREATE TABLE places(
	place_id SERIAL PRIMARY KEY,
	username varchar(50) NOT NULL,
	place_name varchar(100) NOT NULL,
	latitude REAL NOT NULL,
	longitude REAL NOT NULL,
	FOREIGN KEY (username)  REFERENCES users(username)
);

CREATE TABLE songs(
	song_id SERIAL PRIMARY KEY,
	place_id INT NOT NULL,
	username varchar(50) NOT NULL,
	song_name varchar(50),
	raiting INT NOT NULL DEFAULT 0,
	FOREIGN KEY (place_id) REFERENCES places(place_id),
	FOREIGN KEY (username) REFERENCES users(username)
);

CREATE TABLE likes(
	like_id SERIAL PRIMARY KEY,
	username varchar(50) NOT NULL,
	song_id INT NOT NULL,
	type BOOLEAN NOT NULL DEFAULT TRUE,
	FOREIGN KEY (username) REFERENCES users(username),
	FOREIGN KEY (song_id) REFERENCES songs(song_id)
);

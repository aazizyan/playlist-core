CREATE TABLE users(
	user_id SERIAL PRIMARY KEY,
	username CHAR(50) NOT NULL UNIQUE,
	password CHAR(64) NOT NULL,
	name CHAR(30) NOT NULL,
	is_admin BOOLEAN NOT NULL DEFAULT FALSE,
	token CHAR(30),
	token_date TIMESTAMP
);

CREATE TABLE places(
	place_id SERIAL PRIMARY KEY,
	user_id INT NOT NULL,
	place_name CHAR(100) NOT NULL,
	latitude REAL NOT NULL,
	longitude REAL NOT NULL,
	FOREIGN KEY (user_id)  REFERENCES users(user_id)
);

CREATE TABLE songs(
	song_id SERIAL PRIMARY KEY,
	place_id INT NOT NULL,
	user_id INT NOT NULL,
	song_name CHAR(50),
	FOREIGN KEY (place_id) REFERENCES places(place_id),
	FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE likes(
	like_id SERIAL PRIMARY KEY,
	user_id INT NOT NULL,
	song_id INT NOT NULL,
	type BOOLEAN NOT NULL DEFAULT TRUE,
	FOREIGN KEY (user_id) REFERENCES users(user_id)
);
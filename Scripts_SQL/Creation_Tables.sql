CREATE TABLE streamers (
    streamers_id INT AUTO_INCREMENT PRIMARY KEY,
    streamers_login VARCHAR(255) NOT NULL,
    streamers_nombre_followers INT,
    streamers_twitch_id INT NOT NULL
);

CREATE TABLE abonnements (
    abonnements_streamer_id INT NOT NULL,
	abonnements_follower_id INT NOT NULL,
    CONSTRAINT fk_streamer FOREIGN KEY (abonnements_streamer_id) REFERENCES streamers(streamers_id)
);
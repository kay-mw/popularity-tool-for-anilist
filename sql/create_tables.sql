CREATE TABLE anime_info
(
    anime_id      INT PRIMARY KEY,
    average_score INT           NOT NULL,
    title_romaji  NVARCHAR(256) NOT NULL
);

CREATE TABLE user_info
(
    user_id      INT PRIMARY KEY,
    user_name    NVARCHAR(20) NOT NULL,
    request_date DATETIME     NOT NULL
);

CREATE TABLE user_anime_score
(
    user_anime_id INT IDENTITY(1,1) PRIMARY KEY,
    user_id       INT NOT NULL,
    anime_id      INT NOT NULL,
    user_score    INT NOT NULL,
    CONSTRAINT FK_user_info FOREIGN KEY (user_id)
        REFERENCES user_info (user_id),
    CONSTRAINT FK_anime_info FOREIGN KEY (anime_id)
        REFERENCES anime_info (anime_id)
);


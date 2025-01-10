CREATE TABLE anime_info
(
    anime_id      INT PRIMARY KEY,
    average_score INT          NOT NULL,
    title_romaji  VARCHAR(256) NOT NULL,
    genres        JSON         NOT NULL
);

CREATE TABLE manga_info
(
    manga_id      INT PRIMARY KEY,
    average_score INT          NOT NULL,
    title_romaji  VARCHAR(256) NOT NULL,
    genres        JSON         NOT NULL
);

CREATE TABLE user_info
(
    user_id      INT PRIMARY KEY,
    user_name    VARCHAR(20) NOT NULL,
    request_date DATETIME    NOT NULL
);

CREATE TABLE user_anime_score
(
    user_anime_id INT IDENTITY(1,1) PRIMARY KEY,
    user_id       INT      NOT NULL,
    anime_id      INT      NOT NULL,
    user_score    INT      NOT NULL,
    start_date    DATETIME NOT NULL,
    end_date      DATETIME,
    CONSTRAINT FK_user_info FOREIGN KEY (user_id)
        REFERENCES user_info (user_id),
    CONSTRAINT FK_anime_info FOREIGN KEY (anime_id)
        REFERENCES anime_info (anime_id)
);

CREATE TABLE user_manga_score
(
    user_manga_id INT IDENTITY(1,1) PRIMARY KEY,
    user_id       INT      NOT NULL,
    manga_id      INT      NOT NULL,
    user_score    INT      NOT NULL,
    start_date    DATETIME NOT NULL,
    end_date      DATETIME,
    CONSTRAINT MFK_user_info FOREIGN KEY (user_id)
        REFERENCES user_info (user_id),
    CONSTRAINT MFK_manga_info FOREIGN KEY (manga_id)
        REFERENCES manga_info (manga_id)
);


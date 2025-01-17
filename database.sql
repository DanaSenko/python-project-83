
CREATE TABLE IF NOT EXISTS urls (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(255) NOT NULL,
    created_at DATE DEFAULT CURRENT_DATE
);

CREATE TABLE IF NOT EXISTS url_checks (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    url_id BIGINT NOT NULL,
    status_code INT NOT NULL,
    h1 VARCHAR(255),
    title text,
    description text,
    created_at DATE DEFAULT CURRENT_DATE,
    CONSTRAINT fk_url
        FOREIGN KEY (url_id)
        REFERENCES urls (id)
        ON DELETE CASCADE
);

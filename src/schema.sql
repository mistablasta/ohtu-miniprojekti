CREATE TABLE entry (
  id SERIAL PRIMARY KEY,
  title TEXT,
  year INTEGER,
  author TEXT,
  publisher TEXT,
  field TEXT
);

CREATE TABLE entries (
    id SERIAL PRIMARY KEY,
    key TEXT NOT NULL,
    type TEXT NOT NULL,
    fields JSONB NOT NULL
);

CREATE TABLE todos (
  id SERIAL PRIMARY KEY, 
  content TEXT NOT NULL,
  done BOOLEAN DEFAULT FALSE
);

CREATE TABLE entry (
  id SERIAL PRIMARY KEY,
  title TEXT,
  year INTEGER,
  author TEXT,
  publisher TEXT,
  field TEXT
);
PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS books (
 id INTEGER PRIMARY KEY, title TEXT NOT NULL CHECK(length(title) BETWEEN 1 AND 120),
 author TEXT NOT NULL CHECK(length(author) BETWEEN 1 AND 100),
 copies INTEGER NOT NULL CHECK(copies BETWEEN 1 AND 999)
);
CREATE TABLE IF NOT EXISTS readers (
 id INTEGER PRIMARY KEY, name TEXT NOT NULL CHECK(length(name) BETWEEN 1 AND 100),
 code TEXT NOT NULL UNIQUE CHECK(length(code) BETWEEN 1 AND 30)
);
CREATE TABLE IF NOT EXISTS loans (
 id INTEGER PRIMARY KEY,
 book_id INTEGER NOT NULL REFERENCES books(id),
 reader_id INTEGER NOT NULL REFERENCES readers(id),
 borrowed_on TEXT NOT NULL, due_on TEXT NOT NULL CHECK(due_on >= borrowed_on),
 returned_on TEXT CHECK(returned_on IS NULL OR returned_on >= borrowed_on)
);
CREATE INDEX IF NOT EXISTS idx_loans_book ON loans(book_id, returned_on);
CREATE INDEX IF NOT EXISTS idx_loans_due ON loans(due_on) WHERE returned_on IS NULL;

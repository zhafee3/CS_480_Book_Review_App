DROP DATABASE IF EXISTS book_reviews;
CREATE DATABASE book_reviews;
USE book_reviews;

CREATE TABLE Users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email_address VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);
-- Create Table for Books
CREATE TABLE Books (
    isbn VARCHAR(20) PRIMARY KEY,
    title VARCHAR(255),
    author VARCHAR(255),
    genre VARCHAR(255),
    publisher VARCHAR(255),
    publication_year YEAR,
    page_count INT
);

CREATE TABLE Reviews (
    id INT AUTO_INCREMENT PRIMARY KEY,
    book_id VARCHAR(20) NOT NULL,
    user_id INT NOT NULL,
    rating INT,
    written_review VARCHAR(500),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (book_id) REFERENCES Books (isbn),
    FOREIGN KEY (user_id) REFERENCES Users (id)
);

-- Create Table for Reviews
CREATE TABLE Favorites (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    book_id VARCHAR(20) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users (id),
    FOREIGN KEY (book_id) REFERENCES Books (isbn),
    UNIQUE (user_id, book_id)
);



-- Create Table for Book Requests
CREATE TABLE BookRequests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    isbn VARCHAR(20) NOT NULL,
    request_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'Pending',
    FOREIGN KEY (user_id) REFERENCES Users (id),
    FOREIGN KEY (isbn) REFERENCES Books (isbn)
);

CREATE INDEX idx_users_username ON Users (username);
CREATE INDEX idx_users_email ON Users (email_address);
CREATE INDEX idx_users_password ON Users (password);
#CREATE INDEX idx_users_role ON Users (role);


CREATE INDEX idx_books_title ON Books (title);
CREATE INDEX idx_books_isbn ON Books (isbn);
CREATE INDEX idx_books_publisher ON Books (publisher);
#CREATE INDEX idx_books_publication_year ON Books (publication_year);
#CREATE INDEX idx_books_page_count ON Books (page_count);


CREATE INDEX idx_reviews_book_id ON Reviews (book_id);
CREATE INDEX idx_reviews_user_id ON Reviews (user_id);
CREATE INDEX idx_reviews_rating ON Reviews (rating);
CREATE INDEX idx_reviews_written_review ON Reviews (written_review);


CREATE INDEX idx_favorites_user_id ON Favorites (user_id);
CREATE INDEX idx_favorites_book_id ON Favorites (book_id);

CREATE INDEX idx_bookrequests_user_id ON BookRequests (user_id);
CREATE INDEX idx_bookrequests_isbn ON BookRequests (isbn);
CREATE INDEX idx_bookrequests_request_date ON BookRequests (request_date);
CREATE INDEX idx_bookrequests_status ON BookRequests (status);


INSERT INTO Users (username, email_address, password) VALUES
('user1', 'user1@example.com', 'password123'),
('user2', 'user2@example.com', 'password123'),
('admin1', 'admin1@example.com', 'adminpass');

-- Insert Test Data into Books Table

INSERT INTO Books (isbn, title, author, genre, publisher, publication_year, page_count) VALUES
('1234567890123', 'Book A', 'Author A', 'Fiction', 'Publisher A', 2020, 300),
('9876543210987', 'Book B', 'Author B', 'Mystery', 'Publisher B', 2018, 250),
('4567891234567', 'Book C', 'Author C', 'Sci-Fi', 'Publisher C', 2022, 400);

-- Insert Test Data into Reviews Table
INSERT INTO Reviews (book_id, user_id, rating, written_review) VALUES
('1234567890123', 1, 5, 'An amazing book, highly recommend!'),
('9876543210987', 2, 4, 'Very interesting, but a bit slow in the middle.'),
('4567891234567', 1, 3, 'Decent read, but could be better.');

-- Insert Test Data into Favorites Table
INSERT INTO Favorites (user_id, book_id) VALUES
(1, '1234567890123'),
(1, '9876543210987'),
(2, '4567891234567');

-- Insert Test Data into Book Requests Table
INSERT INTO BookRequests (user_id, isbn) VALUES
(1, '1234567890123'),
(2, '9876543210987');



SELECT * FROM Users;
SELECT * FROM Books;
SELECT * FROM Reviews;
SELECT * FROM Favorites;
SELECT * FROM BookRequests;


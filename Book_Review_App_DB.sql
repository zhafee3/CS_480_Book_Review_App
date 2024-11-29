CREATE TABLE Users (
    username VARCHAR(50) PRIMARY KEY UNIQUE,
    email_address VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL UNIQUE
);

-- Create Table for Books
CREATE TABLE Books (
    isbn VARCHAR(20) PRIMARY KEY,
    title VARCHAR(255),
    author VARCHAR(255),
    genre VARCHAR(255),
    publisher VARCHAR(255),
    publicationyear YEAR,
    pagecount INT
);

-- Create Table for Reviews
CREATE TABLE Reviews (
    id INT PRIMARY KEY,
    book_id INT NOT NULL,
    user_id INT NOT NULL,
    rating INT,
    written_review VARCHAR(500),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (book_id) REFERENCES Books (isbn)
    #FOREIGN KEY (user_id) REFERENCES Users (id)
);

-- Create Table for Favorites
CREATE TABLE Favorites (
    id INT PRIMARY KEY,
    user_id INT NOT NULL,
    book_id INT NOT NULL,
    #FOREIGN KEY (user_id) REFERENCES Users (id),
    #FOREIGN KEY (book_id) REFERENCES Books (id),
    UNIQUE (user_id, book_id)
);

-- Create Table for Book Requests
CREATE TABLE BookRequests (
    id INT PRIMARY KEY,
    user_id INT NOT NULL,
    isbn VARCHAR(13) NOT NULL,
    request_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'Pending'
    #FOREIGN KEY (user_id) REFERENCES Users (id)
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
#INSERT INTO Users (id, username, email_address, password, role) VALUES

('user1', 'user1@example.com', 'password123'),
('user2', 'user2@example.com', 'password123'),
('admin1', 'admin1@example.com', 'adminpass');

-- Insert Test Data into Books Table
#INSERT INTO Books (isbn, title, isbn, publisher, publicationyear, pagecount) VALUES
#(1, 'Book A', '1234567890123', 'Publisher A', 2020, 300),
#(2, 'Book B', '9876543210987', 'Publisher B', 2018, 250),
#(3, 'Book C', '4567891234567', 'Publisher C', 2022, 400);

-- Insert Test Data into Reviews Table
INSERT INTO Reviews (id, book_id, user_id, rating, written_review) VALUES
(1, 1, 1, 5, 'An amazing book, highly recommend!'),
(2, 2, 2, 4, 'Very interesting, but a bit slow in the middle.'),
(3, 3, 1, 3, 'Decent read, but could be better.');

-- Insert Test Data into Favorites Table
INSERT INTO Favorites (id, user_id, book_id) VALUES
(1, 1, 1),
(2, 1, 2),
(3, 2, 3);

-- Insert Test Data into Book Requests Table
INSERT INTO BookRequests (id, user_id, isbn) VALUES
(1, 1, '1122334455667'),
(2, 2, '9988776655443');



SELECT * FROM Users;
SELECT * FROM Books;
SELECT * FROM Reviews;
SELECT * FROM Favorites;
SELECT * FROM BookRequests;


USE yes24;
 
-- CREATE TABLE Books (
--     bookID INT AUTO_INCREMENT PRIMARY KEY,
--     title VARCHAR(255) NOT NULL,
--     author VARCHAR(255),
--     publisher VARCHAR(255),
--     publishing DATE,
--     rating DECIMAL(3, 1),
--     reviews INT,
--     sales INT,
--     price DECIMAL(10, 2),
--     ranking INT,
--     ranking_weeks INT
-- );

-- SELECT title, author FROM books;
-- SELECT * FROM books WHERE rating >= 8.0;
-- SELECT title, reviews FROM books WHERE reviews >= 100 ORDER BY reviews DESC;
-- SELECT title, price FROM books WHERE price <= 20000;
-- SELECT * FROM books WHERE ranking_weeks >= 4 ORDER BY ranking_weeks DESC;
-- SELECT * FROM books WHERE author = '최진영 저'
-- SELECT * FROM books WHERE publisher = '은행나무'

-- SELECT author, COUNT(*) AS books_count FROM books GROUP BY author ORDER BY books_count DESC;
-- SELECT publisher, COUNT(*) AS publishing_count FROM books GROUP BY publisher
-- ORDER BY publishing_count;
-- SELECT author, AVG(rating) AS rating_avg FROM books GROUP BY author ORDER BY rating_avg;
-- SELECT * FROM books WHERE ranking = 1;
-- SELECT title, sales, reviews FROM books ORDER BY sales DESC, reviews DESC LIMIT 10;
-- SELECT * FROM books ORDER BY publishing DESC LIMIT 5;

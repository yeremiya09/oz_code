USE yes24;

-- SELECT author, AVG(rating) FROM Books GROUP BY author;
-- SELECT publishing, COUNT(*) FROM Books GROUP BY publishing;
-- SELECT title, AVG(price) FROM Books GROUP BY title;
-- SELECT title, reviews FROM Books ORDER BY reviews DESC LIMIT 5;
-- SELECT ranking, AVG(reviews) FROM Books GROUP BY ranking;

-- SELECT title, rating FROM Books WHERE rating > (SELECT AVG(rating) FROM Books);
-- SELECT title, price FROM Books WHERE price > (SELECT AVG(price) FROM Books);
-- SELECT title, reviews FROM Books WHERE reviews > (SELECT MAX(reviews) FROM Books);
-- SELECT title, sales FROM Books WHERE sales < (SELECT AVG(sales) FROM Books);
-- SELECT title, publishing FROM Books WHERE author = (SELECT author FROM Books GROUP BY author ORDER BY COUNT(*) DESC LIMIT 1) ORDER BY publishing DESC LIMIT 1;
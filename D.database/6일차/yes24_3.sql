USE yes24;
SET SQL_SAFE_UPDATES = 0;
 
-- UPDATE Books SET price = 30000 WHERE title = '천국';
-- UPDATE Books SET title = '영원한 천국' WHERE author = '정유정 저';
-- DELETE FROM Books WHERE sales = (SELECT MIN(sales) FROM Books);

-- # 최소 sales 값을 변수에 저장
-- SET @min_sales = (SELECT MIN(sales) FROM Books);

-- # 변수를 이용해 삭제
-- DELETE FROM Books WHERE sales = @min_sales;


-- UPDATE Books SET rating = rating + 1 WHERE publisher = '은행나무';
-- SELECT * FROM books WHERE rating >= 8.0;
-- SELECT author, AVG(rating) as avg_rating, AVG(sales) as avg_sales FROM Books GROUP BY author;
-- SELECT publishing, AVG(price) as avg_price FROM Books GROUP BY publishing;
-- SELECT publisher, COUNT(*) as num_books, AVG(reviews) as avg_reviews FROM Books GROUP BY publisher;
-- SELECT ranking, AVG(sales) as avg_sales FROM Books GROUP BY ranking;
-- SELECT price, AVG(reviews) as avg_reviews, AVG(rating) as avg_rating FROM Books GROUP BY price;
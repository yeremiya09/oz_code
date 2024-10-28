USE mydatabase;

-- CREATE TABLE employees (
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     name VARCHAR(100),
--     position VARCHAR(100),
--     salary DECIMAL(10, 2)
-- );
-- SELECT * FROM employees;

-- SELECT name, salary FROM employees WHERE position = 'Frontend' AND salary <= 90000;
-- Safe Update Mode 비활성화
SET SQL_SAFE_UPDATES = 0;

-- 해당 쿼리 실행
UPDATE employees SET salary = salary * 1.10 WHERE position = 'PM';
SELECT * FROM employees WHERE position = 'Quality Assurance';
-- Safe Update Mode 다시 활성화 (권장)
UPDATE employees SET salary = salary * 1.05 WHERE position = 'Backend';
DELETE FROM employees WHERE name = '민혁';
SET SQL_SAFE_UPDATES = 1;
SELECT position, AVG(salary) AS average_salary FROM employees GROUP BY position;
DROP TABLE employees; 



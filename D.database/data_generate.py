import mysql.connector
from faker import Faker
import random

# 데이터베이스 연결 설정
try:
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="class-password",
        database="mydatabase"
    )
    cursor = db_connection.cursor()
    print("DB 연결 성공")
except mysql.connector.Error as err:
    print(f"DB 연결 오류: {err}")
    exit()

    faker = Faker()

# Users 테이블에 데이터 삽입
    for i in range(100):
        username = faker.user_name()
        email = faker.email()

        sql = "INSERT INTO users (username, email) VALUES (%s, %s)"
        values = (username, email)

    try:
        cursor.execute(sql, values)
    except mysql.connector.Error as err:
        print(f"사용자 데이터 삽입 오류: {err}")
        continue  # 오류 발생 시 해당 루프는 건너뛰고 다음 루프로

# 유효한 사용자 ID 가져오기
try:
    cursor.execute("SELECT user_id FROM users")
    valid_user_ids = [row[0] for row in cursor.fetchall()]
    if not valid_user_ids:
        raise ValueError("유효한 사용자 ID를 찾을 수 없습니다.")
except mysql.connector.Error as err:
    print(f"유효한 사용자 ID 조회 오류: {err}")
    db_connection.close()
    exit()

# Orders 테이블에 데이터 삽입
for i in range(100):
    user_id = random.choice(valid_user_ids)
    product_name = faker.word()
    quantity = random.randint(1, 10)

    sql = "INSERT INTO orders(user_id, product_name, quantity) VALUES (%s, %s, %s)"
    values = (user_id, product_name, quantity)

    try:
        cursor.execute(sql, values)
    except mysql.connector.Error as err:
        print(f"주문 데이터 삽입 오류: {err}")
        continue  # 오류 발생 시 해당 루프 건너뛰기

# 데이터베이스 커밋 및 연결 종료
try:
    db_connection.commit()
    print("변경사항 커밋 완료")
except mysql.connector.Error as err:
    print(f"커밋 오류: {err}")
finally:
    cursor.close()
    db_connection.close()
    print("DB 연결 종료")

   

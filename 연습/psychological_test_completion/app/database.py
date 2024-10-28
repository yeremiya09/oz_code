from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# 이 코드는 Flask-SQLAlchemy를 사용하여 SQLAlchemy 객체를 생성하는 코드입니다. 이 객체는 Flask 애플리케이션에서 데이터베이스와 상호작용하기 위해 사용됩니다. 하나씩 설명해보겠습니다.

# 1. from flask_sqlalchemy import SQLAlchemy
# 역할: Flask-SQLAlchemy 라이브러리에서 SQLAlchemy 클래스를 가져옵니다. 이 클래스는 데이터베이스와의 상호작용을 추상화하는 ORM(Object Relational Mapper) 기능을 제공합니다.
# ORM이란?: ORM은 객체 지향 프로그래밍 언어의 객체를 데이터베이스의 테이블과 매핑하는 기술입니다. 즉, SQL 쿼리를 직접 작성하지 않고, 파이썬 클래스를 통해 데이터베이스 작업을 할 수 있게 해줍니다.

# 2. db = SQLAlchemy()
# 역할: SQLAlchemy의 인스턴스를 생성하여 db라는 객체에 할당합니다. 이 객체는 애플리케이션의 데이터베이스 작업(데이터 삽입, 수정, 삭제, 조회 등)을 관리하는 역할을 합니다.
# 왜 필요한가?: Flask는 기본적으로 데이터베이스와 통합되지 않으므로 Flask-SQLAlchemy를 통해 Flask 애플리케이션과 데이터베이스를 연결하고, 객체 지향적으로 데이터베이스 작업을 수행할 수 있게 합니다.
# 사용 방법 예시
# 데이터베이스 연결: 생성된 db 객체는 Flask 애플리케이션과 연결된 데이터베이스에 대한 모든 작업을 담당합니다. 데이터베이스 설정은 Flask 애플리케이션의 설정 파일에서 SQLALCHEMY_DATABASE_URI를 통해 지정할 수 있습니다.

# python
# 코드 복사
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
# db = SQLAlchemy(app)

# 모델 정의: db 객체는 데이터베이스 모델을 정의할 때 사용됩니다. 위에서 보여준 Participant, Admin, Question, Quiz와 같은 클래스를 정의할 때 db.Model을 상속받아 테이블을 정의합니다.

# python
# 코드 복사
# class Participant(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50))
#     age = db.Column(db.Integer)
#     gender = db.Column(db.String(10))

# 데이터베이스 작업: db 객체는 데이터 삽입, 삭제, 업데이트 등의 작업을 수행할 수 있게 해줍니다.

# python
# 코드 복사
# # 데이터 삽입
# new_participant = Participant(name="John", age=25, gender="Male")
# db.session.add(new_participant)
# db.session.commit()

# 데이터베이스 초기화: 앱이 시작할 때 db.create_all()을 호출하면, 정의된 모델에 따라 데이터베이스 테이블이 생성됩니다.

# python
# 코드 복사
# with app.app_context():
#     db.create_all()  # 데이터베이스 테이블을 생성

# 따라서 db = SQLAlchemy()는 데이터베이스와 상호작용할 수 있는 핵심 객체를 생성하며, 이 객체를 통해 Flask 애플리케이션에서 데이터베이스 작업을 간편하게 처리할 수 있게 해줍니다.
from flask import Flask
from flask_migrate import Migrate
from flask.cli import with_appcontext
import os
import click
from .database import db
from .models import Question, Admin, Participant  # Question 모델 임포트
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
# 이 코드는 Flask 기반 애플리케이션에서 데이터베이스 설정 및 초기화, 관리 기능을 담당하는 부분입니다. 
# 주로 데이터베이스 관련 설정 및 초기 데이터를 추가하는 기능을 수행하며, SQLite를 사용하고 있습니다. 각 구성 요소를 상세하게 설명하겠습니다.

def create_app():
    app = Flask(__name__)
    app.secret_key = "oz_coding_secret"

# 1. Flask 애플리케이션 생성 및 기본 설정

# app = Flask(__name__): Flask 애플리케이션 인스턴스를 생성합니다.
# app.secret_key = "oz_coding_secret": 세션 및 쿠키 데이터 암호화에 사용되는 비밀 키를 설정합니다. 보안 목적으로 필수적인 설정입니다.

    # 데이터베이스 파일 경로 설정 및 앱 설정
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    dbfile = os.path.join(basedir, "db.sqlite")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + dbfile
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# 2. 데이터베이스 설정
# basedir 및 dbfile: 프로젝트의 루트 디렉토리에서 SQLite 데이터베이스 파일의 경로를 계산합니다.
# os.path.abspath: 파일의 절대 경로를 계산.
# os.path.dirname: 상위 디렉토리 경로를 얻음.
# os.path.join: 경로를 결합해 db.sqlite 파일 경로를 생성합니다.
# app.config["SQLALCHEMY_DATABASE_URI"]: SQLite 데이터베이스 URI를 설정하여 Flask와 데이터베이스를 연결합니다.
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]: SQLAlchemy의 변경 사항 추적 기능을 비활성화합니다. 불필요한 리소스 낭비를 막기 위해 사용됩니다.

    # 데이터베이스 및 마이그레이션 초기화
    db.init_app(app)
    migrate = Migrate(app, db)
# 3. 데이터베이스 초기화 및 마이그레이션 설정
# db.init_app(app): 데이터베이스 객체를 Flask 애플리케이션에 연결하여 초기화합니다.
# Migrate(app, db): Flask-Migrate를 사용하여 데이터베이스 마이그레이션을 관리합니다. 
# 마이그레이션은 데이터베이스 스키마 변경 사항을 손쉽게 적용하기 위한 기능입니다.

    # 라우트(블루프린트) 등록
    from .routes import main as main_blueprint
    from .routes import admin as admin_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(admin_blueprint)
# 4. 라우트(블루프린트) 등록

# from .routes import: routes 모듈에서 두 개의 블루프린트를 가져옵니다.
# 블루프린트 등록: Flask 블루프린트는 라우트를 모듈화할 수 있는 기능을 제공하여 코드 구조를 개선하고 유지 관리를 용이하게 만듭니다. 
# 여기서는 main과 admin 블루프린트를 애플리케이션에 등록합니다.


    # 초기화 명령어 정의
    def add_initial_questions():
        initial_questions = [
            "오즈코딩스쿨에 대해서 알고 계신가요?",
            "프론트엔드 과정에 참여하고 계신가요?",
            "전공자 이신가요?",
            "프로젝트를 진행해보신적 있으신가요?",
            "개발자로 일한 경력이 있으신가요?",
        ]
        yesterday = datetime.now(datetime.timezone.utc) - timedelta(days=1)  # 어제 날짜 계산

# 5. 데이터베이스 초기화 및 기본 데이터 추가 
# utcnow 이제는 권장되지 않는 방식 기존 방식 (경고 발생)
# now = datetime.datetime.utcnow()
# 권장 방식 (시간대 정보 포함)
# now = datetime.datetime.now(datetime.timezone.utc)

# add_initial_questions(): 이 함수는 기본 데이터를 데이터베이스에 추가하는 역할을 합니다. 
# 특히 기본 질문과 관리자 계정 및 참가자 정보를 추가합니다.
# initial_questions 리스트: 추가할 기본 질문을 정의합니다.
# yesterday: UTC 기준으로 어제 날짜를 계산하여 나중에 참가자 생성 시 사용할 수 있도록 준비합니다.

        # 관리자 계정 추가 로직, 비밀번호 해시 처리 적용
        existing_admin = Admin.query.filter_by(username="admin").first()
        if not existing_admin:
            hashed_password = generate_password_hash("0000")  # 비밀번호를 해시 처리
            new_admin = Admin(username="admin", password=hashed_password)
            db.session.add(new_admin)

        participants_without_created_at = Participant.query.filter(
            Participant.created_at == None
        ).all()

        for participant in participants_without_created_at:
            participant.created_at = yesterday
# 6. 관리자 계정 생성 및 참가자 정보 수정

# 관리자 계정 추가: Admin 테이블에서 username이 "admin"인 계정을 찾고, 없으면 새 관리자 계정을 추가합니다. 
# 비밀번호는 generate_password_hash()로 해시하여 보안성을 높입니다.
# 참가자 정보 수정: Participant 테이블에서 created_at 필드가 비어 있는 참가자들을 찾아 어제 날짜로 채웁니다.

        for question_content in initial_questions:
            existing_question = Question.query.filter_by(
                content=question_content
            ).first()
            if not existing_question:
                new_question = Question(content=question_content)
                db.session.add(new_question)
        questions = Question.query.all()
        for question in questions:
            question.order_num = question.id
            question.is_active = True  # 모든 질문을 활성화 상태로 설정
        db.session.commit()
# 7. 질문 추가 및 수정

# 질문 추가: 기본 질문 리스트에서 각 질문을 확인한 뒤, 데이터베이스에 해당 질문이 없으면 새 질문을 추가합니다.
# 질문 수정: 모든 질문의 order_num을 id로 설정하고, 모든 질문을 활성화(is_active = True) 상태로 만듭니다.
# db.session.commit(): 모든 변경 사항을 데이터베이스에 커밋하여 저장합니다.

    @click.command("init-db")
    @with_appcontext
    def init_db_command():
        db.create_all()
        add_initial_questions()
        click.echo("Initialized the database.")
# 8. 커맨드 라인 명령어 정의

# @click.command("init-db"): Flask에서 CLI(커맨드 라인 인터페이스) 명령어를 정의하는 데 사용됩니다. 
# init-db 명령어를 정의하여 데이터베이스를 초기화하고 기본 데이터를 추가할 수 있습니다.
# @with_appcontext: Flask 애플리케이션 컨텍스트 안에서 해당 명령어가 실행될 수 있도록 보장합니다.
# db.create_all(): 모든 데이터베이스 테이블을 생성합니다.
# click.echo("Initialized the database."): 데이터베이스 초기화가 완료되면 사용자에게 완료 메시지를 출력합니다.

    app.cli.add_command(init_db_command)
# 9. 명령어 추가

# app.cli.add_command(): 앞서 정의한 init-db 명령어를 Flask 애플리케이션에 CLI 명령어로 추가하여, 개발자가 커맨드 라인에서 flask init-db 명령어를 실행할 수 있게 만듭니다.

    return app

# 10. 전체 흐름 요약
# 앱 생성: create_app() 함수는 Flask 애플리케이션을 생성하고 설정합니다.
# DB 설정: SQLite 데이터베이스 경로를 설정하고, SQLAlchemy 및 Flask-Migrate를 초기화합니다.
# 라우트 설정: main과 admin 블루프린트를 앱에 등록합니다.
# 기본 데이터 추가: add_initial_questions() 함수는 기본 질문과 관리자 계정을 생성 및 수정합니다.
# CLI 명령어 등록: init-db 명령어는 데이터베이스를 초기화하고 기본 데이터를 삽입하는 작업을 처리합니다.
# 이 코드는 Flask 애플리케이션의 데이터베이스 설정과 초기화에 관한 전반적인 흐름을 처리하며, 기본적인 질문과 관리자 계정을 데이터베이스에 추가하는 등의 초기 설정 작업을 담당합니다.
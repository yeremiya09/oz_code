from app import create_app

application = create_app()

if __name__ == "__main__":
    application.run()

# 이 코드는 Flask 애플리케이션을 실행하는 진입점(entry point)으로, Flask 애플리케이션을 시작하기 위한 설정을 정의하고 있습니다. 세부적으로 하나씩 설명하겠습니다.

# 1. from app import create_app
# 역할: app이라는 모듈에서 create_app이라는 함수를 가져옵니다. 이 함수는 일반적으로 Flask 애플리케이션 인스턴스를 생성하고, 설정 및 블루프린트, 데이터베이스 연결 등을 초기화하는 역할을 합니다.

# 왜 필요한가?: Flask는 애플리케이션을 객체로 관리하기 때문에, create_app 같은 팩토리 함수에서 설정을 캡슐화하는 방식이 많이 사용됩니다. 이렇게 하면 여러 환경(개발, 테스트, 운영)에 맞춰 설정을 손쉽게 변경할 수 있고, 앱의 모듈성을 높일 수 있습니다.

# python
# 코드 복사
# # app/__init__.py 파일 내부에 있을 가능성이 높은 코드
# from flask import Flask

# def create_app():
#     app = Flask(__name__)

#     # 애플리케이션 설정 및 초기화
#     app.config.from_pyfile('config.py')  # 외부 설정 파일을 로드하는 예시

#     # 블루프린트 등록 (모듈별로 나눈 라우팅 파일이 있을 경우)
#     from .main import main as main_blueprint
#     app.register_blueprint(main_blueprint)

#     return app

# 팩토리 패턴: 애플리케이션을 생성하는 함수는 "애플리케이션 팩토리"라고 불리는 패턴을 따릅니다. 이 패턴은 여러 환경에 맞게 Flask 인스턴스를 동적으로 생성할 수 있게 도와줍니다. 예를 들어, 개발 환경과 배포 환경에서 다른 설정을 쉽게 적용할 수 있습니다.

# 2. application = create_app()
# 역할: create_app 함수를 호출하여 애플리케이션 인스턴스를 생성하고, 이를 application이라는 변수에 할당합니다. 이제 application은 Flask 애플리케이션 자체를 나타냅니다.

# 왜 변수명이 application인가?: 일반적으로 WSGI(Web Server Gateway Interface) 서버에서는 애플리케이션 객체를 application으로 정의하는 것을 권장합니다. 이 때문에 많은 Flask 프로젝트에서는 application이라는 변수를 사용하지만, 사실 app이나 다른 변수명을 사용해도 무방합니다. 다만 WSGI 표준에 맞추기 위해 이처럼 사용합니다.

# 3. if __name__ == "__main__":
# 역할: 이 부분은 스크립트가 직접 실행될 때만 아래의 코드를 실행하도록 합니다. __name__은 파이썬 모듈이 실행되는 방식을 나타내는 특별한 변수입니다.

# 직접 실행 vs 모듈로 실행: 파이썬에서 스크립트가 직접 실행되면 __name__ 변수는 "__main__"으로 설정됩니다. 하지만 모듈로 임포트될 경우, __name__ 변수는 모듈 이름(예: app)이 됩니다.

# 4. application.run()
# 역할: Flask 개발 서버를 시작하는 명령어입니다. run() 메서드는 Flask 앱을 실행하며, 기본적으로 localhost에서 실행되며 포트는 5000번을 사용합니다. 예를 들어, http://127.0.0.1:5000에서 애플리케이션에 접근할 수 있습니다.

# 개발 모드 vs 프로덕션 모드: 이 코드는 Flask의 기본 개발 서버를 실행하지만, 실제 배포 환경에서는 WSGI 서버(예: gunicorn, uWSGI)를 통해 실행해야 합니다. application.run()은 개발 중에만 사용되는 간단한 서버이므로, 배포 시에는 사용하지 않는 것이 좋습니다.

# 전체 코드 흐름
# 애플리케이션 팩토리 호출: create_app() 함수를 통해 Flask 애플리케이션 인스턴스를 생성합니다.
# 개발 서버 실행: 이 스크립트가 직접 실행될 경우, Flask의 기본 개발 서버를 실행하여 애플리케이션을 구동합니다.

# 예시: 실제 create_app()이 어떻게 활용되는지
# python
# 코드 복사
# # app/__init__.py
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()

# def create_app():
#     app = Flask(__name__)
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
    
#     db.init_app(app)  # 데이터베이스 초기화
    
#     # 블루프린트 등록
#     from .routes import main as main_blueprint
#     app.register_blueprint(main_blueprint)
    
#     return app

# 그리고 이 코드를 실행하는 스크립트가 있을 때:

# python
# 코드 복사
# # run.py
# from app import create_app

# application = create_app()

# if __name__ == "__main__":
#     application.run(debug=True)  # 디버그 모드로 실행
# 이처럼 create_app을 통해 앱을 생성하고, application.run()으로 서버를 구동하게 됩니다.
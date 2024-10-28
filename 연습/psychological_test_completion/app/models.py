from .database import db
from datetime import datetime

# 1. Participant 클래스
# 테이블 이름: participant
# 기능: 참가자의 정보를 저장하는 테이블입니다.
class Participant(db.Model):
    __tablename__ = "participant"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
# 필드 설명:
# id: 각 참가자를 고유하게 식별하는 필드로, 기본키(primary_key)입니다.
# name: 참가자의 이름을 저장하는 문자열 필드로, 최대 50자의 이름을 입력할 수 있습니다.
# age: 참가자의 나이를 저장하는 정수형 필드입니다.
# gender: 참가자의 성별을 저장하는 문자열 필드로, 최대 10자까지 가능합니다.
# created_at: 참가자가 등록된 시간을 저장하며, 디폴트로 현재 시간이 자동 저장됩니다.


# 2. Admin 클래스
# 테이블 이름: admin
# 기능: 관리자 계정 정보를 저장하는 테이블입니다.
class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
# 필드 설명:
# id: 관리자를 고유하게 식별하는 필드로, 기본키입니다.
# username: 관리자의 사용자명을 저장하는 필드입니다.
# password: 관리자의 비밀번호를 저장하는 필드입니다.


# 3. Question 클래스
# 테이블 이름: question
# 기능: 퀴즈에서 사용되는 질문 정보를 저장하는 테이블입니다.
class Question(db.Model):
    __tablename__ = "question"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255))
    order_num = db.Column(db.Integer, default=0)  
    is_active = db.Column(db.Boolean, default=True)
# 필드 설명:
# id: 각 질문을 고유하게 식별하는 필드로, 기본키입니다.
# content: 질문의 내용을 저장하는 필드로, 최대 255자의 문자열입니다.
# order_num: 질문이 퀴즈에서 표시되는 순서를 나타내는 정수 필드입니다. 기본값은 0이며, 작은 값일수록 먼저 표시됩니다.
# is_active: 해당 질문이 활성화 상태인지 여부를 나타내는 필드입니다. True일 경우 활성화된 질문으로 간주됩니다.


# 4. Quiz 클래스
# 테이블 이름: quiz
# 기능: 각 참가자가 제출한 퀴즈 응답을 저장하는 테이블입니다.
class Quiz(db.Model):
    __tablename__ = "quiz"
    id = db.Column(db.Integer, primary_key=True)
    participant_id = db.Column(db.Integer, db.ForeignKey("participant.id"))
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"))
    chosen_answer = db.Column(db.String(255))

    participant = db.relationship("Participant", backref="quizzes")
    question = db.relationship("Question", backref="quizzes")
# 필드 설명:
# id: 각 퀴즈 응답을 고유하게 식별하는 필드로, 기본키입니다.
# participant_id: 참가자의 ID를 저장하는 필드입니다. ForeignKey("participant.id")로 Participant 테이블과 연결된 외래키입니다.
# question_id: 질문의 ID를 저장하는 필드입니다. ForeignKey("question.id")로 Question 테이블과 연결된 외래키입니다.
# chosen_answer: 참가자가 선택한 답변을 저장하는 문자열 필드입니다.

# 관계 설명:
# participant: Quiz 테이블과 Participant 테이블 간의 관계를 정의합니다. backref="quizzes"는 해당 참가자가 제출한 퀴즈 응답들을 참조할 수 있는 역참조를 생성합니다.
# question: Quiz 테이블과 Question 테이블 간의 관계를 정의합니다. backref="quizzes"는 해당 질문에 답변된 퀴즈 응답들을 참조할 수 있는 역참조를 생성합니다.

# 데이터베이스 관계 설명
# Participant와 Quiz는 1
# (일대다) 관계입니다. 즉, 하나의 참가자는 여러 개의 퀴즈 응답을 제출할 수 있습니다.
# Question과 Quiz도 1
# (일대다) 관계입니다. 즉, 하나의 질문은 여러 참가자들에 의해 여러 번 답변될 수 있습니다.
# 이 코드는 총 네 개의 테이블(Participant, Admin, Question, Quiz)을 정의하며, 각 테이블은 참가자, 관리자, 질문, 그리고 퀴즈 응답 데이터를 처리하는 데 사용됩니다. 이 모델을 기반으로 퀴즈 시스템에서 참가자의 정보, 퀴즈 응답, 질문 등을 데이터베이스에 저장하고 관리할 수 있습니다.
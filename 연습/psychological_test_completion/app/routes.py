from flask import (
    jsonify,
    render_template,
    request,
    Blueprint,
    redirect,
    url_for,
    flash,
    session,
)
from werkzeug.security import check_password_hash
from .models import Question, Participant, Quiz, Admin
from .database import db
import plotly.express as px
import pandas as pd
import plotly
import json
from sqlalchemy import func, extract
import plotly.graph_objs as go
from plotly.offline import plot
from datetime import datetime
# 'main'이라는 이름의 Blueprint 객체 생성
main = Blueprint("main", __name__)
admin = Blueprint("admin", __name__, url_prefix="/admin/")
# 1. main과 admin Blueprint 객체 생성
# main과 admin은 Flask의 Blueprint 객체로, 각각 일반 사용자의 라우트와 관리자 페이지 라우트를 분리 관리하는 역할을 합니다.
# admin은 url_prefix="/admin/"가 설정되어, 모든 관리자 관련 라우트는 /admin/으로 시작합니다.

@main.route("/", methods=["GET"]) # 2. 홈페이지 렌더링
def home():
    # 참여자 정보 입력 페이지를 렌더링합니다.
    return render_template("index.html")
# 사용자가 처음 접속할 때 보여줄 index.html 템플릿을 렌더링합니다. 참여자 정보 입력 페이지로 보입니다.
# 1. 기본 페이지 관리
# 1.1 홈 페이지 렌더링
# 기능: 사용자에게 기본 입력 페이지(index.html)를 렌더링합니다.
# 경로: "/"
# 메서드: GET



@main.route("/participants", methods=["POST"]) # 3. 참여자 정보 저장 
def add_participant():
    data = request.get_json()
    new_participant = Participant(
        name=data["name"], age=data["age"], gender=data["gender"] , created_at=datetime.utcnow()
    )
    db.session.add(new_participant)
    db.session.commit()

    # 리다이렉션 URL과 참여자 ID를 JSON 응답으로 전송
    return jsonify(
        {"redirect": url_for("main.quiz"), "participant_id": new_participant.id}
    )
# 클라이언트로부터 JSON 형식의 데이터를 받아 Participant 객체를 생성한 후 데이터베이스에 저장합니다.
# 저장이 완료되면 퀴즈 페이지로 리다이렉션 URL과 참여자 ID를 JSON으로 반환합니다.
# 1.2 참여자 추가
# 기능: JSON으로 전달된 데이터를 받아 Participant 객체를 생성하고, 데이터베이스에 추가합니다.
# 또한, 성공적으로 추가 후에는 리다이렉션 URL과 참가자 ID를 반환합니다.
# 경로: "/participants"
# 메서드: POST





@main.route("/quiz") # 4. 퀴즈 페이지 렌더링 
def quiz():
    # 퀴즈 페이지를 렌더링합니다. 참여자 ID 쿠키가 필요합니다.
    participant_id = request.cookies.get("participant_id")
    if not participant_id:
        # 참여자 ID가 없으면, 홈페이지로 리다이렉션합니다.
        return redirect(url_for("main.home"))

    questions = Question.query.all()
    questions_list = [question.content for question in questions]
    return render_template("quiz.html", questions=questions_list)
# 참여자 ID가 쿠키에 있는지 확인하고, 없으면 홈 페이지로 리다이렉트합니다.
# 퀴즈 데이터베이스에서 모든 질문을 조회하고 quiz.html로 질문 목록을 전달해 렌더링합니다.
# 2. 퀴즈 관리
# 2.1 퀴즈 페이지 렌더링
# 기능: 참가자 ID가 쿠키에 있는지 확인하고, 퀴즈 페이지(quiz.html)를 렌더링합니다. 참가자 ID가 없으면 홈으로 리다이렉트합니다.
# 경로: "/quiz"
# 메서드: GET




@main.route("/submit", methods=["POST"]) # 5. 퀴즈 답안 제출 
def submit():
    # 참여자 ID가 필요합니다.
    participant_id = request.cookies.get("participant_id")
    if not participant_id:
        return jsonify({"error": "Participant ID not found"}), 400

    data = request.json
    quizzes = data.get("quizzes", [])

    for quiz in quizzes:
        question_id = quiz.get("question_id")
        chosen_answer = quiz.get("chosen_answer")

        # 새 Quiz 인스턴스 생성
        new_quiz_entry = Quiz(
            participant_id=participant_id,
            question_id=question_id,
            chosen_answer=chosen_answer,
        )
        # 데이터베이스에 추가
        db.session.add(new_quiz_entry)

    # 변경 사항 커밋
    db.session.commit()
    return jsonify(
        {
            "message": "Quiz answers submitted successfully.",
            "redirect": url_for("main.show_results"),
        }
    )
# 퀴즈 답안을 JSON 형식으로 받아 Quiz 객체로 변환해 데이터베이스에 저장합니다.
# 데이터 저장 후 성공 메시지와 결과 페이지로 리다이렉션 URL을 JSON으로 반환합니다.
# 2.2 퀴즈 제출
# 기능: 퀴즈 응답을 JSON으로 받아, 데이터베이스에 Quiz 객체로 저장합니다. 참가자 ID가 없으면 에러를 반환합니다.
# 경로: "/submit"
# 메서드: POST




@main.route("/questions") # 6. 질문 목록 가져오기 
def get_questions():
    # is_active가 True인 질문만 선택하고, order_num에 따라 정렬
    questions = (
        Question.query.filter(Question.is_active == True)
        .order_by(Question.order_num)
        .all()
    )
    questions_list = [
        {
            "id": question.id,
            "content": question.content,
            "order_num": question.order_num,
        }
        for question in questions
    ]
    return jsonify(questions=questions_list)
# 데이터베이스에서 활성화된(is_active == True) 질문만 가져오고, order_num 기준으로 정렬해 JSON으로 반환합니다.
# 3. 질문 관리
# 3.1 질문 목록 가져오기
# 기능: is_active가 True인 질문만 가져와 order_num에 따라 정렬된 JSON 목록을 반환합니다.
# 경로: "/questions"
# 메서드: GET




@main.route("/results") # 7. 퀴즈 결과 시각화 
def show_results():
    # 데이터베이스에서 데이터 조회
    participants_query = Participant.query.all()
    quizzes_query = Quiz.query.join(Question).all()

    # pandas DataFrame으로 변환
    participants_data = [
        {"age": participant.age, "gender": participant.gender}
        for participant in participants_query
    ]
    quizzes_data = [
        {
            "question_id": quiz.question_id,
            "chosen_answer": quiz.chosen_answer,
            "participant_age": quiz.participant.age,
        }
        for quiz in quizzes_query
    ]
# 4. 결과 및 시각화
# 4.1 퀴즈 결과 시각화 및 결과 페이지 렌더링
# 기능: 참가자 및 퀴즈 데이터를 pandas DataFrame으로 변환하고, Plotly를 사용해 다양한 통계 그래프를 생성한 뒤, 이를 JSON으로 변환하여 결과 페이지(results.html)에 전달합니다.
# 경로: "/results"
# 메서드: GET
    participants_df = pd.DataFrame(participants_data)
    quizzes_df = pd.DataFrame(quizzes_data)
# 참가자와 퀴즈 데이터를 SQLAlchemy로 가져와서 Pandas DataFrame으로 변환합니다. 이후 이 데이터를 기반으로 시각화를 진행합니다.
    


    # Plotly 시각화 생성
    # 예시 1: 나이별 분포 (도넛 차트)
    # 8. Plotly 그래프 생성
    fig_age = px.pie(
        participants_df,
        names="age",
        hole=0.3,
        title="Age Distribution",
        color_discrete_sequence=px.colors.sequential.RdBu,
        labels={"age": "Age Group"},
    )
    fig_age.update_traces(textposition="inside", textinfo="percent+label")
# 참가자의 나이 분포를 도넛 차트로 시각화하는 코드입니다. participants_df에서 나이를 기준으로 데이터를 분류하여 그래프를 만듭니다.
    fig_gender = px.pie(
        participants_df,
        names="gender",
        hole=0.3,
        title="Gender Distribution",
        color_discrete_sequence=px.colors.sequential.Purp,
        labels={"gender": "Gender"},
    )
    fig_gender.update_traces(textposition="inside", textinfo="percent+label")



    quiz_response_figs = {} # 9. 질문별 응답 히스토그램 생성 

    # 각 질문 ID별로 반복하여 그래프 생성
    for question_id in quizzes_df["question_id"].unique():
        filtered_df = quizzes_df[quizzes_df["question_id"] == question_id]
        fig = px.histogram(
            filtered_df,
            x="chosen_answer",
            title=f"Question {question_id} Responses",
            color="chosen_answer",
            barmode="group",
            category_orders={"chosen_answer": ["yes", "no"]},  # 카테고리 순서 지정
            color_discrete_map={"yes": "RebeccaPurple", "no": "LightSeaGreen"},
        )  # 컬러 매핑
        fig.update_layout(
            xaxis_title="Chosen Answer",
            yaxis_title="Count",
            plot_bgcolor="rgba(0,0,0,0)",  # 배경색 투명
            paper_bgcolor="rgba(0,0,0,0)",  # 전체 배경색 투명
            font=dict(family="Courier New, monospace", size=18, color="#7f7f7f"),
            title_font=dict(
                family="Helvetica, Arial, sans-serif", size=22, color="RebeccaPurple"
            ),
        )
        fig.update_traces(marker_line_width=1.5, opacity=0.6)  # 투명도와 테두리 두께 조정

        # 생성된 그래프를 딕셔너리에 저장
        quiz_response_figs[f"question_{question_id}"] = fig
    age_quiz_response_figs = {}
# 각 질문에 대한 참가자들의 응답을 히스토그램으로 시각화하여 저장합니다. 


    # 나이대를 구분하는 함수
    def age_group(age):
        if age == 'teenage':
            return "10s"
        elif age == 'twenty':
            return "20s"
        elif age == 'thirty':
            return "30s"
        elif age == 'forty':
            return "40s"
        elif age == 'fifties':
            return "50s"
        else:
            return "60s+"

    # 나이대 그룹 열 추가
    quizzes_df["age_group"] = quizzes_df["participant_age"].apply(age_group)

    # 각 질문 ID와 나이대별로 대답 분포를 시각화
    for question_id in quizzes_df["question_id"].unique():
        filtered_df = quizzes_df[quizzes_df["question_id"] == question_id]
        fig = px.histogram(
            filtered_df,
            x="age_group",
            color="chosen_answer",
            barmode="group",
            title=f"Question {question_id} Responses by Age Group",
            labels={"age_group": "Age Group", "chosen_answer": "Chosen Answer"},
            category_orders={"age_group": ["10s", "20s", "30s", "40s", "50s+"]},
        )

        # 스타일 조정
        fig.update_layout(
            xaxis_title="Age Group",
            yaxis_title="Count",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Courier New, monospace", size=18, color="#7f7f7f"),
            title_font=dict(
                family="Helvetica, Arial, sans-serif", size=22, color="RebeccaPurple"
            ),
        )
        fig.update_traces(marker_line_width=1.5, opacity=0.6)
        age_quiz_response_figs[f"question_{question_id}"] = fig
    # 딕셔너리에 저장된 그래프들을 JSON으로 변환
    graphs_json = json.dumps(
        {
            "age_distribution": fig_age,
            "gender_distribution": fig_gender,
            "quiz_responses": quiz_response_figs,
            "age_quiz_response_figs": age_quiz_response_figs,
        },
        cls=plotly.utils.PlotlyJSONEncoder,
    )




    # 데이터를 results.html에 전달
    return render_template("results.html", graphs_json=graphs_json)





# 10. @admin.route("", methods=["GET", "POST"]) - 관리자 로그인
@admin.route("", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        admin = Admin.query.filter_by(username=username).first()

        if admin and check_password_hash(admin.password, password):
            session["admin_logged_in"] = True
            return redirect(url_for("admin.dashboard"))
        else:
            flash("Invalid username or password")

    return render_template("admin.html")
# 관리자는 사용자명과 비밀번호를 입력해 로그인합니다. 
# 비밀번호는 해시된 값으로 저장되고, 로그인 성공 시 관리자 대시보드로 리다이렉트됩니다.
# 5. 관리자 페이지
# 5.1 관리자 로그인
# 기능: 관리자는 사용자명과 비밀번호를 입력하여 로그인할 수 있습니다. 
# 올바르게 로그인되면 관리자 세션을 설정하고 대시보드로 리다이렉트됩니다.
# 경로: "/admin/"
# 메서드: GET, POST




@admin.route("/logout")
def logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("admin.login"))
# 5.2 관리자 로그아웃
# 기능: 관리자가 로그아웃할 때 세션에서 로그인 정보를 제거하고 로그인 페이지로 리다이렉트합니다.
# 경로: "/admin/logout"
# 메서드: GET



from functools import wraps
from flask import redirect, url_for, session


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "admin_logged_in" not in session:
            return redirect(url_for("admin.login", next=request.url))
        return f(*args, **kwargs)

    return decorated_function




# 11. @admin.route("/dashboard") - 관리자 대시보드
@admin.route("dashboard")
@login_required
def dashboard():
    # 날짜별 참가자 수를 계산
    participant_counts = (
        db.session.query(
            func.date(Participant.created_at).label("date"),
            func.count(Participant.id).label("count"),
        )
        .group_by("date")
        .all()
    )

    # 날짜와 참가자 수를 분리하여 리스트에 저장
    dates = [result.date for result in participant_counts]
    counts = [result.count for result in participant_counts]

    # Plotly 그래프 생성
    graph = go.Figure(go.Scatter(x=dates, y=counts, mode="lines+markers"))

    graph.update_layout(title="일자별 참가자 수", xaxis_title="날짜", yaxis_title="참가자 수")

    # Plotly 그래프를 HTML로 변환
    graph_div = plot(graph, output_type="div", include_plotlyjs=False,config = {'displayModeBar': False})

    # 생성된 HTML을 템플릿으로 전달
    return render_template("dashboard.html", graph_div=graph_div)
# 관리자 대시보드에서는 날짜별로 참가자 수를 시각화하여 그래프 형태로 제공합니다.
# 5.3 대시보드
# 기능: 관리자 대시보드에서 날짜별 참가자 수를 그래프로 표시합니다.
# 경로: "/admin/dashboard"
# 메서드: GET
# 데코레이터: @login_required (로그인 여부 확인)





@admin.route("/dashboard/question", methods=["GET", "POST"])
@login_required
def manage_questions():
    if request.method == "POST":
        if "new_question" in request.form:
            # 새 질문 추가
            is_active = (
                "is_active" in request.form and request.form["is_active"] == "on"
            )
            new_question = Question(
                content=request.form["content"],
                order_num=request.form["order_num"],
                is_active=is_active,
            )
            db.session.add(new_question)
            db.session.commit()
        else:
            # 기존 질문 수정
            question_id = request.form["question_id"]
            question = Question.query.get(question_id)
            if question:
                is_active = (
                    "is_active" in request.form and request.form["is_active"] == "on"
                )
                question.content = request.form["content"]
                question.order_num = request.form["order_num"]
                question.is_active = is_active
                db.session.commit()

    questions = Question.query.order_by(Question.order_num).all()
    return render_template("manage_questions.html", questions=questions)
# 5.4 질문 관리
# 기능: 관리자는 새로운 질문을 추가하거나 기존 질문을 수정할 수 있으며, 질문의 활성화 여부(is_active)도 설정 가능합니다.
# 경로: "/admin/dashboard/question"
# 메서드: GET, POST
# 데코레이터: @login_required (로그인 여부 확인)





@admin.route("/dashboard/list")
@login_required
def quiz_list():
    quizzes = Quiz.query.all()
    return render_template("quiz_list.html", quizzes=quizzes)
# quiz_list 함수는 관리자 대시보드에서 퀴즈 응답 목록을 보여주는 기능을 담당합니다.
# :
# 경로: /admin/dashboard/list
# 이 경로로 접근하면 관리자 대시보드에서 퀴즈 응답 목록을 조회할 수 있습니다.
# 메서드: GET
# 이 함수는 GET 요청을 처리하며, 퀴즈 응답 데이터를 가져와 화면에 보여줍니다.
# 데코레이터: @login_required
# 이 데코레이터는 관리자가 로그인되어 있는지를 확인합니다. 
# 로그인하지 않은 상태라면 관리자 로그인 페이지로 리다이렉트됩니다.
# 쿼리:
# Quiz.query.all()을 통해 데이터베이스에서 모든 Quiz 객체를 조회합니다. 
# 이는 퀴즈 응답 데이터 전체를 가져오는 역할을 합니다.
# 템플릿 렌더링:
# quiz_list.html 템플릿 파일로 조회된 퀴즈 응답 데이터를 전달합니다. 
# 이 템플릿 파일에서는 각 퀴즈 응답 데이터를 반복하면서 목록 형태로 화면에 표시될 것입니다.
# 주요 역할:
# 관리자가 모든 퀴즈 응답을 확인하고, 관리 목적으로 이를 리스트 형태로 화면에 표시하는 기능입니다. 
# quiz_list.html에서는 각 퀴즈 응답의 세부 정보(참여자 ID, 질문, 선택한 답변 등)를 볼 수 있을 것으로 예상됩니다.
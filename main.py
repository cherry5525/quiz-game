import json
import random
from datetime import datetime
from pathlib import Path

STATE_FILE = Path(__file__).parent / "state.json"   # main.py와 같은 폴더(프로젝트 루트)


def read_int(prompt, low, high):
    """low~high 사이 정수를 입력받을 때까지 반복해서 묻는다."""
    while True:
        text = input(prompt).strip()          # 앞뒤 공백 제거
        if text == "":
            print("⚠️ 입력이 비어 있습니다. 숫자를 입력하세요.")
            continue
        try:
            number = int(text)
        except ValueError:                    # 'abc' 같은 입력
            print(f"⚠️ 잘못된 입력입니다. {low}-{high} 사이의 숫자를 입력하세요.")
            continue
        if number < low or number > high:
            print(f"⚠️ 잘못된 입력입니다. {low}-{high} 사이의 숫자를 입력하세요.")
            continue
        return number


def read_text(prompt):
    """빈 문자열이 아닌 텍스트를 입력받는다."""
    while True:
        text = input(prompt).strip()
        if text == "":
            print("⚠️ 입력이 비어 있습니다. 다시 입력하세요.")
            continue
        return text


class Quiz:
    def __init__(self, question, choices, answer, hint=""):
        self.question = question      # 문제 (str)
        self.choices = choices        # 선택지 (list, 4개)
        self.answer = answer          # 정답 번호 (int, 1~4)
        self.hint = hint              # 힌트 (str, 없으면 빈 문자열)

    def show(self, number=None):
        """문제와 선택지를 출력한다."""
        if number is not None:
            print(f"[문제 {number}]")
        print(self.question)
        print()
        for i, choice in enumerate(self.choices, start=1):
            print(f"{i}. {choice}")
        print()

    def is_correct(self, user_answer):
        """사용자의 답이 정답인지 True/False로 돌려준다."""
        return user_answer == self.answer

    def to_dict(self):
        """JSON 저장용 딕셔너리로 변환한다."""
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
            "hint": self.hint,
        }

    @classmethod
    def from_dict(cls, data):
        """딕셔너리에서 Quiz 객체를 만든다. 형식이 잘못되면 ValueError를 낸다."""
        q, c, a = data["question"], data["choices"], data["answer"]
        h = data.get("hint", "")      # 예전 state.json(힌트 없음)도 읽을 수 있게 한다
        if not isinstance(q, str) or not q.strip():
            raise ValueError("question")
        if not (isinstance(c, list) and len(c) == 4 and all(isinstance(x, str) for x in c)):
            raise ValueError("choices")
        if type(a) is not int or not 1 <= a <= 4:
            raise ValueError("answer")
        if not isinstance(h, str):
            raise ValueError("hint")
        return cls(q, c, a, h)


class QuizGame:
    HINT_PENALTY = 0.5   # 힌트를 쓰고 맞히면 그 문제 배점의 50%만 인정

    def __init__(self):
        self.quizzes = self.default_quizzes()
        self.best_score = None
        self.history = []             # 게임 기록: 날짜/시간, 푼 문제 수, 점수 등

    def default_quizzes(self):
        return [
            Quiz('AI 올인원 제1기 입학연수(연수과정)의 기간과 본과정 선발 인원으로 옳은 것은?',
                 ['11/2(월)~11/26(목), 약 4주 / 본과정 200명 내외 선발', '11/2(월)~11/30(월), 약 5주 / 본과정 300명 내외 선발', '11/2(월)~11/26(목), 약 4주 / 본과정 300명 내외 선발', '11/9(월)~12/3(목), 약 4주 / 본과정 200명 내외 선발'], 1,
                 '연수 인원(300명)과 선발 인원은 서로 다릅니다.'),
            Quiz('입학연수 장학금(월 100만원)을 받기 위한 지급요건에 대한 설명으로 옳은 것은?',
                 ['시험 점수가 상위 200위 이내여야 한다', '출입 80시간 이상과 Term-Project 제출만 충족하면 된다', '출입 80시간 이상, 동료평가 6회 이상, Term-Project 결과 제출, 사후설문 참여를 모두 충족해야 한다', '4가지 조건 중 3가지 이상만 충족하면 지급된다'], 3,
                 "'모두 충족'이라는 표현에 주목하세요."),
            Quiz('동료평가 6회 이상 조건에서 반드시 충족해야 하는 것은?',
                 ['평가자로 6회 참여', '피평가자로 6회 평가받기', '참여와 받기 각각 3회씩', '참여(평가하기) 1회 이상, 받기(평가받기) 1회 이상 포함'], 4,
                 "합계 6회 안에 '필수 조건'이 따로 있습니다."),
            Quiz('다음 중 장학금을 지급받을 수 있는 경우는?',
                 ['재직자 또는 고용보험 가입자', '사업자등록증이 확인되는 프리랜서', '11/1 이전에 사업자등록증이 폐업 또는 휴업 상태로 처리된 자영업자', '실업급여 대상자'], 3,
                 '예외 조항이 있는 항목을 찾아보세요.'),
            Quiz('본과정 선발 기준의 배점 중 가장 높은 비중을 차지하는 항목은?',
                 ['기초역량(시험점수, 시험 참여 횟수) 30점', '협업 및 태도(Term Project 점수, 사후 설문 참여) 20점', '참여의지(OT 참석, 교육장 출입시간, 동료평가 참여) 50점', '세 항목 모두 동일한 배점'], 3,
                 "시험 점수보다 '참여'가 더 크게 반영됩니다."),
            Quiz('교육장 출입 및 출석 인정에 대한 설명으로 옳은 것은?',
                 ['교육장은 24시간 개방되며, 출석 인정 시간에는 제한이 없다', '교육장은 24시간 개방되며, 출석 인정은 하루 최대 12시간이다', '교육장은 09:00~22:00에만 개방되며, 출석 인정은 하루 최대 12시간이다', '지문 인식은 입실 시에만 하면 된다'], 2,
                 '개방 시간과 출석 인정 시간은 다릅니다.'),
            Quiz('동료평가 규칙으로 옳은 것은?',
                 ['평가자와 피평가자 중 한 명이 불참해도 나머지로 진행할 수 있다', '평가는 대면으로 진행하며, 피평가자의 PC에서 평가한다', '시간 절약을 위해 디스코드로 원격 평가를 해도 된다', '여러 평가를 동시에 진행하면 효율적이므로 권장된다'], 2,
                 '원격 평가는 부정행위로 간주됩니다.'),
            Quiz('매주 금요일 19시 시험이 시작됩니다. 시험모드 전환과 관련해 교육생이 해야 할 일은?',
                 ['시험 시작 1시간 전에 중요 문서를 저장하고 로그아웃한다', '시험 종료 후 1시간 뒤에 로그인한다', '별도 조치 없이 PC를 켜 둔다', '시험 시작 직전에 로그아웃하면 된다'], 1,
                 '전환 작업에 시간이 필요합니다.'),
        ]

    # ---------- 화면 ----------
    def show_menu(self):
        print("=" * 40)
        print("        🎯 나만의 퀴즈 게임 🎯")
        print("=" * 40)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 퀴즈 삭제")
        print("6. 종료")
        print("=" * 40)

    # ---------- 퀴즈 풀기 ----------
    def ask_answer(self, quiz):
        """정답을 입력받는다. 힌트가 있는 퀴즈는 0을 입력하면 힌트를 보여 준다.
        (정답 번호, 힌트 사용 여부)를 돌려준다."""
        hint_used = False
        if quiz.hint:
            prompt, low = "정답 입력 (힌트 보기: 0): ", 0
        else:
            prompt, low = "정답 입력: ", 1
        while True:
            number = read_int(prompt, low, 4)
            if number == 0:
                hint_used = True
                print(f"💡 힌트: {quiz.hint}  (맞혀도 배점 {int(self.HINT_PENALTY * 100)}%만 인정)")
                continue
            return number, hint_used

    def choose_count(self):
        """풀 문제 수를 고른다."""
        total = len(self.quizzes)
        return read_int(f"풀 문제 수를 선택하세요 (1-{total}): ", 1, total)

    def play(self):
        if not self.quizzes:
            print("⚠️ 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가하세요.")
            return

        count = self.choose_count()
        selected = random.sample(self.quizzes, count)   # 랜덤 순서로 count개 선택
        print(f"\n📝 퀴즈를 시작합니다! (총 {count}문제)\n")
        correct = 0
        hints_used = 0
        points = 0.0                                    # 힌트 감점이 반영된 획득 점수

        for i, quiz in enumerate(selected, start=1):
            print("-" * 40)
            quiz.show(i)
            user_answer, hint_used = self.ask_answer(quiz)
            if hint_used:
                hints_used += 1
            if quiz.is_correct(user_answer):
                correct += 1
                if hint_used:
                    points += self.HINT_PENALTY
                    print("✅ 정답입니다! (힌트 사용: 배점 50%)\n")
                else:
                    points += 1
                    print("✅ 정답입니다!\n")
            else:
                print(f"❌ 오답입니다. 정답은 {quiz.answer}번입니다.\n")

        score = round(points / count * 100)
        print("=" * 40)
        print(f"🏆 결과: {count}문제 중 {correct}문제 정답! ({score}점)")
        if hints_used:
            print(f"💡 힌트 사용: {hints_used}회")
        self.update_best_score(score)
        self.add_history(count, correct, hints_used, score)
        print("=" * 40)

    def update_best_score(self, score):
        if self.best_score is None or score > self.best_score:
            self.best_score = score
            print("🎉 새로운 최고 점수입니다!")

    def add_history(self, total, correct, hints_used, score):
        self.history.append({
            "played_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total": total,
            "correct": correct,
            "hints_used": hints_used,
            "score": score,
        })

    # ---------- 퀴즈 추가 ----------
    def add_quiz(self):
        print("\n📌 새로운 퀴즈를 추가합니다.\n")
        question = read_text("문제를 입력하세요: ")
        choices = []
        for i in range(1, 5):
            choices.append(read_text(f"선택지 {i}: "))
        answer = read_int("정답 번호 (1-4): ", 1, 4)
        hint = input("힌트 (없으면 Enter): ").strip()      # 힌트는 선택 사항

        self.quizzes.append(Quiz(question, choices, answer, hint))
        print("\n✅ 퀴즈가 추가되었습니다!")

    # ---------- 퀴즈 목록 ----------
    def show_list(self):
        if not self.quizzes:
            print("⚠️ 등록된 퀴즈가 없습니다.")
            return
        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)\n")
        print("-" * 40)
        for i, quiz in enumerate(self.quizzes, start=1):
            print(f"[{i}] {quiz.question}")
        print("-" * 40)

    # ---------- 퀴즈 삭제 ----------
    def delete_quiz(self):
        if not self.quizzes:
            print("⚠️ 삭제할 퀴즈가 없습니다.")
            return
        self.show_list()
        number = read_int("삭제할 퀴즈 번호 (취소: 0): ", 0, len(self.quizzes))
        if number == 0:
            print("삭제를 취소했습니다.")
            return
        removed = self.quizzes.pop(number - 1)
        print(f"🗑️ 삭제했습니다: {removed.question}")

    # ---------- 점수 확인 ----------
    def show_score(self):
        if self.best_score is None:
            print("⚠️ 아직 퀴즈를 풀지 않았습니다.")
            return
        print(f"\n🏆 최고 점수: {self.best_score}점")
        if self.history:
            recent = self.history[-5:]
            print(f"\n📜 최근 게임 기록 (총 {len(self.history)}회 중 최근 {len(recent)}회)")
            print("-" * 40)
            for record in recent:
                print(f"{record['played_at']} | {record['total']}문제 중 "
                      f"{record['correct']}개 정답 | 힌트 {record['hints_used']}회 | {record['score']}점")
            print("-" * 40)

    # ---------- 파일 저장/불러오기 ----------
    @staticmethod
    def check_history(history):
        """게임 기록 형식이 올바른지 검사한다. 잘못되면 ValueError를 낸다."""
        if not isinstance(history, list):
            raise ValueError("history")
        for record in history:
            if not isinstance(record, dict) or not isinstance(record.get("played_at"), str):
                raise ValueError("history")
            for key in ("total", "correct", "hints_used", "score"):
                if type(record.get(key)) is not int:
                    raise ValueError("history")

    def save(self):
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
            "history": self.history,
        }
        try:
            with open(STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except OSError:
            print("⚠️ 파일을 저장하지 못했습니다.")

    def load(self):
        if not STATE_FILE.exists():
            print("📂 저장 파일이 없어 기본 퀴즈로 시작합니다.")
            return
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, dict) or not isinstance(data.get("quizzes"), list):
                raise ValueError("format")
            quizzes = [Quiz.from_dict(q) for q in data["quizzes"]]   # 형식 검증 포함
            best_score = data["best_score"]
            if best_score is not None and (type(best_score) is not int or not 0 <= best_score <= 100):
                raise ValueError("best_score")
            history = data.get("history", [])       # 예전 파일에는 history가 없을 수 있다
            self.check_history(history)
        except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError):
            print("⚠️ 저장 파일이 손상되어 기본 퀴즈로 초기화합니다.")
            self.quizzes = self.default_quizzes()
            self.best_score = None
            self.history = []
            self.save()
            return

        self.quizzes = quizzes
        self.best_score = best_score
        self.history = history
        score_text = "없음" if best_score is None else f"{best_score}점"
        print(f"📂 저장된 데이터를 불러왔습니다. (퀴즈 {len(quizzes)}개, 최고점수 {score_text})")

    # ---------- 실행 ----------
    def run(self):
        self.load()
        try:
            while True:
                self.show_menu()
                choice = read_int("선택: ", 1, 6)
                if choice == 1:
                    self.play()
                    self.save()          # 점수 갱신 후 저장
                elif choice == 2:
                    self.add_quiz()
                    self.save()          # 퀴즈 추가 후 저장
                elif choice == 3:
                    self.show_list()
                elif choice == 4:
                    self.show_score()
                elif choice == 5:
                    self.delete_quiz()
                    self.save()          # 퀴즈 삭제 후 저장
                elif choice == 6:
                    print("프로그램을 종료합니다.")
                    break
        except (KeyboardInterrupt, EOFError):
            print("\n\n⚠️ 입력이 중단되었습니다. 데이터를 저장하고 안전하게 종료합니다.")
        finally:
            self.save()


if __name__ == "__main__":
    game = QuizGame()
    game.run()

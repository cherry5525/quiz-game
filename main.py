import json
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
    def __init__(self, question, choices, answer):
        self.question = question      # 문제 (str)
        self.choices = choices        # 선택지 (list, 4개)
        self.answer = answer          # 정답 번호 (int, 1~4)

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
        }

    @classmethod
    def from_dict(cls, data):
        """딕셔너리에서 Quiz 객체를 만든다. 형식이 잘못되면 ValueError를 낸다."""
        q, c, a = data["question"], data["choices"], data["answer"]
        if not isinstance(q, str) or not q.strip():
            raise ValueError("question")
        if not (isinstance(c, list) and len(c) == 4 and all(isinstance(x, str) for x in c)):
            raise ValueError("choices")
        if type(a) is not int or not 1 <= a <= 4:
            raise ValueError("answer")
        return cls(q, c, a)


class QuizGame:
    def __init__(self):
        self.quizzes = self.default_quizzes()
        self.best_score = None

    def default_quizzes(self):
        return [
            Quiz("Python의 창시자는?",
                 ["Guido van Rossum", "Linus Torvalds", "Bjarne Stroustrup", "James Gosling"], 1),
            Quiz("딕셔너리(dict)를 만들 때 사용하는 기호는?",
                 ["()", "[]", "{}", "<>"], 3),
            Quiz("반복 횟수를 모르고, 조건이 참인 동안 계속 반복할 때 주로 쓰는 반복문은?",
                 ["for", "while", "if", "def"], 2),
            Quiz("클래스의 메서드에서 객체 자신을 가리키는 첫 번째 매개변수의 관례적인 이름은?",
                 ["this", "me", "self", "cls"], 3),
            Quiz("객체가 만들어질 때 자동으로 실행되어 속성을 초기화하는 메서드는?",
                 ["__init__", "__start__", "__make__", "__create__"], 1),
            Quiz("JSON 파일의 내용을 파이썬 데이터로 읽어 올 때 사용하는 함수는?",
                 ["json.dump", "json.write", "json.save", "json.load"], 4),
            Quiz("Git에서 원격 저장소 전체를 내 컴퓨터로 복제하는 명령어는?",
                 ["git push", "git pull", "git commit", "git clone"], 4),
            Quiz("if와 elif 조건이 모두 거짓일 때 실행되는 블록을 만드는 키워드는?",
                 ["elif", "else", "for", "while"], 2),
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
        print("5. 종료")
        print("=" * 40)

    # ---------- 퀴즈 풀기 ----------
    def play(self):
        if not self.quizzes:
            print("⚠️ 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가하세요.")
            return

        total = len(self.quizzes)
        print(f"\n📝 퀴즈를 시작합니다! (총 {total}문제)\n")
        correct = 0

        for i, quiz in enumerate(self.quizzes, start=1):
            print("-" * 40)
            quiz.show(i)
            user_answer = read_int("정답 입력: ", 1, 4)
            if quiz.is_correct(user_answer):
                print("✅ 정답입니다!\n")
                correct += 1
            else:
                print(f"❌ 오답입니다. 정답은 {quiz.answer}번입니다.\n")

        score = round(correct / total * 100)
        print("=" * 40)
        print(f"🏆 결과: {total}문제 중 {correct}문제 정답! ({score}점)")
        self.update_best_score(score)
        print("=" * 40)

    def update_best_score(self, score):
        if self.best_score is None or score > self.best_score:
            self.best_score = score
            print("🎉 새로운 최고 점수입니다!")

    # ---------- 퀴즈 추가 ----------
    def add_quiz(self):
        print("\n📌 새로운 퀴즈를 추가합니다.\n")
        question = read_text("문제를 입력하세요: ")
        choices = []
        for i in range(1, 5):
            choices.append(read_text(f"선택지 {i}: "))
        answer = read_int("정답 번호 (1-4): ", 1, 4)

        self.quizzes.append(Quiz(question, choices, answer))
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

    # ---------- 점수 확인 ----------
    def show_score(self):
        if self.best_score is None:
            print("⚠️ 아직 퀴즈를 풀지 않았습니다.")
        else:
            print(f"\n🏆 최고 점수: {self.best_score}점")

    # ---------- 파일 저장/불러오기 ----------
    def save(self):
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
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
            quizzes = [Quiz.from_dict(q) for q in data["quizzes"]]   # 형식 검증 포함
            best_score = data["best_score"]
            if best_score is not None and (type(best_score) is not int or not 0 <= best_score <= 100):
                raise ValueError("best_score")
        except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError):
            print("⚠️ 저장 파일이 손상되어 기본 퀴즈로 초기화합니다.")
            self.quizzes = self.default_quizzes()
            self.best_score = None
            self.save()
            return

        self.quizzes = quizzes
        self.best_score = best_score
        score_text = "없음" if best_score is None else f"{best_score}점"
        print(f"📂 저장된 데이터를 불러왔습니다. (퀴즈 {len(quizzes)}개, 최고점수 {score_text})")

    # ---------- 실행 ----------
    def run(self):
        self.load()
        try:
            while True:
                self.show_menu()
                choice = read_int("선택: ", 1, 5)
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
                    print("프로그램을 종료합니다.")
                    break
        except (KeyboardInterrupt, EOFError):
            print("\n\n⚠️ 입력이 중단되었습니다. 데이터를 저장하고 안전하게 종료합니다.")
        finally:
            self.save()


if __name__ == "__main__":
    game = QuizGame()
    game.run()
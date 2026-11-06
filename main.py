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
        """딕셔너리에서 Quiz 객체를 만든다. (불러오기용)"""
        return cls(data["question"], data["choices"], data["answer"])


class QuizGame:
    def __init__(self):
        self.quizzes = self.default_quizzes()
        self.best_score = None

    def default_quizzes(self):
        return [
            Quiz("Python의 창시자는?", ["Guido van Rossum", "Linus Torvalds", "Bjarne Stroustrup", "James Gosling"], 1),
            Quiz("리스트를 나타내는 기호는?", ["()", "[]", "{}", "<>"], 2),
            Quiz("화면에 값을 출력하는 함수는?", ["input", "print", "show", "echo"], 2),
            Quiz("정수 자료형의 이름은?", ["str", "bool", "int", "dict"], 3),
            Quiz("조건이 거짓일 때 실행되는 키워드는?", ["elif", "for", "else", "while"], 3),
        ]

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

    def run(self):
        while True:
            self.show_menu()
            choice = read_int("선택: ", 1, 5)
            if choice == 1:
                print("(퀴즈 풀기 - 준비 중)")
            elif choice == 2:
                print("(퀴즈 추가 - 준비 중)")
            elif choice == 3:
                print("(퀴즈 목록 - 준비 중)")
            elif choice == 4:
                print("(점수 확인 - 준비 중)")
            elif choice == 5:
                print("프로그램을 종료합니다.")
                break


if __name__ == "__main__":
    game = QuizGame()
    game.run()


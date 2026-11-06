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


class QuizGame:
    def __init__(self):
        self.quizzes = []
        self.best_score = None

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
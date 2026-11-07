# 🎯 나만의 퀴즈 게임

## 프로젝트 개요
터미널에서 실행하는 Python 콘솔 퀴즈 게임입니다.
메뉴에서 번호를 선택해 퀴즈 풀기, 퀴즈 추가, 퀴즈 목록 보기, 최고 점수 확인을 할 수 있습니다.
퀴즈와 최고 점수는 `state.json` 파일에 저장되어, 프로그램을 종료하고 다시 실행해도 유지됩니다.

- 사용 언어: Python 3.10 이상 (외부 라이브러리 없음)
- 사용 기술: 클래스(`Quiz`, `QuizGame`), JSON 파일 입출력, 예외 처리(try/except)
- 버전 관리: Git / GitHub (기능 단위 커밋, 브랜치 작업 후 병합)

## 퀴즈 주제와 선정 이유
**주제: 코디세이 올인원 과정**

코디세이 과정이 처음인 동료 교육생들에게 도움이 될 만한, 꼭 알아야 할 내용을 중심으로 퀴즈 주제를 선정했습니다. 장학금 탈락, 본과정 선발 불이익, 평가 Fail, 부정행위 처리처럼 결과에 직접 영향을 주는 내용을 우선하여 장학금 및 선발 기준, 출석과 교육장 이용, 동료평가 규칙, 금요일 시험 대비를 주제로 삼았습니다.

## 실행 방법
1. Python 3.10 이상이 설치되어 있어야 합니다.
2. 저장소를 내려받습니다.
   ```bash
   git clone https://github.com/cherry5525/quiz-game.git
   cd quiz-game
   ```
3. 프로그램을 실행합니다.
   ```bash
   python main.py
   ```
   (Mac/Linux에서 `python`이 동작하지 않으면 `python3 main.py`)

## 기능 목록
| 메뉴 | 설명 |
|---|---|
| 1. 퀴즈 풀기 | 풀 문제 수를 고르면 저장된 퀴즈 중 그 수만큼 무작위로 출제하고, 정답/오답을 알려 준 뒤 결과 점수를 보여 줍니다. 힌트 보기(`0` 입력)를 지원합니다. 최고 점수를 넘으면 갱신합니다. |
| 2. 퀴즈 추가 | 문제, 선택지 4개, 정답 번호를 입력해 새 퀴즈를 등록하고 파일에 저장합니다. |
| 3. 퀴즈 목록 | 등록된 퀴즈의 문제 목록을 보여 줍니다. |
| 4. 점수 확인 | 저장된 최고 점수를 보여 줍니다. |
| 5. 퀴즈 삭제 | 목록에서 번호를 골라 퀴즈를 삭제하고 파일에 반영합니다. (보너스) |
| 6. 종료 | 프로그램을 종료합니다. |

**보너스 기능**
- 랜덤 출제: `random.sample`로 문제 순서를 섞어 출제
- 문제 수 선택: 풀 문제 수를 1~전체 사이에서 선택
- 힌트: `Quiz.hint` 속성 추가, 풀이 중 `0` 입력 시 힌트 표시. 힌트를 쓰고 맞히면 그 문제 배점의 50%만 인정
- 퀴즈 삭제: 메뉴 5번
- 점수 기록 히스토리: 게임마다 날짜/시간, 푼 문제 수, 정답 수, 힌트 사용 횟수, 점수를 저장하고 점수 확인 시 최근 5회 표시

**입력/예외 처리**
- 입력 앞뒤 공백 제거
- 빈 입력, 숫자가 아닌 입력, 허용 범위 밖 숫자 입력 시 안내 후 재입력
- `Ctrl+C`(KeyboardInterrupt) 또는 입력 종료(EOFError) 시 저장 후 안전하게 종료
- `state.json`이 없으면 기본 퀴즈로 시작, 손상되었으면 안내 후 기본 퀴즈로 초기화

## 파일 구조
```
quiz-game/
├── main.py        # Quiz, QuizGame 클래스와 프로그램 진입점
├── state.json     # 퀴즈 목록과 최고 점수 저장 파일 (기본 예시 데이터 포함)
├── README.md      # 프로젝트 설명
├── .gitignore     # Git 추적 제외 목록
└── docs/
    └── screenshots/
        ├── add_quiz.png   # 퀴즈 추가 화면
        ├── dev_env.png    # 개발 환경
        ├── git_log.png    # git log 결과
        ├── menu.png       # 메뉴 화면
        ├── play.png       # 퀴즈 풀기 화면
        └── score.png      # 점수 확인 화면
```

**main.py 구성**
- `read_int()`, `read_text()`: 입력 검증 도우미 함수
- `Quiz`: 문제, 선택지, 정답을 가진 퀴즈 하나를 표현 (출력, 정답 확인, dict 변환)
- `QuizGame`: 메뉴, 퀴즈 풀기/추가/목록/점수 확인, 파일 저장/불러오기 등 게임 전체를 관리

## 데이터 파일 설명 (state.json)
- **경로**: 프로젝트 루트 (`main.py`와 같은 폴더)
- **역할**: 퀴즈 목록과 최고 점수를 저장해 프로그램을 다시 실행해도 유지되게 합니다.
- **인코딩**: UTF-8
- **생성 시점**: 퀴즈를 풀거나 추가한 뒤, 그리고 프로그램 종료 시 자동 저장됩니다.

| 필드 | 타입 | 설명 |
|---|---|---|
| `quizzes` | list | 퀴즈 객체들의 목록 |
| `quizzes[].question` | str | 문제 |
| `quizzes[].choices` | list(str) | 선택지 4개 |
| `quizzes[].answer` | int | 정답 번호 (1~4) |
| `quizzes[].hint` | str | 힌트 (선택 사항, 없으면 빈 문자열. 없는 예전 파일도 읽을 수 있음) |
| `best_score` | int 또는 null | 최고 점수 (아직 퀴즈를 풀지 않았으면 `null`) |
| `history` | list | 게임 기록 목록 (없으면 빈 리스트) |
| `history[].played_at` | str | 플레이 날짜/시간 |
| `history[].total` | int | 푼 문제 수 |
| `history[].correct` | int | 정답 수 |
| `history[].hints_used` | int | 힌트 사용 횟수 |
| `history[].score` | int | 점수 (0~100) |

```json
{
    "quizzes": [
        {
            "question": "매주 금요일 19시 시험이 시작됩니다. 시험모드 전환과 관련해 교육생이 해야 할 일은?",
            "choices": [
                "시험 시작 1시간 전에 중요 문서를 저장하고 로그아웃한다",
                "시험 종료 후 1시간 뒤에 로그인한다",
                "별도 조치 없이 PC를 켜 둔다",
                "시험 시작 직전에 로그아웃하면 된다"
            ],
            "answer": 1,
            "hint": "전환 작업에 시간이 필요합니다."
        }
    ],
    "best_score": 100,
    "history": [
        {
            "played_at": "2026-11-07 19:38:26",
            "total": 6,
            "correct": 6,
            "hints_used": 2,
            "score": 83
        }
    ]
}
```

## 개발 환경
Python 버전, Git 버전, VS Code 환경입니다.

![개발 환경](docs/screenshots/dev_env.png)

## Git 작업 기록
`git log --oneline --graph` 결과입니다. 기능 단위로 커밋했고, `feature/play-quiz` 브랜치를 만들어 작업한 뒤 main에 병합했습니다.

![git log](docs/screenshots/git_log.png)


## 실행 화면

![메뉴](docs/screenshots/menu.png)
![퀴즈 풀기](docs/screenshots/play.png)
![퀴즈 추가](docs/screenshots/add_quiz.png)
![점수 확인](docs/screenshots/score.png)


## clone 실습으로 추가한 줄입니다
quiz-game-clone/README.md
## Git 실습 기록
- 브랜치 작업 후 git merge --no-ff로 병합 커밋을 남겼습니다.
- 별도 폴더에 clone → 수정/commit/push → 원본에서 pull 순서로 실습했습니다.

- (clone 복제본에서 추가) pull 실습 확인용 문장

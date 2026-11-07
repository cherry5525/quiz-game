# 🎯 나만의 퀴즈 게임

## 프로젝트 개요
터미널에서 실행하는 Python 콘솔 퀴즈 게임입니다.
메뉴에서 번호를 선택해 퀴즈 풀기, 퀴즈 추가, 퀴즈 목록 보기, 최고 점수 확인을 할 수 있습니다.
퀴즈와 최고 점수는 `state.json` 파일에 저장되어, 프로그램을 종료하고 다시 실행해도 유지됩니다.

- 사용 언어: Python 3.10 이상 (외부 라이브러리 없음)
- 사용 기술: 클래스(`Quiz`, `QuizGame`), JSON 파일 입출력, 예외 처리(try/except)
- 버전 관리: Git / GitHub (기능 단위 커밋, 브랜치 작업 후 병합)

## 과제 목표와 이 프로젝트에서의 적용
이 과제를 마친 후 아래 내용을 스스로 설명할 수 있어야 하며, 각 항목이 이 프로젝트의 어디에 쓰였는지 함께 정리했습니다.

### Python 기초
| 목표 | 이 프로젝트에서의 예 |
|---|---|
| 변수가 무엇이고 왜 쓰는가 | 값에 이름을 붙여 저장하고 재사용합니다. `correct`, `points`, `best_score`, `STATE_FILE` |
| int / str / bool / list / dict 차이 | int: 점수·정답 번호, str: 문제·힌트, bool: `hint_used`, list: `quizzes`·`choices`, dict: `to_dict()`·`history` 기록 |
| if / elif / else | 메뉴 선택(`run()`), 정답/오답 판정(`play()`), 입력 검증(`read_int()`) |
| for와 while의 차이 | `for`는 횟수·대상이 정해진 반복(문제 출제, 목록 출력), `while True`는 올바른 입력이 올 때까지 반복(`read_int()`, 메뉴 루프) |
| 함수의 매개변수와 반환값 | `read_int(prompt, low, high)`는 검증된 정수를 반환합니다. `read_text(prompt)`도 같은 방식입니다. |

### 클래스와 객체
| 목표 | 이 프로젝트에서의 예 |
|---|---|
| 클래스란 무엇이고 왜 쓰는가 | 데이터와 기능을 하나로 묶어 역할을 분리합니다. 퀴즈 하나는 `Quiz`, 게임 전체는 `QuizGame`이 맡습니다. |
| `__init__`과 `self` | `__init__`은 객체 생성 시 속성을 초기화하고, `self`는 그 객체 자신을 가리킵니다. 예: `self.question = question` |
| 속성(attribute)과 메서드(method) | 속성: `question`, `choices`, `answer`, `hint`, `best_score` / 메서드: `show()`, `is_correct()`, `play()`, `save()` |

### 파일 입출력
| 목표 | 이 프로젝트에서의 예 |
|---|---|
| 파일 열기·읽기·쓰기 | `open(..., "r"/"w", encoding="utf-8")`로 열고 `json.load()`·`json.dump()`로 읽고 씁니다. (`load()`, `save()`) |
| JSON을 쓰는 이유 | list/dict 구조를 그대로 텍스트로 저장할 수 있고, 사람이 읽기 쉬우며 언어 간 호환성이 좋습니다. (`state.json`) |
| try / except 오류 처리 | 파일 없음·손상(`OSError`, `JSONDecodeError`), 숫자 아닌 입력(`ValueError`), `Ctrl+C`(`KeyboardInterrupt`) 처리 |

### Git 기초
| 목표 | 이 프로젝트에서의 예 |
|---|---|
| Git이란, 왜 필요한가 | 변경 이력을 기록해 되돌리고 협업할 수 있게 하는 버전 관리 도구입니다. 기능 단위로 커밋했습니다. |
| `init` | 현재 폴더를 Git 저장소로 만듭니다. |
| `add` | 변경한 파일을 커밋 대상(스테이징)에 올립니다. |
| `commit` | 스테이징한 변경을 이력으로 저장합니다. |
| `push` | 로컬 커밋을 원격 저장소(GitHub)에 올립니다. |
| `pull` | 원격의 변경사항을 가져와 합칩니다. |
| `checkout` | 브랜치를 전환하거나 파일을 이전 상태로 되돌립니다. (`git checkout state.json`) |
| `clone` | 원격 저장소를 통째로 복제합니다. |
| 브랜치 생성·병합 | `feature/play-quiz`, `feature/bonus` 등을 만들어 작업하고 `main`에 병합했습니다. ([docs/git_log.txt](docs/git_log.txt)) |
| clone 후 pull | 별도 폴더에 clone한 뒤 원본의 변경사항을 pull로 가져오는 실습을 했습니다. |

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


## 안정성 · 저장 방식
- **원자적 저장**: `state.json.tmp`에 먼저 쓴 뒤 `os.replace`로 교체하므로, 저장 중 중단돼도 원본이 깨지지 않습니다.
- **자동 백업**: 저장 직전 정상 파일을 `state.json.bak`으로 보관합니다. 손상된 파일로 백업을 덮어쓰지 않습니다.
- **복구 순서**: `state.json` 손상 시 → `state.json.bak`에서 복구 → 백업도 없거나 손상이면 기본 퀴즈로 초기화(손상 파일은 `state.json.corrupt`로 보관).
- **저장 순서**: 퀴즈(`quizzes`) → 최고 점수(`best_score`) → 기록(`history`).
- **저장 실패 시**: 폴더 쓰기 권한과 디스크 공간을 확인하세요. (Windows: 폴더 속성 > 보안, Mac/Linux: `chmod u+w`)
- **동시 실행**: 한 번에 한 프로세스만 실행하는 것을 전제로 합니다.

## 기본 퀴즈와 확장성
- 기본 제공 퀴즈: **8개** (`default_quizzes()`, 최초 실행 시 `state.json`에 저장)
- 대용량: 퀴즈 수천 개 수준까지는 `random.sample`과 JSON 로드가 즉시 끝나므로 문제없습니다. 그보다 커지거나 동시 접근이 필요하면 SQLite 전환을 고려합니다.

## 기능별 메서드 매핑
| 기능 | 위치 |
|---|---|
| 입력 검증 | `read_int()`, `read_text()` |
| 정오답 판정 | `Quiz.is_correct()` |
| 퀴즈 진행 | `QuizGame.play()`, `ask_answer()` |
| 점수 | `update_best_score()`, `add_history()` |
| 저장/불러오기 | `save()`, `load()`, `read_state()` |
| 직렬화 | `Quiz.to_dict()`, `Quiz.from_dict()` |

## 커밋 규칙과 증빙
- 메시지 형식: `Type: 내용` (Type = Feat / Fix / Docs / Refactor / Chore). 예: `Feat: 퀴즈 추가 기능 구현`
- 커밋 수: 27개 이상 — 전체 로그 텍스트는 [docs/git_log.txt](docs/git_log.txt), 그래프는 [docs/git_graph.txt](docs/git_graph.txt)
- 스크린샷 설명: `dev_env.png`(python/git 버전), `git_log.png`(`git log --oneline --graph`), `menu.png`(메뉴), `play.png`(퀴즈 풀기), `add_quiz.png`(퀴즈 추가), `score.png`(점수 확인)
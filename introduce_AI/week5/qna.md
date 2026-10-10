# Week5 Q&A

---

## Q1. `pip`가 없는 것 같은데 brew로 설치하면 되나?

**A.** brew로 설치할 필요는 없다. pip는 이미 설치되어 있고, `pip`라는 이름의 명령어만 없는 상태다.

- Homebrew Python 3.12에는 pip가 함께 들어 있지만, 명령어 이름이 `pip`가 아니라 **`pip3`** 또는 **`python3 -m pip`**이다.
- 다만 Homebrew Python에 바로 `pip3 install ...`을 하면 `externally-managed-environment` 에러가 날 수 있다(PEP 668: 시스템/brew가 관리하는 Python에는 직접 패키지를 설치하지 못하게 막는 정책).
- scikit-learn, datasets 같은 패키지는 brew로 설치하는 것이 아니라 pip로 설치하는 게 일반적이다.

**권장 방법: 가상환경(venv)을 만들어 그 안에 설치**

```bash
cd ~/dev/lecture/introduce_AI
python3 -m venv .venv                 # 가상환경 생성 (한 번만)
source .venv/bin/activate             # 가상환경 활성화 (터미널 열 때마다)
pip install pandas datasets scikit-learn matplotlib   # 활성화 후에는 pip 명령어 사용 가능
python week5/practice/iris_classification.py          # 실습 실행
deactivate                            # 가상환경 종료
```

- 가상환경을 활성화하면 그 안에서는 `pip`, `python` 명령어를 그대로 쓸 수 있다.
- 프로젝트별로 패키지를 따로 관리하므로 시스템 Python을 건드리지 않는다.
- VS Code에서는 인터프리터를 `.venv/bin/python`으로 선택하면 된다.
- `.venv` 폴더는 용량이 크므로 git에 올리지 않도록 `.gitignore`에 추가하는 것이 좋다.

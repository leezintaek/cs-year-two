---
description: 변경사항을 모두 스테이징(git add .)하고 커밋한 뒤 원격 저장소로 push 한다.
disable-model-invocation: true
argument-hint: "[커밋 메시지 (생략 시 자동 생성)]"
allowed-tools: Bash(git status:*), Bash(git diff:*), Bash(git add:*), Bash(git commit:*), Bash(git push:*), Bash(git log:*), Bash(git branch:*), Bash(git rev-parse:*)
---

# git_push

현재 저장소의 모든 변경사항을 add → commit → push 한다.

## 절차

1. `git status` 로 변경사항을 확인한다. 변경사항이 없으면 "커밋할 변경사항이 없습니다"라고 알리고 종료한다.
2. `git add .` 로 모든 변경사항을 스테이징한다.
3. 커밋 메시지를 정한다.
   - 사용자가 인자를 준 경우: `$ARGUMENTS` 를 그대로 커밋 메시지로 사용한다.
   - 인자가 없는 경우: `git diff --cached` 를 보고 변경 내용을 요약한 간결한 메시지를 작성한다.
4. `git commit -m "<메시지>"` 로 커밋한다.
5. `git push` 로 원격에 push 한다. upstream 이 설정되지 않은 브랜치라면 `git push -u origin <현재 브랜치>` 를 사용한다.
6. 커밋 해시, 메시지, push 결과를 짧게 보고한다.

## 주의

- `.env`, 키 파일 등 민감해 보이는 파일이 스테이징되면 커밋 전에 사용자에게 알리고 확인을 받는다.
- push 가 실패하면(예: 원격이 앞서 있음) 강제 push 하지 말고 에러 내용을 보고한다.

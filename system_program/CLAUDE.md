# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 저장소 개요

시스템 프로그래밍 강의자료를 주차별(`week1`, `week2`, `week3`, ...)로 정리하는 저장소입니다. 각 week 폴더에는 강의 PDF 슬라이드가 들어 있으며, 코드나 빌드 설정은 없습니다. Claude Code의 역할은 강의 내용을 정리하고 학습을 보조하는 것입니다.

## 작업 방식

- 강의 PDF의 내용을 정리해 해당 week 폴더 안에 `lecture_summary` 파일로 작성한다.
- 녹음 기반 요약은 `lecture-summary` 스킬로 `summaries/<강의이름>.md`에 작성하며, `lecture_summary` 파일과 별개로 관리한다.
- 사용자가 요청할 경우, 강의 내용을 바탕으로 만든 연습 질문들을 해당 week 폴더의 `quiz` 파일로 작성한다.
- 전문 용어(기술 용어)를 제외한 모든 답변은 한국어로 작성한다.
- 표는 VS Code에서 마크다운 원문으로 볼 때 세로선(`|`)이 줄마다 맞도록 정렬한다. 각 칸을 공백으로 채워 열 너비를 맞추고, 한글 등 전각 문자는 2칸, 영문·숫자·기호는 1칸으로 계산한다. 한 줄이 너무 길어지지 않게 셀 내용은 짧게 쓰고, 긴 설명은 표 아래로 뺀다.

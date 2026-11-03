"""강의 폴더의 영상을 Whisper로 전사하고 PDF 슬라이드 텍스트를 추출한다.

사용법 (lecture_in_inha 루트에서):
  _tools\\transcription\\.venv\\Scripts\\python _tools\\transcription\\transcribe.py _workspace\\system_program\\chapter8 [--model large-v3] [--device cuda|cpu] [--limit 초]
출력 (같은 폴더):
  slides.md                  PDF 페이지별 텍스트
  <영상이름>.transcript.md    [mm:ss] 타임스탬프 전사문
"""
import argparse
import os
import re
import sys
from collections import Counter
from pathlib import Path

# hf_xet 네이티브 DLL이 Windows 애플리케이션 제어 정책에 막히므로 일반 HTTP 다운로드 사용
os.environ.setdefault("HF_HUB_DISABLE_XET", "1")
os.environ.setdefault("HF_HUB_DISABLE_SYMLINKS_WARNING", "1")

VIDEO_EXTS ={".mp4", ".mkv", ".mov", ".avi", ".webm", ".m4a", ".mp3", ".wav"}


def register_cuda_dlls():
    # pip로 설치한 nvidia-cublas / cudnn DLL을 Windows 검색 경로에 추가
    nvidia = Path(sys.prefix) / "Lib" / "site-packages" / "nvidia"
    for bin_dir in nvidia.glob("*/bin"):
        os.add_dll_directory(str(bin_dir))
        os.environ["PATH"] = str(bin_dir) + os.pathsep + os.environ["PATH"]


def extract_slides(pdf_path: Path) -> list[str]:
    from pypdf import PdfReader

    return [(page.extract_text() or "").strip() for page in PdfReader(pdf_path).pages]


def write_slides_md(folder: Path, pdfs: list[Path]) -> list[str]:
    all_pages = []
    lines = []
    for pdf in pdfs:
        pages = extract_slides(pdf)
        all_pages += pages
        lines.append(f"# {pdf.stem}\n")
        for i, text in enumerate(pages, 1):
            lines.append(f"## Slide {i}\n\n```\n{text}\n```\n")
    (folder / "slides.md").write_text("\n".join(lines), encoding="utf-8")
    return all_pages


def build_prompt(pages: list[str], max_terms: int = 60) -> str:
    # 슬라이드에 자주 나오는 영문 용어/레지스터/명령어를 Whisper 힌트로 사용
    words = re.findall(r"%?[A-Za-z][A-Za-z0-9_\-]{2,}", "\n".join(pages))
    counts = Counter(words)
    terms = [w for w, _ in counts.most_common(max_terms)]
    return "대학 강의입니다. 주요 용어: " + ", ".join(terms) + "."


def fmt(t: float) -> str:
    t = int(t)
    h, m, s = t // 3600, t % 3600 // 60, t % 60
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


def transcribe(model, video: Path, prompt: str, limit: float | None) -> str:
    clip = None
    if limit:
        from faster_whisper.audio import decode_audio

        clip = decode_audio(str(video))[: int(limit * 16000)]
    segments, info = model.transcribe(
        clip if clip is not None else str(video),
        language="ko",
        initial_prompt=prompt,
        vad_filter=True,
        beam_size=5,
        condition_on_previous_text=False,
    )
    out = [f"# {video.name} 전사\n"]
    para, para_start = [], None
    for seg in segments:
        if para_start is None:
            para_start = seg.start
        para.append(seg.text.strip())
        print(f"[{fmt(seg.start)}] {seg.text.strip()}", flush=True)
        if seg.end - para_start >= 60:  # 약 1분 단위로 단락 구분
            out.append(f"**[{fmt(para_start)}]** " + " ".join(para) + "\n")
            para, para_start = [], None
    if para:
        out.append(f"**[{fmt(para_start)}]** " + " ".join(para) + "\n")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("folder", type=Path)
    ap.add_argument("--model", default="large-v3")
    ap.add_argument("--device", default="cuda", choices=["cuda", "cpu"])
    ap.add_argument("--limit", type=float, help="앞부분 N초만 전사 (테스트용, 파일 저장 안 함)")
    ap.add_argument("--force", action="store_true", help="이미 있는 전사문도 다시 생성")
    args = ap.parse_args()

    folder = args.folder.resolve()
    pdfs = sorted(folder.glob("*.pdf"))
    videos = sorted(p for p in folder.iterdir() if p.suffix.lower() in VIDEO_EXTS)
    if not videos:
        sys.exit(f"영상이 없습니다: {folder}")

    pages = write_slides_md(folder, pdfs) if pdfs else []
    prompt = build_prompt(pages) if pages else None
    print(f"PDF {len(pdfs)}개 ({len(pages)}쪽), 영상 {len(videos)}개")

    if args.device == "cuda":
        register_cuda_dlls()
    from faster_whisper import WhisperModel

    compute = "float16" if args.device == "cuda" else "int8"
    model = WhisperModel(args.model, device=args.device, compute_type=compute)

    for video in videos:
        out_path = folder / f"{video.stem}.transcript.md"
        if out_path.exists() and not args.force and not args.limit:
            print(f"건너뜀 (이미 있음): {out_path.name}")
            continue
        print(f"\n=== {video.name} ===")
        text = transcribe(model, video, prompt, args.limit)
        if args.limit:
            break
        out_path.write_text(text, encoding="utf-8")
        print(f"저장: {out_path.name}")


if __name__ == "__main__":
    main()

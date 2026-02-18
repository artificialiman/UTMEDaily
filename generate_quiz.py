#!/usr/bin/env python3
"""
generate_quiz.py
Parses JAMB question .txt files and injects the QUESTIONS array
directly into the corresponding quiz HTML pages.

Usage:
    python generate_quiz.py                  # process all .txt files
    python generate_quiz.py physics.txt      # process one file
"""

import os
import re
import sys
import json
from pathlib import Path

# ── File name mapping ─────────────────────────────────────────────────────────
# Maps keywords found in .txt filenames → quiz HTML filenames
FILENAME_MAP = {
    'mathematics': 'quiz-mathematics.html',
    'math':        'quiz-mathematics.html',
    'physics':     'quiz-physics.html',
    'chemistry':   'quiz-chemistry.html',
    'biology':     'quiz-biology.html',
    'english':     'quiz-english.html',
    'literature':  'quiz-literature.html',
    'government':  'quiz-government.html',
    'accounting':  'quiz-accounting.html',
    'economics':   'quiz-economics.html',
    'commerce':    'quiz-commerce.html',
    'crs':         'quiz-crs.html',
}

# ── Parser ────────────────────────────────────────────────────────────────────
def parse_txt(path: Path) -> list[dict]:
    """Parse a JAMB question .txt file into a list of question dicts."""
    questions = []
    current   = None
    collecting_explanation = False
    collecting_exception   = False

    for raw in path.read_text(encoding='utf-8').splitlines():
        line = raw.strip()

        # Skip blank lines and file header
        if not line or re.match(r'^JAMB\s', line) or 'EXCEPTIONAL QUESTIONS' in line:
            continue

        # New question: "1. Question text"
        m = re.match(r'^(\d+)\.\s+(.+)$', line)
        if m:
            if current:
                questions.append(current)
            current = {
                'id':          int(m.group(1)),
                'subject':     subject_from_path(path),
                'text':        m.group(2),
                'options':     {},
                'answer':      None,
                'explanation': '',
                'exception':   '',
            }
            collecting_explanation = False
            collecting_exception   = False
            continue

        if current is None:
            continue

        # Option: "A. text"
        m = re.match(r'^([A-D])\.\s+(.+)$', line)
        if m:
            current['options'][m.group(1)] = m.group(2)
            collecting_explanation = collecting_exception = False
            continue

        # Answer
        if line.startswith('Answer:'):
            current['answer'] = line.replace('Answer:', '').strip()
            collecting_explanation = collecting_exception = False
            continue

        # Explanation
        if line.startswith('Explanation:'):
            current['explanation'] = line.replace('Explanation:', '').strip()
            collecting_explanation = True
            collecting_exception   = False
            continue

        # Exception
        if line.startswith('Exception:'):
            current['exception'] = line.replace('Exception:', '').strip()
            collecting_explanation = False
            collecting_exception   = True
            continue

        # Continuation lines
        if collecting_explanation:
            current['explanation'] += ' ' + line
        elif collecting_exception:
            current['exception'] += ' ' + line

    if current:
        questions.append(current)

    return questions


def subject_from_path(path: Path) -> str:
    """Derive a clean subject name from the filename."""
    name = path.stem  # e.g. JAMB_Mathematics_Q1-35
    # Try to extract the subject word
    parts = re.split(r'[_\-\s]+', name)
    for part in parts:
        if part.lower() in FILENAME_MAP:
            return part.capitalize()
    return parts[-1].capitalize() if parts else name


# ── Injector ──────────────────────────────────────────────────────────────────
def questions_to_js(questions: list[dict]) -> str:
    """Render the QUESTIONS JS array as a formatted string."""
    lines = ['const QUESTIONS = [']
    for i, q in enumerate(questions):
        comma = '' if i == len(questions) - 1 else ','
        opts  = q.get('options', {})
        explanation = q.get('explanation', '').replace('`', "'").replace('\\', '\\\\')
        exception   = q.get('exception',   '').replace('`', "'").replace('\\', '\\\\')
        text        = q['text'].replace('`', "'").replace('\\', '\\\\')
        lines.append(f'  {{')
        lines.append(f'    id: {q["id"]}, subject: {json.dumps(q["subject"])},')
        lines.append(f'    text: {json.dumps(text)},')
        lines.append(f'    options: {{')
        lines.append(f'      A: {json.dumps(opts.get("A",""))},')
        lines.append(f'      B: {json.dumps(opts.get("B",""))},')
        lines.append(f'      C: {json.dumps(opts.get("C",""))},')
        lines.append(f'      D: {json.dumps(opts.get("D",""))}')
        lines.append(f'    }},')
        lines.append(f'    answer: {json.dumps(q.get("answer",""))},')
        lines.append(f'    explanation: {json.dumps(explanation)},')
        lines.append(f'    exception: {json.dumps(exception)}')
        lines.append(f'  }}{comma}')
    lines.append('];')
    return '\n'.join(lines)


def inject_into_html(html_path: Path, questions: list[dict], duration: int) -> bool:
    """
    Replace the QUESTIONS block between the two sentinel comments in the HTML.
    The block looks like:
        <!-- QUESTIONS_START -->
        const DURATION  = ...;
        const QUESTIONS = [...];
        <!-- QUESTIONS_END -->
    """
    html = html_path.read_text(encoding='utf-8')

    new_block = (
        f'const DURATION  = {duration}; // seconds\n\n'
        + questions_to_js(questions)
    )

    # Try sentinel comment replacement first (most reliable)
    pattern = r'(<!-- QUESTIONS_START -->).*?(<!-- QUESTIONS_END -->)'
    replacement = r'\g<1>\n' + new_block + r'\n\2'
    new_html, count = re.subn(pattern, replacement, html, flags=re.DOTALL)

    if count == 0:
        # Fallback: replace between const DURATION and closing ];
        pattern2 = r'(const DURATION\s*=\s*\d+;.*?const QUESTIONS\s*=\s*\[).*?(\];)'
        replacement2 = new_block
        new_html, count = re.subn(pattern2, replacement2, html, flags=re.DOTALL)

    if count == 0:
        print(f'  ⚠️  Could not find injection point in {html_path.name} — skipping')
        return False

    html_path.write_text(new_html, encoding='utf-8')
    return True


# ── Main ──────────────────────────────────────────────────────────────────────
def resolve_html(txt_path: Path) -> Path | None:
    """Find the quiz HTML file that corresponds to a .txt file."""
    name_lower = txt_path.stem.lower()
    for keyword, html_name in FILENAME_MAP.items():
        if keyword in name_lower:
            return Path(html_name)
    return None


def process_file(txt_path: Path) -> bool:
    html_path = resolve_html(txt_path)
    if html_path is None:
        print(f'  ⚠️  No HTML mapping for {txt_path.name} — skipping')
        return False

    if not html_path.exists():
        print(f'  ⚠️  {html_path} does not exist — skipping')
        return False

    questions = parse_txt(txt_path)
    if not questions:
        print(f'  ⚠️  No questions parsed from {txt_path.name} — skipping')
        return False

    # Duration: 15 min for individual subjects
    duration = 900

    ok = inject_into_html(html_path, questions, duration)
    if ok:
        print(f'  ✅  {txt_path.name} → {html_path.name} ({len(questions)} questions)')
    return ok


def main():
    txt_files = []

    if len(sys.argv) > 1:
        # Specific files passed as arguments
        txt_files = [Path(f) for f in sys.argv[1:] if f.endswith('.txt')]
    else:
        # All .txt files in current directory
        txt_files = sorted(Path('.').glob('*.txt'))

    if not txt_files:
        print('No .txt files found.')
        sys.exit(0)

    print(f'\n📚 Processing {len(txt_files)} file(s)...\n')
    success = 0
    for f in txt_files:
        if process_file(f):
            success += 1

    print(f'\n{"─"*40}')
    print(f'Done: {success}/{len(txt_files)} files processed successfully.')
    if success < len(txt_files):
        sys.exit(1)


if __name__ == '__main__':
    main()

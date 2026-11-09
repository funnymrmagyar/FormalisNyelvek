# 4. feladat: regexek (android logcat)
#
# Futtatás:
#   python -m project --input input_file.txt --output output_file1.txt --rgx 1

import re
import sys

from .problem import Problems

# A feladatban megadott kifejezés. Csoportok:
# 2 = időbélyeg, 3 = pid, 4 = tid, 5 = szint, 6 = tag, 7 = üzenet
LINE = re.compile(
    r"(([0-9-]+ [0-9:.]+) +([0-9]+) +([0-9]+) ([IDVEFAW]) (.+?):(?: (.+))?)"
)


def parse(lines):
    """Csak a logsorokat adja vissza (nyers sor + a regex találata)."""
    for line in lines:
        m = LINE.match(line)
        if m:
            yield line, m


def task1(lines):
    c = [0] * 10
    for line in lines:
        if re.match(r"10-15 ", line):
            c[0] += 1
        if re.match(r"10-15 10:18:51\.", line):
            c[1] += 1
        if re.match(r"[0-9-]+ [0-9]{2}:[0-9]{2}:51\.", line):
            c[2] += 1

        m = LINE.match(line)
        if not m:
            continue
        ts, pid, level, tag, msg = m.group(2), m.group(3), m.group(5), m.group(6), m.group(7)

        if re.fullmatch(r"lowmemorykiller\s*", tag):
            c[3] += 1
        if re.fullmatch(r"[0-9-]+ 10:18:51\.[0-9]+", ts) and re.fullmatch(r"221", pid):
            c[4] += 1
        if re.fullmatch(r"E", level):
            c[5] += 1
        if re.fullmatch(r"W", level) and re.fullmatch(r"PackageManager\s*", tag):
            c[6] += 1
        if re.fullmatch(r"D", level) and re.search(r"ExoPlayer", line):
            c[7] += 1
        if re.fullmatch(r"[EW]", level) and re.search(r"\.java:", line):
            c[8] += 1
        if msg and re.search(r"Thread", msg):
            c[9] += 1
    return [str(x) for x in c]


def task2(lines):
    out = []
    for line, m in parse(lines):
        if re.fullmatch(r"E", m.group(5)) and m.group(7):
            out.extend(re.findall(r"([\w$]+\.java):[0-9]+", m.group(7)))
    return out


def task3(lines):
    seen = []
    for line, m in parse(lines):
        pid = m.group(3)
        if pid not in seen:
            seen.append(pid)
    return seen


def task4(lines):
    counts = {}
    for line, m in parse(lines):
        if re.fullmatch(r"E", m.group(5)):
            counts[m.group(3)] = counts.get(m.group(3), 0) + 1
    if not counts:
        return []
    pid = max(counts, key=lambda p: counts[p])  # döntetlennél az első előfordulás
    return [f"PID={pid} ({counts[pid]} errors)"]


def task5(lines):
    n = 0
    for line, m in parse(lines):
        if re.fullmatch(r"E", m.group(5)) and m.group(3) == m.group(4):
            n += 1
    return [str(n)]


TASKS = {1: task1, 2: task2, 3: task3, 4: task4, 5: task5}


class RegexProblem(Problems):
    """Logcat állomány feldolgozása reguláris kifejezésekkel."""

    def run(self, args, input_file: str, output_file: str):
        task = TASKS.get(args.rgx)
        if task is None:
            print(f"Hiba: ismeretlen feladatszám: {args.rgx} (1-5 lehet)", file=sys.stderr)
            sys.exit(1)

        try:
            with open(input_file, "r", encoding="utf-8", errors="replace") as f:
                lines = f.readlines()
        except OSError as e:
            print(f"Hiba: {e}", file=sys.stderr)
            sys.exit(1)

        result = task(lines)
        with open(output_file, "w", encoding="utf-8") as f:
            for r in result:
                f.write(r + "\n")
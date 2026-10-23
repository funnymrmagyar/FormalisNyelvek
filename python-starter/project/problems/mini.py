# 3. feladat: determinisztikus véges automata minimalizálása
#
# Futtatás:
#   python -m project --input input_file1.txt --output output_file1.txt --mini

import re
import sys

from .problem import Problems

# Az elérhetetlen állapotokat elhagyja (a minimális automatában nincsenek).
# Ha nem akarod, írd át False-ra.
REMOVE_UNREACHABLE = True


class AutomataError(Exception):
    pass


def nat_key(name):
    """Természetes sorrend: q2 < q10."""
    return [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", name)]


def new_name(name):
    """q1 -> s1"""
    m = re.fullmatch(r"\D*(\d+)", name)
    return "s" + (m.group(1) if m else name)


def read_automaton(path):
    with open(path, encoding="utf-8") as f:
        lines = [l.rstrip("\n") for l in f]

    if len(lines) < 4:
        raise AutomataError("A bemeneti fájl legalább 4 sort kell tartalmazzon.")

    states = lines[0].split()
    alphabet = lines[1].split()
    start_tokens = lines[2].split()
    finals = lines[3].split()

    if len(start_tokens) != 1:
        raise AutomataError("Pontosan egy kezdőállapotot kell megadni.")
    start = start_tokens[0]

    if start not in states:
        raise AutomataError(f"Ismeretlen kezdőállapot: {start}")
    for q in finals:
        if q not in states:
            raise AutomataError(f"Ismeretlen végállapot: {q}")

    delta = {}
    for i, line in enumerate(lines[4:], start=5):
        if not line.strip():
            continue
        parts = line.split()
        if len(parts) != 3:
            raise AutomataError(f"{i}. sor: hibás átmenet formátum: '{line}'")
        src, sym, dst = parts
        if src not in states:
            raise AutomataError(f"{i}. sor: ismeretlen állapot: {src}")
        if sym not in alphabet:
            raise AutomataError(f"{i}. sor: ismeretlen jel: {sym}")
        if dst not in states:
            raise AutomataError(f"{i}. sor: ismeretlen állapot: {dst}")
        if (src, sym) in delta and delta[(src, sym)] != dst:
            raise AutomataError(f"{i}. sor: az automata nem determinisztikus ({src} {sym})")
        delta[(src, sym)] = dst

    return states, alphabet, start, finals, delta


def minimize(states, alphabet, start, finals, delta):
    # elérhető állapotok
    reach = {start}
    stack = [start]
    while stack:
        q = stack.pop()
        for a in alphabet:
            t = delta.get((q, a))
            if t is not None and t not in reach:
                reach.add(t)
                stack.append(t)

    live = [q for q in states if q in reach] if REMOVE_UNREACHABLE else list(states)
    live = list(dict.fromkeys(live))
    finals_set = set(finals)

    # Partíciófinomítás. A None a hiányzó átmenetek (csapda) helyettesítője.
    cls = {q: (1 if q in finals_set else 0) for q in live}
    cls[None] = 0
    everyone = live + [None]

    while True:
        sig = {
            q: (cls[q], tuple(cls[delta.get((q, a))] for a in alphabet))
            for q in everyone
        }
        ids = {}
        new = {q: ids.setdefault(sig[q], len(ids)) for q in everyone}
        stable = len(ids) == len(set(cls.values()))
        cls = new
        if stable:
            break

    # osztályok legkisebb nevű képviselője
    members = {}
    for q in live:
        members.setdefault(cls[q], []).append(q)
    rep = {c: min(m, key=nat_key) for c, m in members.items()}

    def r(q):
        return rep[cls[q]]

    reps = sorted(set(rep.values()), key=nat_key)
    new_start = r(start)
    new_finals = sorted({r(q) for q in live if q in finals_set}, key=nat_key)

    transitions = set()
    for (src, sym), dst in delta.items():
        if src in cls and dst in cls and src in live and dst in live:
            transitions.add((r(src), sym, r(dst)))
    transitions = sorted(transitions, key=lambda t: (nat_key(t[0]), t[1], nat_key(t[2])))

    return reps, new_start, new_finals, transitions


def write_automaton(path, reps, alphabet, new_start, new_finals, transitions):
    with open(path, "w", encoding="utf-8") as f:
        f.write(" ".join(new_name(q) for q in reps) + "\n")
        f.write(" ".join(alphabet) + "\n")
        f.write(new_name(new_start) + "\n")
        f.write(" ".join(new_name(q) for q in new_finals) + "\n")
        for src, sym, dst in transitions:
            f.write(f"{new_name(src)} {sym} {new_name(dst)}\n")


class Minimization(Problems):
    """Determinisztikus véges automata minimalizálása."""

    def run(self, args, input_file: str, output_file: str):
        try:
            states, alphabet, start, finals, delta = read_automaton(input_file)
        except (AutomataError, OSError) as e:
            print(f"Hiba: {e}", file=sys.stderr)
            sys.exit(1)

        reps, new_start, new_finals, trans = minimize(states, alphabet, start, finals, delta)
        write_automaton(output_file, reps, alphabet, new_start, new_finals, trans)
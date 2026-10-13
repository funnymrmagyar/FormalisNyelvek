# 2. feladat: véges automata determinizálása
#
# Futtatás:
#   python -m project --input input_file1.txt --output output_file1.txt --det

import sys

from .problem import Problems


class AutomataError(Exception):
    pass


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
        delta.setdefault((src, sym), set()).add(dst)

    return states, alphabet, start, finals, delta


def determinize(states, alphabet, start, finals, delta):
    sorted_alpha = sorted(alphabet)
    start_set = frozenset([start])

    index = {start_set: 0}
    order = [start_set]
    transitions = []

    i = 0
    while i < len(order):
        current = order[i]
        for sym in sorted_alpha:
            target = set()
            for q in current:
                target |= delta.get((q, sym), set())
            if not target:
                continue
            target = frozenset(target)
            if target not in index:
                index[target] = len(order)
                order.append(target)
            transitions.append((i, sym, index[target]))
        i += 1

    finals_set = set(finals)
    new_finals = [k for k, S in enumerate(order) if S & finals_set]
    transitions.sort(key=lambda t: (t[0], t[1], t[2]))
    return len(order), new_finals, transitions


def write_automaton(path, n_states, alphabet, new_finals, transitions):
    with open(path, "w", encoding="utf-8") as f:
        f.write(" ".join(f"s{k}" for k in range(n_states)) + "\n")
        f.write(" ".join(alphabet) + "\n")
        f.write("s0\n")
        f.write(" ".join(f"s{k}" for k in new_finals) + "\n")
        for src, sym, dst in transitions:
            f.write(f"s{src} {sym} s{dst}\n")


class Determinization(Problems):
    """Véges automata determinizálása részhalmaz-konstrukcióval."""

    def run(self, args, input_file: str, output_file: str):
        try:
            states, alphabet, start, finals, delta = read_automaton(input_file)
        except (AutomataError, OSError) as e:
            print(f"Hiba: {e}", file=sys.stderr)
            sys.exit(1)

        n, new_finals, trans = determinize(states, alphabet, start, finals, delta)
        write_automaton(output_file, n, alphabet, new_finals, trans)
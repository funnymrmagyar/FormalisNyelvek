# 1. Feladat: Determinisztikus véges automata (DFA) szimulációja
#
# Bemeneti fájl formátuma:
#   1. sor: állapotok szóközzel elválasztva        pl. q0 q1 q2
#   2. sor: ábécé elemei szóközzel elválasztva     pl. 0 1
#   3. sor: kezdőállapot                           pl. q0
#   4. sor: végállapot(ok) szóközzel elválasztva   pl. q0
#   5+. sor: átmenetek formátuma: <állapot> <jel> <következő állapot>
#             pl. q0 0 q2
#
# Parancs:
#   python -m project --input input.txt --output output.txt --check abb
#   Több szó: --check a,ab,abc  (vesszővel elválasztva, szóközök nélkül)
#
# Kimenet: minden szóra egy sor, "IGEN" ha elfogadott, "NEM" ha nem.

from .problem import Problems


class DFAProblem(Problems):
    """DFA szimulációja: beolvas egy automatát, majd szavakat ellenőriz."""

    # ------------------------------------------------------------------ #
    #  Segédosztály: maga a DFA                                           #
    # ------------------------------------------------------------------ #
    class DFA:
        def __init__(self):
            self.states = []          # összes állapot listája
            self.alphabet = []        # ábécé elemei
            self.start = None         # kezdőállapot
            self.finals = set()       # végállapotok halmaza
            self.transitions = {}     # (állapot, jel) -> következő állapot

        def load(self, filepath: str):
            """Betölti az automatát a fájlból."""
            with open(filepath, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f.readlines()]

            # Üres sorok kiszűrése
            lines = [l for l in lines if l]

            self.states  = lines[0].split()
            self.alphabet = lines[1].split()
            self.start   = lines[2].strip()
            self.finals  = set(lines[3].split())

            # Átmenetek beolvasása
            for line in lines[4:]:
                parts = line.split()
                if len(parts) == 3:
                    from_state, symbol, to_state = parts
                    self.transitions[(from_state, symbol)] = to_state

        def accepts(self, word: str) -> bool:
            """Eldönti, hogy az automata elfogadja-e a szót."""
            current = self.start
            for symbol in word:
                key = (current, symbol)
                if key not in self.transitions:
                    # Nincs átmenet -> a szó nem fogadható el
                    return False
                current = self.transitions[key]
            return current in self.finals

    # ------------------------------------------------------------------ #
    #  run(): a Problems interfész megvalósítása                          #
    # ------------------------------------------------------------------ #
    def run(self, args, input_file: str, output_file: str):
        # Automata betöltése
        automata = self.DFA()
        automata.load(input_file)

        # Ellenőrzendő szavak beolvasása (vesszővel elválasztva)
        words = args.check.split(",")

        # Eredmények kiírása
        results = []
        for word in words:
            word = word.strip()
            if automata.accepts(word):
                results.append("IGEN")
            else:
                results.append("NEM")

        with open(output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(results) + "\n")

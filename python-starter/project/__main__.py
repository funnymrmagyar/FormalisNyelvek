"""
Formális Nyelvek – Házi feladat keretrendszer
==============================================

Futtatás (a python-starter mappából!):
    python -m project --input <bemeneti_fájl> --output <kimeneti_fájl> --check <szó/szavak>

Példa:
    python -m project --input input_file1.txt --output output_file1.txt --check abb
    python -m project --input input_file1.txt --output output_file1.txt --check a,ab,abb

Kapcsolók:
    --input   : bemeneti fájl (automata leírása)
    --output  : kimeneti fájl (eredmények)
    --check   : ellenőrzendő szó vagy szavak (vesszővel elválasztva, szóközök nélkül)
    --sum     : (példa) összeadás feladat
"""

import argparse
import sys

from .problems import DFAProblem, SumProblem


def parse_args():
    """Parancssori argumentumok feldolgozása."""
    parser = argparse.ArgumentParser(
        description="Formális Nyelvek – automata szimulátor"
    )
    parser.add_argument("--input",  required=True, help="Bemeneti fájl neve")
    parser.add_argument("--output", required=True, help="Kimeneti fájl neve")

    # Feladatkapcsolók – minden feladathoz külön flag
    parser.add_argument("--check", type=str, default=None,
                        help="Ellenőrzendő szó(k), vesszővel elválasztva (pl. abb vagy a,ab,abb)")
    parser.add_argument("--sum",   action="store_true", default=False,
                        help="Összeadás feladat futtatása (példa)")

    return parser.parse_args()


def main():
    args = parse_args()

    # Feladat kiválasztása az aktív kapcsoló alapján
    if args.check is not None:
        # 1. feladat: DFA szimuláció
        problem = DFAProblem()
        problem.run(args, args.input, args.output)

    elif args.sum:
        # Példa feladat: összeadás
        problem = SumProblem()
        problem.run(args, args.input, args.output)

    else:
        print("Hiba: Adjon meg legalább egy feladatkapcsolót (pl. --check <szó>)!")
        sys.exit(1)


if __name__ == "__main__":
    main()

# Példa feladat: vesszővel elválasztott számok összeadása.
# Bemenet:  egy sor, pl. "3,5,7"
# Kimenet:  az összeg,  pl. "15"
#
# Futtatás:
#   python -m project --input input_file1.txt --output output_file1.txt --sum

from .problem import Problems


class SumProblem(Problems):
    """Összeadja a bemeneti fájlban vesszővel elválasztott számokat."""

    def run(self, args, input_file: str, output_file: str):
        with open(input_file, "r", encoding="utf-8") as f:
            line = f.readline().strip()

        numbers = [int(x) for x in line.split(",")]
        result = sum(numbers)

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(str(result) + "\n")

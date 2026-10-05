# Alap (absztrakt) Problems osztály.
# Minden feladatot megvalósító osztálynak ebből kell származnia,
# és felül kell írnia a run() metódust.

class Problems:
    def run(self, args, input_file: str, output_file: str):
        """
        args        -- az argparse által visszaadott Namespace objektum
        input_file  -- a bemeneti fájl elérési útja
        output_file -- a kimeneti fájl elérési útja
        """
        raise NotImplementedError("A run() metódust felül kell írni!")

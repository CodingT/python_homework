import pandas as pd


class DFPlus(pd.DataFrame):
    @property
    def _constructor(self):
        return DFPlus

    @classmethod
    def from_csv(cls, filepath, **kwargs):
        df = pd.read_csv(filepath, **kwargs)
        return cls(df)

    def print_with_headers(self):
        chunk_size = 10
        total_rows = len(self)

        for start in range(0, total_rows, chunk_size):
            end = min(start + chunk_size, total_rows)
            chunk = super().iloc[start:end]

            print(f"\nRows {start+1} to {end}:")
            print(chunk)

            if end < total_rows:
                print("\n" + "*" * 80 + "\n")


dfp = DFPlus.from_csv("../csv/products.csv")


dfp.print_with_headers()

import pandas as pd


def extract_benchmark_data():
    """
    Extract the first 5000 rows from the PII-200k dataset. 
    This data is used for the benchmark experiments. 
    """
    # Load the original data
    df = pd.read_csv("./experiments/data/pii_200k.csv")

    # Get the first 5000 rows
    df = df.head(5000)

    # Export the first 5000 rows to a csv file
    df.to_csv("./experiments/data/benchmark_data.csv", index=False)


if __name__ == "__main__":
    extract_benchmark_data()

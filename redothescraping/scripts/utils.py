import pandas as pd

def save_to_csv(data, file_path):
    """
    Save a list of dictionaries to a CSV file.
    """
    df = pd.DataFrame(data)
    df.to_csv(file_path, index=False)
    print(f"Data saved to {file_path}")

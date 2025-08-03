import pandas as pd
from pathlib import Path

# Put your four files in the same folder and adjust the pattern if names differ
import pandas as pd

files = [
    "scopus-first-query-2016-2018.csv",
    "scopus-first-query-2020-2021.csv",
    "scopus-first-query-2022-2023.csv",
    "scopus-first-query-2024-2026.csv"
]

# === 2. Read & concat ===
dfs = [pd.read_csv(f) for f in files]
df = pd.concat(dfs, ignore_index=True)

# === 3. De-duplicate ===
# Build a key: use DOI if present, otherwise Title+Year
has_doi = df['DOI'].notna()
df.loc[has_doi, 'dup_key'] = df.loc[has_doi, 'DOI'].str.lower().str.strip()
df.loc[~has_doi, 'dup_key'] = (
    df.loc[~has_doi, 'Title'].str.lower().str.strip()
    + "_" + df.loc[~has_doi, 'Year'].astype(str)
)
df = df.drop_duplicates(subset='dup_key').drop(columns='dup_key')

# === 4. Save the merged file ===
output_path = "scopus_merged_2016-2026_merged.csv"
df.to_csv(output_path, index=False)

print(f"Merged {len(files)} files → {len(df)} unique rows saved to:\n  {output_path}")
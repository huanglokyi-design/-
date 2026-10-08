"""Find collocates for the target word 福贵 in sentences.txt.

Runs find_collocates three times:
  1. method="window", horizon=5
  2. method="window", horizon=10
  3. method="sentence"

For each run: removes stopwords, keeps collocates with >= 2 characters and
p-value < 0.05, sorts by obs_local descending, saves to output/*.csv, and
prints the top 20 rows.
"""

import os

import pandas as pd
from qhchina import load_stopwords
from qhchina.analytics.collocations import find_collocates

INPUT_PATH = "sentences.txt"
OUTPUT_DIR = "output"
TARGET = "福贵"
MAX_P = 0.05

RUNS = [
    {"name": "window_h5", "method": "window", "horizon": 5},
    {"name": "window_h10", "method": "window", "horizon": 10},
    {"name": "sentence", "method": "sentence", "horizon": None},
]


def load_sentences(path: str) -> list[list[str]]:
    with open(path, encoding="utf-8") as f:
        return [line.split() for line in f if line.strip()]


def main() -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    sentences = load_sentences(INPUT_PATH)
    print(f"Loaded {len(sentences)} sentences from {INPUT_PATH}")

    # Stopwords: bundled list plus the user-specified extras
    stopwords = load_stopwords("zh_sim")
    stopwords.update({"的", "了", "在", "是", "我", "有", "和", "就",
                      "不", "人", "都", "一", "一个", "上"})
    print(f"Using {len(stopwords)} stopwords")

    filters = {
        "stopwords": list(stopwords),
        "min_word_length": 2,
        "max_p": MAX_P,
    }

    for run in RUNS:
        print(f"\n=== Run: {run['name']} (method={run['method']}, "
              f"horizon={run['horizon']}) ===")
        df = find_collocates(
            sentences,
            TARGET,
            method=run["method"],
            horizon=run["horizon"],
            filters=filters,
            sort_by="obs_local",
            ascending=False,
        )

        out_path = os.path.join(OUTPUT_DIR, f"collocates_{run['name']}.csv")
        df.to_csv(out_path, index=False, encoding="utf-8-sig")
        print(f"Saved {len(df)} collocates to {out_path}")
        print(df.head(20).to_string(index=False))


if __name__ == "__main__":
    main()
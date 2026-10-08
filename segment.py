"""Segment the novel into tokenized sentences.

- Loads data/novel.txt (UTF-8)
- Converts text to simplified Chinese with OpenCC (jieba works better with simplified)
- Splits text into sentences on Chinese sentence-ending punctuation (。！？)
- Tokenizes each sentence with jieba, removing punctuation
- Keeps only sentences with at least 5 words
- Saves to sentences.txt: one sentence per line, words separated by single spaces
"""

import re

import jieba
from opencc import OpenCC

INPUT_PATH = "data/novel.txt"
OUTPUT_PATH = "sentences.txt"
MIN_WORDS = 5

# Sentence-ending punctuation (full-width and related marks)
SENTENCE_ENDINGS = "。！？!?\n"
# Characters treated as punctuation and removed from token output
PUNCT_PATTERN = re.compile(r"[\s\u3000-\u303F\uFF00-\uFFEF\u2000-\u206F]+")

cc = OpenCC("t2s")  # traditional -> simplified


def is_punctuation(token: str) -> bool:
    """A token is punctuation if it contains no word characters (letters/digits/CJK)."""
    return not re.search(r"[\w\u4e00-\u9fff]", token)


def main() -> None:
    with open(INPUT_PATH, encoding="utf-8") as f:
        text = f.read()

    # Convert to simplified Chinese
    text = cc.convert(text)

    # Split into sentences on 。！？ (and newlines)
    sentences = re.split(r"[。！？!?\n]+", text)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as out:
        kept = 0
        for sent in sentences:
            sent = sent.strip()
            if not sent:
                continue
            words = [
                w for w in jieba.cut(sent)
                if not is_punctuation(w)
            ]
            if len(words) < MIN_WORDS:
                continue
            out.write(" ".join(words) + "\n")
            kept += 1

    print(f"Wrote {kept} sentences to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
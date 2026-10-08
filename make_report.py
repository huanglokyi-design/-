"""Build a single-page HTML report from the three collocate CSVs.

Reads output/collocates_*.csv and writes output/results.html with a
dropdown to switch between the three tables.
"""

import os

import pandas as pd

OUTPUT_DIR = "output"
CSV_FILES = [
    ("window_h5", "Window (horizon=5)", "collocates_window_h5.csv"),
    ("window_h10", "Window (horizon=10)", "collocates_window_h10.csv"),
    ("sentence", "Sentence", "collocates_sentence.csv"),
]

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="utf-8">
<title>Collocates of 福贵</title>
<style>
  body {{ font-family: -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif;
         max-width: 900px; margin: 2rem auto; padding: 0 1rem; color: #222; }}
  h1 {{ font-size: 1.4rem; }}
  .controls {{ margin: 1rem 0; }}
  select {{ font-size: 1rem; padding: 0.4rem 0.6rem; }}
  .meta {{ color: #666; font-size: 0.9rem; margin-bottom: 0.8rem; }}
  table {{ border-collapse: collapse; width: 100%; font-size: 0.95rem; }}
  th, td {{ border: 1px solid #ddd; padding: 0.4rem 0.7rem; text-align: right; }}
  th {{ background: #f4f4f4; }}
  td:first-child, th:first-child, td:nth-child(2), th:nth-child(2) {{ text-align: left; }}
  tr:nth-child(even) {{ background: #fafafa; }}
  .table-block {{ display: none; }}
  .table-block.active {{ display: block; }}
</style>
</head>
<body>
<h1>Collocates of “福贵” in 《活着》</h1>
<div class="controls">
  <label for="run-select">Analysis run: </label>
  <select id="run-select">
{options}
  </select>
</div>
{blocks}
<script>
  const select = document.getElementById('run-select');
  select.addEventListener('change', () => {{
    document.querySelectorAll('.table-block').forEach(b =>
      b.classList.toggle('active', b.id === 'run-' + select.value));
  }});
</script>
</body>
</html>
"""


def build_block(run_id: str, label: str, df: pd.DataFrame) -> str:
    rows = df.to_html(index=False, border=0, classes=None, escape=False)
    return (f'<div class="table-block" id="run-{run_id}">\n'
            f'<p class="meta">{label} — {len(df)} collocates (p &lt; 0.05, '
            f'&ge; 2 chars, stopwords removed)</p>\n{rows}\n</div>')


def main() -> None:
    options = []
    blocks = []
    for i, (run_id, label, filename) in enumerate(CSV_FILES):
        path = os.path.join(OUTPUT_DIR, filename)
        df = pd.read_csv(path)
        selected = " selected" if i == 0 else ""
        options.append(f'    <option value="{run_id}"{selected}>{label}</option>')
        blocks.append(build_block(run_id, label, df))

    html = HTML_TEMPLATE.format(
        options="\n".join(options),
        blocks="\n".join(blocks),
    )

    out_path = os.path.join(OUTPUT_DIR, "results.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
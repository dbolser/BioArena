# The Arena

Differential testing of BioPAIthon against Biopython, release for release.

Two venues:

- **The arena** (`arena.py`): downstream projects' own test suites, run twice,
  once on `biopython==1.88` and once on `biopaithon==1.88`. Only the delta
  between the two runs is reported. A test that fails on both is the project's
  problem; a test that passes on Biopython and fails on BioPAIthon is ours.
- **The crucible** (`crucible.py`): real files from the wild (RCSB mmCIF,
  BinaryCIF and PDB, Pfam Stockholm, GenBank) parsed by both libraries, with
  the parsed results digested and compared field by field.

```
uv run arena.py run                 # all targets in targets.toml
uv run arena.py run pydna augur     # a subset
uv run arena.py report              # rebuild REPORT.md from results/
uv run crucible.py fetch            # build corpus/
uv run crucible.py run              # parse with both sides, diff
```

Override the sides with `--bio biopython==1.88 --pai /path/to/checkout`.

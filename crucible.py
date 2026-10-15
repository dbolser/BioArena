#!/usr/bin/env python3
"""The crucible: parse wild files with both libraries and diff the digests."""

import argparse
import json
import random
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CORPUS = ROOT / "corpus"
WORK = ROOT / "work" / "_crucible"
PROBE = ROOT / "crucible" / "probe.py"
SIDES = ("bio", "pai")


def get(url, dest, retries=3):
    if dest.exists():
        return True
    for i in range(retries):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                dest.write_bytes(r.read())
            return True
        except Exception as e:  # noqa: BLE001
            err = e
            time.sleep(1 + i)
    print(f"  skip {url}: {err}", file=sys.stderr)
    return False


def fetch(args):
    rng = random.Random(args.seed)
    (CORPUS / "rcsb").mkdir(parents=True, exist_ok=True)
    ids = json.load(urllib.request.urlopen("https://data.rcsb.org/rest/v1/holdings/current/entry_ids"))
    sample = rng.sample(sorted(ids), args.structures)
    print(f"RCSB: {len(ids)} entries, sampling {len(sample)}")
    for i, pid in enumerate(sample):
        get(f"https://files.rcsb.org/download/{pid}.cif.gz", CORPUS / "rcsb" / f"{pid}.cif.gz")
        get(f"https://models.rcsb.org/{pid}.bcif", CORPUS / "rcsb" / f"{pid}.bcif")
        get(f"https://files.rcsb.org/download/{pid}.pdb.gz", CORPUS / "rcsb" / f"{pid}.pdb.gz", retries=1)
        if i % 25 == 0:
            print(f"  {i}/{len(sample)}")

    (CORPUS / "pfam").mkdir(exist_ok=True)
    accs = []
    url = "https://www.ebi.ac.uk/interpro/wwwapi/entry/pfam/?page_size=200"
    while url and len(accs) < 1000:
        page = json.load(urllib.request.urlopen(url))
        accs += [e["metadata"]["accession"] for e in page["results"]]
        url = page.get("next")
    sample = rng.sample(accs, args.alignments)
    print(f"Pfam: sampling {len(sample)} seed alignments")
    for acc in sample:
        get(f"https://www.ebi.ac.uk/interpro/wwwapi/entry/pfam/{acc}/?annotation=alignment:seed&download",
            CORPUS / "pfam" / f"{acc}.sto.gz")

    (CORPUS / "genbank").mkdir(exist_ok=True)
    base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    q = json.load(urllib.request.urlopen(
        f"{base}/esearch.fcgi?db=nuccore&term=plasmid[title]+AND+2000:30000[SLEN]+AND+srcdb_refseq[prop]"
        f"&retmax=500&retmode=json"))
    sample = rng.sample(q["esearchresult"]["idlist"], args.genbank)
    print(f"GenBank: sampling {len(sample)} RefSeq plasmids")
    for uid in sample:
        get(f"{base}/efetch.fcgi?db=nuccore&id={uid}&rettype=gbwithparts&retmode=text",
            CORPUS / "genbank" / f"{uid}.gb")
        time.sleep(0.4)


def side_python(side, spec, args):
    venv = WORK / f"venv-{side}"
    py = venv / "bin" / "python"
    if not py.exists():
        subprocess.run(["uv", "venv", "--quiet", "--python", args.python, str(venv)], check=True)
        subprocess.run(["uv", "pip", "install", "--quiet", "--python", str(py), spec, "msgpack"], check=True)
    return py


def run(args):
    WORK.mkdir(parents=True, exist_ok=True)
    digests = {}
    for side in SIDES:
        py = side_python(side, getattr(args, side), args)
        ver = subprocess.run([str(py), "-I", "-c", "import Bio; print(Bio.__version__, Bio.__file__)"],
                             capture_output=True, text=True).stdout.strip()
        print(f"{side}: {ver}")
        out = subprocess.run([str(py), "-I", str(PROBE), str(args.corpus)], capture_output=True, text=True)
        if out.returncode:
            print(out.stderr)
            sys.exit(f"probe failed on {side}")
        digests[side] = json.loads(out.stdout)
        (WORK / f"digest-{side}.json").write_text(out.stdout)
    report(*(digests[s] for s in SIDES))


def report(bio, pai):
    files = sorted(set(bio) | set(pai))
    same, diffs = 0, []
    for f in files:
        a, b = bio.get(f), pai.get(f)
        if a == b:
            same += 1
            continue
        keys = sorted(set(a or {}) | set(b or {}))
        diffs.append((f, {k: (a.get(k) if a else None, b.get(k) if b else None)
                          for k in keys if (a or {}).get(k) != (b or {}).get(k)}))
    errors = {s: sum(1 for r in d.values() if "error" in r) for s, d in (("bio", bio), ("pai", pai))}
    lines = ["# Crucible report", "", f"files: {len(files)}, identical: {same}, differing: {len(diffs)}",
             f"parse errors: bio {errors['bio']}, pai {errors['pai']}", ""]
    for f, d in diffs:
        lines.append(f"## {f}\n")
        for k, (x, y) in d.items():
            lines.append(f"- **{k}**")
            lines.append(f"  - bio: `{json.dumps(x, default=str)[:400]}`")
            lines.append(f"  - pai: `{json.dumps(y, default=str)[:400]}`")
        lines.append("")
    text = "\n".join(lines)
    (ROOT / "CRUCIBLE.md").write_text(text)
    print(text[:4000])
    print(f"\nwrote {ROOT / 'CRUCIBLE.md'}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["fetch", "run", "report"])
    ap.add_argument("--bio", default="biopython==1.88")
    ap.add_argument("--pai", default="biopaithon==1.88")
    ap.add_argument("--python", default="3.12")
    ap.add_argument("--corpus", default=str(CORPUS))
    ap.add_argument("--seed", type=int, default=88)
    ap.add_argument("--structures", type=int, default=200)
    ap.add_argument("--alignments", type=int, default=60)
    ap.add_argument("--genbank", type=int, default=50)
    args = ap.parse_args()
    if args.cmd == "fetch":
        fetch(args)
    elif args.cmd == "run":
        run(args)
    else:
        report(*(json.loads((WORK / f"digest-{s}.json").read_text()) for s in SIDES))


if __name__ == "__main__":
    main()

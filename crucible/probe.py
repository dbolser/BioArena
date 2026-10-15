"""Parse every file in a directory with whichever Bio is installed; emit digests as JSON.

Runs inside each side's venv with `python -I`. Must work on both libraries, so it
uses only the public API shared by Biopython 1.88 and BioPAIthon 1.88.
"""

import gzip
import hashlib
import json
import sys
import traceback
import warnings
from pathlib import Path


def h(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, default=str).encode()).hexdigest()[:16]


def opener(path):
    return gzip.open(path, "rt") if path.suffix == ".gz" else open(path)


def structure_digest(s):
    atoms = []
    disordered = 0
    for model in s:
        for chain in model:
            for res in chain:
                if res.is_disordered():
                    disordered += 1
                for atom in res.get_unpacked_list():
                    atoms.append((model.id, chain.id, res.id, atom.get_id(), atom.get_altloc(),
                                  [round(float(x), 3) for x in atom.coord],
                                  round(float(atom.get_occupancy() or 0), 3),
                                  round(float(atom.get_bfactor() or 0), 3),
                                  atom.element, atom.get_serial_number()))
    chains = sorted({(m.id, c.id, len(c)) for m in s for c in m})
    return {"models": len(s), "chains": chains, "atoms": len(atoms), "disordered_residues": disordered,
            "atoms_hash": h(atoms), "header": h(s.header)}


def mmcif(path):
    from Bio.PDB.MMCIF2Dict import MMCIF2Dict
    from Bio.PDB.MMCIFParser import MMCIFParser
    with opener(path) as fh:
        d = MMCIF2Dict(fh)
    out = {"mmcif2dict": {"keys": len(d), "hash": h({k: v for k, v in d.items()})}}
    with opener(path) as fh:
        out["mmcifparser"] = structure_digest(MMCIFParser(QUIET=True).get_structure(path.stem, fh))
    return out


def bcif(path):
    from Bio.PDB.binary_cif import BinaryCIFParser
    return {"bcifparser": structure_digest(BinaryCIFParser().get_structure(path.stem, str(path)))}


def pdb(path):
    from Bio.PDB.PDBParser import PDBParser
    with opener(path) as fh:
        return {"pdbparser": structure_digest(PDBParser(QUIET=True).get_structure(path.stem, fh))}


def stockholm(path):
    from Bio import Align, AlignIO
    out = {}
    with opener(path) as fh:
        alns = list(Align.parse(fh, "stockholm"))
    out["align"] = {"n": len(alns), "hash": h([
        (a.shape, [r.id for r in a.sequences], [str(r.seq) for r in a.sequences],
         a.annotations, a.column_annotations, [r.letter_annotations for r in a.sequences],
         [r.dbxrefs for r in a.sequences]) for a in alns])}
    with opener(path) as fh:
        alns = list(AlignIO.parse(fh, "stockholm"))
    out["alignio"] = {"n": len(alns), "hash": h([
        (a.get_alignment_length(), [r.id for r in a], [str(r.seq) for r in a],
         a.annotations, a.column_annotations, [r.letter_annotations for r in a]) for a in alns])}
    return out


def genbank(path):
    from Bio import SeqIO
    with opener(path) as fh:
        recs = list(SeqIO.parse(fh, "genbank"))
    return {"seqio": {"n": len(recs), "hash": h([
        (r.id, r.name, r.description, len(r), str(r.seq), r.annotations, r.dbxrefs,
         [(f.type, str(f.location), f.qualifiers) for f in r.features]) for r in recs])}}


HANDLERS = {".cif": mmcif, ".bcif": bcif, ".pdb": pdb, ".ent": pdb, ".sto": stockholm, ".gb": genbank, ".gbk": genbank}


def main(corpus):
    results = {}
    for path in sorted(Path(corpus).rglob("*")):
        if not path.is_file():
            continue
        suffix = path.suffixes[-2] if path.suffix == ".gz" and len(path.suffixes) > 1 else path.suffix
        fn = HANDLERS.get(suffix)
        if fn is None:
            continue
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            try:
                r = fn(path)
            except Exception as e:  # noqa: BLE001 - every outcome is data here
                r = {"error": f"{type(e).__name__}: {e}", "trace": traceback.format_exc().splitlines()[-3:]}
        r["warnings"] = sorted({f"{x.category.__name__}: {x.message}" for x in w})
        results[str(path.relative_to(corpus))] = r
    json.dump(results, sys.stdout, indent=0, sort_keys=True, default=str)


if __name__ == "__main__":
    main(sys.argv[1])

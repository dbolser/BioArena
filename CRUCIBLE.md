# Crucible report

`biopython==1.88` (bio) vs `biopaithon @ git+https://github.com/dbolser/BioPAIthon@9039f486f033141c4772ef6f24cdf090d1c0d51b` (pai), run 2026-10-17.

files: 697, identical: 487, differing: 210
parse errors: bio 196, pai 0

## Fails on one side only

| fails on | files | error |
|---|---|---|
| bio | 196 | `IndexError: index -1 is out of bounds for axis 0 with size 0` |

## pfam/PF00332.sto.gz

- **align**
  - bio: `{"hash": "4f53cda18c2baa0c", "n": 0}`
  - pai: `{"hash": "f7124b415195764f", "n": 1}`

## pfam/PF00381.sto.gz

- **align**
  - bio: `{"hash": "4f53cda18c2baa0c", "n": 0}`
  - pai: `{"hash": "312b974d28bb9d59", "n": 1}`

## pfam/PF00391.sto.gz

- **align**
  - bio: `{"hash": "4f53cda18c2baa0c", "n": 0}`
  - pai: `{"hash": "0f163deb81a9d774", "n": 1}`

## pfam/PF00413.sto.gz

- **align**
  - bio: `{"hash": "4f53cda18c2baa0c", "n": 0}`
  - pai: `{"hash": "778217d3c7956a4f", "n": 1}`

## pfam/PF00425.sto.gz

- **align**
  - bio: `{"hash": "4f53cda18c2baa0c", "n": 0}`
  - pai: `{"hash": "134d8dad84f7cbe4", "n": 1}`

## pfam/PF00581.sto.gz

- **align**
  - bio: `{"hash": "4f53cda18c2baa0c", "n": 0}`
  - pai: `{"hash": "955b11dac5b8ecc3", "n": 1}`

## pfam/PF00644.sto.gz

- **align**
  - bio: `{"hash": "4f53cda18c2baa0c", "n": 0}`
  - pai: `{"hash": "9651a170e87bf532", "n": 1}`

## pfam/PF00680.sto.gz

- **align**
  - bio: `{"hash": "4f53cda18c2baa0c", "n": 0}`
  - pai: `{"hash": "c1ff12ad7e907966", "n": 1}`

## pfam/PF00728.sto.gz

- **align**
  - bio: `{"hash": "4f53cda18c2baa0c", "n": 0}`
  - pai: `{"hash": "526a3182904821e3", "n": 1}`

## pfam/PF00730.sto.gz

- **align**
  - bio: `{"hash": "4f53cda18c2baa0c", "n": 0}`
  - pai: `{"hash": "b241ff1f6043cf4d", "n": 1}`

## pfam/PF00795.sto.gz

- **align**
  - bio: `{"hash": "4f53cda18c2baa0c", "n": 0}`
  - pai: `{"hash": "b0807606a8422420", "n": 1}`

## pfam/PF00925.sto.gz

- **align**
  - bio: `{"hash": "4f53cda18c2baa0c", "n": 0}`
  - pai: `{"hash": "85054562e200a805", "n": 1}`

## rcsb/4AX9.bcif

- **bcifparser**
  - bio: `{"atoms": 2636, "atoms_hash": "04a1b297e6a5a19c", "chains": [[0, "A", 251], [0, "B", 11], [0, "C", 27], [0, "D", 1], [0, "E", 1], [0, "F", 1], [0, "G", 1], [0, "H", 195], [0, "I", 4], [0, "J", 18]], "disordered_residues": 510, "header": "44136fa355b3678a", "models": 1}`
  - pai: `{"atoms": 2644, "atoms_hash": "4138e075a2b458af", "chains": [[0, "A", 251], [0, "B", 11], [0, "C", 28], [0, "D", 1], [0, "E", 1], [0, "F", 1], [0, "G", 1], [0, "H", 195], [0, "I", 4], [0, "J", 18]], "disordered_residues": 4, "header": "44136fa355b3678a", "models": 1}`
- **warnings**
  - bio: `["PDBConstructionWarning: WARNING: Residue (' ', 14, 'K') redefined at line 0."]`
  - pai: `[]`

## rcsb/5HI3.bcif

- **bcifparser**
  - bio: `{"atoms": 8327, "atoms_hash": "716f7aaf63afb6ef", "chains": [[0, "A", 100], [0, "B", 88], [0, "C", 219], [0, "D", 213], [0, "E", 219], [0, "F", 14], [0, "G", 213], [0, "H", 1], [0, "I", 3], [0, "J", 7], [0, "K", 31], [0, "L", 22], [0, "M", 40], [0, "N", 38]], "disordered_residues": 1208, "header": "44136fa355b3678a", "models": 1}`
  - pai: `{"atoms": 8343, "atoms_hash": "59954fac5eface45", "chains": [[0, "A", 100], [0, "B", 88], [0, "C", 220], [0, "D", 213], [0, "E", 220], [0, "F", 14], [0, "G", 213], [0, "H", 1], [0, "I", 3], [0, "J", 7], [0, "K", 31], [0, "L", 22], [0, "M", 40], [0, "N", 38]], "disordered_residues": 3, "header": "44136fa355b3678a", "models": 1}`
- **warnings**
  - bio: `["PDBConstructionWarning: WARNING: Residue (' ', 82, 'C') redefined at line 0."]`
  - pai: `[]`

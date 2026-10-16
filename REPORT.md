# Arena report

| target | status | tests | pass bio | pass pai | regress | improve | only bio | only pai | other |
|---|---|---|---|---|---|---|---|---|---|
| antismash | ok | 214 | 102 | 102 | 0 | 0 | 0 | 0 | 0 |
| augur | ok | 1432 | 1416 | 1366 | 50 | 0 | 0 | 0 | 0 |
| bakta | ok | 298 | 278 | 278 | 0 | 0 | 0 | 0 | 0 |
| bcbio-gff | ok | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| cai | ok | 16 | 16 | 16 | 0 | 0 | 0 | 0 | 0 |
| crazydoc | ok | 4 | 3 | 3 | 0 | 0 | 0 | 0 | 0 |
| crispresso2 | ok | 708 | 696 | 696 | 0 | 0 | 0 | 0 | 0 |
| dnaapler | ok | 117 | 62 | 62 | 0 | 0 | 0 | 0 | 0 |
| dnacauldron | ok | 31 | 28 | 28 | 0 | 0 | 0 | 0 | 0 |
| dnachisel | ok | 149 | 144 | 144 | 0 | 0 | 0 | 0 | 0 |
| dnafeaturesviewer | ok | 20 | 17 | 17 | 0 | 0 | 0 | 0 | 0 |
| geneblocks | ok | 15 | 5 | 5 | 0 | 0 | 0 | 0 | 0 |
| graphein | ok | 74 | 54 | 54 | 0 | 0 | 0 | 0 | 0 |
| macsyfinder | ok | 85 | 45 | 45 | 0 | 0 | 0 | 0 | 0 |
| mdanalysis | ok | 58 | 52 | 52 | 0 | 0 | 0 | 0 | 0 |
| panaroo | ok | 9 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| primavera | ok | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| pyani | ok | 120 | 88 | 88 | 0 | 0 | 0 | 0 | 0 |
| pycirclize | ok | 85 | 85 | 85 | 0 | 0 | 0 | 0 | 0 |
| pydna | ok | 511 | 495 | 495 | 0 | 0 | 0 | 0 | 0 |
| pygenomeviz | ok | 100 | 72 | 72 | 0 | 0 | 0 | 0 | 0 |
| pyvolve | ok | 166 | 155 | 155 | 0 | 0 | 0 | 0 | 0 |
| seqmagick | ok | 154 | 147 | 147 | 0 | 0 | 0 | 0 | 0 |
| treetime | ok | 51 | 48 | 48 | 0 | 0 | 0 | 0 | 0 |

Side info (Bio.__version__ and the distribution that provides `Bio`):

- antismash bio: `1.88 ['biopython']`
- antismash pai: `1.88 ['biopaithon']`
- augur bio: `1.88 ['biopython']`
- augur pai: `1.88 ['biopaithon']`
- bakta bio: `1.88 ['biopython']`
- bakta pai: `1.88 ['biopaithon']`
- bcbio-gff bio: `1.88 ['biopython']`
- bcbio-gff pai: `1.88 ['biopaithon']`
- cai bio: `1.88 ['biopython']`
- cai pai: `1.88 ['biopaithon']`
- crazydoc bio: `1.88 ['biopython']`
- crazydoc pai: `1.88 ['biopaithon']`
- crispresso2 bio: `1.88 ['biopython']`
- crispresso2 pai: `1.88 ['biopaithon']`
- dnaapler bio: `1.88 ['biopython']`
- dnaapler pai: `1.88 ['biopaithon']`
- dnacauldron bio: `1.88 ['biopython']`
- dnacauldron pai: `1.88 ['biopaithon']`
- dnachisel bio: `1.88 ['biopython']`
- dnachisel pai: `1.88 ['biopaithon']`
- dnafeaturesviewer bio: `1.88 ['biopython']`
- dnafeaturesviewer pai: `1.88 ['biopaithon']`
- geneblocks bio: `1.88 ['biopython']`
- geneblocks pai: `1.88 ['biopaithon']`
- graphein bio: `1.88 ['biopython']`
- graphein pai: `1.88 ['biopaithon']`
- macsyfinder bio: `1.88 ['biopython']`
- macsyfinder pai: `1.88 ['biopaithon']`
- mdanalysis bio: `1.88 ['biopython']`
- mdanalysis pai: `1.88 ['biopaithon']`
- panaroo bio: `1.88 ['biopython']`
- panaroo pai: `1.88 ['biopaithon']`
- primavera bio: `1.88 ['biopython']`
- primavera pai: `1.88 ['biopaithon']`
- pyani bio: `1.88 ['biopython']`
- pyani pai: `1.88 ['biopaithon']`
- pycirclize bio: `1.88 ['biopython']`
- pycirclize pai: `1.88 ['biopaithon']`
- pydna bio: `1.88 ['biopython']`
- pydna pai: `1.88 ['biopaithon']`
- pygenomeviz bio: `1.88 ['biopython']`
- pygenomeviz pai: `1.88 ['biopaithon']`
- pyvolve bio: `1.88 ['biopython']`
- pyvolve pai: `1.88 ['biopaithon']`
- seqmagick bio: `1.88 ['biopython']`
- seqmagick pai: `1.88 ['biopaithon']`
- treetime bio: `1.88 ['biopython']`
- treetime pai: `1.88 ['biopaithon']`

## augur: regress

- `tests.io.test_sequences.TestFormat::test_fasta`
- `tests.io.test_sequences.TestFormat::test_genbank`
- `tests.io.test_sequences.TestReadSequences::test_read_sequences_format_misused`
- `tests.io.test_sequences.TestReadSequences::test_read_sequences_from_multiple_files`
- `tests.io.test_sequences.TestReadSequences::test_read_sequences_from_multiple_files_or_buffers`
- `tests.io.test_sequences.TestReadSequences::test_read_sequences_from_multiple_files_with_different_compression`
- `tests.io.test_sequences.TestReadSequences::test_read_sequences_from_single_bzip2_file`
- `tests.io.test_sequences.TestReadSequences::test_read_sequences_from_single_file`
- `tests.io.test_sequences.TestReadSequences::test_read_sequences_from_single_gzip_file`
- `tests.io.test_sequences.TestReadSequences::test_read_sequences_from_single_lzma_file`
- `tests.io.test_sequences.TestReadSequences::test_read_single_fasta_record`
- `tests.io.test_sequences.TestReadSequences::test_read_single_genbank_record`
- `tests.io.test_sequences.TestReadSequences::test_read_single_genbank_record_from_a_path`
- `tests.io.test_sequences.TestReadSingleSequence::test_read_multiple_sequence_error`
- `tests.io.test_sequences.TestReadSingleSequence::test_read_no_sequence_error`
- `tests.io.test_sequences.TestReadSingleSequence::test_read_single_sequence`
- `tests.proximity.test_hamming.TestHammingSimple::test_run_excludes_focal_from_context`
- `tests.proximity.test_hamming.TestHammingSimple::test_run_finds_correct_neighbours`
- `tests.proximity.test_hamming.TestHammingSimple::test_run_k_limits_output`
- `tests.proximity.test_hamming.TestHammingSimple::test_run_max_distance_arg`
- `tests.proximity.test_hamming.TestHammingWithMisingData::test_count_all_ns`
- `tests.proximity.test_hamming.TestHammingWithMisingData::test_ignore_all_ns`
- `tests.proximity.test_hamming.TestHammingWithMisingData::test_ignore_flanking_ns`
- `tests.test_align.TestAlign::test_prepare_no_alignment_multiple_test_seqs`
- `tests.test_align.TestAlign::test_prepare_no_alignment_or_ref`
- `tests.test_align.TestAlign::test_prepare_no_alignment_with_named_ref_missing`
- `tests.test_align.TestAlign::test_prepare_no_alignment_with_ref_file`
- `tests.test_align.TestAlign::test_prepare_no_alignment_with_ref_name`
- `tests.test_align.TestAlign::test_prepare_with_alignment_ref_sequence_wrong_length`
- `tests.test_align.TestAlign::test_prepare_with_alignment_with_duplicate_sequences`
- `tests.test_align.TestAlign::test_prepare_with_alignment_with_named_ref_missing`
- `tests.test_align.TestAlign::test_prepare_with_alignment_with_ref_name`
- `tests.test_align.TestAlign::test_prepare_with_alignment_with_ref_seq`
- `tests.test_align.TestAlign::test_read_sequences`
- `tests.test_align.TestAlign::test_run_remove_reference[True]`
- `tests.test_align.TestAlign::test_run_with_reference_sequence_remove_reference`
- `tests.test_mask.TestMask::test_e2e_fasta_beginning_end_sites`
- `tests.test_mask.TestMask::test_e2e_fasta_mask_file`
- `tests.test_mask.TestMask::test_e2e_fasta_mask_invalid`
- `tests.test_mask.TestMask::test_e2e_fasta_minimal`
- `tests.test_mask.TestMask::test_mask_fasta_from_beginning`
- `tests.test_mask.TestMask::test_mask_fasta_from_beginning_and_end`
- `tests.test_mask.TestMask::test_mask_fasta_from_beginning_and_end_too_long[0-1000]`
- `tests.test_mask.TestMask::test_mask_fasta_from_beginning_and_end_too_long[1000-0]`
- `tests.test_mask.TestMask::test_mask_fasta_from_beginning_and_end_too_long[1000-1000]`
- `tests.test_mask.TestMask::test_mask_fasta_from_end`
- `tests.test_mask.TestMask::test_mask_fasta_invalid_sites[False]`
- `tests.test_mask.TestMask::test_mask_fasta_invalid_sites[True]`
- `tests.test_mask.TestMask::test_mask_fasta_normal_case`
- `tests.test_mask.TestMask::test_mask_fasta_out_of_index`

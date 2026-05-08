#!/usr/bin/env python3
from transcription import Transcriber
from translation import Translator
from protein_lookup import ProteinLookup

# DNA coding strand for insulin protein entry P01308
sequence = 'ATGGTTCTTTCTCCTGCTGATAAAACTAATGTTATCCGTGCTGCTCAAAACTGTTATTCTACTGAAATCAAC'
print('DNA input:')
print(sequence)

transcriber = Transcriber()
mrna = transcriber.transcribe(sequence, sequence_type='DNA', strand_type='coding')
print('\nmRNA output:')
print(mrna)

translator = Translator()
codons, codon_amino_acids, amino_acids, protein_sequence = translator.translate(mrna)
print('\nCodons:')
print(codons)
print('\nProtein sequence:')
print(protein_sequence)
print('\nAmino acids:')
print([a[1] for a in amino_acids])

lookup = ProteinLookup()
matches = lookup.search_database(protein_sequence)
print('\nDatabase matches:')
print(matches)

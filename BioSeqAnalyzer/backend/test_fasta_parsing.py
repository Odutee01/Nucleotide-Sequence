#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(__file__))

from sequence_analyzer import SequenceAnalyzer

# Test FASTA content
fasta_content = """>test_sequence Human insulin gene
ATGGCCCTGTGGATGCGCCTCCTGCCCCTGCTGGCGCTGCTGGCCCTCTGGGGACCTGACCCAGCCGCAGCCTTTGTGAACCAACACCTGTGCGGCTCACACCTGGTGGAAGCTCTCTACCTAGTGTGCGGGGAACGAGGCTTCTTCTACACACCCAAGACCCGCCGGGAGGCAGAGGACCTGCAGGTGGGGCAGGTGGAGCTGGGCGGGGGCCCTGGTGCAGGCAGCCTGCAGCCCTTGGCCCTGGAGGGGTCCCTGCAGAAGCGTGGCATTGTGGAACAATGCTGTACCAGCATCTGCTCCCTCTACCAGCTGGAGAACTACTGCAACTAAG"""

print("Testing FASTA sequence parsing...")
print("Original FASTA content:")
print(fasta_content)
print()

analyzer = SequenceAnalyzer()
result = analyzer.detect_sequence_type(fasta_content)

print("Detection result:")
print(f"Sequence type: {result['sequence_type']}")
print(f"Detected chars: {result['detected_chars']}")
print(f"Valid: {result['valid']}")

# Test the extracted sequence
extracted = analyzer._extract_fasta_sequence(fasta_content)
print(f"\nExtracted sequence length: {len(extracted)}")
print(f"Extracted sequence (first 50 chars): {extracted[:50]}...")

# Test if it's valid DNA
print(f"\nIs extracted sequence valid DNA? {all(c in 'ATGC' for c in extracted.upper())}")
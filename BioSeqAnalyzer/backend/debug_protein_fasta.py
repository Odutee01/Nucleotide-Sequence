#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(__file__))

from sequence_analyzer import SequenceAnalyzer

# Test the protein FASTA sequence
fasta_content = """>sp|P01308|INS_HUMAN Insulin OS=Homo sapiens OX=9606 GN=INS PE=1 SV=1
MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKTRREAED
LQVGQVELGGGPGAGSLQPLALEGSLQKRGIVEQCCTSICSLYQLENYCN"""

print("Testing protein FASTA sequence...")
print("FASTA content:")
print(fasta_content)
print()

analyzer = SequenceAnalyzer()

# Test FASTA extraction
extracted = analyzer._extract_fasta_sequence(fasta_content)
print("Extracted sequence:")
print(extracted)
print(f"Length: {len(extracted)}")
print()

# Test sequence detection
result = analyzer.detect_sequence_type(fasta_content)
print("Detection result:")
print(f"Sequence type: {result['sequence_type']}")
print(f"Detected chars: {result['detected_chars']}")
if 'invalid_chars' in result:
    print(f"Invalid chars: {result['invalid_chars']}")
if 'error' in result:
    print(f"Error: {result['error']}")
print()

# Check unique characters in extracted sequence
unique_chars = set(extracted.upper())
print(f"Unique characters in extracted sequence: {sorted(unique_chars)}")
print(f"DNA bases: {analyzer.DNA_BASES}")
print(f"RNA bases: {analyzer.RNA_BASES}")
print(f"Invalid chars: {unique_chars - analyzer.DNA_BASES - analyzer.RNA_BASES}")
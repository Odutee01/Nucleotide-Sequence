"""
Sequence Detection Module
Detects whether a sequence is DNA, RNA, or invalid
"""

class SequenceAnalyzer:
    """Analyzes nucleotide sequences"""
    
    # Valid nucleotide bases
    DNA_BASES = set('ATGC')
    RNA_BASES = set('AUGC')
    
    def detect_sequence_type(self, sequence):
        """
        Detect if sequence is DNA, RNA, or invalid
        
        Args:
            sequence (str): The nucleotide sequence to analyze
            
        Returns:
            dict: Detection result with sequence_type and detected_chars
        """
        print(f"DEBUG: detect_sequence_type called with sequence length {len(sequence)}")
        sequence = sequence.strip()
        print(f"DEBUG: sequence starts with >: {sequence.startswith('>')}")
        
        # Check if it's a FASTA file
        if sequence.startswith('>'):
            cleaned = self._extract_fasta_sequence(sequence)
        else:
            cleaned = self._clean_sequence(sequence.upper())
        
        print(f"DEBUG: cleaned length {len(cleaned)}")
        
        if not cleaned:
            return {
                'sequence_type': 'INVALID',
                'detected_chars': [],
                'invalid_chars': list(set(sequence)),
                'error': 'Sequence contains no valid nucleotide bases'
            }
        
        # Convert to set of unique characters
        unique_chars = set(cleaned)
        print(f"DEBUG: unique_chars: {unique_chars}")
        
        # Check for invalid characters
        invalid_chars = unique_chars - self.DNA_BASES - self.RNA_BASES
        print(f"DEBUG: invalid_chars: {invalid_chars}")
        
        if invalid_chars:
            print("DEBUG: returning INVALID due to invalid chars")
            return {
                'sequence_type': 'INVALID',
                'detected_chars': sorted(list(unique_chars)),
                'invalid_chars': sorted(list(invalid_chars)),
                'error': f'Invalid characters found: {", ".join(sorted(invalid_chars))}'
            }
        
        # Check if it's DNA, RNA, or could be both
        has_thymine = 'T' in unique_chars
        has_uracil = 'U' in unique_chars
        print(f"DEBUG: has_thymine: {has_thymine}, has_uracil: {has_uracil}")
        
        if has_thymine and not has_uracil:
            seq_type = 'DNA'
        elif has_uracil and not has_thymine:
            seq_type = 'RNA'
        elif has_uracil and has_thymine:
            # Contains both T and U - technically invalid for natural sequences
            # but we'll classify as INVALID
            return {
                'sequence_type': 'INVALID',
                'detected_chars': sorted(list(unique_chars)),
                'invalid_chars': ['Sequence contains both T and U'],
                'error': 'Natural sequences cannot contain both Thymine and Uracil'
            }
        else:
            # Only has A, G, C (ambiguous)
            # Check sequence length and frequency patterns
            seq_type = 'DNA'  # Default to DNA if ambiguous
        
        result = {
            'sequence_type': seq_type,
            'detected_chars': sorted(list(unique_chars)),
            'invalid_chars': [],
            'sequence_length': len(cleaned)
        }
        print(f"DEBUG: result: {result}")
        return result
    
    def _extract_fasta_sequence(self, fasta_content):
        """
        Extract sequence data from FASTA format
        
        Args:
            fasta_content (str): The FASTA file content
            
        Returns:
            str: The extracted sequence
        """
        lines = fasta_content.split('\n')
        sequence_lines = []
        
        for line in lines:
            line = line.strip()
            if not line.startswith('>') and line:  # Skip headers and empty lines
                sequence_lines.append(line)
        
        # Join all sequence lines and clean
        sequence = ''.join(sequence_lines)
        return self._clean_sequence(sequence.upper())
    
    def _clean_sequence(self, sequence):
        """Remove whitespace and non-letter characters"""
        cleaned = ''
        for char in sequence.upper():
            if char.isalpha():
                cleaned += char
            # Ignore numbers, spaces, dashes, etc.
        return cleaned
    
    def _clean_sequence(self, sequence):
        """Remove whitespace and non-letter characters"""
        cleaned = ''
        for char in sequence.upper():
            if char.isalpha():
                cleaned += char
            # Ignore numbers, spaces, dashes, etc.
        return cleaned

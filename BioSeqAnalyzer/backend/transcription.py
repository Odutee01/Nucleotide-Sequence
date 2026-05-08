"""
Transcription Module
Converts DNA to mRNA or RNA to mRNA
"""

class Transcriber:
    """Handles transcription of DNA to mRNA"""
    
    # Complement base pairs for DNA
    DNA_COMPLEMENT = {
        'A': 'T',
        'T': 'A',
        'G': 'C',
        'C': 'G'
    }
    
    # DNA to RNA conversion (replaces T with U)
    DNA_TO_RNA = {
        'A': 'A',
        'T': 'U',
        'G': 'G',
        'C': 'C'
    }
    
    def transcribe(self, sequence, sequence_type='DNA', strand_type='coding'):
        """
        Transcribe a sequence to mRNA
        
        For DNA:
            - If coding strand: transcribe directly by replacing T with U
            - If template strand: reverse-complement the strand to get the coding sequence, then transcribe
        For RNA:
            - Return as-is (already mRNA)
        
        Args:
            sequence (str): The input sequence
            sequence_type (str): 'DNA' or 'RNA'
            strand_type (str): 'coding' or 'template' (only relevant for DNA)
            
        Returns:
            str: The mRNA sequence
        """
        sequence = sequence.upper().strip()
        
        if sequence_type == 'RNA':
            return sequence
        
        elif sequence_type == 'DNA':
            if strand_type == 'coding':
                return self._transcribe_coding(sequence)
            else:  # template
                coding_sequence = self._reverse_complement(sequence)
                return self._transcribe_coding(coding_sequence)
        
        else:
            raise ValueError(f"Unknown sequence type: {sequence_type}")
    
    def _transcribe_coding(self, coding_dna):
        """
        Transcribe a DNA coding strand directly to mRNA by replacing T with U.
        """
        mRNA = ''
        for base in coding_dna:
            if base == 'A':
                mRNA += 'A'
            elif base == 'T':
                mRNA += 'U'
            elif base == 'G':
                mRNA += 'G'
            elif base == 'C':
                mRNA += 'C'
            else:
                mRNA += 'N'
        return mRNA
    
    def _reverse_complement(self, dna_sequence):
        """
        Get the reverse complement of a DNA sequence
        (convert coding strand to template strand)
        
        Args:
            dna_sequence (str): The DNA sequence
            
        Returns:
            str: The reverse complement
        """
        complement = ''
        for base in dna_sequence:
            complement += self.DNA_COMPLEMENT.get(base, 'N')
        
        # Return the reverse
        return complement[::-1]
    
    def _transcribe_template(self, template_dna):
        """
        Transcribe template DNA strand to mRNA
        - DNA base pairs with RNA: A->U, T->A, G->C, C->G
        - Result is read in 5' to 3' direction
        
        Args:
            template_dna (str): The template DNA strand
            
        Returns:
            str: The mRNA sequence
        """
        mRNA = ''
        for base in template_dna:
            if base == 'A':
                mRNA += 'U'
            elif base == 'T':
                mRNA += 'A'
            elif base == 'G':
                mRNA += 'C'
            elif base == 'C':
                mRNA += 'G'
            else:
                mRNA += 'N'  # Unknown base
        
        return mRNA

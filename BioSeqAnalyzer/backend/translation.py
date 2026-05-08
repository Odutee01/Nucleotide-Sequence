"""
Translation Module
Converts mRNA codons to amino acids
"""

class Translator:
    """Handles translation of mRNA to amino acids"""
    
    # Codon table: maps codons to (amino_acid_name, abbreviation)
    CODON_TABLE = {
        # Start codon
        'AUG': ('Methionine', 'Met'),
        
        # Alanine
        'GCU': ('Alanine', 'Ala'),
        'GCC': ('Alanine', 'Ala'),
        'GCA': ('Alanine', 'Ala'),
        'GCG': ('Alanine', 'Ala'),
        
        # Arginine
        'CGU': ('Arginine', 'Arg'),
        'CGC': ('Arginine', 'Arg'),
        'CGA': ('Arginine', 'Arg'),
        'CGG': ('Arginine', 'Arg'),
        'AGA': ('Arginine', 'Arg'),
        'AGG': ('Arginine', 'Arg'),
        
        # Asparagine
        'AAU': ('Asparagine', 'Asn'),
        'AAC': ('Asparagine', 'Asn'),
        
        # Aspartic Acid
        'GAU': ('Aspartic Acid', 'Asp'),
        'GAC': ('Aspartic Acid', 'Asp'),
        
        # Cysteine
        'UGU': ('Cysteine', 'Cys'),
        'UGC': ('Cysteine', 'Cys'),
        
        # Glutamic Acid
        'GAA': ('Glutamic Acid', 'Glu'),
        'GAG': ('Glutamic Acid', 'Glu'),
        
        # Glutamine
        'CAA': ('Glutamine', 'Gln'),
        'CAG': ('Glutamine', 'Gln'),
        
        # Glycine
        'GGU': ('Glycine', 'Gly'),
        'GGC': ('Glycine', 'Gly'),
        'GGA': ('Glycine', 'Gly'),
        'GGG': ('Glycine', 'Gly'),
        
        # Histidine
        'CAU': ('Histidine', 'His'),
        'CAC': ('Histidine', 'His'),
        
        # Isoleucine
        'AUU': ('Isoleucine', 'Ile'),
        'AUC': ('Isoleucine', 'Ile'),
        'AUA': ('Isoleucine', 'Ile'),
        
        # Leucine
        'UUA': ('Leucine', 'Leu'),
        'UUG': ('Leucine', 'Leu'),
        'CUU': ('Leucine', 'Leu'),
        'CUC': ('Leucine', 'Leu'),
        'CUA': ('Leucine', 'Leu'),
        'CUG': ('Leucine', 'Leu'),
        
        # Lysine
        'AAA': ('Lysine', 'Lys'),
        'AAG': ('Lysine', 'Lys'),
        
        # Phenylalanine
        'UUU': ('Phenylalanine', 'Phe'),
        'UUC': ('Phenylalanine', 'Phe'),
        
        # Proline
        'CCU': ('Proline', 'Pro'),
        'CCC': ('Proline', 'Pro'),
        'CCA': ('Proline', 'Pro'),
        'CCG': ('Proline', 'Pro'),
        
        # Serine
        'UCU': ('Serine', 'Ser'),
        'UCC': ('Serine', 'Ser'),
        'UCA': ('Serine', 'Ser'),
        'UCG': ('Serine', 'Ser'),
        'AGU': ('Serine', 'Ser'),
        'AGC': ('Serine', 'Ser'),
        
        # Threonine
        'ACU': ('Threonine', 'Thr'),
        'ACC': ('Threonine', 'Thr'),
        'ACA': ('Threonine', 'Thr'),
        'ACG': ('Threonine', 'Thr'),
        
        # Tryptophan
        'UGG': ('Tryptophan', 'Trp'),
        
        # Tyrosine
        'UAU': ('Tyrosine', 'Tyr'),
        'UAC': ('Tyrosine', 'Tyr'),
        
        # Valine
        'GUU': ('Valine', 'Val'),
        'GUC': ('Valine', 'Val'),
        'GUA': ('Valine', 'Val'),
        'GUG': ('Valine', 'Val'),
        
        # Stop codons
        'UAA': ('STOP', '*'),
        'UAG': ('STOP', '*'),
        'UGA': ('STOP', '*'),
    }
    
    # Single-letter codes for amino acids
    AMINO_ACID_ONELETTER = {
        'Ala': 'A', 'Arg': 'R', 'Asn': 'N', 'Asp': 'D',
        'Cys': 'C', 'Glu': 'E', 'Gln': 'Q', 'Gly': 'G',
        'His': 'H', 'Ile': 'I', 'Leu': 'L', 'Lys': 'K',
        'Met': 'M', 'Phe': 'F', 'Pro': 'P', 'Ser': 'S',
        'Thr': 'T', 'Trp': 'W', 'Tyr': 'Y', 'Val': 'V',
        'Xaa': 'X', '*': '*'
    }

    def translate(self, mRNA):
        """
        Translate mRNA sequence to amino acids and provide codon mappings.
        
        Args:
            mRNA (str): The mRNA sequence
            
        Returns:
            tuple: (codons, codon_amino_acids, amino_acids, protein_sequence)
                - codons: list of codon strings
                - codon_amino_acids: list of (name, abbreviation) tuples for each codon
                - amino_acids: list of (name, abbreviation) tuples for the translated protein chain
                - protein_sequence: single-letter protein sequence for the translated protein
        """
        mRNA = mRNA.upper().strip()
        
        # Split into codons (groups of 3)
        codons = [
            mRNA[i:i+3]
            for i in range(0, len(mRNA), 3)
            if len(mRNA[i:i+3]) == 3
        ]
        
        # Map each codon to an amino acid for display
        codon_amino_acids = []
        for codon in codons:
            if 'N' in codon:
                amino_acid = ('Unknown', 'Xaa')
            else:
                amino_acid = self.CODON_TABLE.get(codon, ('Unknown', 'Xaa'))
            codon_amino_acids.append(amino_acid)
        
        # Build the actual translated protein sequence starting at AUG
        amino_acids = []
        protein_sequence = ''
        started = False
        
        for codon, amino_acid in zip(codons, codon_amino_acids):
            if codon == 'AUG' and not started:
                started = True
                amino_acids.append(amino_acid)
                protein_sequence += self.AMINO_ACID_ONELETTER.get(amino_acid[1], 'X')
                continue
            
            if started:
                if amino_acid[0] == 'STOP':
                    break
                amino_acids.append(amino_acid)
                protein_sequence += self.AMINO_ACID_ONELETTER.get(amino_acid[1], 'X')
        
        return codons, codon_amino_acids, amino_acids, protein_sequence
    
    def get_codon_table(self):
        """Return the full codon table"""
        return self.CODON_TABLE

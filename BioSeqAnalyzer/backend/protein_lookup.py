"""
Protein Lookup Module
Characterizes proteins and searches external databases
"""

import math
from collections import Counter

class ProteinLookup:
    """Handles protein characterization and database searches"""
    
    # Amino acid properties for characterization
    AMINO_ACID_MASS = {
        'A': 89.09, 'R': 174.20, 'N': 132.12, 'D': 133.10,
        'C': 121.16, 'E': 147.13, 'Q': 146.15, 'G': 75.07,
        'H': 155.16, 'I': 131.18, 'L': 131.18, 'K': 146.19,
        'M': 149.21, 'F': 165.19, 'P': 115.13, 'S': 105.09,
        'T': 119.12, 'W': 204.23, 'Y': 181.19, 'V': 117.15,
        '*': 0  # Stop codon
    }
    
    # Aromatic amino acids
    AROMATIC_ACIDS = {'F', 'Y', 'W'}
    
    # Hydropathy index (Kyte-Doolittle)
    HYDROPATHY = {
        'A': 1.8, 'R': -4.5, 'N': -3.5, 'D': -3.5,
        'C': 2.5, 'E': -3.5, 'Q': -3.5, 'G': -0.4,
        'H': -3.2, 'I': 4.5, 'L': 3.8, 'K': -3.9,
        'M': 1.9, 'F': 2.8, 'P': -1.6, 'S': -0.8,
        'T': -0.7, 'W': -0.9, 'Y': -1.3, 'V': 4.2,
        '*': 0
    }
    
    # Isoelectric point estimates
    PI_VALUES = {
        'A': 6.01, 'R': 10.76, 'N': 5.41, 'D': 2.77,
        'C': 5.07, 'E': 3.22, 'Q': 5.65, 'G': 5.97,
        'H': 7.59, 'I': 6.02, 'L': 5.98, 'K': 9.74,
        'M': 5.74, 'F': 5.48, 'P': 6.30, 'S': 5.68,
        'T': 5.60, 'W': 5.89, 'Y': 5.66, 'V': 5.96,
        '*': 7.0
    }
    
    def characterize_protein(self, protein_sequence):
        """
        Calculate physical properties of a protein
        
        Args:
            protein_sequence (str): Protein sequence in single-letter code
            
        Returns:
            dict: Protein characterization properties
        """
        protein_sequence = protein_sequence.upper().replace(' ', '')
        
        if not protein_sequence:
            return {}
        
        # Calculate properties
        molecular_weight = self._calculate_molecular_weight(protein_sequence)
        isoelectric_point = self._estimate_isoelectric_point(protein_sequence)
        aromaticity = self._calculate_aromaticity(protein_sequence)
        gravy = self._calculate_gravy(protein_sequence)
        
        return {
            'length': len(protein_sequence),
            'molecular_weight': molecular_weight,
            'isoelectric_point': isoelectric_point,
            'aromaticity': aromaticity,
            'gravy': gravy,
            'composition': self._get_amino_acid_composition(protein_sequence)
        }
    
    def _calculate_molecular_weight(self, sequence):
        """Calculate approximate molecular weight in Daltons"""
        weight = 0
        for amino_acid in sequence:
            weight += self.AMINO_ACID_MASS.get(amino_acid, 0)
        
        # Subtract water for peptide bonds (18.015 Da per bond)
        peptide_bonds = len(sequence) - 1
        weight -= peptide_bonds * 18.015
        
        return weight
    
    def _estimate_isoelectric_point(self, sequence):
        """
        Estimate isoelectric point (simplified)
        Uses average pI of individual amino acids
        """
        if not sequence:
            return 7.0
        
        total_pi = sum(self.PI_VALUES.get(aa, 7.0) for aa in sequence)
        return total_pi / len(sequence)
    
    def _calculate_aromaticity(self, sequence):
        """Calculate aromaticity (proportion of aromatic amino acids)"""
        if not sequence:
            return 0
        
        aromatic_count = sum(1 for aa in sequence if aa in self.AROMATIC_ACIDS)
        return aromatic_count / len(sequence)
    
    def _calculate_gravy(self, sequence):
        """
        Calculate GRAVY (Grand average of hydropathy)
        Indicates hydrophobicity of the protein
        """
        if not sequence:
            return 0
        
        total_hydropathy = sum(self.HYDROPATHY.get(aa, 0) for aa in sequence)
        return total_hydropathy / len(sequence)
    
    def _get_amino_acid_composition(self, sequence):
        """Get composition percentages of each amino acid"""
        counter = Counter(sequence)
        total = len(sequence)
        
        composition = {}
        for aa in sorted(counter.keys()):
            composition[aa] = (counter[aa] / total) * 100
        
        return composition
    
    def search_database(self, protein_sequence, limit=3):
        """
        Simulate database search for protein matches
        In a real implementation, this would query UniProt/BLAST
        
        Args:
            protein_sequence (str): Protein sequence
            limit (int): Maximum number of matches to return
            
        Returns:
            list: List of database matches
        """
        # This is a simplified mock implementation
        # In production, you would use BLAST API or UniProt REST API
        
        # Example known proteins database
        known_proteins = [
            {
                'sequence': 'MKTAYIAKQRQISFVKSHFSRQLEERLGLIEVQAPILSRVGDGTQDNLSGAEKAVQ',
                'protein_name': 'Hemoglobin subunit alpha',
                'organism': 'Homo sapiens',
                'function': 'Oxygen transport in blood',
                'database_id': 'P69905',
                'url': 'https://www.uniprot.org/uniprotkb/P69905'
            },
            {
                'sequence': 'MVLSPADKTNVIRAAQNCYSTEIN',
                'protein_name': 'Insulin',
                'organism': 'Homo sapiens',
                'function': 'Glucose metabolism regulation',
                'database_id': 'P01308',
                'url': 'https://www.uniprot.org/uniprotkb/P01308'
            },
            {
                'sequence': 'MKTIIALSYIFCLVNADYKDDDDK',
                'protein_name': 'Ubiquitin',
                'organism': 'Homo sapiens',
                'function': 'Protein tagging and degradation',
                'database_id': 'P62988',
                'url': 'https://www.uniprot.org/uniprotkb/P62988'
            }
        ]
        
        matches = []
        protein_sequence = protein_sequence.upper().replace(' ', '')
        
        for known in known_proteins:
            known_seq = known['sequence'].upper()
            similarity = self._calculate_sequence_similarity(
                protein_sequence, known_seq
            )
            
            if similarity > 0.3:  # At least 30% similarity
                matches.append({
                    'protein_name': known['protein_name'],
                    'organism': known['organism'],
                    'function': known['function'],
                    'database_id': known['database_id'],
                    'url': known['url'],
                    'similarity': similarity
                })
        
        # Sort by similarity and limit results
        matches.sort(key=lambda x: x['similarity'], reverse=True)
        return matches[:limit]
    
    def _calculate_sequence_similarity(self, seq1, seq2):
        """
        Calculate sequence similarity using a simple match percentage
        """
        if not seq1 or not seq2:
            return 0
        
        min_len = min(len(seq1), len(seq2))
        max_len = max(len(seq1), len(seq2))
        
        # Count matching positions
        matches = sum(1 for i in range(min_len) if seq1[i] == seq2[i])
        
        # Similarity considering length difference
        similarity = matches / max_len
        return similarity

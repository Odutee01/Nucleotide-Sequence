"""
BioSeqAnalyzer - Backend Flask Application
DNA & RNA Sequence Analysis Pipeline
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
from sequence_analyzer import SequenceAnalyzer
from transcription import Transcriber
from translation import Translator
from protein_lookup import ProteinLookup

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)  # Enable CORS for frontend

@app.route('/')
def index():
    """Serve the frontend index.html"""
    return send_from_directory(app.static_folder, 'index.html')

# Initialize analysis modules
analyzer = SequenceAnalyzer()
transcriber = Transcriber()
translator = Translator()
protein_lookup = ProteinLookup()


@app.route('/api/analyze', methods=['POST'])
def analyze_sequence():
    """Endpoint: Analyze sequence type (DNA/RNA/Invalid)"""
    try:
        data = request.json
        sequence = data.get('sequence', '').upper().strip()
        
        if not sequence:
            return jsonify({'error': 'Empty sequence provided'}), 400
        
        result = analyzer.detect_sequence_type(sequence)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/transcribe', methods=['POST'])
def transcribe():
    """Endpoint: Perform transcription (DNA -> mRNA or RNA -> mRNA)"""
    try:
        data = request.json
        sequence = data.get('sequence', '').strip()
        sequence_type = data.get('sequence_type', 'DNA')
        strand_type = data.get('strand_type', 'coding')
        
        if not sequence:
            return jsonify({'error': 'Empty sequence provided'}), 400
        
        # Extract sequence from FASTA if needed
        if sequence.startswith('>'):
            analyzer = SequenceAnalyzer()
            sequence = analyzer._extract_fasta_sequence(sequence)
        
        mRNA = transcriber.transcribe(sequence, sequence_type, strand_type)
        
        return jsonify({
            'mRNA': mRNA,
            'original_sequence': sequence,
            'sequence_type': sequence_type,
            'strand_type': strand_type if sequence_type == 'DNA' else None
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/translate', methods=['POST'])
def translate():
    """Endpoint: Perform translation (mRNA -> Amino Acids)"""
    try:
        data = request.json
        mRNA = data.get('mRNA', '').upper().strip()
        
        if not mRNA:
            return jsonify({'error': 'Empty mRNA sequence provided'}), 400
        
        codons, codon_amino_acids, amino_acids, protein_seq = translator.translate(mRNA)
        
        return jsonify({
            'codons': codons,
            'codon_amino_acids': [
                {'name': aa[0], 'abbreviation': aa[1]}
                for aa in codon_amino_acids
            ],
            'amino_acids': [
                {'name': aa[0], 'abbreviation': aa[1]} 
                for aa in amino_acids
            ],
            'protein_sequence': protein_seq
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/protein-lookup', methods=['POST'])
def lookup_protein():
    """Endpoint: Protein characterization and database lookup"""
    try:
        data = request.json
        protein_sequence = data.get('protein_sequence', '').strip()
        original_sequence = data.get('original_sequence', '').strip()
        
        if not protein_sequence:
            return jsonify({'error': 'Empty protein sequence provided'}), 400
        
        # Get protein characterization
        characterization = protein_lookup.characterize_protein(protein_sequence)
        
        # Search database for matches
        matches = protein_lookup.search_database(protein_sequence)
        
        return jsonify({
            'characterization': characterization,
            'database_matches': matches
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'BioSeqAnalyzer API'})


if __name__ == '__main__':
    print("BioSeqAnalyzer Backend Starting...")
    port = int(os.environ.get("PORT", 5000))
    print(f"Flask API running on http://localhost:{port}")
    app.run(debug=True, host='0.0.0.0', port=port)

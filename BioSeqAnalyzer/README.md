# BioSeqAnalyzer - DNA & RNA Sequence Analysis

A comprehensive web-based application for analyzing DNA and RNA sequences through the complete molecular biology pipeline: from raw sequence detection to protein characterization and database lookup.

## Project Overview

**Course:** CSC 442 - Computational Biology & Interdisciplinary Studies  
**Level:** 400 Level  
**Academic Session:** 2024/2025 - Second Semester

BioSeqAnalyzer walks users through the fundamental processes of molecular biology with clear, layperson-friendly explanations at each step.

## Features

### 1. Sequence Input (3 Methods)
- **Direct Input:** Type or paste sequences directly
- **File Upload:** Upload .txt, .fasta, .fa, .seq files
- **Drag & Drop:** Drag and drop sequence files onto the application

### 2. Sequence Type Detection
- Automatically detects DNA (A, T, G, C) or RNA (A, U, G, C)
- Validates sequences and detects invalid characters
- Provides plain-English explanations of detection process

### 3. DNA Strand Type Selection (Conditional)
- For DNA sequences only:
  - **Non-template Strand (Coding/Sense Strand)**
  - **Template Strand (Antisense Strand)**
- Selection affects transcription process

### 4. Transcription
- Converts DNA to mRNA
- Handles both template and coding strand inputs correctly
- Displays both input and output sequences
- Includes detailed explanation of the process

### 5. Translation
- Converts mRNA to amino acid sequences via codons
- Displays each codon with its corresponding amino acid
- Identifies START and STOP codons
- Shows codon table with amino acid names and abbreviations

### 6. Amino Acids (Polypeptide Chain)
- Displays complete polypeptide chain
- Shows each amino acid with full name and abbreviation
- Includes position information
- Explains role of amino acids in protein formation

### 7. Protein Characterization & Database Lookup
- Calculates protein properties:
  - Molecular weight (Daltons)
  - Isoelectric point (pI)
  - Aromaticity
  - GRAVY (hydropathy index)
- Searches external database for protein matches
- Displays protein name, organism, function, and similarity score

## Project Structure

```
BioSeqAnalyzer/
├── frontend/
│   ├── index.html              # Main HTML interface
│   ├── css/
│   │   └── style.css           # Styling and responsive design
│   └── js/
│       └── app.js              # Frontend logic and API calls
├── backend/
│   ├── app.py                  # Flask server and API endpoints
│   ├── sequence_analyzer.py    # DNA/RNA type detection
│   ├── transcription.py        # DNA→mRNA transcription logic
│   ├── translation.py          # mRNA→Amino acids translation
│   ├── protein_lookup.py       # Protein characterization & database search
│   └── requirements.txt        # Python dependencies
└── README.md                   # This file
```

## Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js/npm (optional, for development server)
- Modern web browser

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd BioSeqAnalyzer/backend
   ```

2. **Create virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Flask server:**
   ```bash
   python app.py
   ```
   Server will start at `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd BioSeqAnalyzer/frontend
   ```

2. **Open index.html in browser:**
   - Simply open `index.html` in your web browser
   - Or use a local server:
     ```bash
     python -m http.server 8000
     ```
   - Access at `http://localhost:8000`

## API Endpoints

### Base URL
```
http://localhost:5000/api
```

### Endpoints

#### 1. Analyze Sequence
- **POST** `/api/analyze`
- **Body:** `{ "sequence": "ATCGATCG" }`
- **Response:** `{ "sequence_type": "DNA", "detected_chars": [...] }`

#### 2. Transcribe
- **POST** `/api/transcribe`
- **Body:** `{ "sequence": "ATCG", "sequence_type": "DNA", "strand_type": "coding" }`
- **Response:** `{ "mRNA": "UAGC" }`

#### 3. Translate
- **POST** `/api/translate`
- **Body:** `{ "mRNA": "AUGAAA" }`
- **Response:** `{ "codons": [...], "amino_acids": [...], "protein_sequence": "..." }`

#### 4. Protein Lookup
- **POST** `/api/protein-lookup`
- **Body:** `{ "protein_sequence": "MVLS...", "original_sequence": "..." }`
- **Response:** `{ "characterization": {...}, "database_matches": [...] }`

#### 5. Health Check
- **GET** `/api/health`
- **Response:** `{ "status": "healthy", "service": "BioSeqAnalyzer API" }`

## Marking Scheme

| Component | Assessment | Marks |
|-----------|-----------|-------|
| Sequence Input | All three input methods work correctly | 10 |
| Sequence Detection | DNA/RNA identification, validation, explanation | 15 |
| Transcription | Correct mRNA, both sequences displayed, explanation | 15 |
| Translation | Correct codons, amino acid display, START/STOP handling | 20 |
| Amino Acids | Full polypeptide chain with names/abbreviations, explanation | 15 |
| Protein & Database | Protein characterization, database lookup results | 20 |
| Overall Quality | Application runs correctly, clean UI, all explanations | 5 |
| **TOTAL** | | **100** |

## Key Technologies

- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **Backend:** Python, Flask, Flask-CORS
- **Biology Libraries:** BioPython (optional, for advanced features)
- **Database Integration:** UniProt/BLAST API (mock implementation provided)

## Features Implemented

✅ Sequence input (text, file, drag-drop)  
✅ Sequence type detection (DNA/RNA/Invalid)  
✅ DNA strand type selection  
✅ Transcription (DNA→mRNA)  
✅ Translation (mRNA→Amino Acids)  
✅ Polypeptide chain display  
✅ Protein characterization  
✅ Database lookup simulation  
✅ Plain-English explanations at each step  
✅ Responsive, user-friendly interface  

## Usage Example

1. **Start Backend:**
   ```bash
   cd backend
   python app.py
   ```

2. **Open Frontend:**
   - Navigate to `frontend/index.html` in your browser

3. **Enter DNA Sequence:**
   - Type: `ATGAAATAA`
   - Or upload a FASTA file
   - Or drag & drop a file

4. **Follow the Pipeline:**
   - Select strand type if DNA
   - View transcription results
   - See translation with codons
   - Explore amino acids
   - Check protein characterization and database matches

## Biological Background

### DNA (Deoxyribonucleic Acid)
- Contains bases: Adenine (A), Thymine (T), Guanine (G), Cytosine (C)
- Double-stranded helix structure
- Two strand types: Template (antisense) and Non-template (coding/sense)

### RNA (Ribonucleic Acid)
- Contains bases: Adenine (A), Uracil (U), Guanine (G), Cytosine (C)
- Single-stranded
- mRNA carries genetic information for protein synthesis

### Transcription
- Process: DNA → mRNA
- Template strand is used to create complementary mRNA
- Occurs in cell nucleus

### Translation
- Process: mRNA → Protein
- mRNA is read in groups of 3 bases (codons)
- Each codon specifies an amino acid
- Occurs at ribosomes

### Protein
- Made of amino acid chains (polypeptides)
- Performs various cellular functions
- Structure determined by amino acid sequence

## Notes

- **Error Handling:** Application validates all inputs and provides user-friendly error messages
- **CORS Enabled:** Frontend and backend can communicate across different ports
- **Mock Database:** Protein database is simulated; integrate with real UniProt/BLAST API for production
- **Accessibility:** Plain-English explanations make biology concepts understandable to non-specialists

## Future Enhancements

- Integration with real BLAST API
- Support for more file formats (GENBANK, EMBL)
- Multiple sequence alignment
- Protein structure prediction
- Save/export analysis results
- Sequence comparison tools
- Advanced statistical analysis

## Support

For questions or issues, refer to the assignment documentation or check the console output for debugging information.

---

**Assignment:** CSC 442 Programming Assignment - Project 2  
**Created:** 2024/2025  
**Last Updated:** April 2026

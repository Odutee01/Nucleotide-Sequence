// BioSeqAnalyzer - Frontend Application
// DNA & RNA Sequence Analysis

const API_BASE_URL = 'http://localhost:5000/api';

let currentAnalysisState = {
    sequence: '',
    sequenceType: '',
    strandType: '',
    mRNA: '',
    codons: [],
    codonAminoAcids: [],
    aminoAcids: [],
    proteinSequence: ''
};

// ========== DRAG & DROP FUNCTIONALITY ==========
const dragDropZone = document.getElementById('dragDropZone');

dragDropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dragDropZone.classList.add('drag-over');
});

dragDropZone.addEventListener('dragleave', () => {
    dragDropZone.classList.remove('drag-over');
});

dragDropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dragDropZone.classList.remove('drag-over');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        loadFile(files[0]);
    }
});

// ========== FILE INPUT ==========
document.getElementById('fileInput').addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        loadFile(e.target.files[0]);
    }
});

function loadFile(file) {
    const reader = new FileReader();
    reader.onload = (e) => {
        document.getElementById('sequenceInput').value = e.target.result.trim();
    };
    reader.readAsText(file);
}

// ========== ANALYZE BUTTON ==========
document.getElementById('analyzeBtn').addEventListener('click', analyzeSequence);

async function analyzeSequence() {
    const sequence = document.getElementById('sequenceInput').value.trim().toUpperCase();
    
    if (!sequence) {
        showError('Please enter or upload a sequence first.');
        return;
    }

    try {
        showLoading('Analyzing sequence...');
        
        // Send to backend for analysis
        const response = await fetch(`${API_BASE_URL}/analyze`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ sequence })
        });

        const result = await response.json();

        if (!response.ok) {
            showError(result.error || 'An error occurred during analysis.');
            return;
        }

        currentAnalysisState.sequence = sequence;
        currentAnalysisState.sequenceType = result.sequence_type;

        // Display detection result
        displayDetectionResult(result);
        document.getElementById('step2').style.display = 'block';

        // Show strand selection if DNA
        if (result.sequence_type === 'DNA') {
            document.getElementById('step3').style.display = 'block';
        } else {
            // For RNA, proceed directly to transcription
            proceedToTranscription('RNA');
        }

    } catch (error) {
        showError('Network error: ' + error.message);
    }
}

// ========== DETECTION RESULT DISPLAY ==========
function displayDetectionResult(result) {
    const detectionBox = document.getElementById('detectionResult');
    const explanation = generateDetectionExplanation(result);
    
    detectionBox.innerHTML = `
        <h3>Sequence Type: <span style="color: #764ba2;">${result.sequence_type}</span></h3>
        <p><strong>Detected Characters:</strong> ${result.detected_chars.join(', ')}</p>
        <p><strong>Sequence Length:</strong> ${currentAnalysisState.sequence.length} bases</p>
        <div class="explanation">
            <strong>📖 Explanation:</strong> ${explanation}
        </div>
    `;
    hideLoading();
}

function generateDetectionExplanation(result) {
    if (result.sequence_type === 'DNA') {
        return "DNA (deoxyribonucleic acid) contains four nucleotide bases: Adenine (A), Thymine (T), Guanine (G), and Cytosine (C). Your sequence contains only these characters, identifying it as DNA.";
    } else if (result.sequence_type === 'RNA') {
        return "RNA (ribonucleic acid) contains four nucleotide bases: Adenine (A), Uracil (U), Guanine (G), and Cytosine (C). Your sequence contains only these characters, identifying it as RNA. Notice that RNA contains Uracil (U) instead of Thymine (T), which is present in DNA.";
    } else {
        return `Your sequence contains invalid characters: ${result.invalid_chars.join(', ')}. Valid DNA bases are A, T, G, C. Valid RNA bases are A, U, G, C.`;
    }
}

// ========== STRAND SELECTION ==========
document.getElementById('proceedTranscriptionBtn').addEventListener('click', () => {
    const strandType = document.querySelector('input[name="strandType"]:checked');
    
    if (!strandType) {
        showError('Please select a strand type before proceeding.');
        return;
    }

    currentAnalysisState.strandType = strandType.value;
    proceedToTranscription('DNA');
});

// ========== TRANSCRIPTION ==========
async function proceedToTranscription(sequenceType) {
    try {
        showLoading('Performing transcription...');

        const payload = {
            sequence: currentAnalysisState.sequence,
            sequence_type: sequenceType
        };

        if (sequenceType === 'DNA') {
            payload.strand_type = currentAnalysisState.strandType;
        }

        const response = await fetch(`${API_BASE_URL}/transcribe`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const result = await response.json();

        if (!response.ok) {
            showError(result.error || 'Transcription failed.');
            return;
        }

        currentAnalysisState.mRNA = result.mRNA;
        displayTranscriptionResult(result, sequenceType);
        document.getElementById('step4').style.display = 'block';
        proceedToTranslation();

    } catch (error) {
        showError('Network error: ' + error.message);
    }
}

function displayTranscriptionResult(result, sequenceType) {
    const transcriptionBox = document.getElementById('transcriptionResult');
    const explanation = generateTranscriptionExplanation(sequenceType, currentAnalysisState.strandType);

    let inputDisplay = currentAnalysisState.sequence;
    let processInfo = '';

    if (sequenceType === 'DNA') {
        processInfo = `<p><strong>Strand Type:</strong> ${currentAnalysisState.strandType === 'coding' ? 'Non-template (Coding)' : 'Template (Antisense)'}</p>`;
    }

    transcriptionBox.innerHTML = `
        <h3>Transcription Results</h3>
        ${processInfo}
        <p><strong>Input DNA/RNA Sequence:</strong></p>
        <p style="font-family: monospace; background: #f0f0f0; padding: 10px; border-radius: 5px; word-break: break-all;">
            ${formatSequence(inputDisplay)}
        </p>
        <p><strong>Output mRNA Sequence:</strong></p>
        <p style="font-family: monospace; background: #f0f0f0; padding: 10px; border-radius: 5px; word-break: break-all; color: #e74c3c;">
            ${formatSequence(result.mRNA)}
        </p>
        <div class="explanation">
            <strong>📖 Explanation:</strong> ${explanation}
        </div>
    `;
    hideLoading();
}

function generateTranscriptionExplanation(sequenceType, strandType) {
    if (sequenceType === 'DNA') {
        const strandInfo = strandType === 'coding' 
            ? "Since you provided the coding strand, we first convert it to the template strand, then transcribe it."
            : "Since you provided the template strand, we transcribe it directly.";
        
        return `Transcription is the process where DNA is converted into mRNA (messenger RNA). ${strandInfo} During transcription, the DNA bases are paired with RNA bases: Adenine (A) pairs with Uracil (U), Thymine (T) pairs with Adenine (A), Guanine (G) pairs with Cytosine (C), and Cytosine (C) pairs with Guanine (G). The resulting mRNA is displayed above in red.`;
    } else {
        return "This sequence was already identified as RNA. Transcription primarily applies to DNA. The RNA sequence is displayed as-is, though in a biological context, this would be the mRNA product of transcription.";
    }
}

// ========== TRANSLATION ==========
async function proceedToTranslation() {
    try {
        showLoading('Performing translation...');

        const response = await fetch(`${API_BASE_URL}/translate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ mRNA: currentAnalysisState.mRNA })
        });

        const result = await response.json();

        if (!response.ok) {
            showError(result.error || 'Translation failed.');
            return;
        }

        currentAnalysisState.codons = result.codons;
        currentAnalysisState.codonAminoAcids = result.codon_amino_acids;
        currentAnalysisState.aminoAcids = result.amino_acids;
        currentAnalysisState.proteinSequence = result.protein_sequence;

        displayTranslationResult(result);
        document.getElementById('step5').style.display = 'block';
        proceedToAminoAcids();

    } catch (error) {
        showError('Network error: ' + error.message);
    }
}

function displayTranslationResult(result) {
    const translationBox = document.getElementById('translationResult');
    const explanation = generateTranslationExplanation();

    let codonDisplay = '';
    result.codons.forEach((codon, index) => {
        const amino = result.codon_amino_acids[index] || { name: 'Unknown', abbreviation: 'Xaa' };
        const isStart = codon === 'AUG';
        const isStop = codon === 'UAA' || codon === 'UAG' || codon === 'UGA';
        
        codonDisplay += `
            <tr class="${isStart ? 'start' : isStop ? 'stop' : ''}">
                <td>${codon}</td>
                <td>${amino.name}</td>
                <td>${amino.abbreviation}</td>
                <td>${isStart ? 'START' : isStop ? 'STOP' : ''}</td>
            </tr>
        `;
    });

    translationBox.innerHTML = `
        <h3>Translation Results</h3>
        <p><strong>mRNA Sequence:</strong></p>
        <p style="font-family: monospace; background: #f0f0f0; padding: 10px; border-radius: 5px; word-break: break-all;">
            ${formatSequence(currentAnalysisState.mRNA, 3)}
        </p>
        <p><strong>Codons and Their Amino Acids:</strong></p>
        <div class="codon-table">
            <table>
                <thead>
                    <tr>
                        <th>Codon</th>
                        <th>Amino Acid</th>
                        <th>Abbreviation</th>
                        <th>Note</th>
                    </tr>
                </thead>
                <tbody>
                    ${codonDisplay}
                </tbody>
            </table>
        </div>
        <div class="explanation">
            <strong>📖 Explanation:</strong> ${explanation}
        </div>
    `;
    hideLoading();
}

function generateTranslationExplanation() {
    return "Translation is the process of reading the mRNA sequence and building a protein. The mRNA is read in groups of three bases called 'codons.' Each codon specifies which amino acid to add to the growing protein chain. The process starts at the START codon (AUG) and ends when a STOP codon (UAA, UAG, or UGA) is encountered. Above, each codon is paired with its corresponding amino acid name and abbreviation.";
}

// ========== AMINO ACIDS ==========
async function proceedToAminoAcids() {
    try {
        const aminoAcidsBox = document.getElementById('aminoAcidsResult');
        const explanation = generateAminoAcidsExplanation();

        if (currentAnalysisState.aminoAcids.length === 0) {
            aminoAcidsBox.innerHTML = `
                <h3>Polypeptide Chain</h3>
                <p>No translated amino acids were produced.</p>
                <div class="explanation">
                    <strong>📖 Explanation:</strong> ${explanation}
                </div>
            `;
            document.getElementById('step6').style.display = 'block';
            proceedToProtein();
            return;
        }

        let aminoChain = '';
        currentAnalysisState.aminoAcids.forEach((amino) => {
            const isStart = amino.abbreviation === 'Met';
            const isStop = amino.name === 'STOP';
            
            aminoChain += `<span class="amino-acid ${isStart ? 'start' : isStop ? 'stop' : ''}">${amino.abbreviation}</span>`;
        });

        aminoAcidsBox.innerHTML = `
            <h3>Polypeptide Chain</h3>
            <p><strong>Total Amino Acids:</strong> ${currentAnalysisState.aminoAcids.length}</p>
            <div class="amino-acid-chain">
                ${aminoChain}
            </div>
            <table style="width: 100%; margin-top: 20px; border-collapse: collapse;">
                <thead>
                    <tr style="background: #667eea; color: white;">
                        <th style="padding: 10px; text-align: left;">Position</th>
                        <th style="padding: 10px; text-align: left;">Name</th>
                        <th style="padding: 10px; text-align: center;">Abbreviation</th>
                    </tr>
                </thead>
                <tbody>
                    ${currentAnalysisState.aminoAcids.map((amino, idx) => `
                        <tr style="border-bottom: 1px solid #ddd; background: ${idx % 2 === 0 ? '#fff' : '#f9f9f9'};">
                            <td style="padding: 10px;">${idx + 1}</td>
                            <td style="padding: 10px;">${amino.name}</td>
                            <td style="padding: 10px; text-align: center; font-weight: bold;">${amino.abbreviation}</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
            <div class="explanation">
                <strong>📖 Explanation:</strong> ${explanation}
            </div>
        `;

        document.getElementById('step6').style.display = 'block';
        proceedToProtein();

    } catch (error) {
        showError('Error displaying amino acids: ' + error.message);
    }
}

function generateAminoAcidsExplanation() {
    return `Amino acids are organic molecules that are the building blocks of proteins. A polypeptide chain is a linear sequence of amino acids held together by peptide bonds. Each amino acid in this chain was specified by a codon in the mRNA sequence. The chain above shows all ${currentAnalysisState.aminoAcids.length} amino acids that make up your protein, starting with the START amino acid (Methionine/Met, shown in green) and ending with the STOP signal (shown in red). The table below lists each amino acid with its full name, abbreviation, and position in the chain.`;
}

// ========== PROTEIN & DATABASE LOOKUP ==========
async function proceedToProtein() {
    try {
        showLoading('Characterizing protein and searching database...');

        if (!currentAnalysisState.proteinSequence) {
            const proteinBox = document.getElementById('proteinResult');
            proteinBox.innerHTML = `
                <h3>Protein Characterization</h3>
                <p>No protein sequence could be generated from the current translation.</p>
                <div class="explanation">
                    <strong>📖 Explanation:</strong> Translation did not produce a protein because the mRNA sequence does not contain a valid start codon (AUG) in the translated region. Please make sure the input DNA/RNA includes a proper coding region and, for DNA, the correct strand type was selected.
                </div>
            `;
            document.getElementById('step7').style.display = 'block';
            hideLoading();
            return;
        }

        const response = await fetch(`${API_BASE_URL}/protein-lookup`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                protein_sequence: currentAnalysisState.proteinSequence,
                original_sequence: currentAnalysisState.sequence
            })
        });

        const result = await response.json();

        if (!response.ok) {
            showError(result.error || 'Protein lookup failed.');
            return;
        }

        displayProteinResult(result);
        document.getElementById('step7').style.display = 'block';

    } catch (error) {
        showError('Network error: ' + error.message);
    }
}

function displayProteinResult(result) {
    const proteinBox = document.getElementById('proteinResult');
    const dbResultsBox = document.getElementById('databaseResults');
    const explanation = generateProteinExplanation();

    const stats = `
        <div class="stats-grid">
            <div class="stat-box">
                <div class="label">Molecular Weight (Da)</div>
                <div class="value">${result.characterization.molecular_weight.toFixed(2)}</div>
            </div>
            <div class="stat-box">
                <div class="label">Isoelectric Point (pI)</div>
                <div class="value">${result.characterization.isoelectric_point.toFixed(2)}</div>
            </div>
            <div class="stat-box">
                <div class="label">Aromaticity</div>
                <div class="value">${result.characterization.aromaticity.toFixed(3)}</div>
            </div>
            <div class="stat-box">
                <div class="label">Gravy (Hydropathy)</div>
                <div class="value">${result.characterization.gravy.toFixed(3)}</div>
            </div>
        </div>
    `;

    proteinBox.innerHTML = `
        <h3>Protein Characterization</h3>
        <p><strong>Protein Sequence:</strong></p>
        <p style="font-family: monospace; background: #f0f0f0; padding: 10px; border-radius: 5px; word-break: break-all; font-size: 0.9em;">
            ${formatSequence(currentAnalysisState.proteinSequence, 50)}
        </p>
        <h4>Physical Properties:</h4>
        ${stats}
        <div class="explanation">
            <strong>📖 Explanation:</strong> ${explanation}
        </div>
    `;

    if (result.database_matches && result.database_matches.length > 0) {
        let dbHtml = '<h4>Database Matches (UniProt/BLAST):</h4>';
        result.database_matches.forEach((match, idx) => {
            dbHtml += `
                <div class="protein-match">
                    <h4>Match #${idx + 1}: ${match.protein_name}</h4>
                    <p><strong>Organism:</strong> ${match.organism}</p>
                    <p><strong>Similarity Score:</strong> ${(match.similarity * 100).toFixed(1)}%</p>
                    <p><strong>Function:</strong> ${match.function}</p>
                    <p><strong>Database ID:</strong> ${match.database_id}</p>
                    <p><a href="${match.url}" target="_blank">View on Database</a></p>
                </div>
            `;
        });
        dbResultsBox.innerHTML = dbHtml;
    } else {
        dbResultsBox.innerHTML = '<p style="color: #999;">No significant matches found in the database.</p>';
    }

    hideLoading();
}

function generateProteinExplanation() {
    return "A protein is a complex molecule made up of amino acids linked together in a specific sequence. Proteins are essential for all living organisms, performing thousands of different functions such as catalyzing reactions, providing structure, transporting molecules, and defending against pathogens. The characterization above shows important physical properties of your protein: <ul style='margin: 10px 0; padding-left: 20px;'><li><strong>Molecular Weight:</strong> The total mass of your protein.</li><li><strong>Isoelectric Point (pI):</strong> The pH at which your protein has no net electric charge.</li><li><strong>Aromaticity:</strong> The proportion of aromatic amino acids.</li><li><strong>GRAVY:</strong> Grand average of hydropathy - indicates how hydrophobic or hydrophilic the protein is.</li></ul>The database search attempts to find similar proteins in UniProt or BLAST to help identify what this protein might be in nature and what role it might play.";
}

// ========== UTILITY FUNCTIONS ==========
function formatSequence(seq, groupSize = 10) {
    if (!groupSize) return seq;
    
    let formatted = '';
    for (let i = 0; i < seq.length; i += groupSize) {
        formatted += seq.substring(i, i + groupSize) + ' ';
    }
    return formatted.trim();
}

function showError(message) {
    const errorSection = document.getElementById('errorSection');
    document.getElementById('errorMessage').textContent = message;
    errorSection.style.display = 'block';
    hideLoading();
}

function showLoading(message) {
    // Could add a loading spinner here
    console.log(message);
}

function hideLoading() {
    // Hide loading spinner
}

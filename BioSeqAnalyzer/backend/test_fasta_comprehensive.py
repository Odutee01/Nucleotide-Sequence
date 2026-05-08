#!/usr/bin/env python3
"""
Comprehensive FASTA file parsing and API testing
Tests FASTA parsing, sequence analysis, and transcription
"""
import requests
import json
import sys

BASE_URL = 'http://localhost:5000'

# Test FASTA sequence - Human insulin gene
FASTA_SEQUENCE = """>test_sequence Human insulin gene
ATGGCCCTGTGGATGCGCCTCCTGCCCCTGCTGGCGCTGCTGGCCCTCTGGGGACCTGACCCAGCCGCAGCCTTTGTGAACCAACACCTGTGCGGCTCACACCTGGTGGAAGCTCTCTACCTAGTGTGCGGGGAACGAGGCTTCTTCTACACACCCAAGACCCGCCGGGAGGCAGAGGACCTGCAGGTGGGGCAGGTGGAGCTGGGCGGGGGCCCTGGTGCAGGCAGCCTGCAGCCCTTGGCCCTGGAGGGGTCCCTGCAGAAGCGTGGCATTGTGGAACAATGCTGTACCAGCATCTGCTCCCTCTACCAGCTGGAGAACTACTGCAACTAAG"""

# Raw DNA sequence without FASTA header
RAW_SEQUENCE = """ATGGCCCTGTGGATGCGCCTCCTGCCCCTGCTGGCGCTGCTGGCCCTCTGGGGACCTGACCCAGCCGCAGCCTTTGTGAACCAACACCTGTGCGGCTCACACCTGGTGGAAGCTCTCTACCTAGTGTGCGGGGAACGAGGCTTCTTCTACACACCCAAGACCCGCCGGGAGGCAGAGGACCTGCAGGTGGGGCAGGTGGAGCTGGGCGGGGGCCCTGGTGCAGGCAGCCTGCAGCCCTTGGCCCTGGAGGGGTCCCTGCAGAAGCGTGGCATTGTGGAACAATGCTGTACCAGCATCTGCTCCCTCTACCAGCTGGAGAACTACTGCAACTAAG"""

def test_analyze_fasta():
    """Test 1: Analyze FASTA format sequence"""
    print("\n" + "="*70)
    print("TEST 1: Analyze FASTA Format Sequence")
    print("="*70)

    try:
        response = requests.post(
            f'{BASE_URL}/api/analyze',
            json={'sequence': FASTA_SEQUENCE},
            headers={'Content-Type': 'application/json'},
            timeout=5
        )

        print(f"Status Code: {response.status_code}")
        result = response.json()
        print(f"Response: {json.dumps(result, indent=2)}")

        # Verify expectations
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        assert result['sequence_type'] == 'DNA', f"Expected DNA type, got {result['sequence_type']}"
        assert 'sequence_length' in result, "sequence_length not in response"
        assert result['sequence_length'] > 0, "sequence_length should be > 0"

        print("✓ PASSED: FASTA parsed correctly as DNA")
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False

def test_analyze_raw_dna():
    """Test 2: Analyze raw DNA sequence (no FASTA header)"""
    print("\n" + "="*70)
    print("TEST 2: Analyze Raw DNA Sequence (No FASTA Header)")
    print("="*70)

    try:
        response = requests.post(
            f'{BASE_URL}/api/analyze',
            json={'sequence': RAW_SEQUENCE},
            headers={'Content-Type': 'application/json'},
            timeout=5
        )

        print(f"Status Code: {response.status_code}")
        result = response.json()
        print(f"Response: {json.dumps(result, indent=2)}")

        # Verify expectations
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        assert result['sequence_type'] == 'DNA', f"Expected DNA type, got {result['sequence_type']}"

        print("✓ PASSED: Raw DNA sequence detected correctly")
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False

def test_transcribe_fasta():
    """Test 3: Transcribe FASTA sequence"""
    print("\n" + "="*70)
    print("TEST 3: Transcribe FASTA Sequence (DNA -> mRNA)")
    print("="*70)

    try:
        response = requests.post(
            f'{BASE_URL}/api/transcribe',
            json={
                'sequence': FASTA_SEQUENCE,
                'sequence_type': 'DNA',
                'strand_type': 'coding'
            },
            headers={'Content-Type': 'application/json'},
            timeout=5
        )

        print(f"Status Code: {response.status_code}")
        result = response.json()

        # Show first 100 chars of mRNA
        mrna = result.get('mRNA', '')
        print(f"Original DNA (first 100 chars): {FASTA_SEQUENCE[:100]}...")
        print(f"mRNA (first 100 chars):         {mrna[:100]}...")
        print(f"Full Response: {json.dumps(result, indent=2)}")

        # Verify expectations
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        assert 'mRNA' in result, "mRNA not in response"
        assert len(result['mRNA']) > 0, "mRNA should not be empty"
        # mRNA should have U instead of T
        assert 'U' in result['mRNA'], "mRNA should contain U (not T)"
        assert 'T' not in result['mRNA'], "mRNA should not contain T"

        print("✓ PASSED: Transcription successful (T->U conversion)")
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False

def test_transcribe_raw_dna():
    """Test 4: Transcribe raw DNA sequence"""
    print("\n" + "="*70)
    print("TEST 4: Transcribe Raw DNA Sequence (DNA -> mRNA)")
    print("="*70)

    try:
        response = requests.post(
            f'{BASE_URL}/api/transcribe',
            json={
                'sequence': RAW_SEQUENCE,
                'sequence_type': 'DNA',
                'strand_type': 'coding'
            },
            headers={'Content-Type': 'application/json'},
            timeout=5
        )

        print(f"Status Code: {response.status_code}")
        result = response.json()
        print(f"Response: {json.dumps(result, indent=2)}")

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        assert 'mRNA' in result, "mRNA not in response"

        print("✓ PASSED: Raw DNA transcription successful")
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False

def test_invalid_sequence():
    """Test 5: Verify invalid sequence rejection"""
    print("\n" + "="*70)
    print("TEST 5: Test Invalid Sequence Detection")
    print("="*70)

    invalid_seq = ">test\nXYZ123INVALID"

    try:
        response = requests.post(
            f'{BASE_URL}/api/analyze',
            json={'sequence': invalid_seq},
            headers={'Content-Type': 'application/json'},
            timeout=5
        )

        print(f"Status Code: {response.status_code}")
        result = response.json()
        print(f"Response: {json.dumps(result, indent=2)}")

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        assert result['sequence_type'] == 'INVALID', f"Expected INVALID type, got {result['sequence_type']}"
        assert len(result['invalid_chars']) > 0, "Should have detected invalid characters"

        print("✓ PASSED: Invalid sequence correctly rejected")
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False

def test_fasta_extraction():
    """Test 6: Verify FASTA extraction removes headers"""
    print("\n" + "="*70)
    print("TEST 6: Test FASTA Header Extraction")
    print("="*70)

    try:
        # Test with FASTA that has multiple lines
        multiline_fasta = """>sequence1
ATGCATGC
ATGCATGC
ATGCATGC"""

        response = requests.post(
            f'{BASE_URL}/api/analyze',
            json={'sequence': multiline_fasta},
            headers={'Content-Type': 'application/json'},
            timeout=5
        )

        print(f"Status Code: {response.status_code}")
        result = response.json()
        print(f"Response: {json.dumps(result, indent=2)}")

        # Should have extracted all 24 bases (8 per line x 3 lines)
        expected_length = 24
        assert result['sequence_length'] == expected_length, \
            f"Expected length {expected_length}, got {result['sequence_length']}"

        print("✓ PASSED: Multi-line FASTA correctly extracted and joined")
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False

def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("BIOSEQANALYZER - FASTA PARSING & API TESTS")
    print("="*70)
    print(f"Backend URL: {BASE_URL}")

    # Check if backend is running
    try:
        response = requests.get(f'{BASE_URL}/api/analyze', timeout=2)
    except requests.exceptions.ConnectionError:
        print("\n✗ ERROR: Cannot connect to backend at {BASE_URL}")
        print("Please ensure Flask backend is running with: python app.py")
        sys.exit(1)

    # Run all tests
    tests = [
        test_analyze_fasta,
        test_analyze_raw_dna,
        test_transcribe_fasta,
        test_transcribe_raw_dna,
        test_invalid_sequence,
        test_fasta_extraction
    ]

    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"\n✗ CRITICAL ERROR in {test.__name__}: {e}")
            results.append(False)

    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")

    if passed == total:
        print("✓ ALL TESTS PASSED - FASTA parsing is working correctly!")
    else:
        print(f"✗ {total - passed} test(s) failed - Review errors above")

    print("="*70 + "\n")

if __name__ == '__main__':
    main()
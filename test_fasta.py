import requests
import json

# Read the FASTA file
with open('test_fasta.txt', 'r') as f:
    fasta_content = f.read()

print('Testing FASTA sequence analysis...')
print('FASTA content:')
print(fasta_content[:100] + '...' if len(fasta_content) > 100 else fasta_content)
print()

# Test the analyze endpoint
response = requests.post('http://localhost:5000/api/analyze',
                        json={'sequence': fasta_content},
                        headers={'Content-Type': 'application/json'})

print('Analyze endpoint response:')
print(f'Status: {response.status_code}')
if response.status_code == 200:
    result = response.json()
    print(json.dumps(result, indent=2))
else:
    print(f'Error: {response.text}')
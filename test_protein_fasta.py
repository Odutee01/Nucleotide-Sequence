import requests
import json

# Test the protein FASTA sequence
fasta_content = """>sp|P01308|INS_HUMAN Insulin OS=Homo sapiens OX=9606 GN=INS PE=1 SV=1
MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKTRREAED
LQVGQVELGGGPGAGSLQPLALEGSLQKRGIVEQCCTSICSLYQLENYCN"""

print('Testing protein FASTA sequence...')
print('FASTA content:')
print(fasta_content)
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
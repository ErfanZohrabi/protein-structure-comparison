#!/usr/bin/env python3
"""
Simple usage example for protein structure comparison
"""

from test import ProteinStructureComparator

def simple_comparison_example():
    """
    Simple example showing how to compare AlphaFold and ESMFold structures
    """
    # Initialize the comparator
    comparator = ProteinStructureComparator()
    
    # Example proteins to compare
    proteins = [
        {
            "name": "human_insulin",
            "uniprot_id": "P01308",
            "sequence": "GIVEQCCTSICSLYQLENYCNFVNQHLCGSHLVEALYLVCGERGFFYTPKT"
        },
        {
            "name": "lysozyme",
            "uniprot_id": "P61626", 
            "sequence": "KVFGRCELAAAMKRHGLDNYRGYSLGNWVCAAKFESNFNTQATNRNTDGSTDYGILQINSRWWCNDGRTPGSRNLCNIPCSALLSSDITASVNCAKKIVSDGNGMNAWVAWRNRCKGTDVQAWIRGCRL"
        }
    ]
    
    results = []
    
    for protein in proteins:
        print(f"\nProcessing {protein['name']}...")
        print("-" * 50)
        
        result = comparator.compare_proteins(
            uniprot_id=protein["uniprot_id"],
            sequence=protein["sequence"],
            protein_name=protein["name"]
        )
        
        results.append(result)
        
        if result['success']:
            print(f"✓ Successfully compared {protein['name']}")
            print(f"  RMSD: {result['rmsd']:.3f} Å")
        else:
            print(f"✗ Failed to compare {protein['name']}")
    
    # Summary
    print("\n" + "="*60)
    print("COMPARISON SUMMARY")
    print("="*60)
    
    for result in results:
        if result['success']:
            print(f"{result['protein_name']}: RMSD = {result['rmsd']:.3f} Å")
        else:
            print(f"{result['protein_name']}: Comparison failed")

def alphafold_only_example():
    """
    Example showing how to download only AlphaFold structures
    """
    comparator = ProteinStructureComparator()
    
    # Download AlphaFold structure for a protein
    uniprot_id = "P0DTC2"  # SARS-CoV-2 spike protein
    
    print(f"Downloading AlphaFold structure for {uniprot_id}...")
    alphafold_path = comparator.download_alphafold_structure(uniprot_id)
    
    if alphafold_path:
        print(f"Structure downloaded successfully: {alphafold_path}")
    else:
        print("Failed to download structure")

def esmfold_only_example():
    """
    Example showing how to generate only ESMFold predictions
    """
    comparator = ProteinStructureComparator()
    
    # Example short sequence
    sequence = "MKTVRQERLKSIVRILERSKEPVSGAQLAEELSVSRQVIVQDIAYLRSLGYNIVATPRGYVLAGG"
    protein_name = "example_protein"
    
    print(f"Generating ESMFold prediction for {protein_name}...")
    esmfold_path = comparator.generate_esmfold_structure(sequence, protein_name)
    
    if esmfold_path:
        print(f"Structure generated successfully: {esmfold_path}")
    else:
        print("Failed to generate structure")

if __name__ == "__main__":
    print("Protein Structure Comparison Examples")
    print("=" * 60)
    
    choice = input("""
Choose an example to run:
1. Full comparison (AlphaFold vs ESMFold)
2. AlphaFold download only
3. ESMFold prediction only

Enter choice (1-3): """).strip()
    
    if choice == "1":
        simple_comparison_example()
    elif choice == "2":
        alphafold_only_example()
    elif choice == "3":
        esmfold_only_example()
    else:
        print("Invalid choice. Running full comparison example...")
        simple_comparison_example()
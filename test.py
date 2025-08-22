#!/usr/bin/env python3
"""
Protein Structure Comparison: AlphaFold vs ESMFold

This script provides functionality to:
1. Download AlphaFold structures from the database
2. Generate ESMFold predictions using Hugging Face
3. Visualize and compare structures
4. Calculate structural similarity metrics

Requirements:
- pip install requests biopython torch transformers py3Dmol matplotlib numpy
- For ESMFold: pip install fair-esm
"""

import os
import requests
import warnings
from pathlib import Path
from typing import Optional, Tuple, Dict, Any

try:
    import numpy as np
    from Bio.PDB import PDBParser, Superimposer, PDBIO
    from Bio.PDB.Structure import Structure
    import matplotlib.pyplot as plt
except ImportError as e:
    print(f"Required packages missing: {e}")
    print("Install with: pip install biopython matplotlib numpy")
    exit(1)

try:
    import torch
    from transformers import EsmForProteinFolding, AutoTokenizer
except ImportError:
    print("ESMFold dependencies missing. Install with: pip install torch transformers")
    print("For full ESMFold support: pip install fair-esm")

class ProteinStructureComparator:
    """Class to compare AlphaFold and ESMFold protein structures"""
    
    def __init__(self, output_dir: str = "protein_structures"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.parser = PDBParser(QUIET=True)
        
    def download_alphafold_structure(self, uniprot_id: str) -> Optional[str]:
        """
        Download AlphaFold structure from the database
        
        Args:
            uniprot_id: UniProt accession number (e.g., 'P0DTC2')
            
        Returns:
            Path to downloaded PDB file or None if failed
        """
        url = f"https://alphafold.ebi.ac.uk/files/AF-{uniprot_id}-F1-model_v4.pdb"
        output_path = self.output_dir / f"alphafold_{uniprot_id}.pdb"
        
        try:
            print(f"Downloading AlphaFold structure for {uniprot_id}...")
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            with open(output_path, 'w') as f:
                f.write(response.text)
            
            print(f"AlphaFold structure saved to: {output_path}")
            return str(output_path)
            
        except requests.RequestException as e:
            print(f"Error downloading AlphaFold structure: {e}")
            return None
    
    def generate_esmfold_structure(self, sequence: str, protein_name: str) -> Optional[str]:
        """
        Generate ESMFold structure prediction
        
        Args:
            sequence: Protein amino acid sequence
            protein_name: Name for the output file
            
        Returns:
            Path to generated PDB file or None if failed
        """
        try:
            print(f"Generating ESMFold structure for {protein_name}...")
            
            # Load ESMFold model
            model = EsmForProteinFolding.from_pretrained("facebook/esmfold_v1")
            tokenizer = AutoTokenizer.from_pretrained("facebook/esmfold_v1")
            
            # Set model to evaluation mode
            model.eval()
            
            # Tokenize sequence
            tokenized = tokenizer(sequence, return_tensors="pt", add_special_tokens=False)
            
            # Generate structure
            with torch.no_grad():
                output = model(tokenized['input_ids'])
            
            # Extract coordinates and convert to PDB format
            coordinates = output['positions'].squeeze(0).cpu().numpy()
            
            # Create PDB file
            output_path = self.output_dir / f"esmfold_{protein_name}.pdb"
            self._write_pdb_from_coordinates(coordinates, sequence, output_path)
            
            print(f"ESMFold structure saved to: {output_path}")
            return str(output_path)
            
        except Exception as e:
            print(f"Error generating ESMFold structure: {e}")
            print("Note: ESMFold requires significant computational resources")
            return None
    
    def _write_pdb_from_coordinates(self, coordinates: np.ndarray, sequence: str, output_path: Path):
        """
        Write PDB file from coordinates and sequence
        
        Args:
            coordinates: 3D coordinates array (N, 37, 3) for all atoms
            sequence: Amino acid sequence
            output_path: Output file path
        """
        # Simplified PDB writing - in practice, you'd want more sophisticated handling
        atom_names = ['N', 'CA', 'C', 'O']  # Main chain atoms
        
        with open(output_path, 'w') as f:
            f.write("HEADER    ESMFOLD PREDICTION\n")
            atom_id = 1
            
            for i, aa in enumerate(sequence):
                for j, atom_name in enumerate(atom_names):
                    if j < coordinates.shape[1]:  # Check if coordinates exist
                        x, y, z = coordinates[i, j, :]
                        f.write(f"ATOM  {atom_id:5d}  {atom_name:>2s}  {aa} A{i+1:4d}    "
                               f"{x:8.3f}{y:8.3f}{z:8.3f}  1.00 50.00           {atom_name[0]}\n")
                        atom_id += 1
            f.write("END\n")
    
    def calculate_rmsd(self, structure1_path: str, structure2_path: str) -> float:
        """
        Calculate RMSD between two protein structures
        
        Args:
            structure1_path: Path to first PDB file
            structure2_path: Path to second PDB file
            
        Returns:
            RMSD value in Angstroms
        """
        try:
            # Load structures
            structure1 = self.parser.get_structure("struct1", structure1_path)
            structure2 = self.parser.get_structure("struct2", structure2_path)
            
            # Get CA atoms from both structures
            atoms1 = []
            atoms2 = []
            
            for model in structure1:
                for chain in model:
                    for residue in chain:
                        if 'CA' in residue:
                            atoms1.append(residue['CA'])
            
            for model in structure2:
                for chain in model:
                    for residue in chain:
                        if 'CA' in residue:
                            atoms2.append(residue['CA'])
            
            # Ensure same number of atoms
            min_len = min(len(atoms1), len(atoms2))
            atoms1 = atoms1[:min_len]
            atoms2 = atoms2[:min_len]
            
            if len(atoms1) == 0:
                print("Warning: No CA atoms found for RMSD calculation")
                return float('inf')
            
            # Superimpose and calculate RMSD
            superimposer = Superimposer()
            superimposer.set_atoms(atoms1, atoms2)
            
            return superimposer.rms
            
        except Exception as e:
            print(f"Error calculating RMSD: {e}")
            return float('inf')
    
    def visualize_comparison(self, alphafold_path: str, esmfold_path: str, protein_name: str):
        """
        Create a simple visualization comparing the structures
        
        Args:
            alphafold_path: Path to AlphaFold PDB file
            esmfold_path: Path to ESMFold PDB file
            protein_name: Name of the protein
        """
        try:
            # Calculate RMSD
            rmsd = self.calculate_rmsd(alphafold_path, esmfold_path)
            
            # Load structures for coordinate extraction
            af_structure = self.parser.get_structure("alphafold", alphafold_path)
            esm_structure = self.parser.get_structure("esmfold", esmfold_path)
            
            # Extract CA coordinates
            af_coords = []
            esm_coords = []
            
            for model in af_structure:
                for chain in model:
                    for residue in chain:
                        if 'CA' in residue:
                            af_coords.append(residue['CA'].coord)
            
            for model in esm_structure:
                for chain in model:
                    for residue in chain:
                        if 'CA' in residue:
                            esm_coords.append(residue['CA'].coord)
            
            # Create comparison plot
            fig = plt.figure(figsize=(15, 5))
            
            # Plot 1: 3D scatter of AlphaFold
            ax1 = fig.add_subplot(131, projection='3d')
            if af_coords:
                af_coords = np.array(af_coords)
                ax1.scatter(af_coords[:, 0], af_coords[:, 1], af_coords[:, 2], 
                          c='blue', alpha=0.6, s=20)
            ax1.set_title(f'AlphaFold - {protein_name}')
            ax1.set_xlabel('X (Å)')
            ax1.set_ylabel('Y (Å)')
            ax1.set_zlabel('Z (Å)')
            
            # Plot 2: 3D scatter of ESMFold
            ax2 = fig.add_subplot(132, projection='3d')
            if esm_coords:
                esm_coords = np.array(esm_coords)
                ax2.scatter(esm_coords[:, 0], esm_coords[:, 1], esm_coords[:, 2], 
                          c='red', alpha=0.6, s=20)
            ax2.set_title(f'ESMFold - {protein_name}')
            ax2.set_xlabel('X (Å)')
            ax2.set_ylabel('Y (Å)')
            ax2.set_zlabel('Z (Å)')
            
            # Plot 3: Overlay comparison
            ax3 = fig.add_subplot(133, projection='3d')
            if af_coords is not None and len(af_coords) > 0:
                ax3.scatter(af_coords[:, 0], af_coords[:, 1], af_coords[:, 2], 
                          c='blue', alpha=0.6, s=20, label='AlphaFold')
            if esm_coords is not None and len(esm_coords) > 0:
                ax3.scatter(esm_coords[:, 0], esm_coords[:, 1], esm_coords[:, 2], 
                          c='red', alpha=0.6, s=20, label='ESMFold')
            ax3.set_title(f'Overlay (RMSD: {rmsd:.2f} Å)')
            ax3.set_xlabel('X (Å)')
            ax3.set_ylabel('Y (Å)')
            ax3.set_zlabel('Z (Å)')
            ax3.legend()
            
            plt.tight_layout()
            
            # Save plot
            plot_path = self.output_dir / f"{protein_name}_comparison.png"
            plt.savefig(plot_path, dpi=300, bbox_inches='tight')
            print(f"Comparison plot saved to: {plot_path}")
            
            plt.show()
            
        except Exception as e:
            print(f"Error creating visualization: {e}")
    
    def compare_proteins(self, uniprot_id: str, sequence: str, protein_name: str) -> Dict[str, Any]:
        """
        Complete comparison workflow
        
        Args:
            uniprot_id: UniProt accession number
            sequence: Protein sequence
            protein_name: Name for the protein
            
        Returns:
            Dictionary with comparison results
        """
        results = {
            'protein_name': protein_name,
            'uniprot_id': uniprot_id,
            'alphafold_path': None,
            'esmfold_path': None,
            'rmsd': None,
            'success': False
        }
        
        # Download AlphaFold structure
        alphafold_path = self.download_alphafold_structure(uniprot_id)
        if alphafold_path:
            results['alphafold_path'] = alphafold_path
        
        # Generate ESMFold structure
        esmfold_path = self.generate_esmfold_structure(sequence, protein_name)
        if esmfold_path:
            results['esmfold_path'] = esmfold_path
        
        # Compare if both structures are available
        if alphafold_path and esmfold_path:
            rmsd = self.calculate_rmsd(alphafold_path, esmfold_path)
            results['rmsd'] = rmsd
            results['success'] = True
            
            print(f"\nComparison Results for {protein_name}:")
            print(f"RMSD: {rmsd:.3f} Å")
            
            # Create visualization
            self.visualize_comparison(alphafold_path, esmfold_path, protein_name)
        
        return results


def main():
    """Example usage of the ProteinStructureComparator"""
    comparator = ProteinStructureComparator()
    
    # Example 1: Compare insulin (small protein)
    print("=" * 60)
    print("Example 1: Human Insulin")
    print("=" * 60)
    
    insulin_uniprot = "P01308"
    insulin_sequence = "MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKTRREAEDLQVGQVELGGGPGAGSLQPLALEGSLQKRGIVEQCCTSICSLYQLENYCN"
    
    results = comparator.compare_proteins(
        uniprot_id=insulin_uniprot,
        sequence=insulin_sequence,
        protein_name="human_insulin"
    )
    
    # Example 2: Alternative approach using just ESMFold (if AlphaFold fails)
    print("\n" + "=" * 60)
    print("Alternative: ESMFold-only prediction")
    print("=" * 60)
    
    # Small peptide sequence
    peptide_sequence = "MKWVTFISLLLLFSSAYSRGVFRRDAHKSEVAHRFKDLGEENFKALVLIAFAQYLQQCPFEDHVKLVNEVTEFAKTCVADESAENCDKSLHTLFGDKLCTVATLRETYGEMADCCAKQEPERNECFLQHKDDNPNLPRLVRPEVDVMCTAFHDNEETFLKKYLYEIARRHPYFYAPELLFFAKRYKAAFTECCQAADKAACLLPKLDELRDEGKASSAKQRLKCASLQKFGERAFKAWAVARLSQRFPKAEFAEVSKLVTDLTKVHTECCHGDLLECADDRADLAKYICENQDSISSKLKECCEKPLLEKSHCIAEVENDEMPADLPSLAADFVESKDVCKNYAEAKDVFLGMFLYEYARRHPDYSVVLLLRLAKTYETTLEKCCAAADPHECYAKVFDEFKPLVEEPQNLIKQNCELFEQLGEYKFQNALLVRYTKKVPQVSTPTLVEVSRNLGKVGSKCCKHPEAKRMPCAEDYLSVVLNQLCVLHEKTPVSDRVTKCCTESLVNRRPCFSALEVDETYVPKEFNAETFTFHADICTLSEKERQIKKQTALVELVKHKPKATKEQLKAVMDDFAAFVEKCCKADDKETCFAEEGKKLVAASQAALGL"
    
    esmfold_path = comparator.generate_esmfold_structure(peptide_sequence, "example_peptide")
    if esmfold_path:
        print(f"ESMFold structure generated: {esmfold_path}")


if __name__ == "__main__":
    main()
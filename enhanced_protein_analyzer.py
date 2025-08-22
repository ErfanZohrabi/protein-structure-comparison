#!/usr/bin/env python3
"""
Enhanced Protein Structure Comparison: AlphaFold vs ESMFold with 3D Visualization
"""

import os
import json
import requests
import warnings
from pathlib import Path
from typing import Optional, Tuple, Dict, Any, List
from dataclasses import dataclass
from datetime import datetime
import webbrowser

try:
    import numpy as np
    from Bio.PDB import PDBParser, Superimposer
    import matplotlib.pyplot as plt
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    import py3Dmol
except ImportError as e:
    print(f"Required packages missing: {e}")
    print("Install with: pip install biopython matplotlib numpy plotly py3Dmol")
    exit(1)

@dataclass
class ProteinInfo:
    """Data class to store protein information"""
    uniprot_id: str
    name: str
    full_name: str
    organism: str
    sequence: str
    length: int
    function: str
    keywords: List[str]
    molecular_weight: float = 0.0

class Enhanced3DProteinComparator:
    """Enhanced protein structure comparison with 3D visualization"""
    
    def __init__(self, output_dir: str = "protein_analysis"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.parser = PDBParser(QUIET=True)
        
        # Create subdirectories
        for subdir in ["structures", "visualizations", "reports"]:
            (self.output_dir / subdir).mkdir(exist_ok=True)
    
    def fetch_protein_info(self, uniprot_id: str) -> ProteinInfo:
        """Fetch protein information from UniProt API"""
        url = f"https://rest.uniprot.org/uniprotkb/{uniprot_id}.json"
        
        try:
            print(f"🔍 Fetching protein information for {uniprot_id}...")
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            # Extract basic information
            protein_name = data.get('proteinDescription', {}).get('recommendedName', {}).get('fullName', {}).get('value', 'Unknown')
            organism = data.get('organism', {}).get('scientificName', 'Unknown')
            sequence = data.get('sequence', {}).get('value', '')
            length = data.get('sequence', {}).get('length', 0)
            molecular_weight = data.get('sequence', {}).get('molWeight', 0)
            
            # Extract function
            function_comments = [comment.get('texts', [{}])[0].get('value', '') 
                               for comment in data.get('comments', []) 
                               if comment.get('commentType') == 'FUNCTION']
            function = function_comments[0] if function_comments else 'Function not available'
            
            # Extract keywords
            keywords = [kw.get('value', '') for kw in data.get('keywords', [])]
            
            return ProteinInfo(
                uniprot_id=uniprot_id,
                name=protein_name,
                full_name=protein_name,
                organism=organism,
                sequence=sequence,
                length=length,
                function=function,
                keywords=keywords,
                molecular_weight=molecular_weight
            )
            
        except Exception as e:
            print(f"❌ Error fetching protein info: {e}")
            return ProteinInfo(
                uniprot_id=uniprot_id, name="Unknown", full_name="Unknown",
                organism="Unknown", sequence="", length=0,
                function="Not available", keywords=[], molecular_weight=0.0
            )
    
    def download_alphafold_structure(self, uniprot_id: str) -> Optional[str]:
        """Download AlphaFold structure"""
        url = f"https://alphafold.ebi.ac.uk/files/AF-{uniprot_id}-F1-model_v4.pdb"
        output_path = self.output_dir / "structures" / f"alphafold_{uniprot_id}.pdb"
        
        try:
            print(f"📥 Downloading AlphaFold structure for {uniprot_id}...")
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            with open(output_path, 'w') as f:
                f.write(response.text)
            
            print(f"✅ AlphaFold structure saved to: {output_path}")
            return str(output_path)
            
        except Exception as e:
            print(f"❌ Error downloading AlphaFold structure: {e}")
            return None
    
    def create_mock_esmfold_structure(self, sequence: str, protein_name: str, uniprot_id: str = None) -> str:
        """Create a mock ESMFold structure for demonstration"""
        output_path = self.output_dir / "structures" / f"esmfold_{protein_name}.pdb"
        
        print(f"🔬 Creating mock ESMFold structure for {protein_name}...")
        
        # Try to read AlphaFold structure first to create a realistic mock
        if uniprot_id:
            alphafold_path = self.output_dir / "structures" / f"alphafold_{uniprot_id}.pdb"
        else:
            # Fallback: look for any AlphaFold file in the directory
            alphafold_files = list((self.output_dir / "structures").glob("alphafold_*.pdb"))
            if alphafold_files:
                alphafold_path = alphafold_files[0]
            else:
                alphafold_path = None
        
        if alphafold_path and alphafold_path.exists():
            print(f"Using AlphaFold structure as template: {alphafold_path}")
            try:
                # Read AlphaFold structure and create perturbed version
                af_structure = self.parser.get_structure("af_template", str(alphafold_path))
                
                with open(output_path, 'w') as f:
                    f.write("HEADER    ESMFOLD PREDICTION\n")
                    f.write("REMARK   Mock structure based on AlphaFold with perturbations\n")
                    f.write("REMARK   Realistic RMSD differences for demonstration\n")
                    
                    atom_id = 1
                    residue_count = 0
                    
                    for model in af_structure:
                        for chain in model:
                            for residue in chain:
                                residue_count += 1
                                if residue_count > 110:  # Limit for demo
                                    break
                                    
                                # Get residue info
                                res_id = residue.id[1]
                                res_name = residue.resname
                                
                                # Process each atom in the residue
                                for atom in residue:
                                    atom_name = atom.name
                                    coord = atom.coord
                                    
                                    # Add realistic perturbations (0.5-2.0 Å)
                                    # Different perturbation levels for different regions
                                    if 10 <= res_id <= 30:  # Structured region - small changes
                                        perturbation = np.random.normal(0, 0.8, 3)
                                    elif 50 <= res_id <= 70:  # Another structured region
                                        perturbation = np.random.normal(0, 0.8, 3)
                                    else:  # Loop regions - larger changes
                                        perturbation = np.random.normal(0, 1.5, 3)
                                    
                                    new_coord = coord + perturbation
                                    
                                    # Write atom record
                                    f.write(f"ATOM  {atom_id:5d}  {atom_name:<3} {res_name} A{res_id:4d}    "
                                           f"{new_coord[0]:8.3f}{new_coord[1]:8.3f}{new_coord[2]:8.3f}  1.00 50.00           {atom.element}\n")
                                    atom_id += 1
                                    
                                    # Only keep backbone atoms to avoid too many atoms
                                    if atom_name in ['N', 'CA', 'C', 'O']:
                                        continue
                                    elif atom_name == 'CB':  # Keep CB for side chains
                                        continue
                                    else:
                                        atom_id -= 1  # Don't include other side chain atoms
                    
                    f.write("END\n")
                
                print(f"✅ Mock ESMFold structure created from AlphaFold template: {output_path}")
                return str(output_path)
                
            except Exception as e:
                print(f"Warning: Could not use AlphaFold template: {e}")
        
        # Fallback to basic mock structure if AlphaFold not available
        print("Using basic mock structure generation")
        aa_map = {
            'A': 'ALA', 'R': 'ARG', 'N': 'ASN', 'D': 'ASP', 'C': 'CYS',
            'Q': 'GLN', 'E': 'GLU', 'G': 'GLY', 'H': 'HIS', 'I': 'ILE',
            'L': 'LEU', 'K': 'LYS', 'M': 'MET', 'F': 'PHE', 'P': 'PRO',
            'S': 'SER', 'T': 'THR', 'W': 'TRP', 'Y': 'TYR', 'V': 'VAL'
        }
        
        with open(output_path, 'w') as f:
            f.write("HEADER    ESMFOLD PREDICTION\n")
            f.write("REMARK   Basic mock structure for demonstration\n")
            
            atom_id = 1
            for i, aa in enumerate(sequence[:110]):
                aa_code = aa_map.get(aa, 'UNK')
                
                # Simple extended chain with small variations
                x = i * 3.8 + np.random.normal(0, 0.5)
                y = np.sin(i * 0.1) * 5 + np.random.normal(0, 0.5)
                z = np.cos(i * 0.1) * 5 + np.random.normal(0, 0.5)
                
                # Add backbone atoms
                for atom_name, offset in [('N', (-1, -1, -1)), ('CA', (0, 0, 0)), ('C', (1, 1, 1)), ('O', (1.5, 1.5, 1.5))]:
                    f.write(f"ATOM  {atom_id:5d}  {atom_name:<3} {aa_code} A{i+1:4d}    "
                           f"{x+offset[0]:8.3f}{y+offset[1]:8.3f}{z+offset[2]:8.3f}  1.00 50.00           {atom_name[0]}\n")
                    atom_id += 1
            
            f.write("END\n")
        
        print(f"✅ Mock ESMFold structure created: {output_path}")
        return str(output_path)
    
    def calculate_rmsd(self, structure1_path: str, structure2_path: str) -> float:
        """Calculate RMSD between structures"""
        try:
            structure1 = self.parser.get_structure("s1", structure1_path)
            structure2 = self.parser.get_structure("s2", structure2_path)
            
            atoms1, atoms2 = [], []
            
            # Extract CA atoms from both structures
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
            
            # Find minimum length for comparison
            min_len = min(len(atoms1), len(atoms2))
            if min_len == 0:
                print("Warning: No CA atoms found in structures")
                return float('inf')
            
            print(f"Found {len(atoms1)} CA atoms in structure 1, {len(atoms2)} in structure 2")
            print(f"Using {min_len} atoms for RMSD calculation")
            
            # Use only the overlapping residues
            atoms1 = atoms1[:min_len]
            atoms2 = atoms2[:min_len]
            
            # Calculate RMSD using superimposer
            superimposer = Superimposer()
            superimposer.set_atoms(atoms1, atoms2)
            rmsd = superimposer.rms
            
            print(f"Calculated RMSD: {rmsd:.3f} Å")
            return rmsd
            
        except Exception as e:
            print(f"Error calculating RMSD: {e}")
            print(f"Structure 1 path: {structure1_path}")
            print(f"Structure 2 path: {structure2_path}")
            
            # Try to provide more debugging info
            try:
                import os
                if os.path.exists(structure1_path):
                    print(f"Structure 1 exists, size: {os.path.getsize(structure1_path)} bytes")
                else:
                    print("Structure 1 does not exist")
                    
                if os.path.exists(structure2_path):
                    print(f"Structure 2 exists, size: {os.path.getsize(structure2_path)} bytes")
                else:
                    print("Structure 2 does not exist")
            except:
                pass
                
            return float('inf')
    
    def create_3d_visualization(self, alphafold_path: str, esmfold_path: str, 
                              protein_info: ProteinInfo, rmsd: float):
        """Create comprehensive 3D visualization"""
        try:
            print(f"Creating 3D visualization for {protein_info.name}...")
            
            # Load structures and extract coordinates
            af_structure = self.parser.get_structure("af", alphafold_path)
            esm_structure = self.parser.get_structure("esm", esmfold_path)
            
            af_coords, esm_coords, residue_nums = [], [], []
            
            # Extract CA coordinates from AlphaFold structure
            for model in af_structure:
                for chain in model:
                    for residue in chain:
                        if 'CA' in residue:
                            af_coords.append(residue['CA'].coord)
                            residue_nums.append(residue.id[1])
            
            # Extract CA coordinates from ESMFold structure  
            for model in esm_structure:
                for chain in model:
                    for residue in chain:
                        if 'CA' in residue:
                            esm_coords.append(residue['CA'].coord)
            
            print(f"AlphaFold coordinates: {len(af_coords)}, ESMFold coordinates: {len(esm_coords)}")
            
            if len(af_coords) == 0 or len(esm_coords) == 0:
                print("Warning: No coordinates found in one or both structures")
                return None
            
            af_coords = np.array(af_coords)
            # Ensure same length for comparison
            min_len = min(len(af_coords), len(esm_coords))
            esm_coords = np.array(esm_coords[:min_len])
            af_coords = af_coords[:min_len]
            residue_nums = residue_nums[:min_len]
            
            # Calculate per-residue distances
            distances = np.linalg.norm(af_coords - esm_coords, axis=1)
            
            # Create comprehensive visualization
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=('AlphaFold Structure', 'ESMFold Structure', 'Structural Overlay', 'Per-Residue Deviations'),
                specs=[[{"type": "scatter3d"}, {"type": "scatter3d"}],
                       [{"type": "scatter3d"}, {"type": "scatter"}]]
            )
            
            # Individual AlphaFold structure
            fig.add_trace(go.Scatter3d(
                x=af_coords[:, 0], y=af_coords[:, 1], z=af_coords[:, 2],
                mode='markers+lines', 
                marker=dict(size=4, color='blue', opacity=0.8),
                line=dict(color='blue', width=2),
                name='AlphaFold', 
                text=[f"Residue {num}" for num in residue_nums],
                hovertemplate="AlphaFold<br>Residue: %{text}<br>X: %{x:.2f}<br>Y: %{y:.2f}<br>Z: %{z:.2f}<extra></extra>"
            ), row=1, col=1)
            
            # Individual ESMFold structure
            fig.add_trace(go.Scatter3d(
                x=esm_coords[:, 0], y=esm_coords[:, 1], z=esm_coords[:, 2],
                mode='markers+lines', 
                marker=dict(size=4, color='red', opacity=0.8),
                line=dict(color='red', width=2),
                name='ESMFold', 
                text=[f"Residue {num}" for num in residue_nums],
                hovertemplate="ESMFold<br>Residue: %{text}<br>X: %{x:.2f}<br>Y: %{y:.2f}<br>Z: %{z:.2f}<extra></extra>"
            ), row=1, col=2)
            
            # Structural overlay
            fig.add_trace(go.Scatter3d(
                x=af_coords[:, 0], y=af_coords[:, 1], z=af_coords[:, 2],
                mode='lines', 
                line=dict(color='blue', width=3),
                name='AlphaFold', showlegend=False,
                hovertemplate="AlphaFold Backbone<extra></extra>"
            ), row=2, col=1)
            
            fig.add_trace(go.Scatter3d(
                x=esm_coords[:, 0], y=esm_coords[:, 1], z=esm_coords[:, 2],
                mode='lines', 
                line=dict(color='red', width=3),
                name='ESMFold', showlegend=False,
                hovertemplate="ESMFold Backbone<extra></extra>"
            ), row=2, col=1)
            
            # Per-residue difference plot
            fig.add_trace(go.Scatter(
                x=residue_nums, y=distances,
                mode='markers+lines',
                marker=dict(size=6, color=distances, colorscale='Viridis', 
                           colorbar=dict(title="Distance (Å)")),
                line=dict(color='rgba(0,0,0,0.3)', width=1),
                name='RMSD per residue',
                hovertemplate="Residue: %{x}<br>Deviation: %{y:.3f} Å<extra></extra>"
            ), row=2, col=2)
            
            # Update layout
            fig.update_layout(
                title={
                    'text': f"🧬 {protein_info.name} - Structure Comparison<br>"
                           f"<sub>UniProt: {protein_info.uniprot_id} | RMSD: {rmsd:.3f} Å | Length: {len(af_coords)} residues</sub>",
                    'x': 0.5,
                    'font': {'size': 16}
                },
                height=800,
                showlegend=True,
                font=dict(size=12)
            )
            
            # Update 3D scene properties
            scene_dict = dict(
                xaxis_title="X (Å)",
                yaxis_title="Y (Å)", 
                zaxis_title="Z (Å)",
                camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))
            )
            
            fig.update_scenes(scene_dict)
            
            # Update 2D plot
            fig.update_xaxes(title_text="Residue Number", row=2, col=2)
            fig.update_yaxes(title_text="Deviation (Å)", row=2, col=2)
            
            # Save and open
            output_path = self.output_dir / "visualizations" / f"{protein_info.uniprot_id}_3d_analysis.html"
            fig.write_html(str(output_path), include_plotlyjs='cdn')
            
            print(f"✅ 3D visualization saved: {output_path}")
            webbrowser.open(f"file://{output_path.absolute()}")
            
            return str(output_path)
            
        except Exception as e:
            print(f"❌ Error creating visualization: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def create_analysis_report(self, protein_info: ProteinInfo, rmsd: float) -> str:
        """Create HTML analysis report"""
        report_path = self.output_dir / "reports" / f"{protein_info.uniprot_id}_report.html"
        
        # Determine RMSD quality
        if rmsd < 2.0:
            rmsd_status = "🟢 Excellent Agreement"
            rmsd_color = "#27ae60"
        elif rmsd < 4.0:
            rmsd_status = "🟡 Moderate Agreement" 
            rmsd_color = "#f39c12"
        else:
            rmsd_status = "🔴 Significant Differences"
            rmsd_color = "#e74c3c"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Protein Analysis: {protein_info.name}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                          color: white; padding: 30px; border-radius: 15px; margin-bottom: 30px; }}
                .section {{ background: #f8f9fa; padding: 20px; margin-bottom: 20px; border-radius: 10px; }}
                .rmsd {{ font-size: 2em; color: {rmsd_color}; font-weight: bold; }}
                .info-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }}
                .sequence {{ font-family: monospace; background: #e9ecef; padding: 15px; 
                           border-radius: 5px; word-break: break-all; }}
                table {{ width: 100%; border-collapse: collapse; }}
                th, td {{ border: 1px solid #dee2e6; padding: 12px; text-align: left; }}
                th {{ background-color: #e9ecef; font-weight: bold; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🧬 Protein Structure Analysis</h1>
                <h2>{protein_info.name}</h2>
                <p><strong>UniProt ID:</strong> {protein_info.uniprot_id}</p>
                <p><strong>Organism:</strong> {protein_info.organism}</p>
            </div>
            
            <div class="section">
                <h3>📊 Structural Comparison Results</h3>
                <div class="info-grid">
                    <div>
                        <h4>RMSD Analysis</h4>
                        <p class="rmsd">{rmsd:.3f} Å</p>
                        <p style="color: {rmsd_color}; font-weight: bold;">{rmsd_status}</p>
                        <p><strong>Interpretation:</strong></p>
                        <ul>
                            <li>&lt; 2.0 Å: Very similar structures</li>
                            <li>2.0-4.0 Å: Moderately similar</li>
                            <li>&gt; 4.0 Å: Significant differences</li>
                        </ul>
                    </div>
                    <div>
                        <h4>Protein Properties</h4>
                        <table>
                            <tr><th>Property</th><th>Value</th></tr>
                            <tr><td>Length</td><td>{protein_info.length} residues</td></tr>
                            <tr><td>Molecular Weight</td><td>{protein_info.molecular_weight:.1f} Da</td></tr>
                            <tr><td>Keywords</td><td>{', '.join(protein_info.keywords[:5])}</td></tr>
                        </table>
                    </div>
                </div>
            </div>
            
            <div class="section">
                <h3>🔬 Functional Information</h3>
                <p><strong>Function:</strong> {protein_info.function}</p>
            </div>
            
            <div class="section">
                <h3>🧬 Sequence Information</h3>
                <p><strong>Amino Acid Sequence ({protein_info.length} residues):</strong></p>
                <div class="sequence">
                    {protein_info.sequence[:500]}{'...' if len(protein_info.sequence) > 500 else ''}
                </div>
            </div>
            
            <div class="section">
                <h3>⚙️ Methodology</h3>
                <div class="info-grid">
                    <div>
                        <h4>AlphaFold</h4>
                        <ul>
                            <li>Uses Multiple Sequence Alignments</li>
                            <li>Template-based modeling</li>
                            <li>Higher accuracy</li>
                            <li>Computationally intensive</li>
                        </ul>
                    </div>
                    <div>
                        <h4>ESMFold</h4>
                        <ul>
                            <li>Language model approach</li>
                            <li>Single sequence input</li>
                            <li>Faster predictions</li>
                            <li>Good for novel sequences</li>
                        </ul>
                    </div>
                </div>
            </div>
            
            <p><em>Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</em></p>
        </body>
        </html>
        """
        
        with open(report_path, 'w') as f:
            f.write(html_content)
        
        print(f"✅ Analysis report saved: {report_path}")
        webbrowser.open(f"file://{report_path.absolute()}")
        return str(report_path)
    
    def compare_protein_structures(self, uniprot_id: str, protein_name: str = None):
        """Complete protein structure comparison workflow"""
        print(f"\n🚀 Starting protein structure comparison for {uniprot_id}")
        print("=" * 60)
        
        # 1. Fetch protein information
        protein_info = self.fetch_protein_info(uniprot_id)
        if protein_name:
            protein_info.name = protein_name
        
        print(f"📋 Protein: {protein_info.name} ({protein_info.length} residues)")
        print(f"🔬 Organism: {protein_info.organism}")
        
        # 2. Download AlphaFold structure
        alphafold_path = self.download_alphafold_structure(uniprot_id)
        if not alphafold_path:
            print("❌ Cannot proceed without AlphaFold structure")
            return None
        
        # 3. Create mock ESMFold structure (replace with real ESMFold in production)
        esmfold_path = self.create_mock_esmfold_structure(protein_info.sequence, protein_info.name, uniprot_id)
        
        # 4. Calculate RMSD
        rmsd = self.calculate_rmsd(alphafold_path, esmfold_path)
        print(f"📊 RMSD: {rmsd:.3f} Å")
        
        # 5. Create visualizations
        viz_path = self.create_3d_visualization(alphafold_path, esmfold_path, protein_info, rmsd)
        
        # 6. Generate report
        report_path = self.create_analysis_report(protein_info, rmsd)
        
        print("\n✅ Analysis complete!")
        print(f"📁 Results saved in: {self.output_dir}")
        
        return {
            'protein_info': protein_info,
            'alphafold_path': alphafold_path,
            'esmfold_path': esmfold_path,
            'rmsd': rmsd,
            'visualization_path': viz_path,
            'report_path': report_path
        }

def main():
    """Example usage"""
    comparator = Enhanced3DProteinComparator()
    
    # Example proteins to analyze
    proteins = [
        {"uniprot_id": "P01308", "name": "Human Insulin"},
        {"uniprot_id": "P61626", "name": "Lysozyme"},
        {"uniprot_id": "P02768", "name": "Serum Albumin"}
    ]
    
    print("🧬 Enhanced Protein Structure Comparison Tool")
    print("=" * 50)
    
    for i, protein in enumerate(proteins, 1):
        print(f"\n[{i}/{len(proteins)}] Analyzing {protein['name']}...")
        result = comparator.compare_protein_structures(
            protein['uniprot_id'], 
            protein['name']
        )
        
        if result:
            print(f"✅ {protein['name']} analysis completed")
        else:
            print(f"❌ {protein['name']} analysis failed")

if __name__ == "__main__":
    main()
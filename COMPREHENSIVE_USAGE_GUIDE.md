# 📚 Comprehensive Usage Guide - Protein Structure Comparison Tool

## 🎯 Overview

This guide provides detailed instructions for using every feature of the Protein Structure Comparison Tool. Whether you're a researcher, student, or developer, this guide will help you maximize the tool's capabilities.

## 📋 Table of Contents

1. [Quick Start](#-quick-start)
2. [Command-Line Interface (CLI)](#-command-line-interface-cli)
3. [Web Interface](#-web-interface)
4. [Analysis Types](#-analysis-types)
5. [File Formats & Outputs](#-file-formats--outputs)
6. [Advanced Features](#-advanced-features)
7. [Troubleshooting](#-troubleshooting)
8. [Best Practices](#-best-practices)
9. [Educational Examples](#-educational-examples)
10. [Integration Guide](#-integration-guide)

---

## 🚀 Quick Start

### Installation & Setup
```bash
# Clone or navigate to the project directory
cd /path/to/protein_comparison

# Install dependencies
pip install -r requirements.txt

# Quick test - analyze insulin
python protein_cli.py analyze P01308
```

### 30-Second Demo
```bash
# 1. Analyze a protein
python protein_cli.py analyze P01308 --name "Human Insulin"

# 2. Start web interface
python protein_cli.py server

# 3. Open browser to http://localhost:5001
```

---

## 💻 Command-Line Interface (CLI)

### Basic Commands

#### 1. Single Protein Analysis
```bash
# Analyze by UniProt ID
python protein_cli.py analyze P01308

# With custom name
python protein_cli.py analyze P01308 --name "Human Insulin"

# Specify output directory
python protein_cli.py analyze P01308 --output my_results/
```

#### 2. Advanced Analysis
```bash
# Run advanced analysis with homology search
python protein_cli.py advanced P01308

# Advanced analysis with custom output
python protein_cli.py advanced P01308 --output advanced_results/
```

#### 3. Batch Processing
```bash
# Create example protein list
python protein_cli.py create-example

# Run batch analysis
python protein_cli.py batch example_proteins.txt

# Batch with custom output directory
python protein_cli.py batch my_proteins.txt --output batch_results/
```

#### 4. Web Server
```bash
# Start on default port (5001)
python protein_cli.py server

# Start on custom port
python protein_cli.py server --port 8080

# Start with custom host
python protein_cli.py server --host 0.0.0.0 --port 8080
```

#### 5. Interactive Mode
```bash
# Enter interactive mode
python protein_cli.py interactive

# Follow the prompts for guided analysis
```

### CLI Examples by Use Case

#### Research Workflow
```bash
# 1. Analyze key proteins individually
python protein_cli.py analyze P01308 --name "Insulin"
python protein_cli.py analyze P61626 --name "Lysozyme"

# 2. Run advanced analysis for detailed insights
python protein_cli.py advanced P01308

# 3. Create a protein list for your study
echo -e "P01308\tInsulin\nP61626\tLysozyme\nP68871\tHemoglobin" > my_study.txt

# 4. Batch process all proteins
python protein_cli.py batch my_study.txt --output study_results/
```

#### Educational Demo
```bash
# Create diverse protein examples
python protein_cli.py create-example

# Analyze each type step by step
python protein_cli.py analyze P01308  # Hormone
python protein_cli.py analyze P61626  # Enzyme
python protein_cli.py analyze P68871  # Transport protein

# Show students the web interface
python protein_cli.py server --port 8080
```

#### High-Throughput Analysis
```bash
# Prepare large protein list
cat > large_study.txt << EOF
P01308	Human Insulin
P61626	Lysozyme
P68871	Hemoglobin β
P02768	Serum Albumin
P04637	p53 Tumor Suppressor
P01009	Alpha-1-antitrypsin
P02787	Transferrin
P01023	Alpha-2-macroglobulin
EOF

# Run batch analysis
python protein_cli.py batch large_study.txt --output high_throughput/
```

---

## 🌐 Web Interface

### Accessing the Web Interface

1. **Start the Server**
   ```bash
   python protein_cli.py server
   ```

2. **Open Browser**
   - Navigate to `http://localhost:5001`
   - Interface opens automatically

### Web Interface Features

#### 1. **3D Protein Viewer**
- Enter UniProt ID (e.g., P01308)
- Click "Analyze Protein" 
- View side-by-side 3D structures
- Interactive controls:
  - **Cartoon**: Standard protein visualization
  - **Surface**: Molecular surface representation
  - **Stick**: Detailed atomic bonds
  - **Reset**: Return to default view

#### 2. **Feature Navigation**
- **💻 CLI**: Documentation and command examples
- **📚 Documentation**: Usage guides and tutorials
- **🔬 3D Viewer**: Interactive protein visualization
- **📊 Results**: Analysis outputs and reports

#### 3. **Real-time Analysis**
- Live protein information retrieval
- Dynamic 3D structure loading
- Automatic RMSD calculation
- Advanced evolutionary analysis

### Web Interface Examples

#### Basic Analysis Workflow
1. Open web interface: `http://localhost:5001`
2. Click "🔬 3D Viewer" tab
3. Enter "P01308" in search box
4. Click "Analyze Protein"
5. Wait for structures to load
6. Explore using different visualization styles
7. Review analysis results below viewers

#### Educational Demonstration
1. Start server: `python protein_cli.py server --port 8080`
2. Share URL with students: `http://localhost:8080`
3. Demonstrate with different protein types:
   - P01308 (Small hormone - Insulin)
   - P61626 (Enzyme - Lysozyme)
   - P68871 (Transport - Hemoglobin)
4. Show different visualization styles
5. Explain RMSD values and their meaning

---

## 🔬 Analysis Types

### 1. Basic Structure Comparison

**What it does:**
- Downloads AlphaFold structure
- Generates ESMFold prediction
- Calculates RMSD between structures
- Creates 3D visualizations

**When to use:**
- Quick protein analysis
- Structure validation
- Educational demonstrations

**Example:**
```bash
python protein_cli.py analyze P01308
```

**Output:**
- RMSD value and quality assessment
- 3D visualization HTML file
- Comprehensive analysis report

### 2. Advanced Analysis

**What it does:**
- All basic analysis features
- Homology search using MMseqs2
- Evolutionary conservation analysis
- Functional prediction
- Phylogenetic distribution

**When to use:**
- Research projects
- Deep protein characterization
- Evolutionary studies

**Example:**
```bash
python protein_cli.py advanced P01308
```

**Output:**
- Extended analysis with conservation scores
- Homolog statistics
- Ortholog/paralog classification
- Functional predictions

### 3. Batch Processing

**What it does:**
- Processes multiple proteins automatically
- Generates individual reports for each protein
- Creates summary statistics
- Optimizes for high-throughput analysis

**When to use:**
- Large-scale studies
- Comparative genomics
- Systematic protein characterization

**Example:**
```bash
python protein_cli.py batch protein_list.txt
```

**Output:**
- Individual analysis files for each protein
- Batch summary JSON file
- Consolidated statistics

---

## 📁 File Formats & Outputs

### Input Formats

#### Protein List File Format
```
# Comments start with #
# Format: UniProt_ID[TAB]Name (optional)

P01308	Human Insulin
P61626	Lysozyme  
P68871	Hemoglobin β
P02768	Serum Albumin
```

#### Command-Line Arguments
```bash
# UniProt ID (required)
python protein_cli.py analyze P01308

# With optional name
python protein_cli.py analyze P01308 --name "Custom Protein Name"

# With output directory
python protein_cli.py analyze P01308 --output results/
```

### Output Directory Structure

```
protein_analysis/
├── structures/                    # PDB structure files
│   ├── alphafold_P01308.pdb      # Downloaded AlphaFold structure
│   └── esmfold_Insulin.pdb       # Generated ESMFold structure
├── visualizations/               # Interactive 3D plots
│   └── P01308_3d_analysis.html   # Plotly 3D visualization
├── reports/                      # Analysis reports
│   └── P01308_report.html        # Comprehensive HTML report
└── batch_summary.json            # Batch analysis summary
```

### Understanding Output Files

#### 1. **3D Visualization** (`*_3d_analysis.html`)
- Interactive 3D molecular plots
- Side-by-side structure comparison
- Per-residue difference analysis
- Color-coded similarity mapping
- Rotation and zoom controls

#### 2. **Analysis Report** (`*_report.html`)
- Protein information summary
- Structural comparison results
- Methodology explanation
- Quality assessment
- Professional formatting

#### 3. **Structure Files** (`*.pdb`)
- Standard PDB format
- Compatible with PyMOL, ChimeraX
- Contains atomic coordinates
- Can be used for further analysis

#### 4. **Batch Summary** (`batch_summary.json`)
```json
{
  "total_proteins": 5,
  "successful_analyses": 5,
  "failed_analyses": 0,
  "average_rmsd": 2.193,
  "analysis_date": "2024-01-15T10:30:00",
  "proteins": [
    {
      "uniprot_id": "P01308",
      "name": "Human Insulin",
      "rmsd": 2.152,
      "quality": "Good",
      "length": 110
    }
  ]
}
```

---

## 🎯 Advanced Features

### 1. Homology Search & Evolutionary Analysis

**Capabilities:**
- MMseqs2-based homology search
- Conservation score calculation
- Ortholog/paralog identification
- Phylogenetic distribution analysis

**Usage:**
```bash
python protein_cli.py advanced P01308
```

**Interpretation:**
- **Conservation Score > 0.7**: Highly conserved (critical function)
- **Conservation Score 0.3-0.7**: Moderately conserved (important function)
- **Conservation Score < 0.3**: Poorly conserved (specialized/recent)

### 2. Custom Visualization Styles

**Available Styles:**
- **Cartoon**: Standard protein backbone representation
- **Surface**: Molecular surface showing protein shape
- **Stick**: Detailed atomic bond visualization

**Web Interface Control:**
- Use style buttons in each viewer
- Real-time style switching
- Reset view functionality

### 3. Quality Assessment

**RMSD Interpretation:**
- **< 2.0 Å** 🟢 **Excellent**: Structures are very similar
- **2.0-4.0 Å** 🟡 **Good**: Some structural differences
- **> 4.0 Å** 🔴 **Poor**: Significant structural differences

**Factors Affecting Quality:**
- Protein size and complexity
- Structural flexibility
- Prediction algorithm accuracy
- Experimental structure availability

---

## 🔧 Troubleshooting

### Common Issues & Solutions

#### 1. **"PyMMseqs not available" Warning**
```bash
# Install PyMMseqs for advanced analysis
pip install pymmseqs

# Alternative: Use conda
conda install -c conda-forge mmseqs2
```

#### 2. **Port Already in Use**
```bash
# Check what's using the port
lsof -ti:5001

# Kill the process
lsof -ti:5001 | xargs kill -9

# Or use a different port
python protein_cli.py server --port 8080
```

#### 3. **Network/Download Issues**
```bash
# Check internet connection
curl -I https://alphafold.ebi.ac.uk/

# Verify UniProt access
curl -I https://www.uniprot.org/uniprot/P01308.json
```

#### 4. **Missing Dependencies**
```bash
# Reinstall requirements
pip install -r requirements.txt

# Check specific packages
python -c "import plotly, biopython; print('OK')"
```

#### 5. **Browser Not Opening Automatically**
- Manually navigate to `http://localhost:5001`
- Check if firewall is blocking the connection
- Try different port: `--port 8080`

### Performance Optimization

#### For Large Proteins (>500 residues)
- Analysis may take longer
- Consider using `--output` to specify faster storage
- Monitor system memory usage

#### For Batch Processing
- Process proteins in smaller batches
- Use specific output directories
- Monitor disk space for large studies

---

## ✨ Best Practices

### 1. **Research Workflow**
```bash
# 1. Start with basic analysis
python protein_cli.py analyze P01308

# 2. If promising, run advanced analysis
python protein_cli.py advanced P01308

# 3. For multiple proteins, prepare batch file
echo -e "P01308\tInsulin\nP61626\tLysozyme" > study.txt

# 4. Run batch analysis
python protein_cli.py batch study.txt --output research_results/
```

### 2. **File Organization**
```bash
# Create project-specific directories
mkdir my_protein_study
cd my_protein_study

# Run analysis with organized output
python protein_cli.py analyze P01308 --output insulin_analysis/
python protein_cli.py analyze P61626 --output lysozyme_analysis/
```

### 3. **Quality Control**
- Always check RMSD values
- Review 3D visualizations manually
- Compare with known structures when possible
- Document any anomalies

### 4. **Performance Tips**
- Use specific output directories for organization
- Process large batches during off-peak hours
- Keep backup copies of important results
- Regular cleanup of temporary files

---

## 🎓 Educational Examples

### Example 1: Protein Types Comparison
```bash
# Analyze different protein types
python protein_cli.py analyze P01308 --name "Hormone (Insulin)"
python protein_cli.py analyze P61626 --name "Enzyme (Lysozyme)"
python protein_cli.py analyze P68871 --name "Transport (Hemoglobin)"

# Compare their characteristics in the reports
```

### Example 2: Evolutionary Study
```bash
# Compare related proteins
python protein_cli.py advanced P01308  # Human insulin
python protein_cli.py advanced P01315  # Insulin-like growth factor
python protein_cli.py advanced P01317  # Relaxin

# Compare conservation scores and homology results
```

### Example 3: Structure-Function Workshop
```bash
# 1. Start web server for interactive demo
python protein_cli.py server --port 8080

# 2. Demo different proteins with students:
#    - P01308: Small, stable hormone
#    - P61626: Enzyme with active site
#    - P02768: Large, flexible transport protein

# 3. Show how structure relates to function
```

---

## 🔗 Integration Guide

### Using in Python Scripts
```python
from enhanced_protein_analyzer import Enhanced3DProteinComparator

# Initialize
comparator = Enhanced3DProteinComparator()

# Analyze protein
result = comparator.compare_protein_structures("P01308")
print(f"RMSD: {result['rmsd']:.3f} Å")
print(f"Quality: {result['quality_assessment']}")
```

### Integration with Jupyter Notebooks
```python
# In a Jupyter cell
import subprocess
import json

# Run analysis
result = subprocess.run([
    'python', 'protein_cli.py', 'analyze', 'P01308'
], capture_output=True, text=True)

# Display results
print(result.stdout)
```

### API Usage (Web Server)
```python
import requests

# Start server first: python protein_cli.py server

# Make API request
response = requests.post('http://localhost:5001/api/advanced_analysis', 
                        json={'uniprot_id': 'P01308', 'sequence': 'FVNQHLCGS...'})
data = response.json()
print(f"Conservation score: {data['evolutionary_analysis']['conservation_score']}")
```

---

## 📊 Output Examples

### CLI Output Example
```
🔬 Analyzing protein: P01308
==================================================

🚀 Starting protein structure comparison for P01308
============================================================
🔍 Fetching protein information for P01308...
📋 Protein: Human Insulin (110 residues)
🔬 Organism: Homo sapiens
📥 Downloading AlphaFold structure for P01308...
✅ AlphaFold structure saved to: protein_analysis/structures/alphafold_P01308.pdb
📊 RMSD: 2.056 Å
✅ 3D visualization saved: protein_analysis/visualizations/P01308_3d_analysis.html
✅ Analysis report saved: protein_analysis/reports/P01308_report.html

📊 Analysis Results for Human Insulin
----------------------------------------
UniProt ID: P01308
Organism: Homo sapiens
Length: 110 residues
RMSD: 2.056 Å
Quality: 🟡 Good
```

### Web Interface Display
- Clean, modern interface with tabbed navigation
- Real-time 3D molecular viewers
- Interactive controls for visualization styles
- Comprehensive protein information display
- Professional analysis results presentation

---

## 🆘 Support & Resources

### Getting Help
1. Check this comprehensive guide
2. Review the main README.md
3. Examine example output files
4. Test with known proteins (P01308, P61626)

### Useful UniProt IDs for Testing
| ID | Protein | Type | Size | Notes |
|----|---------|------|------|-------|
| P01308 | Human Insulin | Hormone | Small (110) | Good for testing |
| P61626 | Lysozyme | Enzyme | Medium (148) | Classic enzyme |
| P68871 | Hemoglobin β | Transport | Medium (147) | Oxygen transport |
| P02768 | Serum Albumin | Transport | Large (609) | Blood protein |
| P04637 | p53 | Tumor Suppressor | Large (393) | Cancer research |

### Scientific Background
- **RMSD**: Root Mean Square Deviation of atomic positions
- **AlphaFold**: AI-based protein structure prediction (DeepMind)
- **ESMFold**: Language model-based structure prediction (Meta)
- **UniProt**: Universal protein resource database
- **PDB**: Protein Data Bank format for structure files

---

**🎉 You're now ready to use all features of the Protein Structure Comparison Tool!**

This comprehensive guide covers everything from basic usage to advanced research applications. Whether you're doing educational demonstrations, research projects, or large-scale protein studies, these examples and best practices will help you get the most out of the tool.
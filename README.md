# 🧬 Protein Structure Comparison Tool

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![3Dmol.js](https://img.shields.io/badge/3Dmol.js-latest-orange.svg)](https://3dmol.csb.pitt.edu/)

A comprehensive bioinformatics tool for comparing protein 3D structure predictions from **AlphaFold** and **ESMFold**. Features an interactive web interface, command-line tools, and advanced evolutionary analysis capabilities.

![Protein Viewer Interface](https://via.placeholder.com/800x400/667eea/ffffff?text=Interactive+3D+Protein+Viewer)

## ✨ Features

- 🔬 **Interactive 3D Visualization** - Side-by-side molecular viewers using 3Dmol.js
- 📊 **RMSD Calculation** - Quantitative structural similarity analysis  
- 🌐 **Modern Web Interface** - Responsive design with real-time analysis
- 💻 **Comprehensive CLI** - Full command-line interface for automation
- 🧬 **Evolutionary Analysis** - Homology search and conservation scoring
- ⚡ **Batch Processing** - Analyze multiple proteins efficiently
- 📈 **Professional Reports** - Publication-ready HTML reports
- 🔍 **UniProt Integration** - Automatic protein metadata retrieval

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/protein-structure-comparison.git
cd protein-structure-comparison

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Launch Web Interface

```bash
# Start the web server
python protein_cli.py server

# Open browser to http://localhost:5001
```

### Quick Analysis

```bash
# Analyze a single protein
python protein_cli.py analyze P01308

# Advanced analysis with homology
python protein_cli.py advanced P01308

# Batch processing
python protein_cli.py batch proteins.txt
```

## 💻 Command Line Interface

```bash
# Get help
python protein_cli.py --help

# Single protein analysis
python protein_cli.py analyze P01308 --name "Human Insulin"

# Advanced analysis with evolutionary data
python protein_cli.py advanced P01308

# Create example protein list
python protein_cli.py create-example

# Batch process multiple proteins
python protein_cli.py batch example_proteins.txt --output results/

# Interactive mode
python protein_cli.py interactive

# Launch web server on custom port
python protein_cli.py server --port 8080
```

## 🌐 Web Interface

The web interface provides:
- **🔬 3D Viewer**: Interactive molecular visualization with multiple rendering modes
- **💻 CLI Guide**: Built-in documentation with copy-to-clipboard commands  
- **📚 Documentation**: Comprehensive user guides and examples
- **❓ Help System**: Built-in tutorials and troubleshooting

## 📊 Example Analysis

```python
from enhanced_protein_analyzer import Enhanced3DProteinComparator

# Initialize analyzer
comparator = Enhanced3DProteinComparator()

# Analyze protein
result = comparator.compare_protein_structures("P01308")
print(f"RMSD: {result['rmsd']:.3f} Å")
print(f"Quality: {result['quality_assessment']}")
```

## 🧬 Scientific Background

This tool compares protein structures from two state-of-the-art AI prediction models:

- **AlphaFold** (DeepMind): Uses multiple sequence alignments and deep learning
- **ESMFold** (Meta): Uses protein language models for single-sequence prediction

The comparison provides insights into:
- Structural similarity and differences
- Prediction confidence and reliability
- Evolutionary conservation patterns
- Functional implications

## 📁 Project Structure

```
protein-structure-comparison/
├── protein_cli.py              # Main CLI interface
├── backend_server.py           # Flask web server
├── enhanced_protein_analyzer.py # Core analysis engine
├── advanced_protein_analyzer.py # Evolutionary analysis
├── index.html                  # Web interface
├── css/styles.css             # Interface styling
├── js/app.js                  # Frontend functionality
├── requirements.txt           # Python dependencies
├── protein_analysis/          # Generated results
│   ├── structures/           # PDB files
│   ├── visualizations/       # 3D plots
│   └── reports/             # Analysis reports
└── documentation/            # User guides
```

## 🔬 Analysis Output

### RMSD Interpretation
- **< 2.0 Å** 🟢 **Excellent** - Structures are very similar
- **2.0-4.0 Å** 🟡 **Good** - Some structural differences  
- **> 4.0 Å** 🔴 **Poor** - Significant structural differences

### Generated Files
- **PDB Structures**: AlphaFold and ESMFold coordinate files
- **3D Visualizations**: Interactive HTML plots with Plotly
- **Analysis Reports**: Comprehensive HTML summaries
- **Batch Summaries**: JSON files with statistics

## 🛠️ Technology Stack

- **Backend**: Python 3.8+, Flask, BioPython
- **Frontend**: HTML5, CSS3, JavaScript, 3Dmol.js
- **Visualization**: Plotly, 3Dmol.js for molecular graphics
- **Analysis**: PyMMseqs2 for homology search
- **Data Sources**: UniProt, AlphaFold Database

## 📦 Dependencies

Core requirements:
- `biopython>=1.79` - Structural biology utilities
- `flask>=2.0.0` - Web framework
- `plotly>=5.10.0` - Interactive visualizations
- `requests>=2.28.0` - HTTP requests
- `numpy>=1.21.0` - Scientific computing

Optional for advanced features:
- `pymmseqs>=1.0.0` - Homology search
- `torch>=2.0.0` - Deep learning backend
- `fair-esm>=2.0.0` - ESMFold models

## 🎯 Use Cases

### Research Applications
- **Structural Biology**: Compare AI predictions with experimental structures
- **Drug Discovery**: Analyze target protein conformations
- **Protein Engineering**: Validate designed protein structures
- **Evolutionary Studies**: Investigate structure-function relationships

### Educational Applications  
- **Bioinformatics Training**: Hands-on protein analysis experience
- **Structural Biology Courses**: Interactive molecular visualization
- **Research Methods**: Learn modern computational approaches

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **AlphaFold Team** (DeepMind) - Revolutionary protein structure prediction
- **ESMFold Team** (Meta) - Language model-based structure prediction  
- **3Dmol.js** - Excellent molecular visualization library
- **UniProt** - Comprehensive protein database
- **PyMMseqs2** - Ultra-fast sequence search tools

## 📞 Support

- 📖 **Documentation**: See [COMPREHENSIVE_USAGE_GUIDE.md](COMPREHENSIVE_USAGE_GUIDE.md)
- 🐛 **Issues**: Report bugs via GitHub Issues
- 💬 **Discussions**: Join GitHub Discussions for questions
- 📧 **Contact**: [Your Email] for collaboration inquiries

## 🔄 Version History

- **v1.0.0** - Initial release with web interface and CLI
- **v1.1.0** - Added evolutionary analysis and batch processing
- **v1.2.0** - Enhanced UI and comprehensive documentation

---

**⭐ If you find this tool useful, please give it a star on GitHub!**
#!/usr/bin/env python3
"""
🧬 Protein Structure Comparison CLI Tool
=============================================

A comprehensive command-line interface for protein structure analysis,
comparison, and visualization. Supports both AlphaFold vs ESMFold comparisons
and advanced bioinformatics analysis.

Features:
- Single protein analysis
- Batch protein processing
- Web server launch
- Interactive mode
- Advanced homology search
- 3D visualization generation
- Report generation

Usage:
    python protein_cli.py --help
    python protein_cli.py analyze P01308
    python protein_cli.py batch proteins.txt
    python protein_cli.py server
    python protein_cli.py interactive
"""

import argparse
import sys
import os
import json
import subprocess
import signal
import time
from pathlib import Path
from typing import List, Dict, Optional

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from enhanced_protein_analyzer import Enhanced3DProteinComparator
    from advanced_protein_analyzer import AdvancedProteinAnalyzer
except ImportError as e:
    print(f"❌ Error importing required modules: {e}")
    print("Make sure you're in the correct directory and have installed dependencies")
    sys.exit(1)

class ProteinCLI:
    """Comprehensive CLI for protein structure analysis"""
    
    def __init__(self):
        self.comparator = Enhanced3DProteinComparator()
        self.advanced_analyzer = AdvancedProteinAnalyzer()
        self.server_process = None
        
    def analyze_single_protein(self, uniprot_id: str, protein_name: str = None, 
                             output_dir: str = None, advanced: bool = False) -> Dict:
        """Analyze a single protein"""
        print(f"\n🔬 Analyzing protein: {uniprot_id}")
        print("=" * 50)
        
        try:
            # Set output directory if specified
            if output_dir:
                self.comparator.output_dir = Path(output_dir)
                self.comparator.output_dir.mkdir(exist_ok=True)
                for subdir in ["structures", "visualizations", "reports"]:
                    (self.comparator.output_dir / subdir).mkdir(exist_ok=True)
            
            # Basic analysis
            result = self.comparator.compare_protein_structures(uniprot_id, protein_name)
            
            if not result:
                print(f"❌ Failed to analyze {uniprot_id}")
                return None
            
            # Advanced analysis if requested
            if advanced:
                print(f"\n🧬 Running advanced analysis for {uniprot_id}...")
                protein_info = self.advanced_analyzer.fetch_protein_info(uniprot_id)
                homologs = self.advanced_analyzer.perform_homology_search(
                    protein_info['sequence'], uniprot_id
                )
                evolutionary_analysis = self.advanced_analyzer.analyze_evolutionary_conservation(homologs)
                
                result['advanced_analysis'] = {
                    'homologs': len(homologs),
                    'conservation_score': evolutionary_analysis.conservation_score,
                    'orthologs': evolutionary_analysis.ortholog_count,
                    'paralogs': evolutionary_analysis.paralog_count
                }
            
            # Display results
            self._display_results(result)
            
            return result
            
        except Exception as e:
            print(f"❌ Error analyzing {uniprot_id}: {e}")
            return None
    
    def batch_analyze(self, protein_file: str, output_dir: str = None, 
                     advanced: bool = False) -> List[Dict]:
        """Analyze multiple proteins from file"""
        print(f"\n📄 Batch analysis from: {protein_file}")
        print("=" * 50)
        
        try:
            proteins = self._load_protein_list(protein_file)
            results = []
            
            print(f"Found {len(proteins)} proteins to analyze")
            
            for i, protein in enumerate(proteins, 1):
                print(f"\n[{i}/{len(proteins)}] Processing {protein['id']}...")
                
                result = self.analyze_single_protein(
                    protein['id'], 
                    protein.get('name'), 
                    output_dir, 
                    advanced
                )
                
                if result:
                    results.append(result)
                    print(f"✅ {protein['id']} completed")
                else:
                    print(f"❌ {protein['id']} failed")
            
            # Generate summary report
            self._generate_batch_summary(results, output_dir)
            
            return results
            
        except Exception as e:
            print(f"❌ Error in batch analysis: {e}")
            return []
    
    def launch_web_server(self, port: int = 5001, debug: bool = False):
        """Launch the web server"""
        print(f"\n🌐 Launching web server on port {port}...")
        print("=" * 50)
        
        try:
            # Kill any existing process on the port
            os.system(f"lsof -ti:{port} | xargs kill -9 2>/dev/null")
            
            # Change to project directory
            os.chdir(os.path.dirname(os.path.abspath(__file__)))
            
            # Set environment variables
            env = os.environ.copy()
            env['FLASK_PORT'] = str(port)
            
            print(f"🚀 Server starting on http://localhost:{port}")
            print("Press Ctrl+C to stop the server")
            
            # Open browser after a delay
            def open_browser():
                time.sleep(2)
                try:
                    import webbrowser
                    webbrowser.open(f"http://localhost:{port}")
                    print("🌐 Browser opened automatically")
                except:
                    print(f"📱 Open http://localhost:{port} in your browser")
            
            import threading
            browser_thread = threading.Thread(target=open_browser)
            browser_thread.daemon = True
            browser_thread.start()
            
            # Launch server directly
            cmd = [sys.executable, "backend_server.py"]
            if debug:
                env['FLASK_DEBUG'] = '1'
            
            # Run server and handle interruption
            try:
                process = subprocess.run(cmd, env=env, check=True)
            except KeyboardInterrupt:
                print("\n🛑 Stopping server...")
                print("✅ Server stopped")
            except subprocess.CalledProcessError as e:
                print(f"❌ Server error: {e}")
                
        except Exception as e:
            print(f"❌ Error launching server: {e}")
    
    def interactive_mode(self):
        """Enter interactive analysis mode"""
        print("\n🎮 Interactive Protein Analysis Mode")
        print("=" * 50)
        print("Commands:")
        print("  analyze <uniprot_id> [name] - Analyze single protein")
        print("  advanced <uniprot_id> [name] - Advanced analysis")
        print("  batch <file> - Batch analysis from file")
        print("  server [port] - Launch web server")
        print("  examples - Show example proteins")
        print("  help - Show this help")
        print("  exit - Exit interactive mode")
        print()
        
        while True:
            try:
                command = input("🧬 protein-cli> ").strip()
                
                if not command:
                    continue
                    
                parts = command.split()
                cmd = parts[0].lower()
                
                if cmd == "exit":
                    print("👋 Goodbye!")
                    break
                    
                elif cmd == "help":
                    self._show_interactive_help()
                    
                elif cmd == "examples":
                    self._show_examples()
                    
                elif cmd == "analyze":
                    if len(parts) < 2:
                        print("❌ Usage: analyze <uniprot_id> [name]")
                        continue
                    uniprot_id = parts[1]
                    name = " ".join(parts[2:]) if len(parts) > 2 else None
                    self.analyze_single_protein(uniprot_id, name)
                    
                elif cmd == "advanced":
                    if len(parts) < 2:
                        print("❌ Usage: advanced <uniprot_id> [name]")
                        continue
                    uniprot_id = parts[1]
                    name = " ".join(parts[2:]) if len(parts) > 2 else None
                    self.analyze_single_protein(uniprot_id, name, advanced=True)
                    
                elif cmd == "batch":
                    if len(parts) < 2:
                        print("❌ Usage: batch <file>")
                        continue
                    self.batch_analyze(parts[1])
                    
                elif cmd == "server":
                    port = int(parts[1]) if len(parts) > 1 else 5001
                    self.launch_web_server(port)
                    
                else:
                    print(f"❌ Unknown command: {cmd}")
                    print("Type 'help' for available commands")
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def _load_protein_list(self, filename: str) -> List[Dict]:
        """Load protein list from file"""
        proteins = []
        
        try:
            with open(filename, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    
                    # Support different formats
                    if '\t' in line:
                        parts = line.split('\t')
                        proteins.append({'id': parts[0], 'name': parts[1] if len(parts) > 1 else None})
                    elif ',' in line:
                        parts = line.split(',')
                        proteins.append({'id': parts[0], 'name': parts[1] if len(parts) > 1 else None})
                    else:
                        proteins.append({'id': line, 'name': None})
                        
        except FileNotFoundError:
            print(f"❌ File not found: {filename}")
            return []
            
        return proteins
    
    def _display_results(self, result: Dict):
        """Display analysis results"""
        protein_info = result['protein_info']
        rmsd = result['rmsd']
        
        print(f"\n📊 Analysis Results for {protein_info.name}")
        print("-" * 40)
        print(f"UniProt ID: {protein_info.uniprot_id}")
        print(f"Organism: {protein_info.organism}")
        print(f"Length: {protein_info.length} residues")
        print(f"RMSD: {rmsd:.3f} Å")
        
        # RMSD interpretation
        if rmsd < 2.0:
            status = "🟢 Excellent"
        elif rmsd < 4.0:
            status = "🟡 Good"
        else:
            status = "🔴 Poor"
        print(f"Quality: {status}")
        
        # Advanced analysis results
        if 'advanced_analysis' in result:
            adv = result['advanced_analysis']
            print(f"\n🧬 Advanced Analysis:")
            print(f"Homologs found: {adv['homologs']}")
            print(f"Conservation score: {adv['conservation_score']:.3f}")
            print(f"Orthologs: {adv['orthologs']}")
            print(f"Paralogs: {adv['paralogs']}")
        
        print(f"\n📁 Files generated:")
        print(f"  Visualization: {result.get('visualization_path', 'N/A')}")
        print(f"  Report: {result.get('report_path', 'N/A')}")
    
    def _generate_batch_summary(self, results: List[Dict], output_dir: str = None):
        """Generate batch analysis summary"""
        if not results:
            return
            
        output_path = Path(output_dir) if output_dir else Path("protein_analysis")
        summary_file = output_path / "batch_summary.json"
        
        summary = {
            'total_proteins': len(results),
            'successful_analyses': len([r for r in results if r]),
            'average_rmsd': sum(r['rmsd'] for r in results if r and r['rmsd'] != float('inf')) / len(results),
            'proteins': []
        }
        
        for result in results:
            if result:
                summary['proteins'].append({
                    'uniprot_id': result['protein_info'].uniprot_id,
                    'name': result['protein_info'].name,
                    'rmsd': result['rmsd'],
                    'length': result['protein_info'].length
                })
        
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
            
        print(f"\n📊 Batch Summary Generated: {summary_file}")
        print(f"Total proteins: {summary['total_proteins']}")
        print(f"Successful: {summary['successful_analyses']}")
        print(f"Average RMSD: {summary['average_rmsd']:.3f} Å")
    
    def _show_interactive_help(self):
        """Show interactive mode help"""
        print("\n🆘 Interactive Mode Commands:")
        print("━" * 40)
        print("analyze P01308                  - Analyze Human Insulin")
        print("analyze P01308 Human Insulin    - Analyze with custom name")
        print("advanced P01308                 - Advanced analysis with homology")
        print("batch proteins.txt              - Batch process from file")
        print("server                          - Launch web server on port 5001")
        print("server 8080                     - Launch web server on port 8080")
        print("examples                        - Show example proteins")
        print("exit                            - Exit interactive mode")
    
    def _show_examples(self):
        """Show example proteins"""
        examples = [
            ("P01308", "Human Insulin", "Hormone regulating glucose"),
            ("P61626", "Lysozyme", "Antimicrobial enzyme"),
            ("P68871", "Hemoglobin β", "Oxygen transport protein"),
            ("P02768", "Serum Albumin", "Blood plasma protein"),
            ("P04637", "p53 Tumor Suppressor", "Cancer-related protein")
        ]
        
        print("\n🧬 Example Proteins to Try:")
        print("━" * 50)
        for uniprot_id, name, desc in examples:
            print(f"{uniprot_id:<8} {name:<20} {desc}")
        print("\nUsage: analyze P01308")

def create_example_protein_file():
    """Create an example protein list file"""
    example_file = "example_proteins.txt"
    example_content = """# Example protein list for batch analysis
# Format: UniProt_ID[tab]Name (optional)
# Lines starting with # are comments

P01308	Human Insulin
P61626	Lysozyme
P68871	Hemoglobin β
P02768	Serum Albumin
P04637	p53 Tumor Suppressor
"""
    
    with open(example_file, 'w') as f:
        f.write(example_content)
    
    print(f"📄 Created example file: {example_file}")
    return example_file

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="🧬 Protein Structure Comparison CLI Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s analyze P01308                          # Analyze Human Insulin
  %(prog)s analyze P01308 --name "Human Insulin"  # With custom name
  %(prog)s advanced P01308                         # Advanced analysis
  %(prog)s batch proteins.txt                      # Batch analysis
  %(prog)s batch proteins.txt --output results/   # Custom output directory
  %(prog)s server                                  # Launch web server
  %(prog)s server --port 8080                      # Custom port
  %(prog)s interactive                             # Interactive mode
  %(prog)s create-example                          # Create example protein file
        """
    )
    
    # Subcommands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze single protein')
    analyze_parser.add_argument('uniprot_id', help='UniProt ID (e.g., P01308)')
    analyze_parser.add_argument('--name', help='Protein name (optional)')
    analyze_parser.add_argument('--output', help='Output directory')
    analyze_parser.add_argument('--advanced', action='store_true', help='Include advanced analysis')
    
    # Advanced command
    advanced_parser = subparsers.add_parser('advanced', help='Advanced protein analysis')
    advanced_parser.add_argument('uniprot_id', help='UniProt ID (e.g., P01308)')
    advanced_parser.add_argument('--name', help='Protein name (optional)')
    advanced_parser.add_argument('--output', help='Output directory')
    
    # Batch command
    batch_parser = subparsers.add_parser('batch', help='Batch analyze proteins from file')
    batch_parser.add_argument('file', help='File containing protein IDs')
    batch_parser.add_argument('--output', help='Output directory')
    batch_parser.add_argument('--advanced', action='store_true', help='Include advanced analysis')
    
    # Server command
    server_parser = subparsers.add_parser('server', help='Launch web server')
    server_parser.add_argument('--port', type=int, default=5001, help='Server port (default: 5001)')
    server_parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    
    # Interactive command
    subparsers.add_parser('interactive', help='Enter interactive mode')
    
    # Create example command
    subparsers.add_parser('create-example', help='Create example protein file')
    
    args = parser.parse_args()
    
    # Show help if no command
    if not args.command:
        parser.print_help()
        return
    
    # Initialize CLI
    cli = ProteinCLI()
    
    try:
        if args.command == 'analyze':
            cli.analyze_single_protein(args.uniprot_id, args.name, args.output, args.advanced)
            
        elif args.command == 'advanced':
            cli.analyze_single_protein(args.uniprot_id, args.name, args.output, advanced=True)
            
        elif args.command == 'batch':
            cli.batch_analyze(args.file, args.output, args.advanced)
            
        elif args.command == 'server':
            cli.launch_web_server(args.port, args.debug)
            
        elif args.command == 'interactive':
            cli.interactive_mode()
            
        elif args.command == 'create-example':
            create_example_protein_file()
            
    except KeyboardInterrupt:
        print("\n👋 Operation cancelled by user")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
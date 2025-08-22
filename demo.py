#!/usr/bin/env python3
"""
Demo script for Enhanced Protein Structure Comparison Tool

This script demonstrates how to use the enhanced protein analyzer to:
1. Compare AlphaFold vs ESMFold structures
2. Generate 3D visualizations
3. Create detailed analysis reports
4. Display protein information

Usage: python demo.py
"""

from enhanced_protein_analyzer import Enhanced3DProteinComparator
import sys

def demo_single_protein():
    """Demo with a single well-known protein"""
    print("🧬 Single Protein Analysis Demo")
    print("=" * 40)
    
    comparator = Enhanced3DProteinComparator()
    
    # Analyze human insulin (small, well-characterized protein)
    result = comparator.compare_protein_structures(
        uniprot_id="P01308",
        protein_name="Human Insulin"
    )
    
    if result:
        print("\n📋 Analysis Summary:")
        print(f"  • Protein: {result['protein_info'].name}")
        print(f"  • Length: {result['protein_info'].length} residues")
        print(f"  • RMSD: {result['rmsd']:.3f} Å")
        print(f"  • Function: {result['protein_info'].function[:100]}...")
        
        if result['rmsd'] < 2.0:
            print("  • ✅ Excellent structural agreement!")
        elif result['rmsd'] < 4.0:
            print("  • ⚠️ Moderate structural agreement")
        else:
            print("  • ❌ Significant structural differences")
    
    return result

def demo_multiple_proteins():
    """Demo with multiple proteins for comparison"""
    print("\n🧬 Multiple Protein Analysis Demo")
    print("=" * 45)
    
    proteins = [
        {"uniprot_id": "P01308", "name": "Human Insulin", "description": "Hormone regulating glucose"},
        {"uniprot_id": "P61626", "name": "Lysozyme", "description": "Antimicrobial enzyme"},
        {"uniprot_id": "P68871", "name": "Hemoglobin", "description": "Oxygen transport protein"}
    ]
    
    comparator = Enhanced3DProteinComparator()
    results = []
    
    for i, protein in enumerate(proteins, 1):
        print(f"\n[{i}/{len(proteins)}] Analyzing {protein['name']}...")
        print(f"Description: {protein['description']}")
        
        result = comparator.compare_protein_structures(
            protein['uniprot_id'], 
            protein['name']
        )
        
        if result:
            results.append(result)
            print(f"✅ RMSD: {result['rmsd']:.3f} Å")
        else:
            print("❌ Analysis failed")
    
    # Summary comparison
    if results:
        print("\n📊 Comparison Summary:")
        print("-" * 50)
        for result in results:
            quality = "🟢 Excellent" if result['rmsd'] < 2.0 else "🟡 Moderate" if result['rmsd'] < 4.0 else "🔴 Poor"
            print(f"{result['protein_info'].name:15} | RMSD: {result['rmsd']:6.3f} Å | {quality}")
    
    return results

def explain_methodology():
    """Explain the comparison methodology"""
    print("\n🔬 Methodology Explanation")
    print("=" * 35)
    
    explanation = """
    AlphaFold vs ESMFold Comparison:
    
    📊 METRICS:
    • RMSD (Root Mean Square Deviation): Measures structural similarity
    • Lower RMSD = More similar structures
    
    🔵 ALPHAFOLD:
    • Uses Multiple Sequence Alignments (MSAs)
    • Template-based modeling when available
    • Generally higher accuracy
    • Computationally intensive
    • Best for well-studied protein families
    
    🔴 ESMFOLD:
    • Language model approach (ESM)
    • Single sequence input only
    • Faster predictions
    • Good for novel/orphan sequences
    • May struggle with complex domains
    
    📈 INTERPRETATION:
    • < 2.0 Å: Structures are very similar
    • 2.0-4.0 Å: Moderately similar structures  
    • > 4.0 Å: Significant structural differences
    
    🎯 USE CASES:
    • Research: Understanding protein function
    • Drug Discovery: Structure-based design
    • Evolution: Comparing protein families
    • Quality Control: Validating predictions
    """
    
    print(explanation)

def interactive_demo():
    """Interactive demo allowing user input"""
    print("\n🎮 Interactive Demo")
    print("=" * 25)
    
    while True:
        print("\nOptions:")
        print("1. Analyze custom UniProt ID")
        print("2. View example proteins")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            uniprot_id = input("Enter UniProt ID (e.g., P01308): ").strip().upper()
            if uniprot_id:
                comparator = Enhanced3DProteinComparator()
                result = comparator.compare_protein_structures(uniprot_id)
                
                if result:
                    print(f"\n✅ Analysis completed for {result['protein_info'].name}")
                    print(f"📁 Check results in: protein_analysis/")
                else:
                    print("❌ Analysis failed. Check UniProt ID.")
            
        elif choice == "2":
            print("\nExample proteins you can try:")
            examples = [
                ("P01308", "Human Insulin"),
                ("P61626", "Lysozyme"),
                ("P68871", "Hemoglobin subunit beta"),
                ("P02768", "Serum albumin"),
                ("P04637", "Tumor protein p53")
            ]
            
            for uniprot_id, name in examples:
                print(f"  {uniprot_id} - {name}")
            
        elif choice == "3":
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")

def main():
    """Main demo function"""
    print("🧬 Enhanced Protein Structure Comparison Tool - DEMO")
    print("=" * 60)
    
    print("\nThis tool compares AlphaFold and ESMFold protein structures")
    print("Features:")
    print("  • 3D interactive visualizations")
    print("  • Detailed protein information")
    print("  • RMSD calculations")
    print("  • HTML analysis reports")
    print("  • Automatic browser opening")
    
    try:
        # Run methodology explanation
        explain_methodology()
        
        # Run single protein demo
        demo_single_protein()
        
        # Ask if user wants to continue
        continue_demo = input("\n🤔 Would you like to see more examples? (y/n): ").lower().strip()
        
        if continue_demo in ['y', 'yes']:
            # Run multiple protein demo
            demo_multiple_proteins()
            
            # Interactive demo
            interactive_mode = input("\n🎮 Enter interactive mode? (y/n): ").lower().strip()
            if interactive_mode in ['y', 'yes']:
                interactive_demo()
        
        print("\n✨ Demo completed!")
        print("📁 Check the 'protein_analysis' directory for all generated files")
        print("🌐 HTML files should have opened automatically in your browser")
        
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted by user. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error during demo: {e}")
        print("Make sure all dependencies are installed: pip install -r requirements.txt")

if __name__ == "__main__":
    main()
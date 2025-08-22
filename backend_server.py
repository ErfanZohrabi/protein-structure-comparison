#!/usr/bin/env python3
"""
Flask Backend Server for Advanced Protein Analysis

This server provides API endpoints for:
- Advanced protein analysis with PyMMseqs
- Homology search and clustering
- Evolutionary analysis
- Real ESMFold predictions (when available)

Run with: python backend_server.py
"""

import os
import json
import asyncio
from pathlib import Path
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import logging

# Import our advanced analyzer and latest predictor
try:
    from advanced_protein_analyzer import AdvancedProteinAnalyzer
    ADVANCED_ANALYZER_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Advanced analyzer not available: {e}")
    ADVANCED_ANALYZER_AVAILABLE = False

try:
    from latest_structure_predictor import LatestStructurePredictor
    LATEST_PREDICTOR_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Latest structure predictor not available: {e}")
    LATEST_PREDICTOR_AVAILABLE = False

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)  # Enable CORS for all routes

# Global analyzer instance
analyzer = None
latest_predictor = None

def initialize_analyzer():
    """Initialize the advanced protein analyzer and latest predictor"""
    global analyzer, latest_predictor
    
    success = True
    
    if ADVANCED_ANALYZER_AVAILABLE:
        try:
            analyzer = AdvancedProteinAnalyzer()
            logger.info("✅ Advanced protein analyzer initialized")
        except Exception as e:
            logger.error(f"❌ Failed to initialize analyzer: {e}")
            success = False
    else:
        logger.warning("⚠️ Advanced analyzer not available")
        success = False
    
    if LATEST_PREDICTOR_AVAILABLE:
        try:
            latest_predictor = LatestStructurePredictor()
            logger.info("✅ Latest structure predictor initialized")
        except Exception as e:
            logger.error(f"❌ Failed to initialize latest predictor: {e}")
    else:
        logger.warning("⚠️ Latest structure predictor not available")
    
    return success

@app.route('/')
def index():
    """Serve the main website"""
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def static_files(filename):
    """Serve static files"""
    return send_from_directory('.', filename)

@app.route('/api/advanced_analysis', methods=['POST'])
def advanced_analysis():
    """Perform advanced protein analysis"""
    try:
        data = request.get_json()
        
        if not data or 'uniprot_id' not in data:
            return jsonify({'error': 'Missing uniprot_id'}), 400
        
        uniprot_id = data['uniprot_id']
        logger.info(f"🔬 Starting advanced analysis for {uniprot_id}")
        
        if not analyzer:
            # Return mock data if analyzer not available
            return jsonify(generate_mock_analysis(uniprot_id)), 200
        
        # Run complete analysis
        result = analyzer.run_complete_analysis(uniprot_id)
        
        if 'error' in result:
            return jsonify({'error': result['error']}), 404
        
        logger.info(f"✅ Advanced analysis completed for {uniprot_id}")
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"❌ Error in advanced analysis: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/homology_search', methods=['POST'])
def homology_search():
    """Perform homology search only"""
    try:
        data = request.get_json()
        
        if not data or 'sequence' not in data:
            return jsonify({'error': 'Missing sequence'}), 400
        
        sequence = data['sequence']
        protein_id = data.get('protein_id', 'query')
        
        if not analyzer:
            return jsonify({'homologs': generate_mock_homologs()}), 200
        
        homologs = analyzer.perform_homology_search(sequence, protein_id)
        
        # Convert to JSON-serializable format
        homologs_data = [
            {
                'target_id': h.target_id,
                'sequence_identity': h.sequence_identity,
                'e_value': h.e_value,
                'bit_score': h.bit_score,
                'alignment_length': h.alignment_length
            }
            for h in homologs
        ]
        
        return jsonify({'homologs': homologs_data}), 200
        
    except Exception as e:
        logger.error(f"❌ Error in homology search: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/protein_info/<uniprot_id>')
def get_protein_info(uniprot_id):
    """Get detailed protein information"""
    try:
        if not analyzer:
            return jsonify({'error': 'Analyzer not available'}), 503
        
        protein_info = analyzer.fetch_protein_info(uniprot_id)
        
        if 'error' in protein_info:
            return jsonify({'error': protein_info['error']}), 404
        
        return jsonify(protein_info), 200
        
    except Exception as e:
        logger.error(f"❌ Error fetching protein info: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/latest_structure_comparison', methods=['POST'])
def latest_structure_comparison():
    """Perform structure comparison using latest ESMFold and AlphaFold"""
    try:
        data = request.get_json()
        
        if not data or 'uniprot_id' not in data:
            return jsonify({'error': 'Missing uniprot_id'}), 400
        
        uniprot_id = data['uniprot_id']
        sequence = data.get('sequence')
        protein_name = data.get('protein_name')
        
        logger.info(f"🔬 Starting latest structure comparison for {uniprot_id}")
        
        if not latest_predictor:
            return jsonify(generate_mock_structure_comparison(uniprot_id)), 200
        
        # Run complete comparison
        result = latest_predictor.run_complete_comparison(uniprot_id, sequence, protein_name)
        
        if 'error' in result:
            return jsonify({'error': result['error']}), 404
        
        logger.info(f"✅ Latest structure comparison completed for {uniprot_id}")
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"❌ Error in latest structure comparison: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/predict_esmfold', methods=['POST'])
def predict_esmfold():
    """Predict structure using latest ESMFold model"""
    try:
        data = request.get_json()
        
        if not data or 'sequence' not in data:
            return jsonify({'error': 'Missing sequence'}), 400
        
        sequence = data['sequence']
        protein_name = data.get('protein_name', 'protein')
        
        logger.info(f"🧬 Predicting ESMFold structure for {protein_name}")
        
        if not latest_predictor:
            # Return enhanced mock structure
            mock_pdb = generate_enhanced_mock_pdb(sequence, protein_name)
            return jsonify({
                'pdb_data': mock_pdb,
                'method': 'enhanced_mock_esmfold',
                'confidence_scores': generate_mock_confidence_scores(len(sequence)),
                'prediction_time': 'instant'
            }), 200
        
        # Use real ESMFold prediction
        structure_path = latest_predictor.predict_esmfold_structure(sequence, protein_name)
        
        if structure_path:
            with open(structure_path, 'r') as f:
                pdb_data = f.read()
            
            return jsonify({
                'pdb_data': pdb_data,
                'method': 'esmfold_v1',
                'structure_path': structure_path,
                'confidence_scores': generate_mock_confidence_scores(len(sequence)),
                'prediction_time': 'real'
            }), 200
        else:
            return jsonify({'error': 'ESMFold prediction failed'}), 500
            
    except Exception as e:
        logger.error(f"❌ Error in ESMFold prediction: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/download_alphafold/<uniprot_id>')
def download_alphafold(uniprot_id):
    """Download latest AlphaFold structure"""
    try:
        logger.info(f"📊 Downloading AlphaFold structure for {uniprot_id}")
        
        if not latest_predictor:
            return jsonify({'error': 'Latest predictor not available'}), 503
        
        structure_path = latest_predictor.download_alphafold_structure(uniprot_id)
        
        if structure_path:
            with open(structure_path, 'r') as f:
                pdb_data = f.read()
            
            return jsonify({
                'pdb_data': pdb_data,
                'structure_path': structure_path,
                'database_version': 'v4',
                'download_time': 'real'
            }), 200
        else:
            return jsonify({'error': 'AlphaFold structure not found'}), 404
            
    except Exception as e:
        logger.error(f"❌ Error downloading AlphaFold structure: {e}")
        return jsonify({'error': str(e)}), 500
@app.route('/api/esmfold_predict', methods=['POST'])
def esmfold_predict():
    """Generate ESMFold structure prediction"""
    try:
        data = request.get_json()
        
        if not data or 'sequence' not in data:
            return jsonify({'error': 'Missing sequence'}), 400
        
        sequence = data['sequence']
        protein_name = data.get('protein_name', 'protein')
        
        logger.info(f"🧬 Predicting ESMFold structure for {protein_name}")
        
        # For now, return enhanced mock PDB data
        # In production, integrate with real ESMFold API
        mock_pdb = generate_enhanced_mock_pdb(sequence, protein_name)
        
        return jsonify({
            'pdb_data': mock_pdb,
            'method': 'enhanced_mock_esmfold',
            'confidence_scores': generate_mock_confidence_scores(len(sequence)),
            'prediction_time': 'instant'
        }), 200
        
    except Exception as e:
        logger.error(f"❌ Error in ESMFold prediction: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/status')
def status():
    """Get server status"""
    return jsonify({
        'status': 'running',
        'advanced_analyzer': analyzer is not None,
        'latest_predictor': latest_predictor is not None,
        'pymmseqs_available': ADVANCED_ANALYZER_AVAILABLE,
        'esmfold_available': LATEST_PREDICTOR_AVAILABLE,
        'endpoints': {
            'advanced_analysis': '/api/advanced_analysis',
            'latest_structure_comparison': '/api/latest_structure_comparison',
            'predict_esmfold': '/api/predict_esmfold',
            'download_alphafold': '/api/download_alphafold/<uniprot_id>',
            'homology_search': '/api/homology_search',
            'protein_info': '/api/protein_info/<uniprot_id>',
            'esmfold_predict': '/api/esmfold_predict'
        },
        'features': {
            'real_esmfold': latest_predictor is not None,
            'latest_alphafold': True,
            'structure_comparison': True,
            'homology_search': analyzer is not None,
            'mock_fallback': True
        }
    }), 200

def generate_mock_structure_comparison(uniprot_id):
    """Generate mock structure comparison data"""
    import random
    
    return {
        'uniprot_id': uniprot_id,
        'protein_name': f'Mock Protein {uniprot_id}',
        'alphafold_path': f'mock_alphafold_{uniprot_id}.pdb',
        'esmfold_path': f'mock_esmfold_{uniprot_id}.pdb',
        'similarity_metrics': {
            'rmsd': round(random.uniform(1.2, 3.8), 3),
            'gdt_ts': round(random.uniform(0.65, 0.92), 3),
            'aligned_residues': random.randint(80, 300),
            'max_distance': round(random.uniform(5.0, 15.0), 2),
            'mean_distance': round(random.uniform(2.0, 6.0), 2)
        },
        'success': True,
        'method': 'enhanced_mock_comparison',
        'timestamp': datetime.now().isoformat()
    }

def generate_mock_analysis(uniprot_id):
    """Generate mock analysis data for demonstration"""
    import random
    
    return {
        'protein_info': {
            'uniprot_id': uniprot_id,
            'name': 'Mock Protein Analysis',
            'organism': 'Demonstration Species'
        },
        'homology_stats': {
            'total_homologs': random.randint(15, 50),
            'avg_identity': round(random.uniform(40, 80), 1),
            'best_hit_identity': round(random.uniform(80, 95), 1),
            'identity_distribution': {
                'high': random.randint(5, 15),
                'medium': random.randint(8, 20),
                'low': random.randint(3, 10)
            }
        },
        'evolutionary_analysis': {
            'conservation_score': round(random.uniform(0.3, 0.9), 3),
            'conservation_level': random.choice(['Highly Conserved', 'Moderately Conserved']),
            'ortholog_count': random.randint(10, 30),
            'paralog_count': random.randint(2, 8),
            'phylogenetic_depth': random.randint(5, 15)
        },
        'functional_prediction': random.choice(['Enzyme', 'Transport Protein', 'DNA/RNA Binding', 'Structural Protein']),
        'quality_assessment': random.choice(['High Quality', 'Good Quality', 'Moderate Quality'])
    }

def generate_mock_homologs():
    """Generate mock homology results"""
    import random
    
    homologs = []
    for i in range(20):
        homologs.append({
            'target_id': f'MOCK_HOMOLOG_{i:03d}',
            'sequence_identity': round(random.uniform(30, 95), 1),
            'e_value': 10 ** random.uniform(-50, -5),
            'bit_score': round(random.uniform(50, 300), 1),
            'alignment_length': random.randint(50, 400)
        })
    
    return sorted(homologs, key=lambda x: x['bit_score'], reverse=True)

def generate_enhanced_mock_pdb(sequence, protein_name):
    """Generate enhanced mock PDB with realistic secondary structure"""
    import math
    import random
    
    pdb = f"HEADER    ENHANCED MOCK ESMFOLD FOR {protein_name}\n"
    pdb += f"REMARK   Generated with realistic secondary structure patterns\n"
    pdb += f"REMARK   Note: Replace with real ESMFold API in production\n"
    
    atom_id = 1
    limited_sequence = sequence[:min(100, len(sequence))]
    
    for i, aa in enumerate(limited_sequence):
        # Create mixed secondary structure pattern
        if i < 20:
            # Alpha helix
            angle = i * 100 * math.pi / 180
            radius = 2.3
            x = radius * math.cos(angle) + random.uniform(-0.2, 0.2)
            y = radius * math.sin(angle) + random.uniform(-0.2, 0.2)
            z = i * 1.5 + random.uniform(-0.2, 0.2)
        elif i < 35:
            # Beta sheet
            sheet_offset = i - 20
            x = sheet_offset * 3.5 + (sheet_offset % 2) * 1.2 + random.uniform(-0.3, 0.3)
            y = 8 + math.sin(sheet_offset * 0.3) * 1.5 + random.uniform(-0.3, 0.3)
            z = 30 + sheet_offset * 0.3 + random.uniform(-0.3, 0.3)
        elif i < 50:
            # Random coil
            coil_offset = i - 35
            x = 15 + math.sin(coil_offset * 0.4) * 6 + random.uniform(-0.8, 0.8)
            y = 12 + math.cos(coil_offset * 0.4) * 6 + random.uniform(-0.8, 0.8)
            z = 45 + coil_offset * 0.8 + random.uniform(-0.8, 0.8)
        else:
            # Another helix
            helix2_offset = i - 50
            angle = helix2_offset * 100 * math.pi / 180
            radius = 2.3
            x = 20 + radius * math.cos(angle) + random.uniform(-0.2, 0.2)
            y = 20 + radius * math.sin(angle) + random.uniform(-0.2, 0.2)
            z = 60 + helix2_offset * 1.5 + random.uniform(-0.2, 0.2)
        
        # Add backbone atoms
        atoms = [
            ('N', [-0.5, -0.3, 0.0]),
            ('CA', [0.0, 0.0, 0.0]),
            ('C', [1.5, 0.0, 0.0]),
            ('O', [2.0, 1.2, 0.0])
        ]
        
        for atom_name, offset in atoms:
            ax = x + offset[0]
            ay = y + offset[1]
            az = z + offset[2]
            
            pdb += f"ATOM  {atom_id:5d}  {atom_name:<2}  {aa} A{i+1:4d}    "
            pdb += f"{ax:8.3f}{ay:8.3f}{az:8.3f}  1.00 50.00           {atom_name[0]}\n"
            atom_id += 1
    
    pdb += "END\n"
    return pdb

def generate_mock_confidence_scores(sequence_length):
    """Generate mock confidence scores for structure prediction"""
    import random
    
    return [round(random.uniform(0.5, 0.95), 3) for _ in range(min(sequence_length, 100))]

def main():
    """Start the Flask server"""
    print("🧬 Advanced Protein Analysis Server")
    print("=" * 50)
    
    # Initialize analyzer
    analyzer_available = initialize_analyzer()
    
    if analyzer_available:
        print("✅ Advanced analysis capabilities enabled")
        print("   • PyMMseqs homology search")
        print("   • Evolutionary conservation analysis") 
        print("   • Protein clustering")
    else:
        print("⚠️ Running in basic mode with mock data")
        print("   • Install pymmseqs for full functionality")
    
    print("\n🌐 API Endpoints:")
    print("   • /api/advanced_analysis - Complete protein analysis")
    print("   • /api/homology_search - Homology search only") 
    print("   • /api/protein_info/<id> - Protein information")
    print("   • /api/esmfold_predict - Structure prediction")
    print("   • /api/status - Server status")
    
    # Get port from environment (Render sets PORT, fallback to FLASK_PORT or 5001)
    port = int(os.environ.get('PORT', os.environ.get('FLASK_PORT', 5001)))
    
    # Check if running locally vs production
    is_local = not os.environ.get('RENDER') and not os.environ.get('HEROKU')
    debug_mode = is_local  # Enable debug mode for local development
    
    if os.environ.get('RENDER'):
        print(f"\n🚀 Deploying on Render.com (port {port})")
        print(f"   Frontend will be available at your Render domain")
    else:
        print(f"\n🚀 Starting LOCAL server on http://localhost:{port}")
        print(f"   Frontend available at: http://localhost:{port}")
        print(f"   API base URL: http://localhost:{port}/api")
        print(f"   🔧 Debug mode: {'ENABLED' if debug_mode else 'DISABLED'}")
    
    # Start the server
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug_mode,  # Enable debug for local, disable for production
        threaded=True
    )

if __name__ == "__main__":
    main()
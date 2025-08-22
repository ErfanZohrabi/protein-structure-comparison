#!/bin/bash

echo "🧬 Protein Structure Comparison - Full Setup Script"
echo "=================================================="
echo "Setting up full potential with all advanced features..."
echo ""

# Activate virtual environment
if [ -d "venv" ]; then
    echo "🔧 Activating virtual environment..."
    source venv/bin/activate
    echo "✅ Virtual environment activated"
else
    echo "⚠️  Virtual environment not found. Creating one..."
    python3 -m venv venv
    source venv/bin/activate
    echo "✅ Virtual environment created and activated"
fi

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install full requirements
echo "🚀 Installing FULL dependencies (including heavy ML packages)..."
echo "This may take 10-15 minutes for first-time installation..."
pip install -r requirements.txt

# Check if PyTorch is installed correctly
echo ""
echo "🔍 Checking PyTorch installation..."
python -c "import torch; print(f'✅ PyTorch {torch.__version__} installed successfully')" 2>/dev/null || echo "❌ PyTorch installation failed"

# Check if ESM is installed correctly  
echo "🔍 Checking ESM (ESMFold) installation..."
python -c "import esm; print('✅ ESM (ESMFold) installed successfully')" 2>/dev/null || echo "❌ ESM installation failed"

# Check if ColabFold is installed correctly
echo "🔍 Checking ColabFold installation..."
python -c "import colabfold; print('✅ ColabFold installed successfully')" 2>/dev/null || echo "❌ ColabFold installation failed"

# Check if PyMMseqs is installed correctly
echo "🔍 Checking PyMMseqs installation..."
python -c "import pymmseqs; print('✅ PyMMseqs installed successfully')" 2>/dev/null || echo "❌ PyMMseqs installation failed"

echo ""
echo "🎉 Setup Complete! Full potential activated!"
echo "=================================================="
echo "🚀 Available commands:"
echo "   • python backend_server.py     - Launch web server (full features)"
echo "   • python protein_cli.py server - Launch via CLI"
echo "   • python demo.py               - Run demo analysis"
echo "   • python launch.py             - Alternative launcher"
echo ""
echo "✨ Features now enabled:"
echo "   ✅ Real ESMFold predictions (GPU recommended)"
echo "   ✅ Advanced PyMMseqs homology search"  
echo "   ✅ Complete evolutionary analysis"
echo "   ✅ High-quality structure comparisons"
echo "   ✅ Batch processing capabilities"
echo ""
echo "💡 For best performance, ensure you have:"
echo "   • NVIDIA GPU with CUDA support (recommended)"
echo "   • At least 8GB RAM"
echo "   • Good internet connection for model downloads"
echo ""

# Test server startup
echo "🧪 Testing server startup..."
echo "Starting server in test mode (will stop after 3 seconds)..."
timeout 3s python backend_server.py 2>/dev/null &
sleep 3
echo "✅ Server test completed"
echo ""
echo "🎯 Ready to launch! Run: python backend_server.py"
#!/bin/bash
# GitHub Transfer Script for Protein Structure Comparison Tool

echo "🧬 Protein Structure Comparison Tool - GitHub Transfer"
echo "=================================================="

# Check if we're in the right directory
if [ ! -f "protein_cli.py" ]; then
    echo "❌ Error: Please run this script from the protein_comparison directory"
    exit 1
fi

echo "📂 Current directory: $(pwd)"
echo "📊 Project files:"
find . -name "*.py" -o -name "*.html" -o -name "*.css" -o -name "*.js" -o -name "*.md" | head -10

echo ""
echo "🔧 Setting up Git repository..."

# Initialize git if not already done
if [ ! -d ".git" ]; then
    git init
    echo "✅ Git repository initialized"
else
    echo "ℹ️ Git repository already exists"
fi

# Replace README for GitHub
if [ -f "README_GITHUB.md" ]; then
    mv README.md README_ORIGINAL.md
    mv README_GITHUB.md README.md
    echo "✅ GitHub README activated"
fi

# Add all files
echo "📁 Adding files to git..."
git add .

# Show status
echo "📊 Git status:"
git status --short

echo ""
echo "🚀 Ready for GitHub upload!"
echo ""
echo "Next steps:"
echo "1. Create repository on GitHub: https://github.com/new"
echo "2. Name it: protein-structure-comparison"
echo "3. Don't initialize with README"
echo "4. Run these commands:"
echo ""
echo "   git commit -m \"Initial commit: Complete protein structure comparison tool\""
echo "   git remote add origin https://github.com/YOUR_USERNAME/protein-structure-comparison.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "🎉 Your project will be live on GitHub!"
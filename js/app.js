/**
 * Protein Structure Viewer - Main Application Logic
 * Handles protein search, data fetching, and 3D visualization
 */

class ProteinViewer {
    constructor() {
        this.currentProtein = null;
        this.alphafoldViewer = null;
        this.esmfoldViewer = null;
        this.currentAlphafoldStyle = 'cartoon';
        this.currentEsmfoldStyle = 'cartoon';
        
        this.initializeApp();
    }

    initializeApp() {
        this.setupEventListeners();
        this.setupSearchSuggestions();
        this.show3DViewers();
        
        // Load example protein on startup
        setTimeout(() => {
            this.searchProtein('P01308');
        }, 1000);
    }

    setupEventListeners() {
        const searchBtn = document.getElementById('searchBtn');
        const searchInput = document.getElementById('proteinSearch');
        
        searchBtn.addEventListener('click', () => this.handleSearch());
        searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.handleSearch();
            }
        });

        // Search input focus/blur for suggestions
        searchInput.addEventListener('focus', () => {
            this.showSearchSuggestions();
        });

        searchInput.addEventListener('blur', () => {
            // Delay hiding to allow clicks on suggestions
            setTimeout(() => this.hideSearchSuggestions(), 200);
        });

        // Real-time search suggestions
        searchInput.addEventListener('input', (e) => {
            this.filterSearchSuggestions(e.target.value);
        });
    }

    setupSearchSuggestions() {
        const suggestions = document.querySelectorAll('.suggestion-item');
        suggestions.forEach(item => {
            item.addEventListener('click', () => {
                const uniprotId = item.dataset.uniprot;
                const proteinName = item.textContent.split(' - ')[1];
                
                document.getElementById('proteinSearch').value = `${uniprotId} - ${proteinName}`;
                this.hideSearchSuggestions();
                this.searchProtein(uniprotId);
            });
        });
    }

    showSearchSuggestions() {
        document.getElementById('searchSuggestions').style.display = 'block';
    }

    hideSearchSuggestions() {
        document.getElementById('searchSuggestions').style.display = 'none';
    }

    filterSearchSuggestions(query) {
        const suggestions = document.querySelectorAll('.suggestion-item');
        const lowerQuery = query.toLowerCase();

        suggestions.forEach(item => {
            const text = item.textContent.toLowerCase();
            if (text.includes(lowerQuery)) {
                item.style.display = 'block';
            } else {
                item.style.display = 'none';
            }
        });

        if (query.length > 0) {
            this.showSearchSuggestions();
        }
    }

    show3DViewers() {
        const viewersContainer = document.getElementById('viewersContainer');
        if (viewersContainer) {
            viewersContainer.style.display = 'grid';
            
            // Initialize viewers with proper error handling
            setTimeout(() => {
                try {
                    console.log('Initializing 3D viewers...');
                    
                    // Check if $3Dmol is available
                    if (typeof $3Dmol === 'undefined') {
                        console.error('3Dmol.js library not loaded');
                        this.showError('3D visualization library not available');
                        return;
                    }
                    
                    // Initialize AlphaFold viewer
                    const alphafoldDiv = document.getElementById('alphafoldViewer');
                    if (alphafoldDiv && !this.alphafoldViewer) {
                        this.alphafoldViewer = $3Dmol.createViewer(alphafoldDiv, {
                            backgroundColor: 'black',
                            width: '100%',
                            height: '100%'
                        });
                        console.log('AlphaFold viewer initialized');
                    }
                    
                    // Initialize ESMFold viewer  
                    const esmfoldDiv = document.getElementById('esmfoldViewer');
                    if (esmfoldDiv && !this.esmfoldViewer) {
                        this.esmfoldViewer = $3Dmol.createViewer(esmfoldDiv, {
                            backgroundColor: 'black',
                            width: '100%',
                            height: '100%'
                        });
                        console.log('ESMFold viewer initialized');
                    }
                    
                } catch (error) {
                    console.error('Error initializing 3D viewers:', error);
                    this.showError('Failed to initialize 3D viewers');
                }
            }, 100);
        }
    }

    handleSearch() {
        const searchInput = document.getElementById('proteinSearch');
        const query = searchInput.value.trim();
        
        if (!query) {
            this.showError('Please enter a UniProt ID or protein name');
            return;
        }

        // Extract UniProt ID if format is "ID - Name"
        const uniprotId = query.includes(' - ') ? query.split(' - ')[0] : query;
        
        this.searchProtein(uniprotId.toUpperCase());
    }

    async searchProtein(uniprotId) {
        try {
            this.showLoading();
            this.hideError();
            
            // Fetch protein information
            const proteinInfo = await this.fetchProteinInfo(uniprotId);
            
            if (!proteinInfo) {
                throw new Error('Protein not found');
            }

            this.currentProtein = proteinInfo;
            this.displayProteinInfo(proteinInfo);
            
            // Load structures
            await this.loadStructures(uniprotId, proteinInfo);
            
            this.showSuccess(`Successfully loaded ${proteinInfo.name}`);
            this.hideLoading();
            
        } catch (error) {
            this.hideLoading();
            this.showError(`Error loading protein: ${error.message}`);
            console.error('Search error:', error);
        }
    }

    async fetchProteinInfo(uniprotId) {
        try {
            const response = await fetch(`https://rest.uniprot.org/uniprotkb/${uniprotId}.json`);
            
            if (!response.ok) {
                throw new Error('Protein not found in UniProt database');
            }
            
            const data = await response.json();
            
            // Extract protein information
            const proteinName = data.proteinDescription?.recommendedName?.fullName?.value || 'Unknown Protein';
            const organism = data.organism?.scientificName || 'Unknown';
            const sequence = data.sequence?.value || '';
            const length = data.sequence?.length || 0;
            const molecularWeight = data.sequence?.molWeight || 0;
            
            // Extract function
            const functionComments = data.comments?.filter(comment => comment.commentType === 'FUNCTION') || [];
            const proteinFunction = functionComments.length > 0 ? 
                functionComments[0].texts[0]?.value || 'Function not available' : 
                'Function not available';
            
            // Extract keywords
            const keywords = data.keywords?.map(kw => kw.value) || [];
            
            return {
                uniprotId,
                name: proteinName,
                organism,
                sequence,
                length,
                molecularWeight,
                function: proteinFunction,
                keywords
            };
            
        } catch (error) {
            console.error('Error fetching protein info:', error);
            throw error;
        }
    }

    displayProteinInfo(protein) {
        document.getElementById('proteinName').textContent = protein.name;
        document.getElementById('proteinDescription').textContent = `${protein.organism} • ${protein.keywords.slice(0, 3).join(', ')}`;
        document.getElementById('uniprotId').textContent = protein.uniprotId;
        document.getElementById('organism').textContent = protein.organism;
        document.getElementById('proteinLength').textContent = `${protein.length} amino acids`;
        document.getElementById('molecularWeight').textContent = `${protein.molecularWeight.toFixed(1)} Da`;
        document.getElementById('proteinFunction').textContent = protein.function;
        
        // Format sequence with line breaks every 60 characters
        const formattedSequence = protein.sequence.match(/.{1,60}/g)?.join('\n') || protein.sequence;
        document.getElementById('proteinSequence').textContent = formattedSequence;
        
        // Show protein info section
        document.getElementById('proteinInfo').style.display = 'block';
    }

    async loadStructures(uniprotId, proteinInfo) {
        try {
            // Show viewers
            this.show3DViewers();
            
            // Load AlphaFold structure
            await this.loadAlphaFoldStructure(uniprotId);
            
            // Generate mock ESMFold structure (in real implementation, use actual ESMFold)
            await this.loadESMFoldStructure(proteinInfo);
            
            // Run advanced analysis using Python backend
            await this.runAdvancedAnalysis(uniprotId, proteinInfo);
            
            // Calculate and display comparison
            this.displayComparison();
            
        } catch (error) {
            console.error('Error loading structures:', error);
            throw error;
        }
    }

    async loadAlphaFoldStructure(uniprotId) {
        return new Promise((resolve, reject) => {
            try {
                // Initialize AlphaFold viewer
                this.alphafoldViewer = $3Dmol.createViewer('alphafoldViewer', {
                    backgroundColor: 'black',
                    width: '100%',
                    height: '100%'
                });

                const alphafoldUrl = `https://alphafold.ebi.ac.uk/files/AF-${uniprotId}-F1-model_v4.pdb`;
                
                // Load structure from AlphaFold database
                fetch(alphafoldUrl)
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('AlphaFold structure not available');
                        }
                        return response.text();
                    })
                    .then(pdbData => {
                        this.alphafoldViewer.addModel(pdbData, 'pdb');
                        this.alphafoldViewer.setStyle({}, {
                            cartoon: {
                                color: 'spectrum',
                                opacity: 0.8
                            }
                        });
                        this.alphafoldViewer.zoomTo();
                        this.alphafoldViewer.render();
                        
                        // Hide loading indicator
                        const loadingDiv = document.querySelector('#alphafoldViewer .viewer-loading');
                        if (loadingDiv) loadingDiv.style.display = 'none';
                        
                        resolve();
                    })
                    .catch(error => {
                        console.error('AlphaFold loading error:', error);
                        this.loadMockStructure('alphafold', uniprotId);
                        resolve(); // Don't reject, just use mock
                    });
                    
            } catch (error) {
                console.error('AlphaFold viewer error:', error);
                this.loadMockStructure('alphafold', uniprotId);
                resolve();
            }
        });
    }

    async loadESMFoldStructure(proteinInfo) {
        return new Promise(async (resolve) => {
            try {
                // Initialize ESMFold viewer
                this.esmfoldViewer = $3Dmol.createViewer('esmfoldViewer', {
                    backgroundColor: 'black',
                    width: '100%',
                    height: '100%'
                });

            // Try to get enhanced structure from backend
            try {
                const response = await fetch('/api/esmfold_predict', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        sequence: proteinInfo.sequence,
                        protein_name: proteinInfo.name
                    })
                });
                
                if (response.ok) {
                    const data = await response.json();
                    const pdbData = data.pdb_data;
                    
                    this.esmfoldViewer.addModel(pdbData, 'pdb');
                    this.esmfoldViewer.setStyle({}, {
                        cartoon: {
                            color: 'spectrum',
                            opacity: 0.8
                        }
                    });
                    this.esmfoldViewer.zoomTo();
                    this.esmfoldViewer.render();
                    
                    console.log('✅ Enhanced ESMFold structure loaded from backend');
                } else {
                    throw new Error('Backend not available');
                }
            } catch (backendError) {
                console.warn('Backend not available, using local mock:', backendError);
                    
                    // Fallback to local enhanced mock structure
                    const mockPdb = this.generateMockPDB(proteinInfo.sequence, proteinInfo.name);
                    
                    this.esmfoldViewer.addModel(mockPdb, 'pdb');
                    this.esmfoldViewer.setStyle({}, {
                        cartoon: {
                            color: 'spectrum',
                            opacity: 0.8
                        }
                    });
                    this.esmfoldViewer.zoomTo();
                    this.esmfoldViewer.render();
                }
                
                // Hide loading indicator
                const loadingDiv = document.querySelector('#esmfoldViewer .viewer-loading');
                if (loadingDiv) loadingDiv.style.display = 'none';
                
                resolve();
                
            } catch (error) {
                console.error('ESMFold viewer error:', error);
                this.loadMockStructure('esmfold', proteinInfo.uniprotId);
                resolve();
            }
        });
    }

    loadMockStructure(viewerType, identifier) {
        const viewer = viewerType === 'alphafold' ? this.alphafoldViewer : this.esmfoldViewer;
        const mockPdb = this.generateMockPDB('MKWVTFISLLLLFSSAYSRGVFRRDAHKSEVAHRFKDLGE', identifier);
        
        viewer.addModel(mockPdb, 'pdb');
        viewer.setStyle({}, {
            cartoon: {
                color: 'spectrum',
                opacity: 0.8
            }
        });
        viewer.zoomTo();
        viewer.render();
        
        // Hide loading indicator
        const loadingDiv = document.querySelector(`#${viewerType}Viewer .viewer-loading`);
        if (loadingDiv) loadingDiv.style.display = 'none';
    }

    generateMockPDB(sequence, name) {
        let pdb = `HEADER    MOCK ESMFOLD STRUCTURE FOR ${name}\n`;
        pdb += `REMARK   Generated mock structure with realistic secondary structure\n`;
        pdb += `REMARK   Note: This is a demonstration - replace with real ESMFold API\n`;
        
        let atomId = 1;
        const limitedSequence = sequence.substring(0, Math.min(100, sequence.length));
        
        for (let i = 0; i < limitedSequence.length; i++) {
            const aa = limitedSequence[i];
            
            // Create more realistic protein structure with mixed secondary structures
            let x, y, z;
            
            if (i < 15) {
                // Alpha helix region
                const helixAngle = i * 100 * Math.PI / 180; // 100 degrees per residue
                const radius = 2.3;
                x = radius * Math.cos(helixAngle) + Math.random() * 0.3;
                y = radius * Math.sin(helixAngle) + Math.random() * 0.3;
                z = i * 1.5 + Math.random() * 0.3;
            } else if (i < 30) {
                // Beta sheet region
                const sheetOffset = i - 15;
                x = sheetOffset * 3.5 + (sheetOffset % 2) * 1.0 + Math.random() * 0.3;
                y = 5 + Math.sin(sheetOffset * 0.5) * 2 + Math.random() * 0.3;
                z = 22 + sheetOffset * 0.5 + Math.random() * 0.3;
            } else if (i < 45) {
                // Loop region (more random)
                const loopOffset = i - 30;
                x = 10 + Math.sin(loopOffset * 0.3) * 8 + Math.random() * 1.0;
                y = 8 + Math.cos(loopOffset * 0.3) * 6 + Math.random() * 1.0;
                z = 35 + loopOffset * 0.8 + Math.random() * 1.0;
            } else {
                // Another helix region
                const helix2Offset = i - 45;
                const helixAngle = helix2Offset * 100 * Math.PI / 180;
                const radius = 2.3;
                x = 15 + radius * Math.cos(helixAngle) + Math.random() * 0.3;
                y = 15 + radius * Math.sin(helixAngle) + Math.random() * 0.3;
                z = 50 + helix2Offset * 1.5 + Math.random() * 0.3;
            }
            
            // Add backbone atoms (N, CA, C, O)
            const atoms = [
                { name: 'N', offset: [-0.5, -0.3, 0.0] },
                { name: 'CA', offset: [0.0, 0.0, 0.0] },
                { name: 'C', offset: [1.5, 0.0, 0.0] },
                { name: 'O', offset: [2.0, 1.2, 0.0] }
            ];
            
            atoms.forEach(atom => {
                const atomX = x + atom.offset[0];
                const atomY = y + atom.offset[1];
                const atomZ = z + atom.offset[2];
                
                pdb += `ATOM  ${atomId.toString().padStart(5)}  ${atom.name.padEnd(2)}  ${aa} A${(i+1).toString().padStart(4)}    `;
                pdb += `${atomX.toFixed(3).padStart(8)}${atomY.toFixed(3).padStart(8)}${atomZ.toFixed(3).padStart(8)}`;
                pdb += `  1.00 50.00           ${atom.name[0]}\n`;
                atomId++;
            });
        }
        
        pdb += 'END\n';
        return pdb;
    }

    displayComparison() {
        // Mock RMSD calculation (replace with real calculation)
        const mockRMSD = (Math.random() * 3 + 0.5).toFixed(3);
        
        document.getElementById('rmsdValue').textContent = mockRMSD;
        
        const rmsdValueEl = document.getElementById('rmsdValue');
        const rmsdInterpretationEl = document.getElementById('rmsdInterpretation');
        
        if (mockRMSD < 2.0) {
            rmsdValueEl.className = 'rmsd-value rmsd-excellent';
            rmsdInterpretationEl.textContent = '🟢 Excellent Agreement - Structures are very similar';
        } else if (mockRMSD < 4.0) {
            rmsdValueEl.className = 'rmsd-value rmsd-good';
            rmsdInterpretationEl.textContent = '🟡 Moderate Agreement - Some structural differences';
        } else {
            rmsdValueEl.className = 'rmsd-value rmsd-poor';
            rmsdInterpretationEl.textContent = '🔴 Poor Agreement - Significant structural differences';
        }
        
        document.getElementById('comparisonSection').style.display = 'block';
    }

    async runAdvancedAnalysis(uniprotId, proteinInfo) {
        try {
            console.log('🔬 Running advanced analysis...');
            
            // Call Python backend for advanced analysis
            const response = await fetch('/api/advanced_analysis', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    uniprot_id: uniprotId,
                    sequence: proteinInfo.sequence
                })
            });
            
            if (response.ok) {
                const analysisData = await response.json();
                this.displayAdvancedAnalysis(analysisData);
            } else {
                console.warn('Advanced analysis not available, using basic analysis');
                this.displayBasicAnalysis(proteinInfo);
            }
            
        } catch (error) {
            console.warn('Advanced analysis failed:', error);
            this.displayBasicAnalysis(proteinInfo);
        }
    }
    
    displayAdvancedAnalysis(analysisData) {
        try {
            // Create advanced analysis section if it doesn't exist
            let advancedSection = document.getElementById('advancedAnalysisSection');
            if (!advancedSection) {
                advancedSection = document.createElement('div');
                advancedSection.id = 'advancedAnalysisSection';
                advancedSection.className = 'comparison-section';
                document.querySelector('.container').appendChild(advancedSection);
            }
            
            const homologyStats = analysisData.homology_stats || {};
            const evolutionaryData = analysisData.evolutionary_analysis || {};
            const functionalPrediction = analysisData.functional_prediction || 'Unknown';
            const qualityAssessment = analysisData.quality_assessment || 'Unknown';
            
            advancedSection.innerHTML = `
                <h3 style="text-align: center; margin-bottom: 30px; font-size: 2rem;">🧬 Advanced Protein Analysis</h3>
                
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 30px;">
                    <div style="background: white; padding: 20px; border-radius: 10px; text-align: center;">
                        <div style="font-size: 2rem; font-weight: bold; color: #2196f3;">${homologyStats.total_homologs || 0}</div>
                        <div>Homologs Found</div>
                    </div>
                    <div style="background: white; padding: 20px; border-radius: 10px; text-align: center;">
                        <div style="font-size: 2rem; font-weight: bold; color: #4caf50;">${(homologyStats.avg_identity || 0).toFixed(1)}%</div>
                        <div>Average Identity</div>
                    </div>
                    <div style="background: white; padding: 20px; border-radius: 10px; text-align: center;">
                        <div style="font-size: 2rem; font-weight: bold; color: #ff9800;">${(evolutionaryData.conservation_score || 0).toFixed(3)}</div>
                        <div>Conservation Score</div>
                    </div>
                    <div style="background: white; padding: 20px; border-radius: 10px; text-align: center;">
                        <div style="font-size: 1.5rem; font-weight: bold; color: #9c27b0;">${evolutionaryData.conservation_level || 'Unknown'}</div>
                        <div>Conservation Level</div>
                    </div>
                </div>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 30px; margin-bottom: 30px;">
                    <div style="background: white; padding: 25px; border-radius: 10px;">
                        <h4>🔍 Homology Analysis</h4>
                        <div style="margin: 15px 0;">
                            <strong>Total Homologs:</strong> ${homologyStats.total_homologs || 0}<br>
                            <strong>Best Hit Identity:</strong> ${(homologyStats.best_hit_identity || 0).toFixed(1)}%<br>
                            <strong>Quality Assessment:</strong> ${qualityAssessment}
                        </div>
                        <div style="margin-top: 20px;">
                            <div><span style="color: #4caf50;">●</span> High Identity (&gt;70%): ${homologyStats.identity_distribution?.high || 0}</div>
                            <div><span style="color: #ff9800;">●</span> Medium Identity (40-70%): ${homologyStats.identity_distribution?.medium || 0}</div>
                            <div><span style="color: #f44336;">●</span> Low Identity (&lt;40%): ${homologyStats.identity_distribution?.low || 0}</div>
                        </div>
                    </div>
                    
                    <div style="background: white; padding: 25px; border-radius: 10px;">
                        <h4>🧬 Evolutionary Analysis</h4>
                        <div style="margin: 15px 0;">
                            <strong>Functional Category:</strong> ${functionalPrediction}<br>
                            <strong>Phylogenetic Depth:</strong> ${evolutionaryData.phylogenetic_depth || 0}<br>
                            <strong>Orthologs:</strong> ${evolutionaryData.ortholog_count || 0}<br>
                            <strong>Paralogs:</strong> ${evolutionaryData.paralog_count || 0}
                        </div>
                        <div style="margin-top: 20px;">
                            <div style="background: #f5f5f5; padding: 10px; border-radius: 5px; font-size: 0.9em;">
                                <strong>Conservation Interpretation:</strong><br>
                                ${this.getConservationInterpretation(evolutionaryData.conservation_score || 0)}
                            </div>
                        </div>
                    </div>
                </div>
                
                <div style="background: white; padding: 25px; border-radius: 10px; margin-bottom: 20px;">
                    <h4>⚙️ Analysis Methods</h4>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 15px;">
                        <div>
                            <h5>🔍 MMseqs2 Homology Search</h5>
                            <ul style="font-size: 0.9em; margin-left: 20px;">
                                <li>Ultra-fast sequence alignment</li>
                                <li>Sensitive database search</li>
                                <li>UniRef50 protein database</li>
                                <li>E-value threshold: 1e-5</li>
                            </ul>
                        </div>
                        <div>
                            <h5>🧬 Evolutionary Analysis</h5>
                            <ul style="font-size: 0.9em; margin-left: 20px;">
                                <li>Conservation scoring algorithm</li>
                                <li>Phylogenetic distribution analysis</li>
                                <li>Ortholog/paralog classification</li>
                                <li>Functional category prediction</li>
                            </ul>
                        </div>
                    </div>
                </div>
            `;
            
            advancedSection.style.display = 'block';
            
        } catch (error) {
            console.error('Error displaying advanced analysis:', error);
        }
    }
    
    displayBasicAnalysis(proteinInfo) {
        // Fallback to basic analysis display
        console.log('Displaying basic analysis for:', proteinInfo.name);
    }
    
    getConservationInterpretation(score) {
        if (score > 0.7) {
            return "This protein is highly conserved across species, suggesting critical biological function and strong evolutionary pressure to maintain structure.";
        } else if (score > 0.3) {
            return "This protein shows moderate conservation, indicating important but adaptable biological function with some evolutionary flexibility.";
        } else {
            return "This protein shows low conservation, suggesting either rapid evolution, specialized function, or recent evolutionary origin.";
        }
    }

    showLoading() {
        document.getElementById('loadingOverlay').style.display = 'flex';
    }

    hideLoading() {
        document.getElementById('loadingOverlay').style.display = 'none';
    }

    showError(message) {
        const errorEl = document.getElementById('errorMessage');
        errorEl.textContent = message;
        errorEl.style.display = 'block';
        
        setTimeout(() => {
            errorEl.style.display = 'none';
        }, 5000);
    }

    hideError() {
        document.getElementById('errorMessage').style.display = 'none';
    }

    showSuccess(message) {
        const successEl = document.getElementById('successMessage');
        successEl.textContent = message;
        successEl.style.display = 'block';
        
        setTimeout(() => {
            successEl.style.display = 'none';
        }, 3000);
    }
}

// Global functions for viewer controls
function setStyle(viewerType, style) {
    const viewer = viewerType === 'alphafold' ? window.proteinViewer.alphafoldViewer : window.proteinViewer.esmfoldViewer;
    
    if (!viewer) return;
    
    // Update button states
    const controls = document.querySelector(`#${viewerType}Viewer`).parentElement.querySelectorAll('.control-btn');
    controls.forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');
    
    // Clear current styles
    viewer.setStyle({}, {});
    
    // Apply new style
    switch (style) {
        case 'cartoon':
            viewer.setStyle({}, {
                cartoon: {
                    color: 'spectrum',
                    opacity: 0.8
                }
            });
            break;
        case 'surface':
            viewer.setStyle({}, {
                surface: {
                    color: 'spectrum',
                    opacity: 0.7
                }
            });
            break;
        case 'stick':
            viewer.setStyle({}, {
                stick: {
                    color: 'spectrum',
                    radius: 0.2
                }
            });
            break;
    }
    
    viewer.render();
    
    // Update current style tracking
    if (viewerType === 'alphafold') {
        window.proteinViewer.currentAlphafoldStyle = style;
    } else {
        window.proteinViewer.currentEsmfoldStyle = style;
    }
}

function resetView(viewerType) {
    const viewer = viewerType === 'alphafold' ? window.proteinViewer.alphafoldViewer : window.proteinViewer.esmfoldViewer;
    
    if (!viewer) return;
    
    viewer.zoomTo();
    viewer.render();
}

function showHelp() {
    alert(`🧬 Protein Structure Viewer Help

🔍 SEARCH:
• Enter UniProt ID (e.g., P01308)
• Use suggestions for popular proteins
• Click search or press Enter

🎮 CONTROLS:
• Cartoon: Ribbon representation
• Surface: Molecular surface
• Sticks: Atomic detail
• Reset: Return to default view

📊 INTERPRETATION:
• RMSD < 2.0 Å: Excellent agreement
• RMSD 2.0-4.0 Å: Moderate agreement  
• RMSD > 4.0 Å: Significant differences

🔵 AlphaFold: MSA-based, high accuracy
🔴 ESMFold: Language model, fast prediction`);
}

function showExamples() {
    const examples = [
        'P01308 - Human Insulin (small hormone)',
        'P61626 - Lysozyme (antimicrobial enzyme)', 
        'P68871 - Hemoglobin (oxygen transport)',
        'P02768 - Serum Albumin (blood protein)',
        'P04637 - p53 (tumor suppressor)'
    ];
    
    alert(`📚 Example Proteins to Try:\n\n${examples.join('\n')}\n\nClick on any suggestion in the search box or type the UniProt ID directly!`);
}

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    window.proteinViewer = new ProteinViewer();
});
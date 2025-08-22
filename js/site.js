/**
 * Site-specific JavaScript functionality
 * Additional utilities and features for the protein viewer
 */

// Utility functions
const Utils = {
    // Format numbers with proper units
    formatNumber: (num, decimals = 2) => {
        if (num >= 1000000) {
            return (num / 1000000).toFixed(decimals) + 'M';
        } else if (num >= 1000) {
            return (num / 1000).toFixed(decimals) + 'K';
        }
        return num.toFixed(decimals);
    },

    // Debounce function for search
    debounce: (func, wait) => {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },

    // Copy text to clipboard
    copyToClipboard: (text) => {
        navigator.clipboard.writeText(text).then(() => {
            console.log('Copied to clipboard:', text);
        }).catch(err => {
            console.error('Failed to copy:', err);
        });
    },

    // Download data as file
    downloadFile: (content, filename, contentType = 'text/plain') => {
        const blob = new Blob([content], { type: contentType });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
    }
};

// Advanced search functionality
class AdvancedSearch {
    constructor() {
        this.searchHistory = this.loadSearchHistory();
        this.initializeAdvancedFeatures();
    }

    initializeAdvancedFeatures() {
        this.setupKeyboardShortcuts();
        this.setupSearchHistory();
        this.setupQuickActions();
    }

    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Ctrl/Cmd + K for quick search
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                document.getElementById('proteinSearch').focus();
            }

            // Escape to clear search
            if (e.key === 'Escape') {
                document.getElementById('proteinSearch').value = '';
                document.getElementById('proteinSearch').blur();
            }

            // Enter on suggestions
            if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
                this.navigateSuggestions(e.key === 'ArrowDown' ? 1 : -1);
                e.preventDefault();
            }
        });
    }

    setupSearchHistory() {
        // Add current search to history
        const originalSearch = window.proteinViewer.searchProtein.bind(window.proteinViewer);
        window.proteinViewer.searchProtein = (uniprotId) => {
            this.addToHistory(uniprotId);
            return originalSearch(uniprotId);
        };
    }

    setupQuickActions() {
        // Add quick action buttons
        this.addQuickActionButtons();
    }

    addQuickActionButtons() {
        const container = document.querySelector('.header-content');
        const quickActions = document.createElement('div');
        quickActions.className = 'quick-actions';
        quickActions.innerHTML = `
            <button class="control-btn" onclick="AdvancedSearch.showHistory()" title="Search History">
                📂 History
            </button>
            <button class="control-btn" onclick="AdvancedSearch.exportData()" title="Export Current Data">
                💾 Export
            </button>
            <button class="control-btn" onclick="AdvancedSearch.fullscreen()" title="Toggle Fullscreen">
                🔲 Fullscreen
            </button>
        `;
        
        // Insert before existing buttons if they exist
        const existingButtons = container.querySelector('div[style*="flex"]');
        if (existingButtons) {
            container.insertBefore(quickActions, existingButtons);
        } else {
            container.appendChild(quickActions);
        }
    }

    addToHistory(uniprotId) {
        const timestamp = new Date().toISOString();
        const historyItem = { uniprotId, timestamp };
        
        // Remove if already exists
        this.searchHistory = this.searchHistory.filter(item => item.uniprotId !== uniprotId);
        
        // Add to beginning
        this.searchHistory.unshift(historyItem);
        
        // Keep only last 20 items
        this.searchHistory = this.searchHistory.slice(0, 20);
        
        this.saveSearchHistory();
    }

    loadSearchHistory() {
        try {
            return JSON.parse(localStorage.getItem('proteinSearchHistory')) || [];
        } catch {
            return [];
        }
    }

    saveSearchHistory() {
        try {
            localStorage.setItem('proteinSearchHistory', JSON.stringify(this.searchHistory));
        } catch (e) {
            console.warn('Could not save search history:', e);
        }
    }

    static showHistory() {
        const history = window.advancedSearch.searchHistory;
        if (history.length === 0) {
            alert('No search history available');
            return;
        }

        const historyList = history.map(item => {
            const date = new Date(item.timestamp).toLocaleDateString();
            return `${item.uniprotId} (${date})`;
        }).join('\n');

        const selection = prompt(`Search History:\n\n${historyList}\n\nEnter UniProt ID to search:`);
        if (selection) {
            window.proteinViewer.searchProtein(selection.trim().toUpperCase());
        }
    }

    static exportData() {
        if (!window.proteinViewer.currentProtein) {
            alert('No protein data to export');
            return;
        }

        const protein = window.proteinViewer.currentProtein;
        const exportData = {
            protein: protein,
            timestamp: new Date().toISOString(),
            rmsd: document.getElementById('rmsdValue').textContent,
            exportedFrom: 'Protein Structure Viewer'
        };

        const jsonData = JSON.stringify(exportData, null, 2);
        Utils.downloadFile(jsonData, `${protein.uniprotId}_analysis.json`, 'application/json');
    }

    static fullscreen() {
        if (document.fullscreenElement) {
            document.exitFullscreen();
        } else {
            document.documentElement.requestFullscreen();
        }
    }

    navigateSuggestions(direction) {
        const suggestions = document.querySelectorAll('.suggestion-item:not([style*="none"])');
        if (suggestions.length === 0) return;

        let currentIndex = -1;
        suggestions.forEach((item, index) => {
            if (item.classList.contains('highlighted')) {
                currentIndex = index;
                item.classList.remove('highlighted');
            }
        });

        const newIndex = Math.max(0, Math.min(suggestions.length - 1, currentIndex + direction));
        suggestions[newIndex].classList.add('highlighted');
        
        // Update search input
        const uniprotId = suggestions[newIndex].dataset.uniprot;
        const text = suggestions[newIndex].textContent;
        document.getElementById('proteinSearch').value = text;
    }
}

// Performance monitoring
class PerformanceMonitor {
    constructor() {
        this.metrics = {};
        this.startTime = performance.now();
        this.setupPerformanceTracking();
    }

    setupPerformanceTracking() {
        // Track page load time
        window.addEventListener('load', () => {
            this.metrics.pageLoadTime = performance.now() - this.startTime;
            console.log(`Page loaded in ${this.metrics.pageLoadTime.toFixed(2)}ms`);
        });

        // Track viewer initialization
        const originalShow3DViewers = window.proteinViewer?.show3DViewers;
        if (originalShow3DViewers) {
            window.proteinViewer.show3DViewers = () => {
                const start = performance.now();
                originalShow3DViewers.call(window.proteinViewer);
                this.metrics.viewerInitTime = performance.now() - start;
                console.log(`3D viewers initialized in ${this.metrics.viewerInitTime.toFixed(2)}ms`);
            };
        }
    }

    getMetrics() {
        return {
            ...this.metrics,
            memoryUsage: performance.memory ? {
                used: Math.round(performance.memory.usedJSHeapSize / 1024 / 1024),
                total: Math.round(performance.memory.totalJSHeapSize / 1024 / 1024),
                limit: Math.round(performance.memory.jsHeapSizeLimit / 1024 / 1024)
            } : null
        };
    }
}

// Responsive design handler
class ResponsiveHandler {
    constructor() {
        this.breakpoints = {
            mobile: 768,
            tablet: 1024,
            desktop: 1200
        };
        
        this.setupResponsiveFeatures();
    }

    setupResponsiveFeatures() {
        window.addEventListener('resize', Utils.debounce(() => {
            this.handleResize();
        }, 250));

        // Initial setup
        this.handleResize();
    }

    handleResize() {
        const width = window.innerWidth;
        
        if (width < this.breakpoints.mobile) {
            this.enableMobileMode();
        } else if (width < this.breakpoints.tablet) {
            this.enableTabletMode();
        } else {
            this.enableDesktopMode();
        }

        // Refresh 3D viewers if they exist
        this.refresh3DViewers();
    }

    enableMobileMode() {
        document.body.classList.add('mobile-mode');
        document.body.classList.remove('tablet-mode', 'desktop-mode');
        
        // Stack viewers vertically on mobile
        const viewersContainer = document.getElementById('viewersContainer');
        if (viewersContainer) {
            viewersContainer.style.gridTemplateColumns = '1fr';
        }
    }

    enableTabletMode() {
        document.body.classList.add('tablet-mode');
        document.body.classList.remove('mobile-mode', 'desktop-mode');
    }

    enableDesktopMode() {
        document.body.classList.add('desktop-mode');
        document.body.classList.remove('mobile-mode', 'tablet-mode');
        
        // Side-by-side viewers on desktop
        const viewersContainer = document.getElementById('viewersContainer');
        if (viewersContainer) {
            viewersContainer.style.gridTemplateColumns = '1fr 1fr';
        }
    }

    refresh3DViewers() {
        // Refresh 3D viewers after resize
        setTimeout(() => {
            if (window.proteinViewer?.alphafoldViewer) {
                window.proteinViewer.alphafoldViewer.resize();
                window.proteinViewer.alphafoldViewer.render();
            }
            if (window.proteinViewer?.esmfoldViewer) {
                window.proteinViewer.esmfoldViewer.resize();
                window.proteinViewer.esmfoldViewer.render();
            }
        }, 100);
    }
}

// Error handling and logging
class ErrorHandler {
    constructor() {
        this.setupGlobalErrorHandling();
    }

    setupGlobalErrorHandling() {
        window.addEventListener('error', (event) => {
            this.logError('JavaScript Error', event.error);
        });

        window.addEventListener('unhandledrejection', (event) => {
            this.logError('Unhandled Promise Rejection', event.reason);
        });
    }

    logError(type, error) {
        console.error(`${type}:`, error);
        
        // Show user-friendly error message
        if (window.proteinViewer) {
            window.proteinViewer.showError('An unexpected error occurred. Please try again.');
        }
    }
}

// Initialize additional features when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    // Initialize advanced features
    window.advancedSearch = new AdvancedSearch();
    window.performanceMonitor = new PerformanceMonitor();
    window.responsiveHandler = new ResponsiveHandler();
    window.errorHandler = new ErrorHandler();
    
    console.log('🧬 Protein Structure Viewer - Advanced features loaded');
});

// Add CSS for highlighted suggestions
const style = document.createElement('style');
style.textContent = `
    .suggestion-item.highlighted {
        background: #e3f2fd !important;
        border-left: 3px solid #2196f3;
    }
    
    .quick-actions {
        display: flex;
        gap: 10px;
        align-items: center;
    }
    
    @media (max-width: 768px) {
        .quick-actions {
            flex-direction: column;
            gap: 5px;
        }
        
        .quick-actions .control-btn {
            font-size: 0.8rem;
            padding: 6px 10px;
        }
    }
`;
document.head.appendChild(style);
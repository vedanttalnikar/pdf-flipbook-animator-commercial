// PDF Flipbook Animator - Realistic Animation Mode
// Using StPageFlip library for realistic 3D page curl effect

class Flipbook {
    constructor() {
        this.currentPage = 1;
        this.totalPages = parseInt(document.getElementById('total-pages').textContent);
        this.pageFlip = null;
        this.images = [];
        this.isInitialized = false;
        
        // Collect all image paths
        document.querySelectorAll('.page img').forEach(img => {
            this.images.push(img.src);
        });
        
        this.loadStPageFlip();
    }

    loadStPageFlip() {
        // Check if StPageFlip is already loaded
        if (typeof St !== 'undefined' && St.PageFlip) {
            this.init();
            return;
        }

        // Load StPageFlip from CDN
        const script = document.createElement('script');
        script.src = 'https://unpkg.com/page-flip@2.0.7/dist/js/page-flip.browser.js';
        script.onload = () => {
            console.log('StPageFlip library loaded');
            this.init();
        };
        script.onerror = () => {
            console.error('Failed to load StPageFlip library. Falling back to simple mode.');
            this.fallbackToSimpleMode();
        };
        document.head.appendChild(script);
    }

    init() {
        if (this.isInitialized) return;
        
        // Hide original pages
        document.querySelectorAll('.page').forEach(page => {
            page.style.display = 'none';
        });

        // Create new container for StPageFlip
        const viewer = document.getElementById('flipbook-viewer');
        viewer.innerHTML = '';
        
        const flipbookContainer = document.createElement('div');
        flipbookContainer.id = 'stpageflip-container';
        flipbookContainer.style.cssText = 'width: 100%; height: 100%;';
        viewer.appendChild(flipbookContainer);

        // Calculate dimensions
        const viewerWidth = viewer.clientWidth;
        const viewerHeight = viewer.clientHeight;
        const pageWidth = Math.min(viewerWidth / 2, 600);
        const pageHeight = Math.min(viewerHeight, 800);

        try {
            // Initialize StPageFlip
            this.pageFlip = new St.PageFlip(flipbookContainer, {
                width: pageWidth,
                height: pageHeight,
                size: 'stretch',
                minWidth: 315,
                maxWidth: 1000,
                minHeight: 400,
                maxHeight: 1533,
                maxShadowOpacity: 0.5,
                showCover: true,
                mobileScrollSupport: true,
                swipeDistance: 30,
                clickEventForward: true,
                usePortrait: true,
                startPage: 0,
                drawShadow: true,
                flippingTime: 800,
                useMouseEvents: true,
                autoSize: true,
                showPageCorners: true,
                disableFlipByClick: false
            });

            // Load pages as HTML elements
            this.pageFlip.loadFromImages(this.images);

            // Setup event listeners
            this.setupPageFlipEvents();
            this.setupControls();
            this.setupKeyboard();
            
            // Restore saved position
            this.restorePosition();

            this.isInitialized = true;

            // Hide loading spinner
            const loading = document.getElementById('loading');
            if (loading) {
                loading.classList.remove('show');
            }

            console.log(`Flipbook initialized with ${this.totalPages} pages (Realistic mode with StPageFlip)`);
        } catch (error) {
            console.error('Error initializing StPageFlip:', error);
            this.fallbackToSimpleMode();
        }
    }

    setupPageFlipEvents() {
        if (!this.pageFlip) return;

        // Listen to page flip events
        this.pageFlip.on('flip', (e) => {
            this.currentPage = e.data + 1;
            this.updateUI();
            this.savePosition();
        });

        this.pageFlip.on('changeOrientation', (e) => {
            console.log('Orientation changed:', e.data);
        });

        this.pageFlip.on('changeState', (e) => {
            console.log('State changed:', e.data);
        });
    }

    setupControls() {
        const prevBtn = document.getElementById('prev-btn');
        const nextBtn = document.getElementById('next-btn');
        const fullscreenBtn = document.getElementById('fullscreen-btn');

        if (prevBtn) {
            prevBtn.addEventListener('click', () => this.previousPage());
        }

        if (nextBtn) {
            nextBtn.addEventListener('click', () => this.nextPage());
        }

        if (fullscreenBtn) {
            fullscreenBtn.addEventListener('click', () => this.toggleFullscreen());
        }
    }

    setupKeyboard() {
        document.addEventListener('keydown', (e) => {
            switch(e.key) {
                case 'ArrowLeft':
                case 'ArrowUp':
                case 'PageUp':
                    e.preventDefault();
                    this.previousPage();
                    break;
                case 'ArrowRight':
                case 'ArrowDown':
                case 'PageDown':
                case ' ':
                    e.preventDefault();
                    this.nextPage();
                    break;
                case 'Home':
                    e.preventDefault();
                    this.goToPage(1);
                    break;
                case 'End':
                    e.preventDefault();
                    this.goToPage(this.totalPages);
                    break;
                case 'f':
                case 'F':
                    e.preventDefault();
                    this.toggleFullscreen();
                    break;
            }
        });
    }

    nextPage() {
        if (this.pageFlip) {
            this.pageFlip.flipNext();
        }
    }

    previousPage() {
        if (this.pageFlip) {
            this.pageFlip.flipPrev();
        }
    }

    goToPage(pageNum) {
        if (this.pageFlip && pageNum >= 1 && pageNum <= this.totalPages) {
            this.pageFlip.flip(pageNum - 1);
        }
    }

    updateUI() {
        // Update page indicator
        const currentPageEl = document.getElementById('current-page');
        if (currentPageEl) {
            currentPageEl.textContent = this.currentPage;
        }

        // Update buttons
        const prevBtn = document.getElementById('prev-btn');
        const nextBtn = document.getElementById('next-btn');

        if (prevBtn) {
            prevBtn.disabled = this.currentPage === 1;
        }

        if (nextBtn) {
            nextBtn.disabled = this.currentPage === this.totalPages;
        }

        // Update progress bar
        const progress = document.getElementById('progress');
        if (progress) {
            const percentage = (this.currentPage / this.totalPages) * 100;
            progress.style.width = percentage + '%';
        }
    }

    toggleFullscreen() {
        const container = document.querySelector('.container');
        
        if (!document.fullscreenElement) {
            if (container.requestFullscreen) {
                container.requestFullscreen();
            } else if (container.webkitRequestFullscreen) {
                container.webkitRequestFullscreen();
            } else if (container.msRequestFullscreen) {
                container.msRequestFullscreen();
            }
        } else {
            if (document.exitFullscreen) {
                document.exitFullscreen();
            } else if (document.webkitExitFullscreen) {
                document.webkitExitFullscreen();
            } else if (document.msExitFullscreen) {
                document.msExitFullscreen();
            }
        }
    }

    savePosition() {
        try {
            localStorage.setItem('flipbook_current_page', this.currentPage);
        } catch (e) {
            console.warn('Could not save position:', e);
        }
    }

    restorePosition() {
        try {
            const savedPage = localStorage.getItem('flipbook_current_page');
            if (savedPage) {
                const pageNum = parseInt(savedPage);
                if (pageNum >= 1 && pageNum <= this.totalPages) {
                    this.currentPage = pageNum;
                    if (this.pageFlip) {
                        this.pageFlip.flip(pageNum - 1);
                    }
                }
            }
        } catch (e) {
            console.warn('Could not restore position:', e);
        }
    }

    fallbackToSimpleMode() {
        console.warn('Falling back to simple animation mode');
        
        // Restore original pages
        document.querySelectorAll('.page').forEach(page => {
            page.style.display = '';
        });

        // Load simple flipbook script
        const script = document.createElement('script');
        script.textContent = `
            // Simple fallback implementation
            class SimpleFlipbook {
                constructor() {
                    this.currentPage = 1;
                    this.totalPages = ${this.totalPages};
                    this.pages = document.querySelectorAll('.page');
                    this.showPage(1);
                }
                showPage(n) {
                    this.pages.forEach(p => p.classList.remove('active'));
                    if (this.pages[n-1]) {
                        this.pages[n-1].classList.add('active');
                        this.currentPage = n;
                    }
                }
                nextPage() {
                    if (this.currentPage < this.totalPages) this.showPage(this.currentPage + 1);
                }
                previousPage() {
                    if (this.currentPage > 1) this.showPage(this.currentPage - 1);
                }
            }
            window.flipbook = new SimpleFlipbook();
        `;
        document.body.appendChild(script);
        
        // Hide loading spinner
        const loading = document.getElementById('loading');
        if (loading) {
            loading.classList.remove('show');
        }
    }
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        new Flipbook();
    });
} else {
    new Flipbook();
}

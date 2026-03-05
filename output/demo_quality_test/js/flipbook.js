// PDF Flipbook Animator - Realistic Animation Mode
// Using StPageFlip library for realistic 3D page curl effect

class Flipbook {
    constructor() {
        this.currentPage = 1;
        this.totalPages = parseInt(document.getElementById('total-pages').textContent);
        this.pageFlip = null;
        this.images = [];
        this.isInitialized = false;
        this.isResizing = false;
        this.resizeTimeout = null;
        this.aspectRatio = null;
        this.isMobileMode = false; // Track if in mobile (single-page) mode
        this.indexPage = parseInt(document.getElementById('index-btn')?.dataset.indexPage || 2);
        
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

    calculateResponsiveDimensions(aspectRatio) {
        const screenWidth = window.innerWidth;
        const screenHeight = window.innerHeight;
        const pixelRatio = window.devicePixelRatio || 1;
        const isMobile = screenWidth < 768;
        const isTablet = screenWidth >= 768 && screenWidth < 1024;
        const isDesktop = screenWidth >= 1024;

        // Side panels take horizontal space, full vertical height available
        let sidePanelWidth = 260; // 80px left + 180px right
        if (isMobile) sidePanelWidth = 110; // 50px + 60px
        else if (isTablet) sidePanelWidth = 210; // 70px + 140px
        
        const availableHeight = screenHeight - 10; // Almost full height!
        const availableWidth = screenWidth - sidePanelWidth - 20;

        let pageWidth, pageHeight;

        if (isMobile) {
            // Mobile: single page, 95% width
            pageWidth = Math.floor(availableWidth * 0.95);
            pageHeight = Math.floor(pageWidth / aspectRatio);
            
            if (pageHeight > availableHeight) {
                pageHeight = Math.floor(availableHeight);
                pageWidth = Math.floor(pageHeight * aspectRatio);
            }
        } else if (isTablet) {
            // Tablet: single page, 90% width
            pageWidth = Math.floor(availableWidth * 0.9);
            pageHeight = Math.floor(pageWidth / aspectRatio);
            
            if (pageHeight > availableHeight) {
                pageHeight = Math.floor(availableHeight);
                pageWidth = Math.floor(pageHeight * aspectRatio);
            }
        } else {
            // Desktop: two-page spread
            pageWidth = Math.floor(availableWidth / 2.05); // Account for gap
            pageHeight = Math.floor(pageWidth / aspectRatio);
            
            if (pageHeight > availableHeight) {
                pageHeight = Math.floor(availableHeight);
                pageWidth = Math.floor(pageHeight * aspectRatio);
            }
        }

        // Scale dimensions for high-DPI displays
        const scaledWidth = Math.floor(pageWidth * pixelRatio);
        const scaledHeight = Math.floor(pageHeight * pixelRatio);

        console.log(`📱 Responsive dimensions calculated:`);
        console.log(`  Screen: ${screenWidth}x${screenHeight}`);
        console.log(`  Pixel Ratio: ${pixelRatio}x`);
        console.log(`  Mode: ${isMobile ? 'Mobile' : isTablet ? 'Tablet' : 'Desktop'}`);
        console.log(`  Display size: ${pageWidth}x${pageHeight}`);
        console.log(`  Canvas size: ${scaledWidth}x${scaledHeight}`);
        console.log(`  Available: ${availableWidth}x${availableHeight}`);

        return {
            pageWidth: scaledWidth,
            pageHeight: scaledHeight,
            displayWidth: pageWidth,
            displayHeight: pageHeight,
            pixelRatio,
            isMobile,
            isTablet,
            isDesktop
        };
    }

    setupResponsiveResize() {
        const handleResize = () => {
            if (this.isResizing) return;
            
            clearTimeout(this.resizeTimeout);
            this.resizeTimeout = setTimeout(() => {
                console.log('🔄 Window resized, reinitializing flipbook...');
                this.reinitialize();
            }, 300);
        };

        window.addEventListener('resize', handleResize);
        window.addEventListener('orientationchange', () => {
            setTimeout(() => {
                console.log('🔄 Orientation changed, reinitializing flipbook...');
                this.reinitialize();
            }, 100);
        });
    }

    reinitialize() {
        if (!this.aspectRatio) return;
        
        this.isResizing = true;
        
        // Save current page
        const savedPage = this.currentPage;
        
        // Destroy existing pageFlip
        if (this.pageFlip) {
            try {
                this.pageFlip.destroy();
            } catch (e) {
                console.warn('Error destroying pageFlip:', e);
            }
            this.pageFlip = null;
        }
        
        // Mark as not initialized
        this.isInitialized = false;
        
        // Reinitialize with new dimensions
        setTimeout(() => {
            this.initializeFlipbook(this.aspectRatio, savedPage - 1);
            this.isResizing = false;
        }, 100);
    }

    init() {
        if (this.isInitialized) return;
        
        // Load first image to get aspect ratio
        const firstImg = new Image();
        firstImg.src = this.images[0];
        
        firstImg.onload = () => {
            // Get natural image dimensions
            const naturalWidth = firstImg.naturalWidth;
            const naturalHeight = firstImg.naturalHeight;
            this.aspectRatio = naturalWidth / naturalHeight;
            
            console.log(`📄 Original page dimensions: ${naturalWidth}x${naturalHeight}, aspect ratio: ${this.aspectRatio.toFixed(2)}`);
            
            this.initializeFlipbook(this.aspectRatio, 0);
            this.setupResponsiveResize();
        };
        
        firstImg.onerror = () => {
            console.error('Failed to load first image, falling back to simple mode');
            this.fallbackToSimpleMode();
        };
    }

    initializeFlipbook(aspectRatio, startPage = 0) {
        // Hide original pages
        document.querySelectorAll('.page').forEach(page => {
            page.style.display = 'none';
        });

        // Create new container for StPageFlip
        const viewer = document.getElementById('flipbook');
        
        // Clear the container
        viewer.innerHTML = '';
        
        const flipbookContainer = document.createElement('div');
        flipbookContainer.id = 'stpageflip-container';
        flipbookContainer.style.cssText = 'width: 100%; height: 100%;';
        viewer.appendChild(flipbookContainer);

        // Calculate responsive dimensions
        const dimensions = this.calculateResponsiveDimensions(aspectRatio);
        
        // Store mobile mode state for navigation
        this.isMobileMode = dimensions.isMobile;

        try {
            // Initialize StPageFlip with responsive dimensions
            this.pageFlip = new St.PageFlip(flipbookContainer, {
                width: dimensions.displayWidth,
                height: dimensions.displayHeight,
                size: 'fixed',
                minWidth: 315,
                maxWidth: 2000,
                minHeight: 400,
                maxHeight: 3000,
                maxShadowOpacity: 0.6,
                showCover: !dimensions.isMobile, // No cover on mobile
                mobileScrollSupport: true,
                swipeDistance: 50,
                clickEventForward: true,
                usePortrait: true,
                startPage: startPage,
                startZIndex: 0,
                drawShadow: true,
                flippingTime: 1000,
                useMouseEvents: true,
                autoSize: true,
                showPageCorners: true,
                disableFlipByClick: false
            });

            // Create HTML pages for better quality (avoids canvas downscaling)
            const pages = this.images.map((src, index) => {
                const page = document.createElement('div');
                page.className = 'stf__item';
                page.innerHTML = `
                    <img 
                        src="${src}" 
                        alt="Page ${index + 1}"
                        style="width: 100%; height: 100%; object-fit: contain;"
                        loading="${index < 4 ? 'eager' : 'lazy'}"
                    />
                `;
                return page;
            });

            // Load pages as HTML elements (better quality than canvas)
            this.pageFlip.loadFromHTML(pages);

            // Diagnostic logging for quality verification
            setTimeout(() => {
                // Get first image for dimension check
                const firstImg = new Image();
                firstImg.src = this.images[0];
                firstImg.onload = () => {
                    console.log('🔍 IMAGE QUALITY DIAGNOSTIC:');
                    console.log(`  Source image: ${firstImg.naturalWidth}x${firstImg.naturalHeight}px`);
                    console.log(`  Display size: ${dimensions.displayWidth}x${dimensions.displayHeight}px`);
                    
                    const downscaleRatio = firstImg.naturalWidth / dimensions.displayWidth;
                    const pixelLoss = ((1 - (dimensions.displayWidth * dimensions.displayHeight) / (firstImg.naturalWidth * firstImg.naturalHeight)) * 100);
                    
                    console.log(`  Downscaling ratio: ${downscaleRatio.toFixed(2)}:1`);
                    console.log(`  Pixel loss: ${pixelLoss.toFixed(1)}%`);
                    console.log(`  Quality: ${pixelLoss < 50 ? '✅ Good' : pixelLoss < 75 ? '⚠️  Acceptable' : '❌ Poor'}`);
                };

                // Apply high-quality rendering to any canvas elements
                const canvases = flipbookContainer.querySelectorAll('canvas');
                if (canvases.length > 0) {
                    console.log(`📊 Found ${canvases.length} canvas elements, applying HQ smoothing`);
                    canvases.forEach(canvas => {
                        const ctx = canvas.getContext('2d');
                        if (ctx) {
                            ctx.imageSmoothingEnabled = true;
                            ctx.imageSmoothingQuality = 'high';
                        }
                    });
                } else {
                    console.log('✅ Using HTML mode - no canvas downscaling');
                }
            }, 200);

            // Setup event listeners (only once)
            if (!this.isInitialized) {
                this.setupPageFlipEvents();
                this.setupControls();
                this.setupKeyboard();
                
                // Only restore position if not a fresh start (startPage provided)
                if (startPage > 0) {
                    this.restorePosition();
                } else {
                    // Start at page 1 for new sessions
                    this.currentPage = 1;
                    this.updateUI();
                }
            } else {
                // Just update the page
                this.currentPage = startPage + 1;
                this.updateUI();
            }

            this.isInitialized = true;

            // Hide loading spinner
            const loading = document.getElementById('loading');
            if (loading) {
                loading.classList.remove('show');
            }

            console.log(`✅ Flipbook initialized with ${this.totalPages} pages (Fully Responsive Realistic mode)`);
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
        const indexBtn = document.getElementById('index-btn');
        const fullscreenBtn = document.getElementById('fullscreen-btn');

        if (prevBtn) {
            prevBtn.addEventListener('click', () => this.previousPage());
        }

        if (nextBtn) {
            nextBtn.addEventListener('click', () => this.nextPage());
        }

        if (indexBtn) {
            indexBtn.addEventListener('click', () => this.goToPage(this.indexPage));
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
        if (!this.pageFlip) return;
        
        try {
            // Get the actual current page index from StPageFlip (0-based)
            const currentIndex = this.pageFlip.getCurrentPageIndex();
            
            // In two-page spread mode (desktop/tablet), we need to skip by 2
            // In single-page mode (mobile), we skip by 1
            const increment = this.isMobileMode ? 1 : 2;
            const nextIndex = currentIndex + increment;
            
            // Check if we can move forward
            if (nextIndex < this.totalPages) {
                this.pageFlip.flip(nextIndex);
            }
        } catch (e) {
            console.warn('Error in nextPage:', e);
        }
    }

    previousPage() {
        if (!this.pageFlip) return;
        
        try {
            // Get the actual current page index from StPageFlip (0-based)
            const currentIndex = this.pageFlip.getCurrentPageIndex();
            
            // In two-page spread mode (desktop/tablet), we need to skip by 2
            // In single-page mode (mobile), we skip by 1
            const decrement = this.isMobileMode ? 1 : 2;
            const prevIndex = currentIndex - decrement;
            
            // Check if we can move backward
            if (prevIndex >= 0) {
                this.pageFlip.flip(prevIndex);
            }
        } catch (e) {
            console.warn('Error in previousPage:', e);
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
        const indexBtn = document.getElementById('index-btn');

        if (prevBtn) {
            prevBtn.disabled = this.currentPage === 1;
        }

        if (nextBtn) {
            nextBtn.disabled = this.currentPage === this.totalPages;
        }

        if (indexBtn) {
            indexBtn.disabled = this.currentPage === this.indexPage;
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

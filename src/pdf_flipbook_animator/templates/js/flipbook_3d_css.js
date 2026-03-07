// PDF Flipbook Animator - 3D CSS Animation Mode
// CSS 3D transforms with perspective and page folding effect

// LinkOverlay Class - Manages clickable PDF links
class LinkOverlay {
    constructor(flipbook, linksData) {
        this.flipbook = flipbook;
        this.linksData = linksData || {};
        this.overlayContainer = document.getElementById('link-overlay');
        this.currentLinks = [];
        
        if (!this.overlayContainer) {
            console.warn('Link overlay container not found');
            return;
        }
        
        console.log(`LinkOverlay initialized with links on ${Object.keys(this.linksData).length} pages`);
    }
    
    renderLinksForPage(pageNum) {
        if (!this.overlayContainer) return;
        
        // Clear existing links
        this.clearLinks();
        
        const pageLinks = this.linksData[pageNum];
        if (!pageLinks || pageLinks.length === 0) {
            return;
        }
        
        // Get flipbook container dimensions for positioning
        const flipbookContainer = document.getElementById('flipbook');
        if (!flipbookContainer) return;
        
        const containerRect = flipbookContainer.getBoundingClientRect();
        
        pageLinks.forEach((link, index) => {
            const linkEl = document.createElement('a');
            linkEl.className = 'pdf-link';
            linkEl.dataset.targetPage = link.target_page;
            linkEl.dataset.linkIndex = index;
            
            // Position using percentages for responsive behavior
            linkEl.style.cssText = `
                left: ${link.rect.x}%;
                top: ${link.rect.y}%;
                width: ${link.rect.width}%;
                height: ${link.rect.height}%;
            `;
            
            // Add click handler for internal links
            if (link.type === 'internal') {
                linkEl.addEventListener('click', (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    const targetPage = parseInt(link.target_page);
                    console.log(`Link clicked: navigating to page ${targetPage}`);
                    this.flipbook.goToPage(targetPage);
                });
                
                // Add title for accessibility
                linkEl.title = `Go to page ${link.target_page}`;
            }
            
            this.overlayContainer.appendChild(linkEl);
            this.currentLinks.push(linkEl);
        });
        
        console.log(`Rendered ${pageLinks.length} links for page ${pageNum}`);
    }
    
    clearLinks() {
        if (this.overlayContainer) {
            this.overlayContainer.innerHTML = '';
        }
        this.currentLinks = [];
    }
    
    hide() {
        if (this.overlayContainer) {
            this.overlayContainer.classList.add('hidden');
        }
    }
    
    show() {
        if (this.overlayContainer) {
            this.overlayContainer.classList.remove('hidden');
        }
    }
    
    updateForCurrentPage() {
        const currentPage = this.flipbook.currentPage;
        this.renderLinksForPage(currentPage);
    }
}

class Flipbook {
    constructor() {
        this.currentPage = 1;
        this.totalPages = parseInt(document.getElementById('total-pages').textContent);
        this.pages = document.querySelectorAll('.page');
        this.isAnimating = false;
        this.indexPage = parseInt(document.getElementById('index-btn')?.dataset.indexPage || 2);
        
        // Zoom functionality
        this.currentZoom = 1.0;
        this.minZoom = 0.5;
        this.maxZoom = 5.0;
        this.zoomStep = 0.25;
        
        // Responsive spread mode
        this.spreadBreakpoint = 1024;
        this.spreadMode = this.shouldUseSpreadMode();
        
        // Touch handling
        this.touchStartX = 0;
        this.touchEndX = 0;
        this.touchStartY = 0;
        this.touchEndY = 0;
        
        this.init();
    }

    shouldUseSpreadMode() {
        return window.innerWidth >= this.spreadBreakpoint;
    }

    init() {
        // Add 3D container styles
        this.setup3DStyles();
        
        // Setup responsive behavior
        this.setupResponsive();
        
        // Show first page
        this.showPage(1);
        
        // Hide loading spinner
        const loading = document.getElementById('loading');
        if (loading) {
            loading.classList.remove('show');
        }

        // Setup event listeners
        this.setupControls();
        this.setupKeyboard();
        this.setupFullscreen();
        this.setupTouch();
        this.setupZoom();
        this.restoreZoom();
        this.setupPan();
        
        // Restore saved position
        this.restorePosition();
        
        // Initialize link overlay
        if (window.linksDataPromise) {
            window.linksDataPromise.then(linksData => {
                if (linksData) {
                    this.linkOverlay = new LinkOverlay(this, linksData);
                    this.linkOverlay.updateForCurrentPage();
                }
            });
        } else if (window.linksData) {
            this.linkOverlay = new LinkOverlay(this, window.linksData);
            this.linkOverlay.updateForCurrentPage();
        }
        
        // Update UI
        this.updateUI();

        console.log(`Flipbook initialized with ${this.totalPages} pages (3D CSS mode, Spread: ${this.spreadMode})`);
    }

    setupResponsive() {
        let resizeTimer;
        window.addEventListener('resize', () => {
            clearTimeout(resizeTimer);
            resizeTimer = setTimeout(() => {
                const newSpreadMode = this.shouldUseSpreadMode();
                if (newSpreadMode !== this.spreadMode) {
                    this.spreadMode = newSpreadMode;
                    this.setup3DStyles();
                    this.showPage(this.currentPage);
                    console.log(`Switched to ${this.spreadMode ? 'spread' : 'single'} mode`);
                }
            }, 250);
        });
    }

    setup3DStyles() {
        // Add perspective to container
        const viewer = document.getElementById('flipbook-viewer');
        if (viewer) {
            viewer.style.perspective = '2000px';
            viewer.style.perspectiveOrigin = 'center center';
            viewer.style.overflow = 'hidden';
        }

        const flipbook = document.getElementById('flipbook');
        if (flipbook) {
            flipbook.style.position = 'relative';
            flipbook.style.overflow = 'hidden';
            
            if (this.spreadMode) {
                // Flex layout for spread mode
                flipbook.style.display = 'flex';
                flipbook.style.justifyContent = 'center';
                flipbook.style.alignItems = 'center';
                flipbook.style.gap = '0';
            } else {
                flipbook.style.display = 'block';
            }
        }

        // Prepare pages for 3D transforms
        this.pages.forEach((page, index) => {
            if (this.spreadMode) {
                // Spread mode: side-by-side pages
                page.style.position = 'relative';
                page.style.width = '50%';
                page.style.height = '100%';
                page.style.flex = '0 0 auto';
            } else {
                // Single page mode: stacked with 3D flip
                page.style.position = 'absolute';
                page.style.top = '0';
                page.style.left = '0';
                page.style.width = '100%';
                page.style.height = '100%';
                page.style.flex = 'none';
            }
            
            page.style.transformStyle = 'preserve-3d';
            page.style.transformOrigin = 'left center';
            page.style.backfaceVisibility = 'hidden';
            page.style.zIndex = '0'; // Default z-index
            
            // Add shadow element for depth if not exists
            let shadow = page.querySelector('.page-shadow');
            if (!shadow) {
                shadow = document.createElement('div');
                shadow.className = 'page-shadow';
                shadow.style.cssText = `
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background: linear-gradient(to right, rgba(0,0,0,0.3), transparent);
                    opacity: 0;
                    transition: opacity 0.3s ease;
                    pointer-events: none;
                    z-index: 1;
                `;
                page.appendChild(shadow);
            }
        });
    }

    setupControls() {
        const prevBtn = document.getElementById('prev-btn');
        const nextBtn = document.getElementById('next-btn');
        const indexBtn = document.getElementById('index-btn');

        if (prevBtn) {
            prevBtn.addEventListener('click', () => this.previousPage());
        }

        if (nextBtn) {
            nextBtn.addEventListener('click', () => this.nextPage());
        }

        if (indexBtn) {
            indexBtn.addEventListener('click', () => this.goToPage(this.indexPage));
        }

        // Click on page to advance
        document.querySelectorAll('.page').forEach(page => {
            page.addEventListener('click', () => this.nextPage());
        });
    }

    setupKeyboard() {
        document.addEventListener('keydown', (e) => {
            if (this.isAnimating) return;
            
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
                case '+':
                case '=':
                    if (e.ctrlKey || e.metaKey) {
                        e.preventDefault();
                        this.zoomIn();
                    }
                    break;
                case '-':
                case '_':
                    if (e.ctrlKey || e.metaKey) {
                        e.preventDefault();
                        this.zoomOut();
                    }
                    break;
                case '0':
                    if (e.ctrlKey || e.metaKey) {
                        e.preventDefault();
                        this.resetZoom();
                    }
                    break;
            }
        });
    }

    setupFullscreen() {
        const fullscreenBtn = document.getElementById('fullscreen-btn');
        if (fullscreenBtn) {
            fullscreenBtn.addEventListener('click', () => this.toggleFullscreen());
        }
    }

    setupTouch() {
        const flipbook = document.getElementById('flipbook');
        if (!flipbook) return;
        
        let touchCount = 0;

        // Touch start
        flipbook.addEventListener('touchstart', (e) => {
            touchCount = e.touches.length;
            
            // Only track single-finger for page flips
            if (touchCount === 1) {
                this.touchStartX = e.changedTouches[0].screenX;
                this.touchStartY = e.changedTouches[0].screenY;
            }
        });

        // Touch end - detect swipe
        flipbook.addEventListener('touchend', (e) => {
            // Ignore multi-touch gestures (pinch zoom)
            if (touchCount > 1) {
                touchCount = 0;
                return;
            }
            
            if (e.changedTouches.length === 0) return;
            
            this.touchEndX = e.changedTouches[0].screenX;
            this.touchEndY = e.changedTouches[0].screenY;
            this.handleSwipe();
            
            touchCount = 0;
        });
    }

    setupZoom() {
        const zoomInBtn = document.getElementById('zoom-in-btn');
        const zoomOutBtn = document.getElementById('zoom-out-btn');
        const zoomResetBtn = document.getElementById('zoom-reset-btn');
        const flipbookContainer = document.getElementById('flipbook');
        
        if (zoomInBtn) {
            zoomInBtn.addEventListener('click', () => this.zoomIn());
        }
        
        if (zoomOutBtn) {
            zoomOutBtn.addEventListener('click', () => this.zoomOut());
        }
        
        if (zoomResetBtn) {
            zoomResetBtn.addEventListener('click', () => this.resetZoom());
        }
        
        // Mouse wheel zoom (Ctrl + Wheel)
        if (flipbookContainer) {
            flipbookContainer.addEventListener('wheel', (e) => {
                if (e.ctrlKey || e.metaKey) {
                    e.preventDefault();
                    if (e.deltaY < 0) {
                        this.zoomIn();
                    } else {
                        this.zoomOut();
                    }
                }
            }, { passive: false });
            
            // Pinch zoom for mobile
            let initialDistance = 0;
            let currentDistance = 0;
            let isPinching = false;
            
            flipbookContainer.addEventListener('touchstart', (e) => {
                if (e.touches.length === 2) {
                    isPinching = true;
                    e.preventDefault();
                    initialDistance = this.getTouchDistance(e.touches[0], e.touches[1]);
                }
            }, { passive: false });
            
            flipbookContainer.addEventListener('touchmove', (e) => {
                if (e.touches.length === 2 && isPinching) {
                    e.preventDefault();
                    currentDistance = this.getTouchDistance(e.touches[0], e.touches[1]);
                    const delta = currentDistance - initialDistance;
                    
                    if (Math.abs(delta) > 10) {
                        if (delta > 0) {
                            this.zoomIn(0.1);
                        } else {
                            this.zoomOut(0.1);
                        }
                        initialDistance = currentDistance;
                    }
                }
            }, { passive: false });
            
            flipbookContainer.addEventListener('touchend', (e) => {
                if (e.touches.length < 2) {
                    isPinching = false;
                }
            });
        }
    }

    getTouchDistance(touch1, touch2) {
        const dx = touch1.clientX - touch2.clientX;
        const dy = touch1.clientY - touch2.clientY;
        return Math.sqrt(dx * dx + dy * dy);
    }

    zoomIn(step = this.zoomStep) {
        this.setZoom(Math.min(this.currentZoom + step, this.maxZoom));
    }

    zoomOut(step = this.zoomStep) {
        this.setZoom(Math.max(this.currentZoom - step, this.minZoom));
    }

    resetZoom() {
        this.setZoom(1.0);
    }

    setZoom(zoomLevel) {
        this.currentZoom = zoomLevel;
        const flipbookContainer = document.getElementById('flipbook');
        const zoomLevelDisplay = document.getElementById('zoom-level');
        const mainContainer = document.querySelector('.main');
        
        // Reset pan position when zoom changes
        if (this.resetPanPosition) {
            this.resetPanPosition();
        }
        
        if (flipbookContainer) {
            flipbookContainer.style.transform = `scale(${zoomLevel})`;
            flipbookContainer.style.transformOrigin = 'center center';
            
            // Add/remove zoomed class for styling
            if (zoomLevel > 1) {
                flipbookContainer.classList.add('zoomed');
                if (mainContainer) mainContainer.classList.add('zoomed');
            } else {
                flipbookContainer.classList.remove('zoomed');
                if (mainContainer) mainContainer.classList.remove('zoomed');
            }
        }
        
        if (zoomLevelDisplay) {
            zoomLevelDisplay.textContent = `${Math.round(zoomLevel * 100)}%`;
        }
        
        // Save zoom level
        try {
            localStorage.setItem('flipbook_zoom', zoomLevel.toString());
        } catch (e) {
            console.warn('Could not save zoom level:', e);
        }
        
        console.log(`Zoom set to ${Math.round(zoomLevel * 100)}%`);
    }

    restoreZoom() {
        try {
            const savedZoom = localStorage.getItem('flipbook_zoom');
            if (savedZoom) {
                const zoomLevel = parseFloat(savedZoom);
                if (zoomLevel >= this.minZoom && zoomLevel <= this.maxZoom) {
                    this.setZoom(zoomLevel);
                }
            }
        } catch (e) {
            console.warn('Could not restore zoom:', e);
        }
    }

    setupPan() {
        const mainContainer = document.querySelector('.main');
        const flipbookContainer = document.getElementById('flipbook');
        if (!mainContainer || !flipbookContainer) return;
        
        let isPanning = false;
        let hasMoved = false;
        let startX = 0, startY = 0;
        let initialX = 0, initialY = 0;
        let currentPanX = 0, currentPanY = 0;
        const moveThreshold = 5;
        
        this.isActivePan = false;
        
        // Mouse drag to pan when zoomed
        mainContainer.addEventListener('mousedown', (e) => {
            if (this.currentZoom <= 1) return;
            if (e.target.closest('button, a, .zoom-btn, .icon-btn, .side-nav-btn')) return;
            
            isPanning = true;
            hasMoved = false;
            startX = e.clientX;
            startY = e.clientY;
            initialX = e.clientX;
            initialY = e.clientY;
            e.preventDefault();
            e.stopPropagation();
        });
        
        mainContainer.addEventListener('mousemove', (e) => {
            if (!isPanning) return;
            e.preventDefault();
            e.stopPropagation();
            
            const deltaX = e.clientX - startX;
            const deltaY = e.clientY - startY;
            
            const totalMoved = Math.sqrt(Math.pow(e.clientX - initialX, 2) + Math.pow(e.clientY - initialY, 2));
            if (totalMoved > moveThreshold && !hasMoved) {
                hasMoved = true;
                this.isActivePan = true;
                mainContainer.classList.add('panning');
                flipbookContainer.classList.add('panning');
            }
            
            if (hasMoved) {
                currentPanX += deltaX;
                currentPanY += deltaY;
                startX = e.clientX;
                startY = e.clientY;
                flipbookContainer.style.transform = `scale(${this.currentZoom}) translate(${currentPanX / this.currentZoom}px, ${currentPanY / this.currentZoom}px)`;
            }
        });
        
        mainContainer.addEventListener('mouseup', (e) => {
            if (hasMoved) {
                e.preventDefault();
                e.stopPropagation();
            }
            isPanning = false;
            mainContainer.classList.remove('panning');
            flipbookContainer.classList.remove('panning');
            setTimeout(() => { this.isActivePan = false; }, 100);
        });
        
        mainContainer.addEventListener('mouseleave', () => {
            isPanning = false;
            hasMoved = false;
            mainContainer.classList.remove('panning');
            flipbookContainer.classList.remove('panning');
            this.isActivePan = false;
        });
        
        // Touch drag to pan when zoomed (single finger)
        let touchStartX = 0, touchStartY = 0;
        let touchInitialX = 0, touchInitialY = 0;
        let isTouchPanning = false;
        let touchHasMoved = false;
        
        mainContainer.addEventListener('touchstart', (e) => {
            if (this.currentZoom <= 1) return;
            if (e.touches.length !== 1) return;
            if (e.target.closest('button, a, .zoom-btn, .icon-btn, .side-nav-btn')) return;
            
            isTouchPanning = true;
            touchHasMoved = false;
            touchStartX = e.touches[0].clientX;
            touchStartY = e.touches[0].clientY;
            touchInitialX = e.touches[0].clientX;
            touchInitialY = e.touches[0].clientY;
        }, { passive: false });
        
        mainContainer.addEventListener('touchmove', (e) => {
            if (!isTouchPanning || e.touches.length !== 1) return;
            
            const deltaX = e.touches[0].clientX - touchStartX;
            const deltaY = e.touches[0].clientY - touchStartY;
            
            const totalMoved = Math.sqrt(Math.pow(e.touches[0].clientX - touchInitialX, 2) + Math.pow(e.touches[0].clientY - touchInitialY, 2));
            if (totalMoved > moveThreshold && !touchHasMoved) {
                touchHasMoved = true;
                this.isActivePan = true;
                mainContainer.classList.add('panning');
                flipbookContainer.classList.add('panning');
                e.preventDefault();
            }
            
            if (touchHasMoved) {
                e.preventDefault();
                e.stopPropagation();
                currentPanX += deltaX;
                currentPanY += deltaY;
                touchStartX = e.touches[0].clientX;
                touchStartY = e.touches[0].clientY;
                flipbookContainer.style.transform = `scale(${this.currentZoom}) translate(${currentPanX / this.currentZoom}px, ${currentPanY / this.currentZoom}px)`;
            }
        }, { passive: false });
        
        mainContainer.addEventListener('touchend', (e) => {
            if (touchHasMoved) {
                e.preventDefault();
                e.stopPropagation();
            }
            isTouchPanning = false;
            touchHasMoved = false;
            mainContainer.classList.remove('panning');
            flipbookContainer.classList.remove('panning');
            setTimeout(() => { this.isActivePan = false; }, 100);
        });
        
        this.resetPanPosition = () => {
            currentPanX = 0;
            currentPanY = 0;
        };
    }

    handleSwipe() {
        if (this.isAnimating) return;
        
        const deltaX = this.touchEndX - this.touchStartX;
        const deltaY = this.touchEndY - this.touchStartY;
        const minSwipeDistance = 50;

        // Check if swipe is primarily horizontal
        if (Math.abs(deltaX) > Math.abs(deltaY)) {
            if (Math.abs(deltaX) > minSwipeDistance) {
                if (deltaX > 0) {
                    // Swipe right - go to previous page
                    this.previousPage();
                } else {
                    // Swipe left - go to next page
                    this.nextPage();
                }
            }
        }
    }

    showPage(pageNum, direction = 'forward') {
        if (pageNum < 1 || pageNum > this.totalPages || this.isAnimating) return;
        
        if (this.spreadMode) {
            this.showSpread(pageNum);
        } else {
            this.showSinglePage(pageNum, direction);
        }
    }

    showSpread(pageNum) {
        // In spread mode, show two pages side-by-side with smooth cross-fade
        const leftPageNum = pageNum % 2 === 0 ? pageNum - 1 : pageNum;
        const rightPageNum = leftPageNum + 1;
        
        const oldCurrentPage = this.currentPage;
        const oldLeftPageNum = oldCurrentPage % 2 === 0 ? oldCurrentPage - 1 : oldCurrentPage;
        
        // Update current page immediately
        this.currentPage = pageNum;
        
        // If same spread or first load, just show without animation
        if (leftPageNum === oldLeftPageNum || !oldCurrentPage || oldCurrentPage === pageNum) {
            // Hide all pages
            this.pages.forEach(page => {
                page.classList.remove('active');
                page.style.display = 'none';
                page.style.opacity = '1';
                page.style.transition = '';
            });
            
            // Show left page
            if (leftPageNum >= 1 && leftPageNum <= this.totalPages) {
                const leftPage = this.pages[leftPageNum - 1];
                leftPage.style.display = 'flex';
                leftPage.classList.add('active');
            }
            
            // Show right page
            if (rightPageNum <= this.totalPages) {
                const rightPage = this.pages[rightPageNum - 1];
                rightPage.style.display = 'flex';
                rightPage.classList.add('active');
            }
            
            this.preloadPages(pageNum);
            this.savePosition();
            this.updateUI();
            return;
        }
        
        if (this.isAnimating) return;
        this.isAnimating = true;
        
        const duration = 300;
        const flipbook = document.getElementById('flipbook');
        
        // Get new pages references
        const newLeftPage = this.pages[leftPageNum - 1];
        const newRightPage = rightPageNum <= this.totalPages ? this.pages[rightPageNum - 1] : null;
        
        // Position new pages absolutely on top to avoid expansion
        if (newLeftPage) {
            newLeftPage.style.position = 'absolute';
            newLeftPage.style.top = '0';
            newLeftPage.style.left = '0';
            newLeftPage.style.display = 'flex';
            newLeftPage.style.opacity = '0';
        }
        if (newRightPage) {
            newRightPage.style.position = 'absolute';
            newRightPage.style.top = '0';
            newRightPage.style.left = '50%';
            newRightPage.style.display = 'flex';
            newRightPage.style.opacity = '0';
        }
        
        // Trigger reflow
        if (newLeftPage) newLeftPage.offsetHeight;
        
        // Cross-fade: old fade out, new fade in simultaneously
        this.pages.forEach(page => {
            if (page.classList.contains('active')) {
                page.style.transition = `opacity ${duration}ms ease`;
                page.style.opacity = '0';
            }
        });
        
        if (newLeftPage) {
            newLeftPage.style.transition = `opacity ${duration}ms ease`;
            newLeftPage.style.opacity = '1';
        }
        if (newRightPage) {
            newRightPage.style.transition = `opacity ${duration}ms ease`;
            newRightPage.style.opacity = '1';
        }
        
        // Clean up after transition
        setTimeout(() => {
            // Remove old pages
            this.pages.forEach(page => {
                if (page !== newLeftPage && page !== newRightPage) {
                    page.classList.remove('active');
                    page.style.display = 'none';
                    page.style.opacity = '1';
                    page.style.transition = '';
                }
            });
            
            // Finalize new pages - revert to normal flex layout
            if (newLeftPage) {
                newLeftPage.classList.add('active');
                newLeftPage.style.position = '';
                newLeftPage.style.top = '';
                newLeftPage.style.left = '';
                newLeftPage.style.transition = '';
            }
            if (newRightPage) {
                newRightPage.classList.add('active');
                newRightPage.style.position = '';
                newRightPage.style.top = '';
                newRightPage.style.left = '';
                newRightPage.style.transition = '';
            }
            
            this.isAnimating = false;
            this.preloadPages(pageNum);
            this.savePosition();
            this.updateUI();
            
            // Update link overlay
            if (this.linkOverlay) {
                this.linkOverlay.updateForCurrentPage();
            }
        }, duration);
    }

    showSinglePage(pageNum, direction = 'forward') {
        this.isAnimating = true;
        const oldPage = this.currentPage;

        // Get current and target pages
        const currentPageEl = this.pages[oldPage - 1];
        const targetPageEl = this.pages[pageNum - 1];

        // Hide all pages first and reset z-index
        this.pages.forEach(page => {
            if (page !== currentPageEl && page !== targetPageEl) {
                page.classList.remove('active');
                page.style.display = 'none';
                page.style.zIndex = '0';
            }
        });

        // Animate out current page with 3D flip
        if (currentPageEl && oldPage !== pageNum) {
            currentPageEl.style.display = 'flex';
            currentPageEl.style.zIndex = '2'; // Put current page above others
            
            this.animate3DPageFlip(currentPageEl, direction === 'forward' ? -180 : 180, () => {
                currentPageEl.classList.remove('active');
                currentPageEl.style.display = 'none';
                currentPageEl.style.transform = '';
                currentPageEl.style.zIndex = '0';
                
                // Reset shadow
                const shadow = currentPageEl.querySelector('.page-shadow');
                if (shadow) shadow.style.opacity = '0';
            });
        }

        // Animate in target page
        if (targetPageEl) {
            // Prepare target page
            targetPageEl.style.display = 'flex';
            targetPageEl.style.zIndex = '3'; // Put target page above current
            targetPageEl.style.transform = `rotateY(${direction === 'forward' ? 180 : -180}deg)`;
            targetPageEl.classList.add('active');
            
            // Trigger reflow
            targetPageEl.offsetHeight;
            
            // Animate to normal position
            setTimeout(() => {
                this.animate3DPageFlip(targetPageEl, 0, () => {
                    this.isAnimating = false;
                    this.currentPage = pageNum;
                    targetPageEl.style.zIndex = '1'; // Keep active page at z-index 1
                    
                    // Preload adjacent pages
                    this.preloadPages(pageNum);
                    
                    // Save position
                    this.savePosition();
                    
                    // Update UI
                    this.updateUI();
                    
                    // Update link overlay
                    if (this.linkOverlay) {
                        this.linkOverlay.updateForCurrentPage();
                    }
                });
            }, 50);
        } else {
            this.isAnimating = false;
        }
    }

    animate3DPageFlip(pageEl, targetRotation, callback) {
        const duration = 800; // Animation duration in ms
        pageEl.style.transition = `transform ${duration}ms cubic-bezier(0.645, 0.045, 0.355, 1)`;
        pageEl.style.transform = `rotateY(${targetRotation}deg)`;
        
        // Animate shadow
        const shadow = pageEl.querySelector('.page-shadow');
        if (shadow) {
            shadow.style.opacity = targetRotation === 0 ? '0' : '0.5';
        }
        
        // Call callback after animation
        setTimeout(callback, duration);
    }

    preloadPages(currentPage) {
        // Preload next 2 pages
        for (let i = 1; i <= 2; i++) {
            const nextPage = currentPage + i;
            if (nextPage <= this.totalPages) {
                const img = this.pages[nextPage - 1].querySelector('img');
                if (img && !img.complete) {
                    img.loading = 'eager';
                }
            }
        }
    }

    nextPage() {
        if (this.currentPage < this.totalPages && !this.isAnimating) {
            const increment = this.spreadMode ? 2 : 1;
            const nextPage = Math.min(this.currentPage + increment, this.totalPages);
            this.showPage(nextPage, 'forward');
        }
    }

    previousPage() {
        if (this.currentPage > 1 && !this.isAnimating) {
            const decrement = this.spreadMode ? 2 : 1;
            const prevPage = Math.max(this.currentPage - decrement, 1);
            this.showPage(prevPage, 'backward');
        }
    }

    goToPage(pageNum) {
        const direction = pageNum > this.currentPage ? 'forward' : 'backward';
        this.showPage(pageNum, direction);
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
            prevBtn.disabled = this.currentPage === 1 || this.isAnimating;
        }

        if (nextBtn) {
            nextBtn.disabled = this.currentPage === this.totalPages || this.isAnimating;
        }

        if (indexBtn) {
            indexBtn.disabled = this.currentPage === this.indexPage || this.isAnimating;
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
                    this.showPage(pageNum);
                }
            }
        } catch (e) {
            console.warn('Could not restore position:', e);
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

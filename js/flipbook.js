// PDF Flipbook Animator - 3D CSS Animation Mode
// CSS 3D transforms with perspective and page folding effect

class Flipbook {
    constructor() {
        this.currentPage = 1;
        this.totalPages = parseInt(document.getElementById('total-pages').textContent);
        this.pages = document.querySelectorAll('.page');
        this.isAnimating = false;
        
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
        
        // Restore saved position
        this.restorePosition();
        
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
            viewer.style.overflow = 'hidden'; // Prevent page visibility below
        }

        const flipbook = document.getElementById('flipbook');
        if (flipbook) {
            if (this.spreadMode) {
                flipbook.style.position = 'relative';
                flipbook.style.overflow = 'hidden';
                flipbook.style.display = 'flex';
                flipbook.style.justifyContent = 'center';
                flipbook.style.alignItems = 'center';
                flipbook.style.gap = '0';
            } else {
                flipbook.style.position = 'relative';
                flipbook.style.overflow = 'hidden';
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

        if (prevBtn) {
            prevBtn.addEventListener('click', () => this.previousPage());
        }

        if (nextBtn) {
            nextBtn.addEventListener('click', () => this.nextPage());
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

        // Touch start
        flipbook.addEventListener('touchstart', (e) => {
            this.touchStartX = e.changedTouches[0].screenX;
            this.touchStartY = e.changedTouches[0].screenY;
        }, { passive: true });

        // Touch end - detect swipe
        flipbook.addEventListener('touchend', (e) => {
            this.touchEndX = e.changedTouches[0].screenX;
            this.touchEndY = e.changedTouches[0].screenY;
            this.handleSwipe();
        }, { passive: true });
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

    showSpread(pageNum, direction = 'forward') {
        // In spread mode, show two pages side-by-side with smooth animation
        if (this.isAnimating) return;
        
        this.isAnimating = true;
        const oldPage = this.currentPage;
        
        // Ensure we start on an odd page (left page)
        const leftPageNum = pageNum % 2 === 0 ? pageNum - 1 : pageNum;
        const rightPageNum = leftPageNum + 1;
        
        // Get current and target spread pages
        const oldLeftPageNum = oldPage % 2 === 0 ? oldPage - 1 : oldPage;
        const oldRightPageNum = oldLeftPageNum + 1;
        
        const currentLeftPage = this.pages[oldLeftPageNum - 1];
        const currentRightPage = oldRightPageNum <= this.totalPages ? this.pages[oldRightPageNum - 1] : null;
        const targetLeftPage = this.pages[leftPageNum - 1];
        const targetRightPage = rightPageNum <= this.totalPages ? this.pages[rightPageNum - 1] : null;
        
        // Determine animation direction
        const slideDirection = leftPageNum > oldLeftPageNum ? 'left' : 'right';
        const duration = 600;
        
        // Animate out current spread
        const animateOut = (page, callback) => {
            if (!page) {
                callback();
                return;
            }
            page.style.transition = `transform ${duration}ms cubic-bezier(0.4, 0.0, 0.2, 1), opacity ${duration}ms ease`;
            page.style.transform = slideDirection === 'left' ? 'translateX(-50%)' : 'translateX(50%)';
            page.style.opacity = '0';
            setTimeout(callback, duration);
        };
        
        // Animate in target spread
        const animateIn = (page) => {
            if (!page) return;
            page.style.display = 'flex';
            page.style.opacity = '0';
            page.style.transform = slideDirection === 'left' ? 'translateX(50%)' : 'translateX(-50%)';
            page.classList.add('active');
            
            // Trigger reflow
            page.offsetHeight;
            
            page.style.transition = `transform ${duration}ms cubic-bezier(0.4, 0.0, 0.2, 1), opacity ${duration}ms ease`;
            page.style.transform = 'translateX(0)';
            page.style.opacity = '1';
        };
        
        // Hide all other pages
        this.pages.forEach(page => {
            if (page !== currentLeftPage && page !== currentRightPage && 
                page !== targetLeftPage && page !== targetRightPage) {
                page.classList.remove('active');
                page.style.display = 'none';
                page.style.transform = '';
                page.style.opacity = '1';
            }
        });
        
        // Start animation sequence
        let animationsComplete = 0;
        const checkComplete = () => {
            animationsComplete++;
            if (animationsComplete >= 2) { // Wait for both old pages to animate out
                // Animate in new pages
                animateIn(targetLeftPage);
                if (targetRightPage) animateIn(targetRightPage);
                
                // Clean up after animation
                setTimeout(() => {
                    if (currentLeftPage && currentLeftPage !== targetLeftPage) {
                        currentLeftPage.classList.remove('active');
                        currentLeftPage.style.display = 'none';
                        currentLeftPage.style.transform = '';
                        currentLeftPage.style.opacity = '1';
                        currentLeftPage.style.transition = '';
                    }
                    if (currentRightPage && currentRightPage !== targetRightPage) {
                        currentRightPage.classList.remove('active');
                        currentRightPage.style.display = 'none';
                        currentRightPage.style.transform = '';
                        currentRightPage.style.opacity = '1';
                        currentRightPage.style.transition = '';
                    }
                    if (targetLeftPage) {
                        targetLeftPage.style.transition = '';
                    }
                    if (targetRightPage) {
                        targetRightPage.style.transition = '';
                    }
                    
                    this.isAnimating = false;
                    this.currentPage = pageNum;
                    
                    // Preload adjacent pages
                    this.preloadPages(pageNum);
                    
                    // Save position
                    this.savePosition();
                    
                    // Update UI
                    this.updateUI();
                }, duration);
            }
        };
        
        // Animate out current pages
        if (oldPage !== pageNum) {
            animateOut(currentLeftPage, checkComplete);
            animateOut(currentRightPage, checkComplete);
        } else {
            // Same page, just show it
            checkComplete();
            checkComplete();
        }
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

        if (prevBtn) {
            prevBtn.disabled = this.currentPage === 1 || this.isAnimating;
        }

        if (nextBtn) {
            nextBtn.disabled = this.currentPage === this.totalPages || this.isAnimating;
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

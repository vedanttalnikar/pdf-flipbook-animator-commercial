// PDF Flipbook Animator - Simple Animation Mode
// Fast CSS transitions with minimal resource usage

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
            linkEl.dataset.linkIndex = index;
            
            // Position using percentages for responsive behavior
            linkEl.style.cssText = `
                left: ${link.rect.x}%;
                top: ${link.rect.y}%;
                width: ${link.rect.width}%;
                height: ${link.rect.height}%;
            `;
            
            // Add click handler based on link type
            if (link.type === 'internal') {
                linkEl.dataset.targetPage = link.target_page;
                linkEl.addEventListener('click', (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    const targetPage = parseInt(link.target_page);
                    console.log(`Internal link clicked: navigating to page ${targetPage}`);
                    this.flipbook.goToPage(targetPage);
                });
                linkEl.title = `Go to page ${link.target_page}`;
            } else if (link.type === 'external') {
                linkEl.href = link.url;
                linkEl.target = '_blank';
                linkEl.rel = 'noopener noreferrer';
                linkEl.addEventListener('click', (e) => {
                    e.stopPropagation();
                    console.log(`External link clicked: opening ${link.url}`);
                });
                linkEl.title = link.url;
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

// TocDrawer Class - Slide-out Table of Contents sidebar
class TocDrawer {
    constructor(flipbook, tocData) {
        this.flipbook = flipbook;
        this.tocData = tocData || [];
        this.drawer = document.getElementById('toc-drawer');
        this.backdrop = document.getElementById('toc-backdrop');
        this.tocList = document.getElementById('toc-list');
        this.searchInput = document.getElementById('toc-search-input');
        this.isOpen = false;
        this.items = [];

        if (!this.drawer || !this.tocList || this.tocData.length === 0) {
            console.warn('TOC drawer: missing elements or empty data');
            return;
        }

        this.renderToc();
        this.setupEvents();
        console.log(`TocDrawer initialized with ${this.tocData.length} entries`);
    }

    renderToc() {
        this.tocList.innerHTML = '';
        this.items = [];

        this.tocData.forEach((entry, index) => {
            const li = document.createElement('li');
            li.className = 'toc-item';
            li.dataset.level = entry.level;
            li.dataset.page = entry.page;
            li.dataset.index = index;

            const titleSpan = document.createElement('span');
            titleSpan.className = 'toc-item-title';
            titleSpan.textContent = entry.title;

            const pageSpan = document.createElement('span');
            pageSpan.className = 'toc-item-page';
            pageSpan.textContent = `p.${entry.page}`;

            li.appendChild(titleSpan);
            li.appendChild(pageSpan);

            li.addEventListener('click', () => {
                this.flipbook.goToPage(entry.page);
                this.highlightActive(entry.page);
                setTimeout(() => this.close(), 250);
            });

            this.tocList.appendChild(li);
            this.items.push({ element: li, entry });
        });
    }

    setupEvents() {
        const tocBtn = document.getElementById('toc-btn');
        if (tocBtn) tocBtn.addEventListener('click', () => this.toggle());

        const closeBtn = document.getElementById('toc-close-btn');
        if (closeBtn) closeBtn.addEventListener('click', () => this.close());

        if (this.backdrop) this.backdrop.addEventListener('click', () => this.close());

        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.isOpen) this.close();
        });

        if (this.searchInput) this.searchInput.addEventListener('input', () => this.filterToc());
    }

    filterToc() {
        const query = this.searchInput.value.trim().toLowerCase();
        let visibleCount = 0;

        this.items.forEach(({ element, entry }) => {
            if (!query || entry.title.toLowerCase().includes(query) || String(entry.page).includes(query)) {
                element.classList.remove('hidden');
                visibleCount++;
            } else {
                element.classList.add('hidden');
            }
        });

        const existing = this.tocList.querySelector('.toc-no-results');
        if (visibleCount === 0 && query) {
            if (!existing) {
                const noResults = document.createElement('li');
                noResults.className = 'toc-no-results';
                noResults.textContent = 'No matching chapters found';
                this.tocList.appendChild(noResults);
            }
        } else if (existing) {
            existing.remove();
        }
    }

    highlightActive(pageNum) {
        let activeEntry = null;
        for (let i = this.items.length - 1; i >= 0; i--) {
            if (this.items[i].entry.page <= pageNum) {
                activeEntry = this.items[i];
                break;
            }
        }

        this.items.forEach(({ element }) => element.classList.remove('active'));

        if (activeEntry) {
            activeEntry.element.classList.add('active');
            if (this.isOpen) {
                activeEntry.element.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            }
        }
    }

    updateForCurrentPage() {
        this.highlightActive(this.flipbook.currentPage);
    }

    open() {
        this.isOpen = true;
        if (this.drawer) this.drawer.classList.add('visible');
        if (this.backdrop) this.backdrop.classList.add('visible');
        this.highlightActive(this.flipbook.currentPage);
        if (this.searchInput) setTimeout(() => this.searchInput.focus(), 350);
    }

    close() {
        this.isOpen = false;
        if (this.drawer) this.drawer.classList.remove('visible');
        if (this.backdrop) this.backdrop.classList.remove('visible');
    }

    toggle() {
        if (this.isOpen) this.close(); else this.open();
    }
}

class Flipbook {
    constructor() {
        this.currentPage = 1;
        this.totalPages = parseInt(document.getElementById('total-pages').textContent);
        this.pages = document.querySelectorAll('.page');
        this.indexPage = parseInt(document.getElementById('index-btn')?.dataset.indexPage || 2);
        
        // Zoom functionality
        this.currentZoom = 1.0;
        this.minZoom = 0.5;
        this.maxZoom = 5.0;
        this.zoomStep = 0.25;
        
        // Touch handling
        this.touchStartX = 0;
        this.touchEndX = 0;
        this.touchStartY = 0;
        this.touchEndY = 0;
        
        this.init();
    }

    init() {
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
        
        // Initialize link overlay (wait for links data to load)
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
        
        // Initialize TOC drawer
        if (window.tocDataPromise) {
            window.tocDataPromise.then(tocData => {
                if (tocData && tocData.length > 0) {
                    this.tocDrawer = new TocDrawer(this, tocData);
                    this.tocDrawer.updateForCurrentPage();
                }
            });
        } else if (window.tocData && window.tocData.length > 0) {
            this.tocDrawer = new TocDrawer(this, window.tocData);
            this.tocDrawer.updateForCurrentPage();
        }
        
        // Restore saved position
        this.restorePosition();
        
        // Update UI
        this.updateUI();

        console.log(`Flipbook initialized with ${this.totalPages} pages (Simple mode)`);
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

    showPage(pageNum) {
        if (pageNum < 1 || pageNum > this.totalPages) return;

        // Hide all pages with fade out
        this.pages.forEach(page => {
            page.classList.remove('active');
        });

        // Show target page with fade in
        const targetPage = this.pages[pageNum - 1];
        if (targetPage) {
            targetPage.classList.add('active');
            this.currentPage = pageNum;
            
            // Preload adjacent pages
            this.preloadPages(pageNum);
            
            // Save position
            this.savePosition();
            
            // Update link overlay
            if (this.linkOverlay) {
                this.linkOverlay.updateForCurrentPage();
            }
            
            // Update TOC active highlight
            if (this.tocDrawer) {
                this.tocDrawer.updateForCurrentPage();
            }
            
            // Update UI
            this.updateUI();
        }
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
        if (this.currentPage < this.totalPages) {
            this.showPage(this.currentPage + 1);
        }
    }

    previousPage() {
        if (this.currentPage > 1) {
            this.showPage(this.currentPage - 1);
        }
    }

    goToPage(pageNum) {
        this.showPage(pageNum);
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

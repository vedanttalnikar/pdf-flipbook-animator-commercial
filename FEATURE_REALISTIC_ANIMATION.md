# Feature: Realistic Page Flip Animation

## Overview
Enhance the flipbook viewer with realistic 3D page flip animations that simulate the physical experience of flipping through a book.

## Problem Statement
Current implementation uses simple CSS transitions (fade/slide) which lack visual appeal. Users want a more natural page-turning experience that mimics real book behavior with:
- 3D page curl effect
- Physics-based animation
- Shadow and depth perception
- Smooth, performant transitions

## Proposed Solution

### Animation Modes
Provide three animation modes to balance visual quality with performance:

#### 1. Simple (Current - Default)
- Fast CSS transitions
- Minimal resource usage
- Best for large PDFs (100+ pages)
- No 3D effects

#### 2. 3D CSS
- CSS 3D transforms with `perspective` and `rotateY`
- Lightweight implementation
- Good performance on most devices
- Page folding effect without external libraries

#### 3. Realistic (StPageFlip)
- Full 3D page curl using StPageFlip library
- Physics-based animation with realistic shadows
- Interactive dragging
- Best visual quality but higher resource usage
- Recommended for presentations and small-to-medium PDFs

## Technical Implementation

### Option A: StPageFlip Library (Recommended)
**Library**: [StPageFlip](https://github.com/Nodlik/StPageFlip) by Nodlik
- Standalone JavaScript (no jQuery dependency)
- WebGL rendering for smooth 60 FPS
- Touch and mouse drag support
- Configurable page stiffness, shadows, angles
- MIT License

**Integration Approach**:
```javascript
// Load from CDN or bundle locally
<script src="https://unpkg.com/page-flip@2.0.7/dist/js/page-flip.browser.js"></script>

// Initialize
const pageFlip = new St.PageFlip(document.getElementById('flipbook'), {
    width: 800,
    height: 1000,
    size: "stretch",
    minWidth: 315,
    maxWidth: 1000,
    minHeight: 400,
    maxHeight: 1533,
    maxShadowOpacity: 0.5,
    showCover: true,
    mobileScrollSupport: true
});
```

### Option B: Pure CSS 3D (Lightweight Alternative)
Use CSS transforms for 3D folding effect:
```css
.page {
    transform-style: preserve-3d;
    transform-origin: left center;
    transition: transform 800ms cubic-bezier(0.645, 0.045, 0.355, 1);
}
.page.flipping {
    transform: rotateY(-180deg);
}
```

## Configuration Changes

### config.py
Add new fields to `Config` dataclass:
```python
@dataclass
class Config:
    # ... existing fields ...
    
    # Animation settings
    animation_mode: str = "simple"  # simple, 3d-css, realistic
    enable_page_curl: bool = False
    page_flip_duration: int = 800  # milliseconds
    flip_easing: str = "ease-in-out"  # CSS easing function
    enable_flip_sound: bool = False
    
    def __post_init__(self):
        # ... existing validations ...
        
        # Validate animation mode
        valid_modes = ["simple", "3d-css", "realistic"]
        if self.animation_mode not in valid_modes:
            raise ValueError(f"animation_mode must be one of {valid_modes}")
        
        # Validate flip duration
        if not 200 <= self.page_flip_duration <= 2000:
            raise ValueError("page_flip_duration must be between 200-2000ms")
```

### CLI Updates
Add new flags to `convert` command:
```python
@click.command()
@click.argument("pdf_path", type=click.Path(exists=True))
@click.option("--animation-mode", "-a", 
              type=click.Choice(["simple", "3d-css", "realistic"]),
              default="simple",
              help="Page flip animation style")
@click.option("--flip-duration", "-d",
              type=int,
              default=800,
              help="Animation duration in milliseconds (200-2000)")
@click.option("--enable-curl", is_flag=True,
              help="Enable 3D page curl effect (realistic mode only)")
def convert(pdf_path, animation_mode, flip_duration, enable_curl):
    # ... implementation ...
```

## Generator Updates

### Template Structure
Create separate JavaScript templates for each mode:
```
src/pdf_flipbook_animator/templates/
├── js/
│   ├── flipbook_simple.js      # Current implementation
│   ├── flipbook_3d_css.js      # CSS 3D transforms
│   └── flipbook_realistic.js   # StPageFlip integration
```

### generator.py Changes
```python
class FlipbookGenerator:
    def _generate_js(self) -> str:
        """Generate appropriate JavaScript based on animation mode."""
        mode = self.config.animation_mode
        
        if mode == "simple":
            return self._generate_simple_js()
        elif mode == "3d-css":
            return self._generate_3d_css_js()
        elif mode == "realistic":
            return self._generate_realistic_js()
    
    def _generate_realistic_js(self) -> str:
        """Generate StPageFlip-based JavaScript."""
        return f"""
        // Load StPageFlip library
        const script = document.createElement('script');
        script.src = 'https://unpkg.com/page-flip@2.0.7/dist/js/page-flip.browser.js';
        script.onload = initFlipbook;
        document.head.appendChild(script);
        
        function initFlipbook() {{
            const pageFlip = new St.PageFlip(
                document.getElementById('flipbook-container'),
                {{
                    width: {self.config.page_width},
                    height: {self.config.page_height},
                    size: "stretch",
                    duration: {self.config.page_flip_duration},
                    // ... more config ...
                }}
            );
            
            // Load pages
            pageFlip.loadFromImages([
                {', '.join(f"'images/{img}'" for img in self.images)}
            ]);
        }}
        """
```

## Testing Requirements

### Unit Tests
- [ ] Config validation for animation_mode
- [ ] Config validation for flip_duration range
- [ ] Generator produces correct JS for each mode
- [ ] CLI accepts and validates animation flags

### Integration Tests
- [ ] Convert with `--animation-mode simple`
- [ ] Convert with `--animation-mode 3d-css`
- [ ] Convert with `--animation-mode realistic`
- [ ] Verify correct JS library is included in output
- [ ] Check HTML structure matches mode requirements

### Manual Testing
- [ ] Simple mode works on mobile/desktop
- [ ] 3D CSS mode shows page folding effect
- [ ] Realistic mode displays page curl
- [ ] Performance is acceptable for 50+ page PDFs
- [ ] Touch gestures work on tablets
- [ ] Keyboard navigation still functional
- [ ] Fallback to simple mode if WebGL unavailable

## Performance Targets

| Animation Mode | Target FPS | Max PDF Pages | Load Time (50pg) | Browser Support |
|----------------|------------|---------------|------------------|-----------------|
| Simple         | 60 FPS     | 500+          | <1s              | All modern      |
| 3D CSS         | 60 FPS     | 200           | <2s              | 95% browsers    |
| Realistic      | 30+ FPS    | 100           | <3s              | WebGL required  |

## Documentation Updates

### Files to Update
1. **README.md** - Add animation mode examples
2. **docs/usage/basic.md** - Document all animation flags
3. **docs/usage/advanced.md** - Deep dive into each mode with pros/cons
4. **docs/examples.md** - Interactive demos for each mode
5. **CHANGELOG.md** - Add v0.2.0 entry

### Example Usage
```bash
# Simple animation (default, fastest)
pdf-flipbook convert document.pdf

# 3D CSS animation (balanced)
pdf-flipbook convert document.pdf --animation-mode 3d-css

# Realistic animation with page curl
pdf-flipbook convert document.pdf --animation-mode realistic --enable-curl

# Custom flip duration
pdf-flipbook convert document.pdf -a realistic -d 1200
```

## Implementation Timeline

### Phase 1: Foundation (Days 1-2)
- [ ] Update config.py with new fields and validation
- [ ] Add CLI flags for animation options
- [ ] Create template directory structure
- [ ] Write unit tests for config changes

### Phase 2: 3D CSS Mode (Days 3-5)
- [ ] Implement CSS 3D transforms in new template
- [ ] Add perspective and rotateY effects
- [ ] Create smooth transition animations
- [ ] Test on multiple browsers and devices

### Phase 3: StPageFlip Integration (Days 6-10)
- [ ] Research StPageFlip API and options
- [ ] Create realistic template with library integration
- [ ] Handle CDN loading and fallbacks
- [ ] Implement page dragging and touch support
- [ ] Add error handling for WebGL unavailable

### Phase 4: Testing & Refinement (Days 11-15)
- [ ] Comprehensive cross-browser testing
- [ ] Performance benchmarking
- [ ] Mobile device testing
- [ ] Fix bugs and optimize

### Phase 5: Documentation (Days 16-20)
- [ ] Write detailed usage guides
- [ ] Create video demonstrations
- [ ] Update all documentation files
- [ ] Add migration guide from v0.1.0

### Phase 6: Release Preparation (Days 21-28)
- [ ] Update CHANGELOG.md
- [ ] Final code review
- [ ] Create release branch
- [ ] Tag v0.2.0
- [ ] Deploy documentation

## Success Metrics
- 90%+ users report improved visual experience
- No performance degradation for simple mode
- <5% increase in output file size
- Compatible with 95%+ modern browsers
- Positive feedback on GitHub discussions

## Risks & Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| StPageFlip performance issues | High | Medium | Provide 3D CSS fallback, warn for large PDFs |
| Browser compatibility | Medium | Low | Progressive enhancement, detect WebGL |
| Increased bundle size | Low | High | CDN loading, optional local bundling |
| Complex configuration | Medium | Medium | Sensible defaults, good documentation |

## Future Enhancements (v0.3.0+)
- Page flip sound effects (swish sound on turn)
- Configurable page thickness and material
- Auto-flip mode for presentations
- Custom animations (fade, slide, zoom)
- Animation presets (magazine, comic book, textbook)

---

**Status**: Ready for Implementation  
**Priority**: High (P1)  
**Target Release**: v0.2.0 (April 2026)  
**Estimated Effort**: 20-28 days (1 developer)  
**Dependencies**: None (standalone feature)

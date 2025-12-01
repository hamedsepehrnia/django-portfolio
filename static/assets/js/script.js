// Three.js Starfield Setup
let scene, camera, renderer, starfield;
let starsGeometry, starsMaterial, stars;
let velocities = null;

// Lazy Loading for Backgrounds and Images
function initLazyLoading() {
    const lazyBackgrounds = document.querySelectorAll('.lazy-bg[data-bg]');
    const lazyImages = document.querySelectorAll('img[data-src], img[data-srcset]');
    if (!lazyBackgrounds.length && !lazyImages.length) {
        return;
    }
    const observerConfig = {
        root: null,
        rootMargin: '0px 0px 200px 0px',
        threshold: 0.01
    };

    const loadBackground = (element) => {
        const bgUrl = element.dataset.bg;
        if (!bgUrl) {
            return;
        }
        const image = new Image();
        image.src = bgUrl;
        image.onload = () => {
            element.style.backgroundImage = `url("${bgUrl}")`;
            element.classList.add('lazy-loaded');
        };
        image.onerror = () => {
            element.classList.add('lazy-error');
        };
        element.removeAttribute('data-bg');
    };

    const loadImage = (imageEl) => {
        const { src: currentSrc } = imageEl;
        const dataSrc = imageEl.dataset.src;
        const dataSrcSet = imageEl.dataset.srcset;

        if (dataSrcSet) {
            imageEl.srcset = dataSrcSet;
            imageEl.removeAttribute('data-srcset');
        }
        if (dataSrc) {
            if (!currentSrc) {
                imageEl.src = dataSrc;
            } else {
                imageEl.setAttribute('src', dataSrc);
            }
            imageEl.removeAttribute('data-src');
        }
        imageEl.classList.add('lazy-loaded');
    };

    if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver((entries, entryObserver) => {
            entries.forEach((entry) => {
                if (!entry.isIntersecting && entry.intersectionRatio <= 0) {
                    return;
                }

                const target = entry.target;

                if (target.dataset && target.dataset.bg) {
                    loadBackground(target);
                } else if (target.dataset && (target.dataset.src || target.dataset.srcset)) {
                    loadImage(target);
                }

                entryObserver.unobserve(target);
            });
        }, observerConfig);

        lazyBackgrounds.forEach((bg) => observer.observe(bg));
        lazyImages.forEach((img) => observer.observe(img));
    } else {
        lazyBackgrounds.forEach(loadBackground);
        lazyImages.forEach(loadImage);
    }
}

// GSAP Animation Setup (will be registered when available)
let gsapReady = false;

// Initialize Three.js Scene
function initThreeJS() {
    // Scene
    scene = new THREE.Scene();
    scene.background = null; // Transparent background
    
    // Camera
    camera = new THREE.PerspectiveCamera(
        75,
        window.innerWidth / window.innerHeight,
        0.1,
        2000
    );
    camera.position.z = 1000;
    
    // Renderer
    const canvasContainer = document.getElementById('canvas-container');
    const isMobile = window.innerWidth <= 768;
    renderer = new THREE.WebGLRenderer({ 
        alpha: true,
        antialias: !isMobile // Disable antialiasing on mobile for better performance
    });
    renderer.setSize(window.innerWidth, window.innerHeight);
    // Lower pixel ratio on mobile for better performance
    renderer.setPixelRatio(isMobile ? Math.min(window.devicePixelRatio, 1.5) : Math.min(window.devicePixelRatio, 2));
    canvasContainer.appendChild(renderer.domElement);
    
    // Create Starfield
    createStarfield();
    
    // Lighting (for any future 3D objects)
    const ambientLight = new THREE.AmbientLight(0xEAF2FF, 0.5);
    scene.add(ambientLight);
    
    const directionalLight = new THREE.DirectionalLight(0xBBD7FF, 0.5);
    directionalLight.position.set(5, 5, 5);
    scene.add(directionalLight);
    
    // Handle Window Resize
    window.addEventListener('resize', onWindowResize);
    
    // Start Animation Loop
    animate();
}

// Create Starfield with Points
function createStarfield() {
    // Reduce particle count - less crowded
    const isMobile = window.innerWidth <= 768;
    const particleCount = isMobile ? 6000 : 12000; // Further reduced for cleaner look
    const positions = new Float32Array(particleCount * 3);
    const colors = new Float32Array(particleCount * 3);
    const sizes = new Float32Array(particleCount);
    const opacities = new Float32Array(particleCount);
    velocities = new Float32Array(particleCount);
    
    // Original color palette with full variety
    const colorPalette = [
        new THREE.Color(0x0050FF), // Primary blue
        new THREE.Color(0x66CCFF), // Light blue
        new THREE.Color(0xFFFFFF), // White
        new THREE.Color(0xFFCCE6)  // Pink
    ];
    
    for (let i = 0; i < particleCount; i++) {
        const i3 = i * 3;
        
        // Random positions in a sphere
        const radius = Math.random() * 2000 + 500;
        const theta = Math.random() * Math.PI * 2;
        const phi = Math.acos(Math.random() * 2 - 1);
        
        positions[i3] = radius * Math.sin(phi) * Math.cos(theta);
        positions[i3 + 1] = radius * Math.sin(phi) * Math.sin(theta);
        positions[i3 + 2] = radius * Math.cos(phi);
        
        // Random colors from palette - full variety
        const color = colorPalette[Math.floor(Math.random() * colorPalette.length)];
        colors[i3] = color.r;
        colors[i3 + 1] = color.g;
        colors[i3 + 2] = color.b;
        
        // Random sizes (larger for better visibility)
        sizes[i] = Math.random() * 4 + 1.5;
        
        // Random opacities
        opacities[i] = Math.random() * 0.8 + 0.2;
        
        // Random velocities for drift
        velocities[i] = (Math.random() - 0.5) * 0.5;
    }
    
    // Geometry
    starsGeometry = new THREE.BufferGeometry();
    starsGeometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    starsGeometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
    starsGeometry.setAttribute('size', new THREE.BufferAttribute(sizes, 1));
    starsGeometry.setAttribute('opacity', new THREE.BufferAttribute(opacities, 1));
    
    // Material - normal opacity for light mode
    const isDarkMode = document.body.classList.contains('dark-mode');
    starsMaterial = new THREE.PointsMaterial({
        size: 4, // Increased size for better visibility
        vertexColors: true,
        transparent: true,
        opacity: isDarkMode ? 0.25 : 0.9, // Lower only in dark mode
        blending: THREE.AdditiveBlending,
        depthWrite: false,
        sizeAttenuation: true
    });
    
    // Points
    stars = new THREE.Points(starsGeometry, starsMaterial);
    scene.add(stars);
}

// Update starfield for dark mode
function updateStarfieldForDarkMode(isDarkMode) {
    if (!stars || !starsMaterial || !starsGeometry) return;
    
    // Update material opacity - significantly reduce in dark mode
    starsMaterial.opacity = isDarkMode ? 0.25 : 0.9;
    starsMaterial.needsUpdate = true;
    
    // Update colors for dark mode - replace white and bright colors with darker blues
    const colors = starsGeometry.attributes.color.array;
    
    // Update white and bright particles to darker colors in dark mode
    for (let i = 0; i < colors.length; i += 3) {
        const r = colors[i];
        const g = colors[i + 1];
        const b = colors[i + 2];
        
        if (isDarkMode) {
            // Replace white particles (bright) with subtle blue
            if (r > 0.85 && g > 0.85 && b > 0.85) {
                // Convert white to subtle blue-gray
                colors[i] = 0.2;     // R - dark blue-gray
                colors[i + 1] = 0.3; // G
                colors[i + 2] = 0.5; // B - slightly more blue
            }
            // Replace pink particles with dark purple-blue
            else if (r > 0.8 && g > 0.6 && b > 0.7) {
                colors[i] = 0.15;    // R
                colors[i + 1] = 0.2; // G
                colors[i + 2] = 0.4; // B
            }
            // Reduce brightness of all bright blue particles (but not white/pink which are already handled)
            else if (b > 0.7 && r < 0.3 && g < 0.9) {
                colors[i] = Math.max(0, colors[i] * 0.4);
                colors[i + 1] = Math.max(0, colors[i + 1] * 0.5);
                colors[i + 2] = Math.max(0, colors[i + 2] * 0.6);
            }
        } else {
            // In light mode, restore original vibrant colors
            // Check if it's a dark mode color (dark blue-gray) and restore to original palette
            if (r < 0.3 && g < 0.4 && b < 0.6) {
                // This looks like a dark mode color, restore to original vibrant color
                const originalPalette = [
                    { r: 0.0, g: 0.31, b: 1.0 },  // Primary blue
                    { r: 0.4, g: 0.8, b: 1.0 },   // Light blue
                    { r: 1.0, g: 1.0, b: 1.0 },   // White
                    { r: 1.0, g: 0.8, b: 0.9 }    // Pink
                ];
                const restoreColor = originalPalette[Math.floor(Math.random() * originalPalette.length)];
                colors[i] = restoreColor.r;
                colors[i + 1] = restoreColor.g;
                colors[i + 2] = restoreColor.b;
            }
        }
    }
    
    starsGeometry.attributes.color.needsUpdate = true;
    
    // Update opacities - significantly reduce in dark mode
    const opacities = starsGeometry.attributes.opacity.array;
    for (let i = 0; i < opacities.length; i++) {
        if (isDarkMode) {
            // Reduce opacity significantly for all particles in dark mode
            opacities[i] = Math.max(0.05, opacities[i] * 0.3);
        } else {
            // Restore original opacity range for light mode
            opacities[i] = Math.random() * 0.8 + 0.2;
        }
    }
    starsGeometry.attributes.opacity.needsUpdate = true;
}

// Animation Loop
function animate() {
    requestAnimationFrame(animate);
    
    // Slow drift rotation
    if (stars && starsGeometry && velocities) {
        stars.rotation.y += 0.0005;
        stars.rotation.x += 0.0002;
        
        // Update particle positions for drift
        const positions = starsGeometry.attributes.position.array;
        for (let i = 0; i < positions.length; i += 3) {
            const index = i / 3;
            if (velocities[index] !== undefined) {
                positions[i + 2] += velocities[index] * 0.1;
                if (positions[i + 2] > 1500) positions[i + 2] = -1500;
                if (positions[i + 2] < -1500) positions[i + 2] = 1500;
            }
        }
        starsGeometry.attributes.position.needsUpdate = true;
    }
    
    if (renderer && scene && camera) {
        renderer.render(scene, camera);
    }
}

// Snap scroll functionality removed to allow free scrolling

// Initialize GSAP Animations
function initGSAPAnimations() {
    // Register ScrollTrigger and ScrollToPlugin if not already registered
    if (typeof gsap !== 'undefined' && typeof gsap.registerPlugin !== 'undefined') {
        if (typeof ScrollTrigger !== 'undefined') {
            gsap.registerPlugin(ScrollTrigger);
        }
        if (typeof ScrollToPlugin !== 'undefined') {
            gsap.registerPlugin(ScrollToPlugin);
        }
        gsapReady = true;
    } else {
        console.warn('GSAP or plugins not loaded');
        return;
    }
    
    // Hero Logo Animation on Load (only if logo exists)
    const heroLogoContainer = document.querySelector('.hero-logo-container');
    if (heroLogoContainer) {
        gsap.to('.hero-logo-container', {
            opacity: 1,
            y: 0,
            duration: 1.5,
            ease: 'power3.out',
            delay: 0.3
        });
    }
    
    // Hero Title Animation (adjusted delay if no logo)
    const titleDelay = heroLogoContainer ? 0.6 : 0.3;
    gsap.to('.hero-title', {
        opacity: 1,
        y: 0,
        duration: 1.2,
        ease: 'power3.out',
        delay: titleDelay
    });
    
    gsap.to('.hero-subtitle', {
        opacity: 1,
        y: 0,
        duration: 1.2,
        ease: 'power3.out',
        delay: titleDelay + 0.2
    });
    
    gsap.to('.hero-description', {
        opacity: 1,
        y: 0,
        duration: 1.2,
        ease: 'power3.out',
        delay: titleDelay + 0.4
    });
    
    /*
    // Scroll indicator delay (sooner if no logo)
    const scrollDelay = heroLogoContainer ? 1.5 : titleDelay + 0.8;
    gsap.to('.scroll-indicator', {
        opacity: 1,
        duration: 1,
        delay: scrollDelay
    });
    */
    
    // Scroll-based Camera Movement (compatible with snap scroll)
    ScrollTrigger.create({
        trigger: 'body',
        start: 'top top',
        end: 'bottom bottom',
        scrub: 0.5, // Smoother scrub for snap scroll
        onUpdate: (self) => {
            if (camera && stars) {
                const scrollProgress = self.progress;
                
                // Keep camera at fixed position to maintain consistent star visibility
                // Only slight movement for subtle parallax effect
                camera.position.z = 1000 - (scrollProgress * 100);
                
                const scale = 1 + scrollProgress * 3;
                stars.scale.set(scale, scale, scale);
                
                if (starsMaterial) {
                    starsMaterial.size = 4 + (scrollProgress * 8);
                }
            }
        }
    });
    
    // Section Title Animations
    gsap.utils.toArray('.section-title').forEach((title) => {
        gsap.to(title, {
            opacity: 1,
            y: 0,
            duration: 1,
            ease: 'power3.out',
            scrollTrigger: {
                trigger: title,
                start: 'top 80%',
                end: 'top 50%',
                toggleActions: 'play none none none'
            }
        });
    });
    
    // Text Block Animations
    gsap.utils.toArray('.text-block').forEach((block, index) => {
        gsap.to(block, {
            opacity: 1,
            y: 0,
            duration: 1,
            ease: 'power3.out',
            delay: index * 0.2,
            scrollTrigger: {
                trigger: block,
                start: 'top 85%',
                end: 'top 60%',
                toggleActions: 'play none none none'
            }
        });
    });
    
    // Portfolio Item Animations
    gsap.utils.toArray('.portfolio-item').forEach((item, index) => {
        gsap.to(item, {
            opacity: 1,
            y: 0,
            duration: 0.8,
            ease: 'power3.out',
            delay: index * 0.1,
            scrollTrigger: {
                trigger: item,
                start: 'top 85%',
                end: 'top 60%',
                toggleActions: 'play none none none'
            }
        });
    });
    
    // Service Card Animations
    gsap.utils.toArray('.service-card').forEach((card, index) => {
        gsap.to(card, {
            opacity: 1,
            y: 0,
            duration: 0.8,
            ease: 'power3.out',
            delay: index * 0.15,
            scrollTrigger: {
                trigger: card,
                start: 'top 85%',
                end: 'top 60%',
                toggleActions: 'play none none none'
            }
        });
    });
    
    // Contact Section Animations
    gsap.to('.contact-info-section', {
        opacity: 1,
        y: 0,
        duration: 1,
        ease: 'power3.out',
        scrollTrigger: {
            trigger: '.contact-section',
            start: 'top 80%',
            end: 'top 50%',
            toggleActions: 'play none none none'
        }
    });
    
    gsap.to('.contact-form-container', {
        opacity: 1,
        y: 0,
        duration: 1,
        ease: 'power3.out',
        delay: 0.2,
        scrollTrigger: {
            trigger: '.contact-section',
            start: 'top 80%',
            end: 'top 50%',
            toggleActions: 'play none none none'
        }
    });
    
    // Animate contact detail items
    gsap.utils.toArray('.contact-detail-item').forEach((item, index) => {
        gsap.to(item, {
            opacity: 1,
            y: 0,
            duration: 0.8,
            ease: 'power3.out',
            delay: index * 0.15,
            scrollTrigger: {
                trigger: item,
                start: 'top 85%',
                end: 'top 60%',
                toggleActions: 'play none none none'
            }
        });
    });
}

// Cursor Trail Effect (Optional - can be disabled)
function initCursorTrail() {
    const trail = document.querySelector('.cursor-trail');
    if (!trail) return;
    
    // Set to false to disable cursor trail
    const enableCursorTrail = true;
    if (!enableCursorTrail) {
        trail.style.display = 'none';
        return;
    }
    
    let mouseX = 0;
    let mouseY = 0;
    let trailX = 0;
    let trailY = 0;
    
    // Check if device is mobile
    const isMobile = window.innerWidth <= 768 || 'ontouchstart' in window;
    let hideTimeout = null;
    
    const resetHideTimer = () => {
        if (isMobile) {
            // Clear existing timer
            if (hideTimeout) {
                clearTimeout(hideTimeout);
            }
            // Set new timer to hide after 3 seconds of inactivity
            hideTimeout = setTimeout(() => {
                trail.classList.remove('active');
            }, 3000);
        }
    };
    
    document.addEventListener('mousemove', (e) => {
        mouseX = e.clientX;
        mouseY = e.clientY;
        trail.classList.add('active');
        // Reset hide timer on mouse movement (mobile only)
        resetHideTimer();
    });
    
    function updateTrail() {
        trailX += (mouseX - trailX) * 0.1;
        trailY += (mouseY - trailY) * 0.1;
        trail.style.left = trailX - 10 + 'px';
        trail.style.top = trailY - 10 + 'px';
        requestAnimationFrame(updateTrail);
    }
    
    updateTrail();
    
    document.addEventListener('mouseleave', () => {
        trail.classList.remove('active');
        // Clear timer when mouse leaves
        if (hideTimeout) {
            clearTimeout(hideTimeout);
        }
    });
}

// Handle Window Resize
function onWindowResize() {
    if (camera && renderer) {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    }
}

// Smooth Scroll for Navigation Links with GSAP
function initNavigationScroll() {
    const nav = document.querySelector('.nav');
    const getNavOffset = () => (nav ? nav.offsetHeight : 0);
    const isMobile = window.innerWidth <= 768 || 'ontouchstart' in window;
    
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const targetId = this.getAttribute('href');
            
            if (targetId === '#') return;
            
            const target = document.querySelector(targetId);
            
            if (!target) return;
            
            e.preventDefault();
            
            // Close mobile menu immediately (before scroll starts) to remove delay
            if (isMobile) {
                const menuToggle = document.querySelector('.menu-toggle');
                const navMenu = document.querySelector('.nav-menu');
                if (menuToggle && navMenu) {
                    menuToggle.classList.remove('active');
                    navMenu.classList.remove('active');
                }
            }
            
            const offset = getNavOffset();
            
            // Start scroll immediately without waiting for menu animation
            if (typeof gsap !== 'undefined' && typeof ScrollToPlugin !== 'undefined') {
                // Kill any existing scroll animations to prevent conflicts
                gsap.killTweensOf(window);
                
                // Start scroll immediately using requestAnimationFrame for instant start
                requestAnimationFrame(() => {
                    gsap.to(window, {
                        duration: 1.8, // Slower duration for smoother feel
                        scrollTo: {
                            y: target,
                            offsetY: offset
                        },
                        ease: 'power2.inOut',
                        overwrite: true, // Overwrite any existing animations
                        immediateRender: true // Start immediately
                    });
                });
            } else {
                const targetTop = target.getBoundingClientRect().top + window.pageYOffset - offset;
                window.scrollTo({
                    top: Math.max(0, targetTop),
                    behavior: 'smooth'
                });
            }
        });
    });
}

// Performance Monitoring (optional)
function monitorPerformance() {
    let lastTime = performance.now();
    let frameCount = 0;
    
    function checkFrameRate() {
        frameCount++;
        const currentTime = performance.now();
        const deltaTime = currentTime - lastTime;
        
        if (deltaTime >= 1000) {
            const fps = Math.round((frameCount * 1000) / deltaTime);
            if (fps < 50) {
                console.warn('Frame rate below target:', fps);
            }
            frameCount = 0;
            lastTime = currentTime;
        }
        
        requestAnimationFrame(checkFrameRate);
    }
    
    checkFrameRate();
}

function initNextSectionButton() {
    const button = document.getElementById('pageNextButton');
    const navMenu = document.querySelector('.nav-menu');
    if (!button || !navMenu) return;
    const navLinks = navMenu.querySelectorAll('.nav-link[href^="#"]');
    const sections = [];
    navLinks.forEach(link => {
        const id = link.getAttribute('href');
        if (!id || id === '#') return;
        const el = document.querySelector(id);
        if (!el) return;
        sections.push({ id, el });
    });
    if (!sections.length) {
        button.classList.add('is-hidden');
        return;
    }
    function updateTarget() {
        const scrollY = window.pageYOffset || document.documentElement.scrollTop || 0;
        const viewportHeight = window.innerHeight || 0;
        const center = scrollY + viewportHeight / 2;
        let currentIndex = 0;
        for (let i = 0; i < sections.length; i++) {
            const rect = sections[i].el.getBoundingClientRect();
            const top = rect.top + scrollY;
            const bottom = top + rect.height;
            if (center >= top && center < bottom) {
                currentIndex = i;
                break;
            }
        }
        if (currentIndex >= sections.length - 1) {
            button.classList.add('is-hidden');
            return;
        }
        button.classList.remove('is-hidden');
        const next = sections[currentIndex + 1];
        button.setAttribute('href', next.id);
    }
    updateTarget();
    window.addEventListener('scroll', updateTarget);
    window.addEventListener('resize', updateTarget);
}

// Initialize Dark Mode
function initDarkMode() {
    const darkModeToggle = document.getElementById('darkModeToggle');
    const body = document.body;
    
    // Check for saved theme preference or default to light mode
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
        body.classList.add('dark-mode');
    }
    
    // Update starfield for initial dark mode state (with delay to ensure Three.js is ready)
    const updateStarfield = () => {
        if (stars && starsMaterial && starsGeometry) {
            updateStarfieldForDarkMode(body.classList.contains('dark-mode'));
        } else {
            // Retry after a short delay if Three.js isn't ready yet
            setTimeout(updateStarfield, 50);
        }
    };
    updateStarfield();
    
    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', () => {
            body.classList.toggle('dark-mode');
            const isDark = body.classList.contains('dark-mode');
            
            // Save preference
            localStorage.setItem('theme', isDark ? 'dark' : 'light');
            
            // Update starfield for dark mode
            updateStarfieldForDarkMode(isDark);
            
            // Icons are controlled by CSS transitions
        });
    }
}

// Initialize Mobile Menu
function initMobileMenu() {
    const menuToggle = document.querySelector('.menu-toggle');
    const navMenu = document.querySelector('.nav-menu');
    const navLinks = document.querySelectorAll('.nav-link');
    
    if (menuToggle && navMenu) {
        menuToggle.addEventListener('click', () => {
            menuToggle.classList.toggle('active');
            navMenu.classList.toggle('active');
        });
        
        // Close menu when clicking on a link
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                menuToggle.classList.remove('active');
                navMenu.classList.remove('active');
            });
        });
        
        // Close menu when clicking outside
        document.addEventListener('click', (e) => {
            if (!navMenu.contains(e.target) && !menuToggle.contains(e.target)) {
                menuToggle.classList.remove('active');
                navMenu.classList.remove('active');
            }
        });
    }
}

// Initialize Everything
window.addEventListener('load', () => {
    // Initialize Three.js first
    if (typeof THREE !== 'undefined') {
        initThreeJS();
    } else {
        console.error('Three.js not loaded');
    }
    
    // Initialize GSAP animations
    if (typeof gsap !== 'undefined') {
        // Small delay to ensure ScrollTrigger and ScrollToPlugin are loaded
        setTimeout(() => {
            initGSAPAnimations();
            initNavigationScroll();
        }, 150);
    } else {
        console.error('GSAP not loaded');
    }
    
    // Initialize dark mode (should be called after Three.js to update starfield)
    // But we need to check if Three.js is ready
    setTimeout(() => {
        initDarkMode();
    }, 100);
    
    // Initialize mobile menu
    initMobileMenu();
    
    // Initialize cursor trail
    initCursorTrail();
    
    // Initialize contact form handler
    initContactForm();
    
    initNextSectionButton();
    
    // monitorPerformance(); // Uncomment for performance monitoring
});

// Contact Form Handler
function initContactForm() {
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        // Remove preventDefault to allow normal form submission
        // Form will submit normally to Django backend
        contactForm.addEventListener('submit', function(e) {
            // Let the form submit normally - Django will handle it
            // No need to prevent default or show alert
            // Success/error messages will be shown by Django messages framework
        });
    }
}

const initLazyLoadingWhenReady = () => {
    document.removeEventListener('DOMContentLoaded', initLazyLoadingWhenReady);
    initLazyLoading();
};

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initLazyLoadingWhenReady);
} else {
    initLazyLoading();
}


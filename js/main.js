/**
 * Eman Ahmed - Academic Portfolio
 * Main JavaScript File
 */

(function() {
    'use strict';

    // ========================================
    // Mobile Navigation Toggle
    // ========================================
    
    const navToggle = document.querySelector('.nav__toggle');
    const nav = document.querySelector('.nav');
    
    if (navToggle && nav) {
        navToggle.addEventListener('click', function() {
            nav.classList.toggle('nav--open');
            navToggle.classList.toggle('nav__toggle--active');
            
            // Toggle aria-expanded for accessibility
            const isOpen = nav.classList.contains('nav--open');
            navToggle.setAttribute('aria-expanded', isOpen);
            
            // Prevent body scroll when menu is open
            document.body.style.overflow = isOpen ? 'hidden' : '';
        });
        
        // Close menu when clicking a link
        const navLinks = nav.querySelectorAll('.nav__link');
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                nav.classList.remove('nav--open');
                navToggle.classList.remove('nav__toggle--active');
                document.body.style.overflow = '';
            });
        });
        
        // Close menu when clicking outside
        document.addEventListener('click', function(e) {
            if (!nav.contains(e.target) && !navToggle.contains(e.target)) {
                nav.classList.remove('nav--open');
                navToggle.classList.remove('nav__toggle--active');
                document.body.style.overflow = '';
            }
        });
    }

    // ========================================
    // Header Scroll Effect
    // ========================================
    
    const header = document.querySelector('.header');
    
    if (header) {
        let lastScroll = 0;
        
        window.addEventListener('scroll', function() {
            const currentScroll = window.pageYOffset;
            
            // Add shadow when scrolled
            if (currentScroll > 50) {
                header.classList.add('header--scrolled');
            } else {
                header.classList.remove('header--scrolled');
            }
            
            lastScroll = currentScroll;
        });
    }

    // ========================================
    // Active Navigation Link
    // ========================================
    
    function setActiveNavLink() {
        const currentPage = window.location.pathname.split('/').pop() || 'index.html';
        const navLinks = document.querySelectorAll('.nav__link');
        
        navLinks.forEach(link => {
            const href = link.getAttribute('href');
            if (href === currentPage || (currentPage === '' && href === 'index.html')) {
                link.classList.add('nav__link--active');
            } else {
                link.classList.remove('nav__link--active');
            }
        });
    }
    
    setActiveNavLink();

    // ========================================
    // Publication Abstract Toggle
    // ========================================
    
    const abstractToggles = document.querySelectorAll('[data-toggle-abstract]');
    
    abstractToggles.forEach(toggle => {
        toggle.addEventListener('click', function() {
            const publicationId = this.getAttribute('data-toggle-abstract');
            const abstract = document.getElementById(`abstract-${publicationId}`);
            
            if (abstract) {
                abstract.classList.toggle('publication__abstract--visible');
                
                // Update button text
                const isVisible = abstract.classList.contains('publication__abstract--visible');
                this.textContent = isVisible ? 'Hide Abstract' : 'Show Abstract';
            }
        });
    });

    // ========================================
    // Copy Citation to Clipboard
    // ========================================
    
    const copyButtons = document.querySelectorAll('[data-copy-citation]');
    
    copyButtons.forEach(button => {
        button.addEventListener('click', async function() {
            const citation = this.getAttribute('data-copy-citation');
            
            try {
                await navigator.clipboard.writeText(citation);
                
                // Show feedback
                const originalText = this.textContent;
                this.textContent = 'Copied!';
                this.style.backgroundColor = 'var(--color-success)';
                this.style.color = 'var(--color-white)';
                
                setTimeout(() => {
                    this.textContent = originalText;
                    this.style.backgroundColor = '';
                    this.style.color = '';
                }, 2000);
            } catch (err) {
                console.error('Failed to copy citation:', err);
            }
        });
    });

    // ========================================
    // Copy BibTeX to Clipboard
    // ========================================
    
    const bibtexButtons = document.querySelectorAll('[data-copy-bibtex]');
    
    bibtexButtons.forEach(button => {
        button.addEventListener('click', async function() {
            const bibtex = this.getAttribute('data-copy-bibtex');
            
            try {
                await navigator.clipboard.writeText(bibtex);
                
                // Show feedback
                const originalText = this.textContent;
                this.textContent = 'Copied!';
                this.style.backgroundColor = 'var(--color-success)';
                this.style.color = 'var(--color-white)';
                
                setTimeout(() => {
                    this.textContent = originalText;
                    this.style.backgroundColor = '';
                    this.style.color = '';
                }, 2000);
            } catch (err) {
                console.error('Failed to copy BibTeX:', err);
            }
        });
    });

    // ========================================
    // Smooth Scroll for Anchor Links
    // ========================================
    
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                const headerOffset = 100;
                const elementPosition = targetElement.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
                
                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });

    // ========================================
    // Intersection Observer for Animations
    // ========================================
    
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observe elements with animation class
    document.querySelectorAll('.animate-on-scroll').forEach(el => {
        el.style.opacity = '0';
        observer.observe(el);
    });

    // ========================================
    // Form Validation & Submission
    // ========================================
    
    const contactForm = document.getElementById('contact-form');
    
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            // Form will be handled by Formspree
            // Add any additional validation here if needed
            
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.textContent = 'Sending...';
                submitBtn.disabled = true;
            }
        });
    }

    // ========================================
    // Blog Post Reading Time Calculator
    // ========================================
    
    function calculateReadingTime(text) {
        const wordsPerMinute = 200;
        const words = text.trim().split(/\s+/).length;
        const minutes = Math.ceil(words / wordsPerMinute);
        return minutes;
    }
    
    const blogPosts = document.querySelectorAll('[data-reading-time]');
    blogPosts.forEach(post => {
        const content = post.querySelector('.blog-content');
        if (content) {
            const minutes = calculateReadingTime(content.textContent);
            const readingTimeEl = post.querySelector('.reading-time');
            if (readingTimeEl) {
                readingTimeEl.textContent = `${minutes} min read`;
            }
        }
    });

    // ========================================
    // Theme Toggle (Optional Dark Mode)
    // ========================================
    
    const themeToggle = document.getElementById('theme-toggle');
    
    if (themeToggle) {
        // Check for saved theme preference
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme === 'dark') {
            document.body.classList.add('dark-theme');
        }
        
        themeToggle.addEventListener('click', function() {
            document.body.classList.toggle('dark-theme');
            
            // Save preference
            const isDark = document.body.classList.contains('dark-theme');
            localStorage.setItem('theme', isDark ? 'dark' : 'light');
        });
    }

    // ========================================
    // Scroll to Top Button
    // ========================================
    
    const scrollTopBtn = document.getElementById('scroll-top');
    
    if (scrollTopBtn) {
        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 300) {
                scrollTopBtn.classList.add('visible');
            } else {
                scrollTopBtn.classList.remove('visible');
            }
        });
        
        scrollTopBtn.addEventListener('click', function() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }

    // ========================================
    // Lazy Loading Images
    // ========================================
    
    if ('IntersectionObserver' in window) {
        const lazyImages = document.querySelectorAll('img[data-src]');
        
        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        lazyImages.forEach(img => imageObserver.observe(img));
    }

    // ========================================
    // Console Easter Egg
    // ========================================
    
    console.log('%c👋 Hello, fellow developer!', 'font-size: 20px; font-weight: bold;');
    console.log('%cThis is Eman Ahmed\'s academic portfolio.', 'font-size: 14px;');
    console.log('%cInterested in my research? Contact me at eman.ahmed@rutgers.edu', 'font-size: 14px; color: #cd1532;');

})();

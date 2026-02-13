/*
 * Global Loading Indicator Controller
 * ====================================
 * Manages the display of loading indicators during page loads,
 * form submissions, and async operations.
 */

(function() {
    'use strict';

    // Configuration
    const CONFIG = {
        minDisplayTime: 300,        // Minimum time to show loader (ms) - prevents flashing
        autoHideTimeout: 30000,     // Auto-hide after 30 seconds (failsafe)
        showOnNavigation: true,     // Show loader on link clicks (actual navigation)
        showOnFormSubmit: false,    // Don't auto-show for forms (use inline loaders)
        showOnPageLoad: false,      // Don't show during page load
        excludeSelectors: [         // Don't show loader for these elements
            '.no-loader',
            '[data-no-loader]',
            '[target="_blank"]',
            'button[type="button"]', // Don't show for non-submit buttons
            '.modal',                // Don't show for modal interactions
            'a[href^="#"]'          // Don't show for anchor links
        ]
    };

    // Loader state management
    let loaderState = {
        visible: false,
        showTime: null,
        autoHideTimer: null,
        activeRequests: 0
    };

    /**
     * Initialize the global loader
     */
    function initGlobalLoader() {
        // Create loader HTML if it doesn't exist
        if (!document.getElementById('global-loader')) {
            createLoaderElement();
        }

        // Set up event listeners
        setupEventListeners();

        // Hide loader when page is fully loaded
        if (document.readyState === 'complete') {
            hideLoader();
        } else {
            window.addEventListener('load', function() {
                hideLoader();
            });
        }
    }

    /**
     * Create the loader HTML element
     */
    function createLoaderElement() {
        const loaderHTML = `
            <div id="global-loader">
                <div class="loader-container">
                    <div class="loader-spinner"></div>
                    <div class="loader-text">Loading...</div>
                    <div class="loader-subtext">Please wait</div>
                </div>
            </div>
        `;

        document.body.insertAdjacentHTML('afterbegin', loaderHTML);
    }

    /**
     * Set up event listeners for automatic loader display
     */
    function setupEventListeners() {
        // Show loader on form submissions (only if data-show-loader attribute is present)
        document.addEventListener('submit', function(e) {
            const form = e.target;

            // Only show if form explicitly requests it
            if (!form.hasAttribute('data-show-loader')) {
                return;
            }

            // Check if form should trigger loader
            if (!shouldShowLoader(form)) {
                return;
            }

            // Show loader with custom message if specified
            const loadingMessage = form.getAttribute('data-loading-message') || 'Processing...';
            const loadingSubtext = form.getAttribute('data-loading-subtext') || 'Please wait';

            showLoader(loadingMessage, loadingSubtext);
        });

        // Show loader on navigation (link clicks) - only for actual page navigation
        if (CONFIG.showOnNavigation) {
            document.addEventListener('click', function(e) {
                const link = e.target.closest('a');

                if (!link) return;

                // Check if link should trigger loader
                if (!shouldShowLoader(link)) {
                    return;
                }

                // Only show loader for actual navigation (not anchors, not javascript:, not external)
                const href = link.getAttribute('href');
                if (href &&
                    !href.startsWith('#') &&
                    !href.startsWith('javascript:') &&
                    !link.hasAttribute('data-no-loader')) {

                    // Check if it's same-origin navigation
                    const isSameOrigin = href.startsWith('/') ||
                                        href.startsWith(window.location.origin) ||
                                        !href.match(/^https?:\/\//);

                    if (isSameOrigin) {
                        const loadingMessage = link.getAttribute('data-loading-message') || 'Loading page...';
                        showLoader(loadingMessage, 'Please wait');
                    }
                }
            });
        }

        // Handle back/forward browser navigation
        window.addEventListener('pageshow', function(event) {
            // Hide loader when using back/forward buttons
            if (event.persisted) {
                hideLoader(true);
            }
        });

        // Error handling - hide loader on errors
        window.addEventListener('error', function() {
            // Hide loader on JavaScript errors (failsafe)
            setTimeout(function() {
                hideLoader(true);
            }, 1000);
        });
    }

    /**
     * Check if element should trigger loader
     */
    function shouldShowLoader(element) {
        if (!element) return false;

        // Check exclusion selectors
        for (let i = 0; i < CONFIG.excludeSelectors.length; i++) {
            if (element.matches && element.matches(CONFIG.excludeSelectors[i])) {
                return false;
            }
        }

        return true;
    }

    /**
     * Show the global loader
     */
    function showLoader(message, subtext) {
        const loader = document.getElementById('global-loader');
        if (!loader) {
            createLoaderElement();
            return showLoader(message, subtext);
        }

        // Update loader text if provided
        if (message) {
            const textElement = loader.querySelector('.loader-text');
            if (textElement) textElement.textContent = message;
        }

        if (subtext) {
            const subtextElement = loader.querySelector('.loader-subtext');
            if (subtextElement) subtextElement.textContent = subtext;
        }

        // Show loader
        loaderState.visible = true;
        loaderState.showTime = Date.now();
        loaderState.activeRequests++;

        loader.classList.add('active');

        // Failsafe: Auto-hide after timeout
        clearTimeout(loaderState.autoHideTimer);
        loaderState.autoHideTimer = setTimeout(function() {
            console.warn('Loader auto-hidden after timeout');
            hideLoader(true);
        }, CONFIG.autoHideTimeout);
    }

    /**
     * Hide the global loader
     */
    function hideLoader(force) {
        const loader = document.getElementById('global-loader');
        if (!loader) return;

        // Decrement active requests
        if (!force) {
            loaderState.activeRequests = Math.max(0, loaderState.activeRequests - 1);
        } else {
            loaderState.activeRequests = 0;
        }

        // Only hide if no active requests
        if (loaderState.activeRequests > 0 && !force) {
            return;
        }

        // Calculate time shown
        const timeShown = loaderState.showTime ? Date.now() - loaderState.showTime : 0;

        // Ensure minimum display time (prevents flashing)
        const remainingTime = Math.max(0, CONFIG.minDisplayTime - timeShown);

        setTimeout(function() {
            loader.classList.remove('active');
            loaderState.visible = false;
            loaderState.showTime = null;

            // Clear auto-hide timer
            clearTimeout(loaderState.autoHideTimer);

            // Reset loader text to default
            const textElement = loader.querySelector('.loader-text');
            const subtextElement = loader.querySelector('.loader-subtext');
            if (textElement) textElement.textContent = 'Loading...';
            if (subtextElement) subtextElement.textContent = 'Please wait';
        }, remainingTime);
    }

    /**
     * Intercept fetch requests to show/hide loader (REMOVED - too aggressive)
     * Use inline loaders or manual GlobalLoader.show() for AJAX operations instead
     */
    function interceptFetchRequests() {
        // Disabled to prevent blocking UI for all AJAX requests
        // Use button-level or inline loaders for better UX
        return;
    }

    /**
     * Public API - expose functions for manual control
     */
    window.GlobalLoader = {
        show: showLoader,
        hide: hideLoader,
        isVisible: function() {
            return loaderState.visible;
        },
        config: CONFIG
    };

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initGlobalLoader);
    } else {
        initGlobalLoader();
    }

    // Export for module systems (if needed)
    if (typeof module !== 'undefined' && module.exports) {
        module.exports = window.GlobalLoader;
    }

})();

/*
 * Usage Examples:
 * ===============
 *
 * AUTOMATIC BEHAVIOR (Minimal - Opt-in):
 * - Shows on link clicks for same-origin navigation (can disable with data-no-loader)
 * - Does NOT auto-show for forms (use inline loaders instead)
 * - Does NOT auto-show for fetch/AJAX (use inline loaders instead)
 *
 * MANUAL CONTROL (Recommended for AJAX):
 * 1. Full-page blocking loader:
 *    GlobalLoader.show('Processing payment...', 'This may take a moment');
 *    // ... perform operation ...
 *    GlobalLoader.hide();
 *
 * 2. Form with global loader (use sparingly):
 *    <form data-show-loader data-loading-message="Saving..." data-loading-subtext="Please wait">
 *
 * 3. Disable loader for specific link:
 *    <a href="/page" data-no-loader>No Loading Indicator</a>
 *
 * 4. Custom navigation loading message:
 *    <a href="/export" data-loading-message="Generating report...">Export CSV</a>
 *
 * INLINE LOADERS (Recommended for AJAX/Forms):
 * Use button-level spinners instead of full-page blocking:
 *    button.disabled = true;
 *    button.classList.add('btn-loading');
 *    button.textContent = 'Saving...';
 *    // ... perform AJAX ...
 *    button.disabled = false;
 *    button.classList.remove('btn-loading');
 *
 * CHECK STATUS:
 *    if (GlobalLoader.isVisible()) {
 *        console.log('Loader is currently visible');
 *    }
 */

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
        showOnNavigation: true,     // Show loader on link clicks
        showOnFormSubmit: true,     // Show loader on form submissions
        showOnPageLoad: true,       // Show loader during page load
        excludeSelectors: [         // Don't show loader for these elements
            '.no-loader',
            '[data-no-loader]',
            '[target="_blank"]'
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
        // Show loader on form submissions
        if (CONFIG.showOnFormSubmit) {
            document.addEventListener('submit', function(e) {
                const form = e.target;

                // Check if form should trigger loader
                if (!shouldShowLoader(form)) {
                    return;
                }

                // Show loader with custom message if specified
                const loadingMessage = form.getAttribute('data-loading-message') || 'Processing...';
                const loadingSubtext = form.getAttribute('data-loading-subtext') || 'Please wait';

                showLoader(loadingMessage, loadingSubtext);
            });
        }

        // Show loader on navigation (link clicks)
        if (CONFIG.showOnNavigation) {
            document.addEventListener('click', function(e) {
                const link = e.target.closest('a');

                if (!link) return;

                // Check if link should trigger loader
                if (!shouldShowLoader(link)) {
                    return;
                }

                // Only show loader for same-page navigation (not external links)
                const href = link.getAttribute('href');
                if (href && !href.startsWith('#') && !href.startsWith('javascript:')) {
                    const loadingMessage = link.getAttribute('data-loading-message') || 'Loading...';
                    showLoader(loadingMessage);
                }
            });
        }

        // Intercept AJAX/Fetch requests (if using fetch API)
        interceptFetchRequests();

        // Handle back/forward browser navigation
        window.addEventListener('pageshow', function(event) {
            // Hide loader when using back/forward buttons
            if (event.persisted) {
                hideLoader(true);
            }
        });

        // Handle browser unload (page navigation away)
        window.addEventListener('beforeunload', function() {
            showLoader('Loading...', 'Navigating to page');
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
     * Intercept fetch requests to show/hide loader
     */
    function interceptFetchRequests() {
        if (typeof window.fetch === 'undefined') return;

        const originalFetch = window.fetch;

        window.fetch = function() {
            // Show loader for fetch requests
            showLoader('Loading...', 'Fetching data');

            return originalFetch.apply(this, arguments)
                .then(function(response) {
                    hideLoader();
                    return response;
                })
                .catch(function(error) {
                    hideLoader();
                    throw error;
                });
        };
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
 * 1. Manual control:
 *    GlobalLoader.show('Processing payment...', 'This may take a moment');
 *    // ... perform operation ...
 *    GlobalLoader.hide();
 *
 * 2. Custom form loading message:
 *    <form data-loading-message="Saving data..." data-loading-subtext="Please don't close this window">
 *
 * 3. Disable loader for specific link:
 *    <a href="/page" class="no-loader">No Loading Indicator</a>
 *
 * 4. Custom link loading message:
 *    <a href="/export" data-loading-message="Generating report...">Export CSV</a>
 *
 * 5. Check loader status:
 *    if (GlobalLoader.isVisible()) {
 *        console.log('Loader is currently visible');
 *    }
 */

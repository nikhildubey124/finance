/**
 * FinanceTracker - Mobile & UI Enhancements
 */

// ===== Mobile Menu Toggle =====
function initMobileMenu() {
    const nav = document.querySelector('header nav');
    const menuToggle = document.querySelector('.mobile-menu-toggle');
    const menuOverlay = document.querySelector('.mobile-menu-overlay');

    if (!nav || !menuToggle) return;

    menuToggle.addEventListener('click', function() {
        nav.classList.toggle('active');
        menuOverlay.classList.toggle('active');
    });

    menuOverlay.addEventListener('click', function() {
        nav.classList.remove('active');
        menuOverlay.classList.remove('active');
    });

    // Close menu when clicking a link
    nav.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', function() {
            nav.classList.remove('active');
            menuOverlay.classList.remove('active');
        });
    });
}

// ===== Toast Notifications =====
const Toast = {
    container: null,

    init() {
        if (!this.container) {
            this.container = document.createElement('div');
            this.container.className = 'toast-container';
            document.body.appendChild(this.container);
        }
    },

    show(message, type = 'info', duration = 3000) {
        this.init();

        const toast = document.createElement('div');
        toast.className = `toast ${type}`;

        const icons = {
            success: '✓',
            error: '✕',
            info: 'ℹ'
        };

        toast.innerHTML = `
            <span class="toast-icon">${icons[type] || icons.info}</span>
            <div class="toast-message">${message}</div>
            <button class="toast-close">&times;</button>
        `;

        this.container.appendChild(toast);

        const closeBtn = toast.querySelector('.toast-close');
        closeBtn.addEventListener('click', () => this.remove(toast));

        // Auto remove after duration
        setTimeout(() => this.remove(toast), duration);
    },

    remove(toast) {
        toast.style.animation = 'slideIn 0.3s ease reverse';
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 300);
    },

    success(message, duration) {
        this.show(message, 'success', duration);
    },

    error(message, duration) {
        this.show(message, 'error', duration);
    },

    info(message, duration) {
        this.show(message, 'info', duration);
    }
};

// ===== Loading Spinner =====
// Integrated with GlobalLoader for consistency
const Loading = {
    show(message, subtext) {
        // Use GlobalLoader if available, fallback to legacy behavior
        if (window.GlobalLoader) {
            window.GlobalLoader.show(message || 'Processing...', subtext || 'Please wait');
        }
    },

    hide() {
        // Use GlobalLoader if available
        if (window.GlobalLoader) {
            window.GlobalLoader.hide();
        }
    }
};

// ===== Form Submission Enhancement =====
function enhanceForms() {
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                // Disable button to prevent double-submission
                submitBtn.disabled = true;
                submitBtn.style.opacity = '0.6';

                // Store original text
                if (!submitBtn.dataset.originalText) {
                    submitBtn.dataset.originalText = submitBtn.textContent;
                }
                submitBtn.textContent = 'Processing...';

                // GlobalLoader handles showing the loader automatically
                // No need to call Loading.show() here as it would be redundant
            }
        });
    });
}

// ===== Chart Responsive Helper =====
function makeChartsResponsive() {
    // Ensure charts resize properly on orientation change
    window.addEventListener('orientationchange', function() {
        setTimeout(() => {
            window.dispatchEvent(new Event('resize'));
        }, 200);
    });
}

// ===== Initialize Everything =====
document.addEventListener('DOMContentLoaded', function() {
    initMobileMenu();
    enhanceForms();
    makeChartsResponsive();

    // Show success message if present (from URL params)
    const urlParams = new URLSearchParams(window.location.search);
    const successMsg = urlParams.get('success');
    if (successMsg) {
        Toast.success(decodeURIComponent(successMsg));
    }
    const errorMsg = urlParams.get('error');
    if (errorMsg) {
        Toast.error(decodeURIComponent(errorMsg));
    }
});

// ===== Export for global use =====
window.Toast = Toast;
window.Loading = Loading;

const QuickView = {
    init: function () {
        this.modal = document.getElementById('quick-view');
        this.titleElement = document.getElementById('quick-view-title');
        this.closeButton = document.querySelector('.close');

        if (this.closeButton) {
            this.closeButton.addEventListener('click', () => this.close());
        }
    },

    show: function (productId) {
        fetch(`/api/products/${productId}`)
            .then(response => {
                if (!response.ok) throw new Error('Product not found');
                return response.json();
            })
            .then(product => {
                this.titleElement.textContent = product.name;
                // Populate other fields here
                this.modal.style.display = 'block';
            })
            .catch(error => {
                console.error('Error loading product:', error);
                // Show error message to user
            });
    },

    close: function () {
        this.modal.style.display = 'none';
    }
};

// Carousel Module
const Carousel = {
    init: function () {
        this.carousel = document.querySelector('.carousel-inner');
        this.items = document.querySelectorAll('.carousel-item');
        this.indicators = document.querySelectorAll('.indicator');
        this.prevBtn = document.querySelector('.prev');
        this.nextBtn = document.querySelector('.next');
        this.currentIndex = 0;
        this.itemCount = this.items.length;
        this.autoSlideInterval = null;

        if (this.items.length === 0) return;

        this.setupEventListeners();
        this.startAutoSlide();
    },

    setupEventListeners: function () {
        if (this.nextBtn) this.nextBtn.addEventListener('click', () => this.nextSlide());
        if (this.prevBtn) this.prevBtn.addEventListener('click', () => this.prevSlide());

        this.indicators.forEach((indicator, index) => {
            indicator.addEventListener('click', () => this.goToSlide(index));
        });
    },

    updateCarousel: function () {
        this.carousel.style.transform = `translateX(-${this.currentIndex * 100}%)`;
        this.indicators.forEach((indicator, index) => {
            indicator.classList.toggle('active', index === this.currentIndex);
        });
    },

    nextSlide: function () {
        this.currentIndex = (this.currentIndex + 1) % this.itemCount;
        this.updateCarousel();
    },

    prevSlide: function () {
        this.currentIndex = (this.currentIndex - 1 + this.itemCount) % this.itemCount;
        this.updateCarousel();
    },

    goToSlide: function (index) {
        this.currentIndex = index;
        this.updateCarousel();
    },

    startAutoSlide: function () {
        this.autoSlideInterval = setInterval(() => this.nextSlide(), 5000);
    },

    stopAutoSlide: function () {
        if (this.autoSlideInterval) {
            clearInterval(this.autoSlideInterval);
        }
    }
};

// Recently Viewed Products Module
const RecentlyViewed = {
    init: function () {
        this.viewedContainer = document.getElementById('recently-viewed');
        if (!this.viewedContainer) return;

        this.showRecentlyViewed();
    },

    trackProductView: function (productId) {
        let viewed = JSON.parse(localStorage.getItem('viewed') || []);
        viewed = [productId, ...viewed.filter(id => id !== productId)].slice(0, 5);
        localStorage.setItem('viewed', JSON.stringify(viewed));
    },

    showRecentlyViewed: function () {
        const viewed = JSON.parse(localStorage.getItem('viewed') || []);

        if (viewed.length === 0) {
            this.viewedContainer.style.display = 'none';
            return;
        }

        // Create product cards for recently viewed items
        viewed.forEach(id => {
            // Implementation would fetch product data and create cards
        });
    }
};

// Search Module
const Search = {
    init: function () {
        this.searchInput = document.getElementById('search');
        this.resultsContainer = document.getElementById('search-results');

        if (this.searchInput && this.resultsContainer) {
            this.searchInput.addEventListener('input', (e) => this.showSuggestions(e.target.value));
        }
    },

    showSuggestions: function (query) {
        if (query.length < 2) {
            this.resultsContainer.innerHTML = '';
            return;
        }

        fetch(`/api/search?q=${encodeURIComponent(query)}`)
            .then(response => {
                if (!response.ok) throw new Error('Search failed');
                return response.json();
            })
            .then(results => {
                this.resultsContainer.innerHTML = results.map(item => `
  <a href="/product/${item.id}" class="search-result-item">${item.name}</a>
`).join('');
            })
            .catch(error => {
                console.error('Search error:', error);
                this.resultsContainer.innerHTML = '<div class="search-error">Failed to load results</div>';
            });
    }
};

// Initialize all modules when DOM is loaded
document.addEventListener('DOMContentLoaded', function () {
    QuickView.init();
    Carousel.init();
    RecentlyViewed.init();
    Search.init();

    // Example of attaching quick view to product cards
    document.querySelectorAll('.product-card').forEach(card => {
        card.addEventListener('click', function () {
            const productId = this.dataset.productId;
            QuickView.show(productId);
        });
    });
});

# UI/UX Design Specification

## Design Philosophy
- **Professional & Clean**: Government-appropriate aesthetic
- **Nepali-First**: Optimized for Nepali language and culture
- **Print-Ready**: Designed with A4 PDF output in mind
- **Accessible**: WCAG 2.1 AA compliant
- **Responsive**: Works on all device sizes

## Color Palette

### Primary Colors
```css
:root {
  /* Government of Nepal Colors */
  --primary-red: #DC143C;        /* Crimson - Nepal flag red */
  --primary-blue: #003893;       /* Dark blue - official government blue */
  --primary-gold: #FFD700;       /* Gold - ceremonial accent */
  
  /* Supporting Colors */
  --success-green: #28a745;      /* Success states */
  --warning-orange: #fd7e14;     /* Warnings */
  --danger-red: #dc3545;         /* Errors */
  --info-blue: #17a2b8;          /* Information */
  
  /* Neutral Colors */
  --gray-900: #212529;           /* Dark text */
  --gray-700: #495057;           /* Medium text */
  --gray-500: #6c757d;           /* Light text */
  --gray-300: #dee2e6;           /* Borders */
  --gray-100: #f8f9fa;           /* Light backgrounds */
  --white: #ffffff;              /* Pure white */
}
```

### Usage Guidelines
- **Primary Red**: Headers, important CTAs, navigation highlights
- **Primary Blue**: Links, secondary actions, data highlights
- **Gold**: Special accents, achievements, important metrics
- **Neutrals**: Body text, backgrounds, borders

## Typography

### Font Stack
```css
/* Nepali Text */
.nepali-text {
  font-family: 'Mukti', 'Kalimati', 'Devanagari', serif;
  font-feature-settings: "liga" 1, "kern" 1;
}

/* English Text */
.english-text {
  font-family: 'Inter', 'Segoe UI', 'Roboto', sans-serif;
  font-feature-settings: "liga" 1, "kern" 1;
}

/* Monospace (Code/Data) */
.monospace {
  font-family: 'JetBrains Mono', 'Consolas', monospace;
}
```

### Type Scale
```css
/* Headings */
.h1 { font-size: 2.5rem; font-weight: 700; line-height: 1.2; }
.h2 { font-size: 2rem; font-weight: 600; line-height: 1.3; }
.h3 { font-size: 1.75rem; font-weight: 600; line-height: 1.3; }
.h4 { font-size: 1.5rem; font-weight: 500; line-height: 1.4; }
.h5 { font-size: 1.25rem; font-weight: 500; line-height: 1.4; }
.h6 { font-size: 1.125rem; font-weight: 500; line-height: 1.4; }

/* Body Text */
.body-large { font-size: 1.125rem; line-height: 1.6; }
.body-normal { font-size: 1rem; line-height: 1.5; }
.body-small { font-size: 0.875rem; line-height: 1.5; }
.caption { font-size: 0.75rem; line-height: 1.4; }
```

## Layout System

### Grid System
```css
/* Container Sizes */
.container-sm { max-width: 540px; }
.container-md { max-width: 720px; }
.container-lg { max-width: 960px; }
.container-xl { max-width: 1140px; }
.container-xxl { max-width: 1320px; }

/* A4 Optimized Layout */
.a4-container {
  max-width: 794px; /* A4 width in pixels at 96 DPI */
  margin: 0 auto;
  padding: 2rem;
}
```

### Component Spacing
```css
/* Spacing Scale (rem) */
--space-1: 0.25rem;  /* 4px */
--space-2: 0.5rem;   /* 8px */
--space-3: 0.75rem;  /* 12px */
--space-4: 1rem;     /* 16px */
--space-5: 1.25rem;  /* 20px */
--space-6: 1.5rem;   /* 24px */
--space-8: 2rem;     /* 32px */
--space-10: 2.5rem;  /* 40px */
--space-12: 3rem;    /* 48px */
--space-16: 4rem;    /* 64px */
```

## Component Library

### Header Component
```html
<header class="main-header">
  <div class="header-brand">
    <img src="logo.png" alt="गढवा नगरपालिका" class="logo">
    <div class="brand-text">
      <h1 class="municipality-name nepali-text">गढवा नगरपालिका</h1>
      <p class="tagline">डिजिटल प्रोफाइल प्रतिवेदन</p>
    </div>
  </div>
  <nav class="main-navigation">
    <!-- Navigation items -->
  </nav>
</header>
```

### Navigation Component
```html
<nav class="chapter-navigation">
  <div class="nav-item">
    <span class="chapter-number">१</span>
    <span class="chapter-title nepali-text">परिचय</span>
  </div>
  <!-- More chapters -->
</nav>
```

### Data Table Component
```html
<div class="data-table-container">
  <table class="data-table">
    <thead>
      <tr>
        <th class="nepali-text">विवरण</th>
        <th class="nepali-text">संख्या</th>
        <th class="nepali-text">प्रतिशत</th>
      </tr>
    </thead>
    <tbody>
      <!-- Table rows -->
    </tbody>
  </table>
</div>
```

### Chart Component
```html
<div class="chart-container">
  <div class="chart-header">
    <h3 class="chart-title nepali-text">जनसंख्या वितरण</h3>
    <p class="chart-subtitle">वडा अनुसार</p>
  </div>
  <div class="chart-canvas">
    <canvas id="populationChart"></canvas>
  </div>
  <div class="chart-legend">
    <!-- Legend items -->
  </div>
</div>
```

### Statistics Card
```html
<div class="stat-card">
  <div class="stat-icon">
    <i class="icon-people"></i>
  </div>
  <div class="stat-content">
    <h3 class="stat-number">१२,३४५</h3>
    <p class="stat-label nepali-text">कुल जनसंख्या</p>
  </div>
</div>
```

## PDF-Specific Styling

### Page Layout
```css
@media print {
  @page {
    size: A4;
    margin: 2.5cm 2cm 2cm 2cm;
    
    @top-center {
      content: "गढवा नगरपालिका - डिजिटल प्रोफाइल प्रतिवेदन";
      font-size: 10pt;
      color: #666;
    }
    
    @bottom-right {
      content: "पृष्ठ " counter(page) " को " counter(pages);
      font-size: 9pt;
      color: #666;
    }
  }
  
  /* Page breaks */
  .chapter { page-break-before: always; }
  .no-break { page-break-inside: avoid; }
  
  /* Hide web-only elements */
  .web-only { display: none; }
  
  /* Adjust colors for print */
  .chart-container { 
    background: white !important;
    border: 1px solid #ccc;
  }
}
```

### Typography for Print
```css
@media print {
  /* Ensure good contrast */
  body { color: #000 !important; }
  
  /* Optimize font sizes */
  h1 { font-size: 18pt; }
  h2 { font-size: 16pt; }
  h3 { font-size: 14pt; }
  h4 { font-size: 12pt; }
  p, td, th { font-size: 10pt; }
  
  /* Table styling */
  table {
    border-collapse: collapse;
    width: 100%;
  }
  
  th, td {
    border: 1px solid #333;
    padding: 8pt;
    text-align: left;
  }
  
  th {
    background-color: #f0f0f0 !important;
    font-weight: bold;
  }
}
```

## Interactive Elements

### Navigation Behavior
```javascript
// Smooth scrolling for in-page navigation
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();
    document.querySelector(this.getAttribute('href')).scrollIntoView({
      behavior: 'smooth'
    });
  });
});

// Highlight current section in navigation
const observerOptions = {
  rootMargin: '-20% 0px -70% 0px'
};

const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      // Update active navigation item
      updateActiveNavItem(entry.target.id);
    }
  });
}, observerOptions);
```

### Chart Interactions
```javascript
// Chart.js configuration for better print output
const chartConfig = {
  responsive: true,
  maintainAspectRatio: true,
  plugins: {
    legend: {
      position: 'bottom',
      labels: {
        usePointStyle: true,
        padding: 20
      }
    }
  },
  animation: {
    // Disable animations for PDF generation
    duration: window.isPdfMode ? 0 : 1000
  }
};
```

## Responsive Breakpoints
```css
/* Mobile First Approach */
/* Small devices (576px and up) */
@media (min-width: 576px) { }

/* Medium devices (768px and up) */
@media (min-width: 768px) { }

/* Large devices (992px and up) */
@media (min-width: 992px) { }

/* Extra large devices (1200px and up) */
@media (min-width: 1200px) { }

/* XXL devices (1400px and up) */
@media (min-width: 1400px) { }
```

## Accessibility Guidelines

### Keyboard Navigation
- All interactive elements accessible via keyboard
- Logical tab order throughout the interface
- Focus indicators clearly visible
- Skip links for main content areas

### Screen Reader Support
```html
<!-- Proper ARIA labels -->
<nav aria-label="मुख्य नेभिगेसन">
<main aria-label="मुख्य सामग्री">
<aside aria-label="साइडबार">

<!-- Chart accessibility -->
<canvas aria-describedby="chart-description">
<div id="chart-description" class="sr-only">
  यो चार्टले जनसंख्याको वितरण देखाउँछ...
</div>
```

### Color Contrast
- All text meets WCAG AA standards (4.5:1 ratio)
- Important information not conveyed by color alone
- High contrast mode support

## Performance Considerations

### Loading Strategy
```javascript
// Lazy load charts and heavy content
const chartObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      loadChart(entry.target);
      chartObserver.unobserve(entry.target);
    }
  });
});

// Progressive image loading
const imageObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const img = entry.target;
      img.src = img.dataset.src;
      img.classList.remove('lazy');
      imageObserver.unobserve(img);
    }
  });
});
```

### Bundle Optimization
- Critical CSS inlined
- Non-critical CSS loaded asynchronously
- JavaScript modules loaded on demand
- Images optimized and properly sized

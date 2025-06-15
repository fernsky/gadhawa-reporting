# PDF Generation & Styling Specification

## Overview

This document outlines the approach for generating beautiful, professional A4 PDF reports from HTML/CSS using WeasyPrint, with special considerations for Nepali language content and government report standards.

## Technology Stack

### Core Technologies

- **WeasyPrint**: HTML/CSS to PDF conversion
- **Django Templates**: Dynamic content generation
- **CSS Grid/Flexbox**: Layout control
- **Chart.js**: Data visualization
- **Custom CSS**: Print-optimized styling

### Font Requirements

```css
/* Nepali Font Stack */
@font-face {
  font-family: "Mukti";
  src: url("../fonts/mukti/Mukti.woff2") format("woff2"), url("../fonts/mukti/Mukti.woff")
      format("woff");
  font-weight: normal;
  font-style: normal;
}

@font-face {
  font-family: "Kalimati";
  src: url("../fonts/kalimati/Kalimati.woff2") format("woff2"), url("../fonts/kalimati/Kalimati.woff")
      format("woff");
  font-weight: normal;
  font-style: normal;
}

/* English Font Stack */
@font-face {
  font-family: "Inter";
  src: url("../fonts/inter/Inter-Variable.woff2") format("woff2-variations");
  font-weight: 100 900;
  font-style: normal;
}
```

## Page Layout Structure

### A4 Page Setup

```css
@page {
  size: A4 portrait;
  margin: 2.5cm 2cm 2cm 2cm;

  /* Header */
  @top-left {
    content: element(header-left);
    width: 30%;
  }

  @top-center {
    content: element(header-center);
    width: 40%;
  }

  @top-right {
    content: element(header-right);
    width: 30%;
  }

  /* Footer */
  @bottom-left {
    content: "तयारी मिति: " attr(data-date);
    font-size: 8pt;
    color: #666;
  }

  @bottom-center {
    content: "लुङ्ग्री नगरपालिका";
    font-size: 8pt;
    color: #666;
    font-family: "Mukti", serif;
  }

  @bottom-right {
    content: "पृष्ठ " counter(page) " को " counter(pages);
    font-size: 8pt;
    color: #666;
  }
}

/* Special pages */
@page :first {
  margin: 0;
  @top-left {
    content: none;
  }
  @top-center {
    content: none;
  }
  @top-right {
    content: none;
  }
  @bottom-left {
    content: none;
  }
  @bottom-center {
    content: none;
  }
  @bottom-right {
    content: none;
  }
}

@page chapter {
  page-break-before: always;
  @top-center {
    content: string(chapter-title);
    font-weight: bold;
  }
}
```

### Document Structure

```html
<!DOCTYPE html>
<html lang="ne">
  <head>
    <meta charset="UTF-8" />
    <title>{{ municipality.name_nepali }} - डिजिटल प्रोफाइल प्रतिवेदन</title>
    <link rel="stylesheet" href="{% static 'css/pdf-report.css' %}" />
  </head>
  <body>
    <!-- Cover Page -->
    <div class="cover-page">
      <div class="header-section">
        <img
          src="{% static 'images/nepal-logo.png' %}"
          alt="नेपाल सरकार"
          class="national-logo"
        />
        <img
          src="{% static 'images/province-logo.png' %}"
          alt="प्रदेश सरकार"
          class="province-logo"
        />
      </div>

      <div class="title-section">
        <h1 class="main-title">{{ municipality.name_nepali }}</h1>
        <h2 class="report-title">डिजिटल प्रोफाइल प्रतिवेदन</h2>
        <p class="subtitle">
          {{ municipality.district_nepali }}, {{ municipality.province_nepali }}
        </p>
      </div>

      <div class="date-section">
        <p class="preparation-date">
          तयारी मिति: {{ report.created_at|date:"Y/m/d" }}
        </p>
      </div>

      <div class="footer-section">
        <img
          src="{% static 'images/municipality-logo.png' %}"
          alt="{{ municipality.name_nepali }}"
          class="municipality-logo"
        />
      </div>
    </div>

    <!-- Table of Contents -->
    <div class="table-of-contents page-break">
      <h2>विषय सूची</h2>
      <div class="toc-entries">
        {% for chapter in chapters %}
        <div class="toc-entry">
          <span class="toc-title">{{ chapter.title_nepali }}</span>
          <span class="toc-dots"></span>
          <span class="toc-page">{{ chapter.page_number }}</span>
        </div>
        {% endfor %}
      </div>
    </div>

    <!-- List of Figures -->
    <div class="list-of-figures page-break">
      <h2>चित्रहरूको सूची</h2>
      <!-- Auto-generated from charts -->
    </div>

    <!-- List of Tables -->
    <div class="list-of-tables page-break">
      <h2>तालिकाहरूको सूची</h2>
      <!-- Auto-generated from tables -->
    </div>

    <!-- Chapters -->
    {% for chapter in chapters %}
    <div class="chapter" style="page: chapter;">
      <h1
        class="chapter-title"
        style="string-set: chapter-title '{{ chapter.title_nepali }}';"
      >
        {{ chapter.title_nepali }}
      </h1>
      {{ chapter.content|safe }}
    </div>
    {% endfor %}
  </body>
</html>
```

## Typography System

### Nepali Text Styling

```css
.nepali-text {
  font-family: "Mukti", "Kalimati", "Devanagari", serif;
  line-height: 1.8;
  word-spacing: 0.1em;
  letter-spacing: 0.02em;
}

/* Heading hierarchy */
.chapter-title {
  font-size: 18pt;
  font-weight: bold;
  color: #1a365d;
  margin-bottom: 24pt;
  text-align: center;
  page-break-after: avoid;
}

.section-title {
  font-size: 14pt;
  font-weight: bold;
  color: #2d3748;
  margin-top: 18pt;
  margin-bottom: 12pt;
  page-break-after: avoid;
}

.subsection-title {
  font-size: 12pt;
  font-weight: bold;
  color: #4a5568;
  margin-top: 14pt;
  margin-bottom: 8pt;
  page-break-after: avoid;
}

/* Body text */
.body-text {
  font-size: 10pt;
  line-height: 1.6;
  margin-bottom: 8pt;
  text-align: justify;
  hyphens: auto;
}

/* Numbers in Nepali */
.nepali-number {
  font-family: "Mukti", serif;
  font-variant-numeric: lining-nums;
}
```

### English Text Styling

```css
.english-text {
  font-family: "Inter", "Segoe UI", "Roboto", sans-serif;
  line-height: 1.5;
}

.table-english {
  font-family: "Inter", sans-serif;
  font-size: 9pt;
  line-height: 1.4;
}
```

## Table Styling

### Standard Data Table

```css
.data-table {
  width: 100%;
  border-collapse: collapse;
  margin: 12pt 0;
  page-break-inside: avoid;
  font-size: 9pt;
  line-height: 1.3;
}

.data-table th {
  background-color: #f7fafc;
  border: 1pt solid #2d3748;
  padding: 8pt 6pt;
  text-align: center;
  font-weight: bold;
  color: #1a202c;
  vertical-align: middle;
}

.data-table td {
  border: 0.5pt solid #718096;
  padding: 6pt;
  text-align: center;
  vertical-align: middle;
}

.data-table .text-left {
  text-align: left;
}
.data-table .text-right {
  text-align: right;
}

/* Zebra striping */
.data-table tbody tr:nth-child(even) {
  background-color: #f8f9fa;
}

/* Table caption */
.table-caption {
  font-size: 10pt;
  font-weight: bold;
  text-align: center;
  margin-bottom: 8pt;
  color: #2d3748;
}

.table-source {
  font-size: 8pt;
  font-style: italic;
  text-align: left;
  margin-top: 4pt;
  color: #718096;
}
```

### Summary Table Style

```css
.summary-table {
  width: 100%;
  border: 2pt solid #2d3748;
  margin: 16pt 0;
  page-break-inside: avoid;
}

.summary-table th {
  background-color: #2d3748;
  color: white;
  padding: 10pt;
  font-weight: bold;
  text-align: center;
}

.summary-table td {
  padding: 8pt;
  border-bottom: 1pt solid #e2e8f0;
}

.summary-table .total-row {
  background-color: #edf2f7;
  font-weight: bold;
}
```

## Chart Integration

### Chart Container

```css
.chart-container {
  width: 100%;
  margin: 16pt 0;
  page-break-inside: avoid;
  text-align: center;
}

.chart-title {
  font-size: 11pt;
  font-weight: bold;
  margin-bottom: 8pt;
  color: #2d3748;
}

.chart-canvas {
  width: 100%;
  height: 300pt;
  margin: 8pt 0;
}

.chart-legend {
  margin-top: 8pt;
  font-size: 9pt;
  text-align: center;
}

.chart-source {
  font-size: 8pt;
  font-style: italic;
  color: #718096;
  margin-top: 4pt;
}
```

### Chart Configuration for PDF

```javascript
// Chart.js configuration optimized for PDF output
const pdfChartConfig = {
  responsive: false,
  animation: false,
  devicePixelRatio: 2, // Higher DPI for print
  plugins: {
    legend: {
      position: "bottom",
      labels: {
        usePointStyle: true,
        padding: 15,
        font: {
          size: 10,
        },
      },
    },
    tooltip: {
      enabled: false, // Disable for PDF
    },
  },
  scales: {
    x: {
      ticks: {
        font: {
          size: 9,
        },
      },
    },
    y: {
      ticks: {
        font: {
          size: 9,
        },
      },
    },
  },
};
```

## Statistics Cards

### Stat Box Layout

```css
.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12pt;
  margin: 16pt 0;
  page-break-inside: avoid;
}

.stat-box {
  border: 1pt solid #e2e8f0;
  border-radius: 4pt;
  padding: 12pt;
  text-align: center;
  background-color: #f7fafc;
}

.stat-number {
  font-size: 18pt;
  font-weight: bold;
  color: #1a365d;
  margin-bottom: 4pt;
}

.stat-label {
  font-size: 9pt;
  color: #4a5568;
  line-height: 1.3;
}

.stat-box.highlight {
  background-color: #ebf8ff;
  border-color: #3182ce;
}

.stat-box.highlight .stat-number {
  color: #1e40af;
}
```

## Page Break Controls

### Strategic Page Breaks

```css
/* Force page breaks */
.page-break {
  page-break-before: always;
}

.page-break-after {
  page-break-after: always;
}

/* Avoid page breaks */
.no-break {
  page-break-inside: avoid;
}

.keep-with-next {
  page-break-after: avoid;
}

/* Widows and orphans */
h1,
h2,
h3,
h4,
h5,
h6 {
  page-break-after: avoid;
  orphans: 3;
  widows: 3;
}

p {
  orphans: 2;
  widows: 2;
}

/* Table page breaks */
.data-table {
  page-break-inside: avoid;
}

.data-table tr {
  page-break-inside: avoid;
}
```

## Special Elements

### Map Integration

```css
.map-container {
  width: 100%;
  height: 400pt;
  margin: 16pt 0;
  border: 1pt solid #e2e8f0;
  page-break-inside: avoid;
}

.map-title {
  font-size: 11pt;
  font-weight: bold;
  text-align: center;
  margin-bottom: 8pt;
}

.map-legend {
  margin-top: 8pt;
  font-size: 8pt;
  padding: 8pt;
  background-color: #f7fafc;
  border: 1pt solid #e2e8f0;
}
```

### Highlighted Text Boxes

```css
.info-box {
  background-color: #ebf8ff;
  border-left: 4pt solid #3182ce;
  padding: 12pt;
  margin: 12pt 0;
  page-break-inside: avoid;
}

.warning-box {
  background-color: #fffbeb;
  border-left: 4pt solid #f59e0b;
  padding: 12pt;
  margin: 12pt 0;
  page-break-inside: avoid;
}

.success-box {
  background-color: #f0fff4;
  border-left: 4pt solid #10b981;
  padding: 12pt;
  margin: 12pt 0;
  page-break-inside: avoid;
}
```

### Appendix Styling

```css
.appendix {
  page-break-before: always;
  counter-reset: appendix-counter;
}

.appendix-item {
  margin-bottom: 24pt;
  page-break-inside: avoid;
}

.appendix-title {
  font-size: 12pt;
  font-weight: bold;
  margin-bottom: 8pt;
  counter-increment: appendix-counter;
}

.appendix-title::before {
  content: "अनुसूची - " counter(appendix-counter, decimal) ": ";
}
```

## WeasyPrint Configuration

### Python Configuration

```python
from weasyprint import HTML, CSS
from weasyprint.fonts import FontConfiguration

def generate_pdf_report(html_content, css_files=None):
    """
    Generate PDF from HTML content with custom CSS
    """
    # Font configuration
    font_config = FontConfiguration()

    # CSS files
    css = []
    if css_files:
        for css_file in css_files:
            css.append(CSS(filename=css_file, font_config=font_config))

    # Generate PDF
    html_doc = HTML(string=html_content)
    pdf_bytes = html_doc.write_pdf(
        stylesheets=css,
        font_config=font_config,
        optimize_images=True,
        presentational_hints=True
    )

    return pdf_bytes

# Usage in Django view
def export_pdf(request, municipality_id):
    municipality = get_object_or_404(Municipality, id=municipality_id)

    # Render HTML template
    html_content = render_to_string('reports/pdf/full_report.html', {
        'municipality': municipality,
        'chapters': get_report_chapters(municipality),
        'statistics': get_municipality_statistics(municipality),
    })

    # Generate PDF
    css_files = [
        settings.STATIC_ROOT + '/css/pdf-report.css',
        settings.STATIC_ROOT + '/css/pdf-tables.css',
        settings.STATIC_ROOT + '/css/pdf-charts.css',
    ]

    pdf_bytes = generate_pdf_report(html_content, css_files)

    # Return PDF response
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{municipality.name}_report.pdf"'

    return response
```

### Performance Optimization

```python
# Async PDF generation for large reports
import asyncio
from celery import shared_task

@shared_task
def generate_report_async(municipality_id, template_id, user_id):
    """
    Asynchronous PDF generation using Celery
    """
    try:
        municipality = Municipality.objects.get(id=municipality_id)
        template = ReportTemplate.objects.get(id=template_id)
        user = User.objects.get(id=user_id)

        # Create report record
        report = GeneratedReport.objects.create(
            municipality=municipality,
            template=template,
            requested_by=user,
            status='processing'
        )

        # Generate content
        html_content = render_report_content(municipality, template)

        # Generate PDF
        pdf_bytes = generate_pdf_report(html_content)

        # Save to file
        pdf_file = ContentFile(pdf_bytes)
        report.pdf_file.save(
            f'{municipality.name}_report_{report.id}.pdf',
            pdf_file
        )

        # Update status
        report.status = 'completed'
        report.completed_at = timezone.now()
        report.file_size_bytes = len(pdf_bytes)
        report.save()

        # Send notification to user
        send_report_ready_notification(user, report)

    except Exception as e:
        report.status = 'failed'
        report.error_message = str(e)
        report.save()

        # Send error notification
        send_report_error_notification(user, report, str(e))
```

This PDF generation system provides:

- Professional A4 layout optimized for printing
- Full Nepali language support with proper fonts
- Automatic page numbering and headers/footers
- Table of contents and figure lists
- Strategic page break control
- High-quality chart integration
- Asynchronous generation for large reports
- Error handling and progress tracking

# Gadhawa Digital Profile Report System
## Complete Documentation & Design Specification

## 📋 Project Overview

This repository contains the complete documentation and design specifications for the **Gadhawa Digital Profile Report System** - a comprehensive web application for generating beautiful, professional A4 PDF reports for Nepali municipalities.

### 🎯 Project Goals
- **Beautiful PDF Reports**: Professional A4 layout optimized for printing
- **Interactive Web Interface**: Browse and explore municipal data online
- **Nepali Language Support**: Full Unicode support for Nepali content
- **Data Visualization**: Charts, graphs, and statistical representations
- **Government Standards**: Compliance with official report structures
- **Lightning Fast Development**: MVP in 3-5 days using Django

### 🏗️ Architecture Overview
```
Django + DRF + PostgreSQL + WeasyPrint + Bootstrap + HTMX + Alpine.js
```

## 📚 Documentation Structure

### 📖 Core Documentation
- **[Report Structure](docs/report-structure.md)** - Official 13-chapter report format
- **[Project Overview](docs/project-overview.md)** - Vision, architecture, and technical approach
- **[Project Structure](docs/project-structure.md)** - Directory layout and organization
- **[Database Design](docs/database-design.md)** - Complete data models and relationships
- **[Requirements](docs/requirements.md)** - Dependencies and setup instructions
- **[Development Roadmap](docs/development-roadmap.md)** - 5-day implementation plan

### 🎨 Design Specifications
- **[UI/UX Specification](docs/design/ui-ux-specification.md)** - Complete design system
- **[PDF Generation](docs/design/pdf-generation.md)** - Print-optimized styling and layouts

### 🔌 API Documentation
- **[API Endpoints](docs/api/endpoints.md)** - Complete REST API specification

## 🚀 Quick Start Guide

### Prerequisites
```bash
Python 3.11+
PostgreSQL 13+
4GB+ RAM
50GB+ Storage
```

### Installation
```bash
# Clone repository
git clone <repository-url>
cd gadhawa-report

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements/development.txt

# Setup environment
cp .env.example .env
# Edit .env with your configuration

# Setup database
python manage.py migrate
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

## 🏛️ Report Structure

The system generates reports following the official 13-chapter structure:

1. **परिच्छेद – १: परिचय** (Introduction)
2. **परिच्छेद – २: गाउँ÷नगरपालिकाको चिनारी** (Municipality Profile)
3. **परिच्छेद – ३: पारिवारिक विवरण तथा जनसंख्याको अवस्था** (Demographics)
4. **परिच्छेद – ४: आर्थिक अवस्था** (Economic Status)
5. **परिच्छेद – ५: सामाजिक अवस्था** (Social Status)
6. **परिच्छेद – ६: वन तथा वातावरणीय स्थिति** (Environment)
7. **परिच्छेद – ७: भौतिक विकासको अवस्था** (Infrastructure)
8. **परिच्छेद – ८: संस्थागत तथा सुशासनको स्थिति** (Governance)

Plus comprehensive appendices and data tables.

## 🔧 Technical Stack

### Backend
- **Django 5.0+** - Web framework
- **Django REST Framework** - API development
- **PostgreSQL** - Primary database
- **WeasyPrint** - PDF generation
- **Celery** - Background tasks
- **Redis** - Caching and task queue

### Frontend
- **Django Templates** - Server-side rendering
- **Bootstrap 5** - CSS framework
- **HTMX** - Dynamic interactions
- **Alpine.js** - JavaScript reactivity
- **Chart.js** - Data visualization

### Infrastructure
- **Gunicorn** - WSGI server
- **Nginx** - Reverse proxy
- **Docker** - Containerization
- **PostgreSQL** - Database

## 📊 Key Features

### 🖨️ PDF Generation
- Professional A4 layout
- Nepali Unicode font support
- Automatic table of contents
- Page numbering and headers
- Print-optimized styling
- Chart rendering in PDF

### 🌐 Web Interface
- Responsive design
- Interactive data tables
- Real-time charts
- Search and filtering
- Mobile-friendly
- Admin interface

### 📈 Data Management
- Complete CRUD operations
- Data validation
- Import/Export tools
- Audit trails
- Version control
- Backup systems

### 🔐 Security & Performance
- JWT authentication
- Role-based access
- Input validation
- SQL injection protection
- Caching optimization
- Query optimization

## 📋 Development Timeline

### Day 1: Foundation
- ✅ Project setup and configuration
- ✅ Database models and migrations
- ✅ Django admin interface
- ✅ Basic API endpoints

### Day 2: Core Features
- ✅ Complete data models
- ✅ API development
- ✅ Authentication system
- ✅ Sample data creation

### Day 3: Web Interface
- ✅ Template system
- ✅ Dashboard interface
- ✅ Chart integration
- ✅ Data tables

### Day 4: PDF Generation
- ✅ WeasyPrint setup
- ✅ PDF templates
- ✅ Report generation
- ✅ Styling and layout

### Day 5: Production Ready
- ✅ Testing and QA
- ✅ Performance optimization
- ✅ Deployment setup
- ✅ Documentation

## 🎨 Design System

### Color Palette
```css
--primary-red: #DC143C;     /* Nepal flag red */
--primary-blue: #003893;    /* Government blue */
--primary-gold: #FFD700;    /* Ceremonial gold */
--success-green: #28a745;
--warning-orange: #fd7e14;
--gray-scale: #212529 to #f8f9fa;
```

### Typography
- **Nepali**: Mukti, Kalimati, Devanagari
- **English**: Inter, Segoe UI, Roboto
- **Monospace**: JetBrains Mono, Consolas

### Components
- Navigation system
- Data tables
- Chart containers
- Statistics cards
- Form elements
- Modal dialogs

## 🚀 Deployment

### Production Requirements
- 2+ CPU cores, 2.4GHz+
- 8GB+ RAM
- 50GB+ SSD storage
- SSL certificate
- Domain name

### Deployment Options
1. **Traditional Server** - Ubuntu/CentOS with Nginx
2. **Docker Containers** - Docker Compose setup
3. **Cloud Platforms** - AWS/DigitalOcean/Heroku
4. **Government Infrastructure** - On-premise deployment

## 📚 API Documentation

### Authentication
```http
POST /api/v1/auth/login/
POST /api/v1/auth/refresh/
POST /api/v1/auth/logout/
```

### Core Resources
```http
GET /api/v1/municipalities/
GET /api/v1/demographics/population/
GET /api/v1/economics/overview/
GET /api/v1/social/education/
POST /api/v1/reports/generate/
```

### Report Generation
```http
POST /api/v1/reports/generate/
{
  "municipality_id": "uuid",
  "format": "pdf|html",
  "chapters": ["demographics", "economics"],
  "language": "ne|en"
}
```

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create feature branch
3. Install development dependencies
4. Run tests before committing
5. Submit pull request

### Code Standards
- **Python**: PEP 8, Black formatting
- **JavaScript**: ES6+, Prettier formatting
- **CSS**: BEM methodology
- **Templates**: Django best practices

### Testing
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov

# Run specific tests
pytest apps/core/tests/
```

## 📞 Support & Contact

### Development Team
- **Project Lead**: [Contact Information]
- **Backend Developer**: [Contact Information]
- **Frontend Developer**: [Contact Information]
- **DevOps Engineer**: [Contact Information]

### Issues & Bugs
- Create GitHub issues for bugs
- Use issue templates
- Provide detailed reproduction steps
- Include system information

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Government of Nepal for report structure guidelines
- Gadhawa Municipality for requirements and feedback
- Open source community for excellent tools and libraries
- Contributors and testers for their valuable input

---

**Ready to build a beautiful, professional digital profile report system in just 5 days! 🚀**

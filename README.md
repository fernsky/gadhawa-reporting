# गधावा गाउँपालिका डिजिटल प्रोफाइल प्रतिवेदन प्रणाली
# Gadhawa Rural Municipality Digital Profile Report System

A comprehensive Django-based system for creating and managing digital profile reports for Gadhawa Rural Municipality (गधावा गाउँपालिका), Dang District, Lumbini Province, Nepal.

## 🌟 Features

### ✅ Phase 1 Complete: Foundation & Authentication
- **Django 4.2.7** with REST Framework
- **Custom User Authentication** with JWT tokens
- **Nepali Language Support** (Unicode Devanagari)
- **Security Hardening** with proper permissions and session tracking
- **Beautiful Web Interface** with Bootstrap 5 and Nepali fonts
- **API Documentation** with Swagger/OpenAPI
- **Development Environment** with virtual environment setup

### 🚧 Phase 2 Upcoming: Data Models
Based on provided SQL schemas, will implement models for:
- **Demographics** (जनसंख्या विवरण)
- **Economics** (आर्थिक अवस्था)
- **Social** (सामाजिक अवस्था)
- **Environment** (वातावरणीय स्थिति)
- **Infrastructure** (पूर्वाधार विकास)
- **Governance** (सुशासन)

### 🎯 Future Phases
- PDF Report Generation
- Advanced Analytics & Charts
- Data Import/Export
- Multi-ward data management

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Git

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd gadhawa-report
```

2. **Set up virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Environment setup**
```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your settings
```

5. **Database setup**
```bash
python manage.py migrate
python manage.py createsuperuser
```

6. **Run development server**
```bash
# Windows
start-dev.bat

# Linux/Mac
chmod +x start-dev.sh
./start-dev.sh

# Or manually
python manage.py runserver
```

## 🌐 Access Points

- **Main Application**: http://127.0.0.1:8000/
- **Admin Interface**: http://127.0.0.1:8000/admin/
- **API Documentation**: http://127.0.0.1:8000/api/docs/
- **API Schema**: http://127.0.0.1:8000/api/schema/

## 👥 User Roles

The system supports the following user roles:

- **प्रशासक (Admin)**: Full system access
- **प्रबन्धक (Manager)**: Manage data and users
- **डाटा एन्ट्री (Data Entry)**: Input and edit data
- **वडा अधिकारी (Ward Officer)**: Ward-specific data management
- **दर्शक (Viewer)**: Read-only access

## 🏗️ Project Structure

```
gadhawa-report/
├── apps/                      # Django applications
│   ├── core/                  # Core utilities and base models
│   ├── users/                 # User management and authentication
│   ├── demographics/          # Population and demographic data
│   ├── economics/             # Economic data and statistics
│   ├── social/                # Social indicators and data
│   ├── environment/           # Environmental data
│   ├── infrastructure/        # Infrastructure data
│   ├── governance/            # Governance and administrative data
│   └── reports/               # Report generation
├── docs/                      # Project documentation
├── gadhawa_report/            # Django project settings
├── templates/                 # HTML templates
├── static/                    # Static files (CSS, JS, images)
├── media/                     # User uploads
├── venv/                      # Virtual environment
└── requirements.txt           # Python dependencies
```

## 🔧 Development

### Settings
- **Development**: `gadhawa_report.settings.development`
- **Production**: `gadhawa_report.settings.production`

### Database
- **Development**: SQLite (db.sqlite3)
- **Production**: PostgreSQL (recommended)

### Key Dependencies
- Django 4.2.7
- Django REST Framework 3.14.0
- SimpleJWT for authentication
- drf-spectacular for API docs
- python-decouple for environment variables

## 🔐 Security Features

- JWT-based authentication
- Session tracking for security audits
- Account lockout after failed login attempts
- Password validation and policies
- CORS protection
- Security headers
- User permission system

## 🌏 Localization

The system is primarily designed for Nepali language with:
- Nepali Unicode (Devanagari) support
- Localized field names and interface
- English fallbacks where needed
- Date/time formatting for Nepal timezone

## 📊 Data Models (Phase 2)

Will implement comprehensive models based on Nepal's rural municipality data standards:

### Demographics
- Ward-wise population statistics
- Age and gender distributions
- Caste and ethnicity data
- Migration and settlement patterns

### Economics
- Household economic indicators
- Agricultural production
- Employment and occupation data
- Financial inclusion metrics

### Social
- Education statistics
- Health indicators
- Social services access
- Infrastructure usage

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is developed for Gadhawa Rural Municipality and follows appropriate licensing for government software projects.

## 📞 Support

For technical support or questions about the system:
- Email: tech@gadhawa.gov.np
- Phone: +977-XX-XXXXXX

---

**विकसित**: गधावा गाउँपालिकाको लागि डिजिटल प्रोफाइल प्रतिवेदन प्रणाली  
**Developed**: Digital Profile Report System for Gadhawa Rural Municipality

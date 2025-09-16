# Faculty CO-PO & Results Analysis System

A comprehensive Django-based web application for faculty to manage student results, analyze CO-PO attainment, and track academic progress.

## Features

### 🔐 Authentication & Authorization

- Faculty-only login system
- Secure session management
- Role-based access control

### 📊 Results Management

- Excel file upload and processing
- Student results analysis
- Pass/fail statistics
- Interactive charts and visualizations
- Download Excel templates

### 🎯 Academic Management

- Year, Scheme, Department, and Subject selection
- Student enrollment tracking
- Course outcome (CO) management
- Program outcome (PO) mapping
- Faculty assignment to subjects

### 📈 Analytics & Reporting

- Real-time statistics dashboard
- Pass/fail distribution charts
- Score analysis and trends
- Export capabilities

### 🎨 Modern UI/UX

- Responsive design with Tailwind CSS
- Professional academic theme
- Interactive charts with Chart.js
- Mobile-friendly interface

## Technology Stack

- **Backend**: Django 4.2.7
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Styling**: Tailwind CSS
- **Charts**: Chart.js
- **Database**: SQLite (development)
- **Data Processing**: Pandas, OpenPyXL
- **Icons**: Font Awesome

## Installation & Setup

### Prerequisites

- Python 3.8+
- pip (Python package installer)

### 1. Clone the Repository

```bash
git clone <repository-url>
cd faculty_portal
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Database Setup (Supabase only)

Create a `.env` with your Supabase pooled connection string:

```
DATABASE_URL=postgresql://<user-with-project-ref>:<password>@<pooled-host>:<port>/postgres?sslmode=require
```

Then apply migrations:

```
python manage.py migrate
```

### 5. Populate Initial Data

```bash
python manage.py populate_data
```

### 6. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 7. Run Development Server

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## Default Login Credentials

### Faculty Accounts

- **Username**: `faculty1` | **Password**: `password123`
- **Username**: `faculty2` | **Password**: `password123`
- **Username**: `faculty3` | **Password**: `password123`

### Admin Account

- **Username**: `admin` | **Password**: `admin123`

## Project Structure

```
faculty_portal/
├── faculty_portal/          # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── dashboard/               # Main application
│   ├── models.py           # Database models
│   ├── views.py            # View functions
│   ├── urls.py             # URL patterns
│   ├── forms.py            # Django forms
│   ├── admin.py            # Admin configuration
│   ├── templates/          # HTML templates
│   │   └── dashboard/
│   │       ├── base.html
│   │       ├── login.html
│   │       ├── selection.html
│   │       ├── dashboard.html
│   │       ├── home.html
│   │       ├── results.html
│   │       └── coming_soon.html
│   ├── static/             # Static files
│   │   └── dashboard/
│   │       ├── css/
│   │       │   └── style.css
│   │       ├── js/
│   │       │   └── main.js
│   │       └── images/
│   └── management/         # Custom management commands
│       └── commands/
│           └── populate_data.py
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Usage Guide

### 1. Login

- Navigate to the login page
- Use faculty credentials to access the system
- Faculty-only access is enforced

### 2. Selection Page

- Choose Year (1st-4th)
- Select Scheme (R19-20, NEP, Autonomous)
- Pick Department
- Optionally select Subject
- Save selections for the session

### 3. Dashboard

- View personalized dashboard
- See current session selections
- Quick access to all features
- Motivational quotes

### 4. Results Management

- Download Excel template
- Upload filled Excel file with student results
- View summary statistics
- Analyze pass/fail distribution
- Interactive charts and tables

### 5. Other Features

- Goal Set (Coming Soon)
- Tool Assignment (Coming Soon)
- Marks Entry (Coming Soon)
- CO Attainment (Coming Soon)
- CO-PO Mapping (Coming Soon)

## Excel Template Format

The Excel template should contain the following columns:

- **Roll Number**: Student's roll number
- **Name**: Student's full name
- **Marks**: Marks obtained (0-100)

Example:
| Roll Number | Name | Marks |
|-------------|------|-------|
| 21CS001 | John Doe | 85 |
| 21CS002 | Jane Smith | 92 |

## API Endpoints

- `POST /results/upload/` - Upload Excel file
- `GET /results/download-template/` - Download Excel template
- `GET /api/results/summary/` - Get results summary
- `GET /api/results/list/` - Get results list

## Database Models

### Faculty

- User profile with employee details
- Department and designation information

### Department

- Academic departments with codes

### Subject

- Course subjects with year, scheme, and credits

### Student

- Student information with roll numbers

### Result

- Student marks and performance data

### FacultySelection

- Faculty's current session selections

### COPO

- Course outcomes and program outcome mappings

## Customization

### Adding New Departments

1. Access Django admin panel
2. Navigate to Departments
3. Add new department with name and code

### Adding New Subjects

1. Go to Subjects in admin panel
2. Create new subject with required details
3. Assign to appropriate department and faculty

### Modifying UI Theme

- Edit `dashboard/static/dashboard/css/style.css`
- Update Tailwind classes in templates
- Customize color scheme and layout

## Development

### Running Tests

```bash
python manage.py test
```

### Creating Migrations

```bash
python manage.py makemigrations
```

### Applying Migrations

```bash
python manage.py migrate
```

### Collecting Static Files

```bash
python manage.py collectstatic
```

## Supabase (PostgreSQL)

1. Install dependencies

```
pip install -r requirements.txt
```

2. Configure environment (pooled URI preferred)

```
DATABASE_URL=postgresql://<user-with-project-ref>:<password>@<pooled-host>:<port>/postgres?sslmode=require
```

Alternative explicit variables (only if not using DATABASE_URL): `SUPABASE_HOST`, `SUPABASE_PORT`, `SUPABASE_DB`, `SUPABASE_USER`, `SUPABASE_PASSWORD`, `SUPABASE_SSLMODE`.

3. Apply migrations

```
python manage.py migrate
```

4. Run server

```
python manage.py runserver
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions:

- Create an issue in the repository
- Contact the development team
- Check the documentation

## Changelog

### Version 1.0.0

- Initial release
- Faculty authentication system
- Results management and analysis
- Excel upload/processing
- Interactive dashboard
- Responsive design

---

**Faculty Portal** - Empowering educators with modern academic management tools.

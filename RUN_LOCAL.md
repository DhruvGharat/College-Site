## Run Locally (Windows)

Prereqs:
- Python 3.13 (or 3.12)
- Git (optional)

1) Clone and enter folder
```
git clone <repo-url>
cd College-Site
```

2) Create venv and install deps
```
python -m venv myenv
myenv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

3) Apply migrations (first time only)
```
python manage.py migrate
```

5) (Optional) Create an admin user
```
python manage.py createsuperuser
```

6) Run server
```
python manage.py runserver
```

Open http://127.0.0.1:8000

Notes:
- This project uses Django's default authentication system with SQLite database.
- To create faculty accounts: either use `/admin` or run a short shell snippet to create `User` and linked `Faculty` with a valid `Department`.

### Create a user + faculty via CLI

With the server stopped and `.env` set (DATABASE_URL present), run:

1) Create a regular user with a hashed password
```
python manage.py shell -c "from django.contrib.auth.models import User; u=User.objects.create_user(username='faculty_new', password='Password123!', first_name='New', last_name='Faculty', email='new.faculty@example.com'); print('user id:', u.id)"
```

2) Ensure a department exists and create the faculty profile linked to that user
```
python manage.py shell -c "from dashboard.models import Department, Faculty; from django.contrib.auth.models import User; dept,_=Department.objects.get_or_create(code='CSE', defaults={'name':'Computer Science and Engineering'}); u=User.objects.get(username='faculty_new'); Faculty.objects.get_or_create(user=u, defaults={'employee_id':'EMP1004','department':dept,'designation':'Assistant Professor','phone':''}); print('faculty ok')"
```

3) Login in the app using:
- username: `faculty_new`
- password: `Password123!`


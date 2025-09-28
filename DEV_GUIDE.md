python manage.py shellpython manage.py shellfrom dashboard.models import Department
try:
    d = Department.objects.get(name='Computer Science and Engineering ( IOT and Cybersrcurity)')
    d.name = 'Computer Science and Engineering ( IOT and Cybersecurity)'
    d.save()
    print('Renamed successfully')
except Department.DoesNotExist:
    print('Old misspelled department not found')# Developer & Deployment Guide (Extended)

This document supplements the existing `README.md` and focuses on the customized logic you recently added: predefined subjects, restricted departments, academic year ranges, and data seeding.

## Quick Overview

| Feature                                     | Purpose                                                                                    |
| ------------------------------------------- | ------------------------------------------------------------------------------------------ |
| PredefinedSubject model                     | Stores the selectable subject names per department (instead of hardcoding in the template) |
| Restricted department list                  | Limits UI choices to the four core engineering departments                                 |
| Academic year range field (`academic_year`) | Stores session like `2024-2025` in addition to numeric `year`                              |
| Dynamic subject dropdown                    | Populates subject list only when a department with predefined subjects is selected         |
| Department seeding migration                | Ensures the four base departments always exist                                             |

## Core Departments

The system currently recognizes and filters to these four names exactly (must match your DB):

1. Information Technology
2. Electronics and telecommunication
3. Computer Engineering
4. Computer Science and Engineering ( IOT and Cybersecurity)

If any spelling differs in the database, they will not appear in the add-subject page.

## Models Added / Modified

### Subject (extended)

| Field           | Type                    | Notes                                                                              |
| --------------- | ----------------------- | ---------------------------------------------------------------------------------- |
| `academic_year` | CharField(max_length=9) | Holds range like `2005-2006`; original `year` (1–4) still required by model logic. |

### PredefinedSubject (new)

| Field        | Type             | Notes                                   |
| ------------ | ---------------- | --------------------------------------- |
| `department` | FK -> Department | Which department the subject belongs to |
| `name`       | CharField(200)   | Subject title displayed in UI           |
| `active`     | Boolean          | Toggle availability without deleting    |
| `created_at` | DateTime         | Auto timestamp                          |

Unique constraint: `(department, name)`

## Migrations Introduced

| File                            | Purpose                                                      |
| ------------------------------- | ------------------------------------------------------------ |
| `0006_subject_academic_year.py` | Adds `academic_year` to `Subject`                            |
| `0007_predefinedsubject.py`     | Creates `PredefinedSubject` and seeds IT subjects            |
| `0008_seed_core_departments.py` | Ensures the four core departments exist (creates if missing) |

Run them (after pulling latest changes):

```powershell
python manage.py migrate
```

## Adding Subjects for Other Departments

You have three ways:

### 1. Django Admin (Recommended)

1. Start server: `python manage.py runserver`
2. Visit: `http://127.0.0.1:8000/admin/`
3. Open "Predefined subjects"
4. Add entries (Department + Name + Active)
5. Save — they will load once JS enhancement for multi-department support is added (currently only IT subjects are wired in JS).

### 2. Django Shell (Bulk Insert)

```powershell
python manage.py shell
```

Inside shell:

```python
from dashboard.models import Department, PredefinedSubject

bulk = {
    'Electronics and telecommunication': [
        'Signals and Systems', 'Digital Electronics', 'Communication Theory'
    ],
    'Computer Engineering': [
        'Operating Systems', 'Database Management Systems', 'Theory of Computation'
    ],
  'Computer Science and Engineering ( IOT and Cybersecurity)': [
        'IoT Fundamentals', 'Cybersecurity Principles', 'Embedded Systems'
    ]
}

for dept_name, subjects in bulk.items():
    try:
        d = Department.objects.get(name=dept_name)
    except Department.DoesNotExist:
        print('Missing department:', dept_name)
        continue
    for s in subjects:
        PredefinedSubject.objects.get_or_create(department=d, name=s)
```

### 3. Data Migration (Repeatable)

Create a new migration with a `RunPython` operation similar to `0007_predefinedsubject.py` adding your subject lists.

## Dynamic Subject Dropdown Logic

| File                  | Purpose                                                                         |
| --------------------- | ------------------------------------------------------------------------------- |
| `views.py`            | Builds a map `{department_id: [subject names...]}` (currently only for IT)      |
| `addsubjectpage.html` | Parses JSON and repopulates `<select id="subjectName">` when department changes |

Enhancement (not yet implemented): include _all_ departments in the map:

```python
# Replace filter(department__name='Information Technology', ...)
for ps in PredefinedSubject.objects.filter(active=True).select_related('department'):
    predefined_map.setdefault(ps.department_id, []).append(ps.name)
```

Then JS will naturally support them once you change the condition.

### Current JS Condition (simplified):

```javascript
if (selectedText === "Information Technology") {
  const list = predefinedSubjects[deptId] || [];
  // populate
} else {
  subjectSelect.disabled = true;
}
```

Modify to:

```javascript
const list = predefinedSubjects[deptId] || [];
if (list.length) {
  list.forEach(...);
  subjectSelect.disabled = false;
  subjectHint.textContent = 'Select a predefined subject.';
} else {
  subjectSelect.disabled = true;
  subjectHint.textContent = 'No predefined subjects for this department yet.';
}
```

## Academic Year Handling

- UI sends a range like `2024-2025` → stored in `Subject.academic_year`.
- Legacy `year` integer still required (currently defaulted to `1` for range input unless user inputs numeric).
- If you want to deprecate the integer `year`, you would need to:
  1. Make it nullable.
  2. Update forms / views to stop validating it as an int.
  3. Adjust any code that filters on `year`.

## Common Errors & Fixes

| Error                                               | Cause                                                   | Fix                                             |
| --------------------------------------------------- | ------------------------------------------------------- | ----------------------------------------------- |
| `no such table: dashboard_predefinedsubject`        | Migration not applied                                   | Run `python manage.py migrate`                  |
| `TemplateSyntaxError: default requires 2 arguments` | Misuse of `default` filter in template                  | Removed in new template version                 |
| Subjects dropdown empty                             | No `PredefinedSubject` rows or department name mismatch | Seed subjects / verify department spelling      |
| Wrong departments showing                           | Names in DB differ from filter list                     | Adjust list or rename via admin                 |
| Academic year ignored                               | Only stored in `academic_year` field                    | Display it wherever needed (e.g., subject list) |

## Windows PowerShell Quick Commands

| Action           | Command                            |
| ---------------- | ---------------------------------- |
| Create venv      | `python -m venv myenv`             |
| Activate venv    | `myenv\Scripts\Activate.ps1`       |
| Install deps     | `pip install -r requirements.txt`  |
| Migrate          | `python manage.py migrate`         |
| Run server       | `python manage.py runserver`       |
| Create superuser | `python manage.py createsuperuser` |
| Open shell       | `python manage.py shell`           |

## Suggested Future Enhancements

1. Multi-department predefined subjects support (JS + view change)
2. Fallback manual text input when no predefined list
3. Admin bulk upload for subjects (CSV)
4. Replace integer `year` with derived value or drop it entirely
5. REST API endpoint: `/api/predefined-subjects/` returning mapping
6. Frontend caching of subject lists (reduce DOM rebuilds)

## How to Safely Modify Logic

| Goal                            | File to Edit                        | Notes                           |
| ------------------------------- | ----------------------------------- | ------------------------------- |
| Add subjects for any dept       | `admin` or shell                    | No code changes needed          |
| Expose all subjects in dropdown | `views.py` + template JS            | Include all in `predefined_map` |
| Remove year integer requirement | `models.py`, `views.py`, migrations | Plan a data migration           |
| Add analytics on subject usage  | New model or logging                | Track faculty selections        |

## Verification Checklist After Fresh Clone

1. Create & activate venv
2. `pip install -r requirements.txt`
3. `python manage.py migrate`
4. Confirm four departments exist (`python manage.py shell` → `Department.objects.all()`)
5. Confirm IT predefined subjects exist (`PredefinedSubject.objects.filter(department__name='Information Technology')`)
6. Create superuser
7. Login and test add-subject page
8. Select IT → subjects appear

## FAQ

Q: Subjects not appearing for other departments?  
A: You haven’t inserted their `PredefinedSubject` entries yet AND the current code only exposes IT; implement enhancement above.

Q: Can I let faculty type custom subject names?  
A: Yes—add a toggle: if no predefined list, show a text `<input>` instead of the disabled `<select>`.

Q: Why store both `year` and `academic_year`?  
A: Backward compatibility with previous logic using integer year choices; range adds clarity for academic session.

---

**End of Developer Guide**

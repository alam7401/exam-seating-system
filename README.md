# ExamSeat Pro — Exam Seating Arrangement System

A full-stack web application built with **Django** (backend) and **HTML/CSS/JS** (frontend) for managing exam seating arrangements in educational institutions.

---

## Features

- **Hall Management** — Create exam halls with custom rows × columns layouts
- **Student Management** — Add students with roll number, name, department, and email; live search filter
- **Exam Scheduling** — Schedule exams with date, time, and hall assignment
- **Visual Seat Grid** — Interactive grid showing all seats; click to select and assign
- **Auto-Assignment** — Randomly assign all students to seats with one click
- **Manual Assignment** — Click any seat on the grid and assign a specific student
- **Print / Export** — Print-friendly seating chart; JSON API endpoint for integration
- **Dashboard** — Overview of halls, exams, students, and total assignments

---

## Tech Stack

| Layer     | Technology                    |
|-----------|-------------------------------|
| Backend   | Python 3.10+, Django 4.2      |
| Database  | SQLite (dev) / PostgreSQL (prod) |
| Frontend  | HTML5, CSS3 (custom), Vanilla JS |
| Fonts     | Syne + Space Mono (Google Fonts) |

---

## Project Structure

```
exam_seating/
├── exam_seating/          # Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── seating/               # Main Django app
│   ├── models.py          # Hall, Exam, Student, SeatingArrangement
│   ├── views.py           # All views + API endpoint
│   ├── urls.py            # URL routing
│   └── migrations/
├── templates/
│   └── seating/
│       ├── base.html      # Base layout with sidebar nav
│       ├── dashboard.html # Stats + quick actions
│       ├── hall_list.html # Hall CRUD
│       ├── student_list.html # Student CRUD + search
│       ├── exam_list.html # Exam CRUD
│       └── seating_view.html # Interactive seat grid
├── static/
│   ├── css/
│   └── js/
├── manage.py
├── seed.py                # Sample data seeder
└── requirements.txt
```

---

## Setup & Installation

### 1. Clone / unzip the project

```bash
cd exam_seating
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate      # Linux / Mac
venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. (Optional) Seed sample data

```bash
python seed.py
```
This creates 3 sample halls, 12 students, and 3 exams.

### 6. Create a superuser (for /admin panel)

```bash
python manage.py createsuperuser
```

### 7. Run the development server

```bash
python manage.py runserver
```

Open **http://127.0.0.1:8000** in your browser.

---

## Usage Guide

### Step 1 — Add Halls
Go to **Halls** → click **+ Add Hall** → enter name, rows, and columns.

### Step 2 — Add Students
Go to **Students** → click **+ Add Student** → fill in roll number, name, department.

### Step 3 — Schedule an Exam
Go to **Exams** → click **+ Schedule Exam** → select hall, date, and time.

### Step 4 — Arrange Seats
Click **🗺 Seating** on any exam:
- **Auto-Assign** — randomly places all students into seats
- **Manual** — click a seat on the grid, then pick a student from the dropdown and click Assign
- **Print** — opens a printable seating chart
- **JSON API** — visit `/api/exams/<id>/seating/` for machine-readable output

---

## API Endpoint

```
GET /api/exams/{exam_id}/seating/
```

**Response:**
```json
{
  "exam": "Data Structures & Algorithms",
  "seating": [
    {"seat": "A1", "roll": "CS2024001", "name": "Aarav Sharma", "department": "Computer Science"},
    ...
  ]
}
```

---

## Database Models

```
Hall          → id, name, rows, columns, capacity
Exam          → id, name, date, time, hall (FK)
Student       → id, roll_number, name, email, department
SeatingArrangement → id, exam (FK), student (FK), seat_row, seat_column, seat_label
```

---

## Customization

- Change the color palette in `base.html` `:root` CSS variables
- Set `DATABASES` in `settings.py` to PostgreSQL for production
- Add `django-crispy-forms` for enhanced form rendering
- Deploy with `gunicorn` + `nginx` for production

---

## License

MIT — free for academic and commercial use.

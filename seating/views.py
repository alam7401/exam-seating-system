from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
import json, random

from .models import Hall, Exam, Student, SeatingArrangement


def dashboard(request):
    halls = Hall.objects.all()
    exams = Exam.objects.select_related('hall').order_by('-date')
    students = Student.objects.all()
    arrangements_count = SeatingArrangement.objects.count()
    context = {
        'halls': halls,
        'exams': exams,
        'students': students,
        'total_halls': halls.count(),
        'total_exams': exams.count(),
        'total_students': students.count(),
        'total_arrangements': arrangements_count,
    }
    return render(request, 'seating/dashboard.html', context)


# ── HALL VIEWS ────────────────────────────────────────────────────────────────
def hall_list(request):
    halls = Hall.objects.all()
    return render(request, 'seating/hall_list.html', {'halls': halls})


def hall_create(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        rows = int(request.POST.get('rows', 5))
        columns = int(request.POST.get('columns', 6))
        if name:
            Hall.objects.create(name=name, rows=rows, columns=columns)
            messages.success(request, f'Hall "{name}" created successfully!')
        return redirect('hall_list')
    return redirect('hall_list')


def hall_delete(request, pk):
    hall = get_object_or_404(Hall, pk=pk)
    hall.delete()
    messages.success(request, 'Hall deleted.')
    return redirect('hall_list')


# ── STUDENT VIEWS ─────────────────────────────────────────────────────────────
def student_list(request):
    students = Student.objects.all().order_by('roll_number')
    return render(request, 'seating/student_list.html', {'students': students})


def student_create(request):
    if request.method == 'POST':
        roll = request.POST.get('roll_number', '').strip()
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        dept = request.POST.get('department', '').strip()
        if roll and name:
            if Student.objects.filter(roll_number=roll).exists():
                messages.error(request, f'Roll number {roll} already exists.')
            else:
                Student.objects.create(roll_number=roll, name=name, email=email, department=dept)
                messages.success(request, f'Student "{name}" added!')
        return redirect('student_list')
    return redirect('student_list')


def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    student.delete()
    messages.success(request, 'Student deleted.')
    return redirect('student_list')


# ── EXAM VIEWS ────────────────────────────────────────────────────────────────
def exam_list(request):
    exams = Exam.objects.select_related('hall').order_by('-date')
    halls = Hall.objects.all()
    return render(request, 'seating/exam_list.html', {'exams': exams, 'halls': halls})


def exam_create(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        date = request.POST.get('date')
        time = request.POST.get('time')
        hall_id = request.POST.get('hall')
        if name and date and time and hall_id:
            hall = get_object_or_404(Hall, pk=hall_id)
            Exam.objects.create(name=name, date=date, time=time, hall=hall)
            messages.success(request, f'Exam "{name}" created!')
        return redirect('exam_list')
    return redirect('exam_list')


def exam_delete(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    exam.delete()
    messages.success(request, 'Exam deleted.')
    return redirect('exam_list')


# ── SEATING VIEWS ─────────────────────────────────────────────────────────────
def seating_view(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id)
    arrangements = SeatingArrangement.objects.filter(exam=exam).select_related('student')
    seated_map = {(a.seat_row, a.seat_column): a for a in arrangements}

    grid = []
    for r in range(1, exam.hall.rows + 1):
        row_data = []
        for c in range(1, exam.hall.columns + 1):
            label = f"{chr(64+r)}{c}"
            seat = seated_map.get((r, c))
            row_data.append({'label': label, 'row': r, 'col': c, 'arrangement': seat})
        grid.append(row_data)

    students_without_seat = Student.objects.exclude(
        arrangements__exam=exam
    )
    context = {
        'exam': exam,
        'grid': grid,
        'arrangements': arrangements,
        'students_without_seat': students_without_seat,
        'total_seats': exam.hall.capacity,
        'occupied': arrangements.count(),
    }
    return render(request, 'seating/seating_view.html', context)


@require_POST
def auto_assign(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id)
    # Clear existing arrangements
    SeatingArrangement.objects.filter(exam=exam).delete()

    students = list(Student.objects.all())
    random.shuffle(students)

    seats = []
    for r in range(1, exam.hall.rows + 1):
        for c in range(1, exam.hall.columns + 1):
            seats.append((r, c, f"{chr(64+r)}{c}"))

    created = 0
    for i, student in enumerate(students):
        if i >= len(seats):
            break
        r, c, label = seats[i]
        SeatingArrangement.objects.create(
            exam=exam, student=student,
            seat_row=r, seat_column=c, seat_label=label
        )
        created += 1

    messages.success(request, f'Auto-assigned {created} students to seats.')
    return redirect('seating_view', exam_id=exam_id)


@require_POST
def assign_seat(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id)
    student_id = request.POST.get('student_id')
    seat_row = int(request.POST.get('seat_row'))
    seat_col = int(request.POST.get('seat_col'))
    label = f"{chr(64+seat_row)}{seat_col}"

    student = get_object_or_404(Student, pk=student_id)

    # Remove existing assignment for this student in this exam
    SeatingArrangement.objects.filter(exam=exam, student=student).delete()
    # Remove any student already at this seat
    SeatingArrangement.objects.filter(exam=exam, seat_row=seat_row, seat_column=seat_col).delete()

    SeatingArrangement.objects.create(
        exam=exam, student=student,
        seat_row=seat_row, seat_column=seat_col, seat_label=label
    )
    messages.success(request, f'{student.name} assigned to seat {label}.')
    return redirect('seating_view', exam_id=exam_id)


def clear_seating(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id)
    SeatingArrangement.objects.filter(exam=exam).delete()
    messages.success(request, 'All seat assignments cleared.')
    return redirect('seating_view', exam_id=exam_id)


# ── API ───────────────────────────────────────────────────────────────────────
def api_seating(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id)
    arrangements = SeatingArrangement.objects.filter(exam=exam).select_related('student')
    data = [
        {
            'seat': a.seat_label,
            'roll': a.student.roll_number,
            'name': a.student.name,
            'department': a.student.department,
        }
        for a in arrangements
    ]
    return JsonResponse({'exam': exam.name, 'seating': data})

from django.db import models

class Hall(models.Model):
    name = models.CharField(max_length=100)
    rows = models.IntegerField(default=5)
    columns = models.IntegerField(default=6)
    capacity = models.IntegerField(editable=False, default=0)

    def save(self, *args, **kwargs):
        self.capacity = self.rows * self.columns
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Exam(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField()
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name='exams')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.date}"

class Student(models.Model):
    roll_number = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    department = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.roll_number} - {self.name}"

class SeatingArrangement(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='arrangements')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='arrangements')
    seat_row = models.IntegerField()
    seat_column = models.IntegerField()
    seat_label = models.CharField(max_length=10)

    class Meta:
        unique_together = [('exam', 'seat_row', 'seat_column'), ('exam', 'student')]

    def __str__(self):
        return f"{self.student.roll_number} -> Seat {self.seat_label} ({self.exam.name})"

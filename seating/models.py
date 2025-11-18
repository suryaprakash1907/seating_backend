from django.db import models

class UploadedFile(models.Model):
    """Store uploaded Excel files (students or timetable)."""
    file = models.FileField(upload_to='uploads/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.description or self.file.name} ({self.uploaded_at})"


class Student(models.Model):
    roll = models.CharField(max_length=128, db_index=True)
    year = models.PositiveSmallIntegerField(choices=[(1,'I'),(2,'II'),(3,'III')])
    uploaded_file = models.ForeignKey(UploadedFile, on_delete=models.SET_NULL, null=True, blank=True)
    extra = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.roll} (Year {self.year})"


class TimetableRow(models.Model):
    date = models.DateField(db_index=True)
    i_year_subject = models.CharField(max_length=255, blank=True, null=True)
    ii_year_subject = models.CharField(max_length=255, blank=True, null=True)
    iii_year_subject = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return str(self.date)


class Room(models.Model):
    code = models.CharField(max_length=64, unique=True)
    capacity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code} ({self.capacity})"


class Seating(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    exam_date = models.DateField()
    year = models.PositiveSmallIntegerField(choices=[(1,'I'),(2,'II'),(3,'III')])
    roll = models.CharField(max_length=128, blank=True)
    row_index = models.PositiveIntegerField()   # 0-indexed row in that room
    col_index = models.PositiveIntegerField()   # 0-indexed column (0..8)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['exam_date','room']),
        ]

    def __str__(self):
        return f"{self.roll} in {self.room} on {self.exam_date} r{self.row_index}c{self.col_index}"

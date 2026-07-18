from django.db import models


class Section(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, default='')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            'id': self.pk,
            'name': self.name,
            'description': self.description,
        }


class Student(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='students')
    roll = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    attendance = models.IntegerField()

    class Meta:
        ordering = ['roll']

    def __str__(self):
        return f'{self.roll} — {self.name}'

    def to_dict(self):
        return {
            'id': self.pk,
            'section': self.section.pk,
            'roll': self.roll,
            'name': self.name,
            'contact': self.contact,
            'attendance': self.attendance,
        }

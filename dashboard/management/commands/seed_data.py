"""Management command: seed the database with sample sections & students."""
from django.core.management.base import BaseCommand
from dashboard.models import Section, Student


SEED_DATA = {
    'B.Tech CSE': {
        'description': 'Branch: Computer Science & Engineering',
        'students': [
            ('26CU0310001', 'Naveen',  '9104332181', 55),
            ('26CU0310002', 'Payal',   '9600133890', 62),
            ('26CU0310003', 'Preeti',  '9386379402', 48),
            ('26CU0310004', 'Lakshya', '9654235116', 58),
            ('26CU0310005', 'Dhruv',   '9559407816', 65),
            ('26CU0310006', 'Kabir',   '9849593103', 52),
            ('26CU0310007', 'Vanshika','9413164752', 60),
            ('26CU0310008', 'Tanish',  '9534192832', 45),
            ('26CU0310009', 'Suman',   '9648350305', 92),
            ('26CU0310010', 'Pallavi', '9413953767', 88),
            ('26CU0310011', 'Devansh', '9423884969', 95),
            ('26CU0310012', 'Raghav',  '9328710122', 90),
            ('26CU0310013', 'Girish',  '9691669784', 87),
            ('26CU0310014', 'Sneha',   '9018451462', 93),
            ('26CU0310015', 'Vidya',   '9048281489', 78),
            ('26CU0310016', 'Saanvi',  '9252880957', 82),
            ('26CU0310017', 'Aditya',  '9154303911', 80),
            ('26CU0310018', 'Palak',   '9718227824', 76),
            ('26CU0310019', 'Ravi',    '9963834657', 79),
            ('26CU0310020', 'Sanjay',  '9713315098', 83),
            ('26CU0310021', 'Anika',   '9930103105', 75),
            ('26CU0310022', 'Rohan',   '9834738299', 75),
            ('26CU0310023', 'Kunal',   '9376311656', 75),
            ('26CU0310024', 'Snehal',  '9701065133', 75),
            ('26CU0310025', 'Myra',    '9872624731', 75),
            ('26CU0310026', 'Radhika', '9810801326', 75),
            ('26CU0310027', 'Vikram',  '9736026064', 75),
        ],
    },
    'B.Tech AERO': {
        'description': 'Branch: Aerospace Engineering',
        'students': [
            ('26AU0310001', 'Shreya',  '9687234309', 63),
            ('26AU0310002', 'Ritika',  '9805009788', 50),
            ('26AU0310003', 'Ananya',  '9081219136', 57),
            ('26AU0310004', 'Sarthak', '9939909169', 42),
            ('26AU0310005', 'Komal',   '9854353462', 68),
            ('26AU0310006', 'Tarun',   '9475107991', 55),
            ('26AU0310007', 'Ajay',    '9384251354', 47),
            ('26AU0310008', 'Vishal',  '9498084124', 61),
            ('26AU0310009', 'Yash',    '9182449353', 89),
            ('26AU0310010', 'Sanya',   '9874016400', 91),
            ('26AU0310011', 'Varun',   '9242786801', 96),
            ('26AU0310012', 'Mohit',   '9280598262', 88),
            ('26AU0310013', 'Sai',     '9450533158', 94),
            ('26AU0310014', 'Nandini', '9356159514', 87),
            ('26AU0310015', 'Isha',    '9232260256', 77),
            ('26AU0310016', 'Aman',    '9433036541', 81),
            ('26AU0310017', 'Nisha',   '9586850142', 84),
            ('26AU0310018', 'Anjali',  '9401965569', 76),
            ('26AU0310019', 'Manish',  '9169340608', 82),
            ('26AU0310020', 'Neha',    '9421607337', 79),
            ('26AU0310021', 'Deepak',  '9465648236', 75),
            ('26AU0310022', 'Ayush',   '9299468044', 75),
            ('26AU0310023', 'Aadhya',  '9699577738', 75),
            ('26AU0310024', 'Diya',    '9148951343', 75),
            ('26AU0310025', 'Vihaan',  '9037917693', 75),
            ('26AU0310026', 'Juhi',    '9676320163', 75),
            ('26AU0310027', 'Ishita',  '9870831727', 75),
        ],
    },
    'B.Tech IT': {
        'description': 'Branch: Information Technology',
        'students': [
            ('26IT0310001', 'Rashi',     '9579868727', 59),
            ('26IT0310002', 'Namrata',   '9434873471', 53),
            ('26IT0310003', 'Pooja',     '9455812236', 66),
            ('26IT0310004', 'Harsh',     '9316658760', 44),
            ('26IT0310005', 'Ritu',      '9690967054', 87),
            ('26IT0310006', 'Tanya',     '9668893734', 90),
            ('26IT0310007', 'Bhavna',    '9706562729', 88),
            ('26IT0310008', 'Divya',     '9990162720', 92),
            ('26IT0310009', 'Nikhil',    '9375564641', 86),
            ('26IT0310010', 'Sakshi',    '9805310033', 95),
            ('26IT0310011', 'Rudra',     '9719374529', 89),
            ('26IT0310012', 'Vaishnavi', '9124190496', 91),
            ('26IT0310013', 'Rajat',     '9314919058', 78),
            ('26IT0310014', 'Swati',     '9518506716', 83),
            ('26IT0310015', 'Bhavya',    '9262849877', 80),
            ('26IT0310016', 'Tanvi',     '9531473799', 77),
            ('26IT0310017', 'Siddharth', '9075273545', 81),
            ('26IT0310018', 'Vivaan',    '9831367837', 79),
            ('26IT0310019', 'Suraj',     '9770143634', 76),
            ('26IT0310020', 'Pranav',    '9957885685', 82),
            ('26IT0310021', 'Gaurav',    '9744431351', 75),
            ('26IT0310022', 'Urvashi',   '9233749894', 75),
            ('26IT0310023', 'Kritika',   '9352408240', 75),
            ('26IT0310024', 'Reyansh',   '9842710947', 75),
            ('26IT0310025', 'Rahul',     '9752047116', 75),
            ('26IT0310026', 'Shalini',   '9022941318', 75),
        ],
    },
}


class Command(BaseCommand):
    help = 'Seed the database with sample sections and students'

    def handle(self, *args, **options):
        self.stdout.write('Clearing existing data ...')
        Student.objects.all().delete()
        Section.objects.all().delete()

        total_students = 0
        for sec_name, sec_data in SEED_DATA.items():
            section = Section.objects.create(
                name=sec_name,
                description=sec_data['description'],
            )
            students = [
                Student(
                    section=section,
                    roll=roll,
                    name=name,
                    contact=contact,
                    attendance=att,
                )
                for roll, name, contact, att in sec_data['students']
            ]
            Student.objects.bulk_create(students)
            count = len(students)
            total_students += count
            self.stdout.write(self.style.SUCCESS(
                f'  Created section "{sec_name}" with {count} students'
            ))

        self.stdout.write(self.style.SUCCESS(
            f'\nDone — {len(SEED_DATA)} sections, {total_students} students seeded.'
        ))

from django.test import TestCase

# Create your tests here.
from door_visits.models import User

user = User.objects.filter(username='ldy').exists()
print(user)


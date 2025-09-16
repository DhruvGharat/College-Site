import os
import json
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'faculty_portal.settings')
django.setup()

from django.db import connection

print(json.dumps(connection.settings_dict, default=str))


import os

from django.db.utils import IntegrityError
from django.contrib.auth.models import User

from dotenv import load_dotenv


load_dotenv()

try:
    User.objects.create_superuser(
        os.environ.get("ADMIN_USERNAME"), password=os.environ.get("ADMIN_PASSWORD")
    )
except IntegrityError:
    pass

exit()

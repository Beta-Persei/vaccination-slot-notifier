import os

from django.db.utils import IntegrityError
from django.contrib.auth.models import User

try:
    User.objects.create_superuser(
        os.environ.get("ADMIN_USERNAME"), os.environ.get("ADMIN_PASSWORD")
    )
except IntegrityError:
    pass

exit()
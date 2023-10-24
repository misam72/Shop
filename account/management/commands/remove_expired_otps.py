from typing import Any
from django.core.management.base import BaseCommand
from account.models import OtpCode
from datetime import datetime, timedelta
import pytz


class Command(BaseCommand):
    help = 'Remove all expired codes'
    
    def handle(self, *args: Any, **options: Any):
        expired_time = datetime.now(tz=pytz.timezone("Asia/Tehran")) - timedelta(minutes=2)
        # Remove the codes that their lifetime is bigger than 2 minutes.
        OtpCode.objects.filter(created__lt=expired_time).delete()
        # We can also use styles...
        self.stdout.write('All expired otp codes removed.')
        
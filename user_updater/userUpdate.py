from main_website.models import Member
from django.utils import timezone

def update_user():
    members = Member.objects.all()
    for member in members:
        if (member.membership_type == "m" and timezone.now() > member.end_time):
            member.membership_type = "g"
            member.start_time = None
            member.end_time = None
            member.save()

from main_website.models import Member
from datetime import date

def update_user():
    members = Member.objects.all()
    for member in members:
        if (member.membership_type == "m" and date.today() > member.end_time):
            member.membership_type = "g"
            member.start_time = None
            member.end_time = None
            member.save()

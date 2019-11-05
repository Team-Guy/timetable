from django.http import HttpResponse
from schedule.models import User
import json


# Create your views here.


def _process_register(post_body):
    post=json.loads(post_body)
    # print(post)
    user = User(
        name=post["name"],
        group=post["group"],
        email=post["email"]
    )
    user.save()

def register(request):

    if request.method == "POST":
        _process_register(request.body)
    return HttpResponse("OK")
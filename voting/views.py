from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from voting.models import Administration, Votingpoll, Result
from voters.models import Voter
from candidates.models import Candidate
from datetime import datetime, date
# Create your views here.


# home page
def Home(request):
    return render(request, "index.html")


# admin login
class AdminLogin(View):

    def get(self, request):
        try:
            if request.session.get('admin') != None:
                return render(request, "administration/home.html")
            return render(request, "administration/login.html")
        except Exception as e:
            print(e)

    def post(self, request):
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            if Administration.objects.filter(username=username, password=password).exists():
                request.session['admin'] = username
                return render(request, "administration/home.html")
            else:
                data = {
                    "msg": "invalid credentials"
                }
                return render(request, "administration/login.html", data)
        except Exception as e:
            print(e)


# admin logout
def AdminLogout(request):
    try:
        if request.method == "GET":
            if request.session.get('admin') != None:
                del request.session['admin']
                return redirect("/")
            else:
                return redirect("/")
    except Exception as e:
        print(e)


# to create poll
class CreateVotingPoll(View):

    def get(self, request):
        try:
            if request.session.get('admin') != None:
                if Administration.objects.filter(username=request.session.get('admin')).exists():
                    return render(request, "administration/createVotingPoll.html")
                else:
                    return redirect("/")
            else:
                return redirect("/")
        except Exception as e:
            print(e)

    def post(self, request):
        try:
            poll_name = request.POST.get("poll_name")
            voting_date = request.POST.get("vote_date")
            start_time = request.POST.get("start_time")
            end_time = request.POST.get("end_time")
            result_date = request.POST.get("result_date")
            result_time = request.POST.get("result_time")

            if Votingpoll.objects.filter(voting_date=voting_date).exists():
                data = {
                    'msg': "poll on this day already exists"
                }
                return render(request, "administration/createVotingPoll.html", data)
            else:
                v = Votingpoll(poll_name=poll_name, voting_date=voting_date,
                               start_time=start_time, end_time=end_time, result_date=result_date, result_time=result_time)
                v.save()
                data = {
                    'msg': "poll added successfully"
                }
                return render(request, "administration/createVotingPoll.html", data)
        except Exception as e:
            print(e)


# get voting poll page
class VotePoll(View):
    def get(self, request):
        try:
            if request.session.get('admin') != None:
                if Voter.objects.filter(email=request.session.get('admin')).exists():
                    date_today = date.today()
                    if Votingpoll.objects.filter(voting_date=date_today).exists():
                        data = {
                            'poll': Votingpoll.objects.get(voting_date=date_today),
                            'candidates': Candidate.objects.all(),
                        }
                        return render(request, "votingPoll.html", data)
                    else:
                        data = {
                            'msg': 'no poll available'
                        }
                        return render(request, "votingPoll.html", data)
                else:
                    return redirect("/")
            else:
                return redirect("/")
        except Exception as e:
            print(e)

    def post(self, request):
        try:
            if request.session.get('admin') != None:
                if Voter.objects.filter(email=request.session.get('admin')).exists():
                    poll_id = request.POST.get('poll_id')
                    candidate_id = request.POST.get('candidate_id')
                    print(poll_id, candidate_id)
                    data = {
                        'msg': "Thanks for your vote",
                    }
                    return render(request, "index.html", data)
                else:
                    return redirect("/")
            else:
                return redirect("/")
        except Exception as e:
            print(e)


# result of voting polls for admin
class VotingResultList(View):
    def get(self, request):
        try:
            if request.session.get('admin') != None:
                if Administration.objects.filter(email=request.session.get('admin')).exists():
                    result_list = Result.objects.all()
                    # print(result_list)
                    # poll title,date,candidate first name lastname,total_votes
                    # result_data = {}
                    # for result in result_list:
                    # print(result.poll_id.poll_name)
                    data = {
                        'results': result_list,
                    }
                    return render(request, "administration/resultlist.html", data)
                else:
                    return redirect("/")
            else:
                return redirect("/")
        except Exception as e:
            print(e)

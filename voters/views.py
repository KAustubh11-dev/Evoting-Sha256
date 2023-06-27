from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
import random
from datetime import datetime, date
from voters.models import Voter
from candidates.models import Candidate
from voting.models import Votingpoll, Voted, Result
from django.core.mail import EmailMessage
from django.conf import settings
from voting.tasks import sendEmailTask
import base64
from PIL import Image
import io


# voter registration
class VoterRegistration(View):

    def get(self, request):
        try:
            return render(request, "voters/registration.html")
        except Exception as e:
            print(e)

    def post(self, request):
        try:
            first_name = request.POST.get('f_name')
            last_name = request.POST.get('l_name')
            profile_img = request.POST.get('profile_img')
            adhar = request.POST.get('adhar')
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            birth_date = request.POST.get('dob')
            gender = request.POST.get('gender')
            city = request.POST.get('city')
            # adhar_photo = request.FILES.get('adhar_img')

            age = self.getAge(birth_date)
            pwd = self.getPassword(first_name)
            voter_data = {'adhar': adhar, 'first_name': first_name,
                          'last_name': last_name, 'username': email, 'password': pwd, 'phone': phone, 'email': email, 'birth_date': birth_date, 'age': age, 'gender': gender, 'city': city}
            # print(first_name, last_name, adhar, phone,
            #   email, birth_date, age, pwd, gender, city, profile_photo)
            return_msg = self.validateData(voter_data)
            # print(return_msg)
            if return_msg == None:
                profile_photo = self.uploadProfile(profile_img, adhar)
                v = Voter(adhar=adhar, first_name=first_name, last_name=last_name, username=email, password=pwd, phone=phone, email=email,
                          profile_photo=profile_photo, birth_date=birth_date, age=age, gender=gender, city=city)
                v.save()

                self.sendEmail(voter_data)

                data = {
                    'msg': 'registered successfully'
                }
                return render(request, "voters/registration.html", data)
            else:
                data = {
                    'msg': return_msg
                }
                return render(request, "voters/registration.html", data)
        except Exception as e:
            print(e)

    # to upload profile image
    def uploadProfile(self, base64_profile_photo, adhar_no):
        try:
            binary_data = base64.b64decode(base64_profile_photo)
            # print(binary_data)
            profile_img = Image.open(io.BytesIO(binary_data))

            date_now = datetime.now()
            # print(date_now)
            date_now = str(date_now).replace(" ", "")
            date_now = str(date_now).replace(":", "")
            date_now = str(date_now).replace(".", "")
            date_now = str(date_now).replace("-", "")
            img_name = str(adhar_no)+"_"+str(date_now)
            # print(img_name)
            # print(type(img_name))
            # profile_img.show()
            imagePath = (
                'E:/datta/my programs/projectenv/djangoprojects/Evoting/media/images/profile/'+f"{img_name}.jpeg")
            profile_img.save(imagePath, 'jpeg')
            # send DB image save path back
            db_img_path = "media/images/profile/"+f"{img_name}.jpeg"
            return db_img_path
        except Exception as e:
            print(e)

    def getAge(self, birth_date):
        try:
            dob = datetime.fromisoformat(birth_date).date()
            today = date.today()
            age = today.year - dob.year - \
                ((today.month, today.day) < (dob.month, dob.day))
            return age
        except Exception as e:
            print(e)

    def getPassword(self, name):
        small_char = ('adfeff', 'bsdfdsfyuj', 'cyujy', 'dtjytj', 'ejty', 'fasdfghk', 'gjyuj', 'hsdcdsc', 'isdcds', 'jsdcdscs', 'kscsdcds', 'lcs',
                      'mtjytj', 'ndfvfdv', 'o', 'pdfvdsfv', 'qdfvfdvdf', 'rdsfvdsfvd', 'sdfvfdv', 'tdfvd', 'usdcfsd', 'vjtj', 'wmiunb', 'xjhgf', 'ymmnbvc', 'zoiuy')
        capital_char = ('Advd', 'lkjhgB', 'Cdfvdf', 'Drg', 'Egrg', 'Frgrtgr', 'Ghg', 'Hlkj', 'Irgbrgr', 'Jsdfsd', 'Kfdssd', 'Ldvd',
                        'Mdfvdsf', 'Nfvdf', 'Ovrf', 'Pvf', 'Qrfvrf', 'Refe', 'Sefesr', 'Terfer', 'Udgrdrt', 'Vds', 'Wsdcsdcs', 'Xdfsfsf', 'Ydsfds', 'Zsdfsd')
        special_symbol = ('!', '@', '#', '$', '%', '&', '*')

        #name = name.lower()
        # pwd = name.capitalize()+str(random.choice(special_symbol))+str(random.choice(small_char) +
        #                                                              str(random.choice(capital_char))+str(random.randint(1, 1000)))
        pwd = str(random.choice(special_symbol))+str(random.choice(small_char) +
                                                     str(random.choice(capital_char))+str(random.randint(1, 1000)))

        return pwd

    def validateData(self, data):
        try:
            # print("validate data:", data)
            msg = None
            if Voter.objects.filter(adhar=data.get('adhar')).exists():
                msg = "already registered with this adhar"
            elif Voter.objects.filter(phone=data.get('phone')).exists():
                msg = "phone already taken"
            elif Voter.objects.filter(username=data.get('username')).exists():
                msg = "email already taken"
            elif Voter.objects.filter(email=data.get('email')).exists():
                msg = "email already taken"
            else:
                msg = None
            return msg
        except Exception as e:
            print(e)

    def sendEmail(self, voter):
        try:
            # print(voter)
            sub = "Dear voter, your credentials to vote"
            msg_to = voter.get('email')
            msg = "use below credentials to login"+"\n\n"+"username: " + \
                voter.get('username') + "\n"+"password: "+voter.get('password') + \
                "\n"+"\nNote: Do not reply, this is an system generated mail."
            data = {'sub': sub, 'msg_to': msg_to, 'msg': msg}
            sendEmailTask.delay(data)
        except Exception as e:
            print(e)


# for voter login
class VoterLogin(View):

    def get(self, request):
        try:
            if request.session.get('voter') != None:
                user = request.session.get('voter')
                # print(user)
                if Voter.objects.filter(email=user).exists():
                    date_today = date.today()
                    voter_obj = Voter.objects.get(email=user)
                    if Votingpoll.objects.filter(voting_date=date_today).exists():
                        poll_today = Votingpoll.objects.get(
                            voting_date=date_today)
                        # print(poll_today)
                        current_time = datetime.now().time()
                        if current_time < poll_today.start_time or current_time > poll_today.end_time:
                            data = {
                                'user': voter_obj,
                                'msg': False,
                            }
                            return render(request, "voters/votingPollList.html", data)
                        else:
                            data = {
                                'user': voter_obj,
                                'poll': poll_today,
                            }
                            return render(request, "voters/votingPollList.html", data)
                    else:
                        data = {
                            'user': voter_obj,
                            'msg': False,
                        }
                        return render(request, "voters/votingPollList.html", data)
                else:
                    return render(request, "voters/login.html")
            return render(request, "voters/login.html")
        except Exception as e:
            print(e)

    def post(self, request):
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            # print(username, password)
            if Voter.objects.filter(username=username, password=password).exists():
                request.session['voter'] = username
                # print("ok")
                date_today = date.today()
                voter_obj = Voter.objects.get(email=username)
                if Votingpoll.objects.filter(voting_date=date_today).exists():
                    poll_today = Votingpoll.objects.get(
                        voting_date=date_today)
                    # print(poll_today)
                    current_time = datetime.now().time()
                    if current_time < poll_today.start_time or current_time > poll_today.end_time:
                        data = {
                            'user': voter_obj,
                            'msg': False,
                        }
                        return render(request, "voters/votingPollList.html", data)
                    else:
                        data = {
                            'user': voter_obj,
                            'poll': poll_today,
                        }
                        return render(request, "voters/votingPollList.html", data)
                else:
                    data = {
                        'user': voter_obj,
                        'msg': False,
                    }
                    return render(request, "voters/votingPollList.html", data)
            else:
                data = {
                    "msg": "invalid credentials"
                }
                return render(request, "voters/login.html", data)
        except Exception as e:
            print(e)


# get voting poll page for voter
class VotePoll(View):
    def get(self, request):
        try:
            if request.session.get('voter') != None:
                if Voter.objects.filter(email=request.session.get('voter')).exists():
                    date_today = date.today()
                    # voter_obj = Voter.objects.get(
                    #     email=request.session.get('voter'))
                    # already_voted = Voted.objects.filter()

                    #voter_age = None
                    #if_voted_already = None

                    if Votingpoll.objects.filter(voting_date=date_today).exists():
                        poll = Votingpoll.objects.get(voting_date=date_today)
                        candidates = Candidate.objects.all()
                        data = {
                            'poll': poll,
                            'candidates': candidates,
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
            if request.session.get('voter') != None:
                if Voter.objects.filter(email=request.session.get('voter')).exists():
                    poll_id = request.POST.get('poll_id')
                    candidate_adhar = request.POST.get('candidate_id')
                    print(poll_id, candidate_adhar)

                    # call to save result method
                    self.saveResult(request, poll_id, candidate_adhar)

                    # update in voted table in db
                    self.voter_voted(request, poll_id)

                    data = {
                        'msg': True,
                    }
                    return render(request, "resultPage.html", data)
                else:
                    return redirect("/")
            else:
                return redirect("/")
        except Exception as e:
            print(e)

    def saveResult(self, request, poll_id, candidate_adhar):
        try:
            voter = Voter.objects.filter(email=request.session.get('voter'))
            candidate_obj = Candidate.objects.get(adhar=candidate_adhar)
            poll_obj = Votingpoll.objects.get(poll_id=poll_id)
            if Result.objects.filter(poll_id=poll_id).exists():
                result_object = Result.objects.get(poll_id=poll_id)
                votes = result_object.votes+1
                Result.objects.filter(
                    candidate_adhar=candidate_obj).update(votes=votes)
            else:
                r = Result(poll_id=poll_obj,
                           candidate_adhar=candidate_obj, votes=1)
                r.save()
        except Exception as e:
            print(e)

    def voter_voted(self, request, poll_id):
        try:
            voter_obj = Voter.objects.get(
                email=request.session.get('voter'))
            poll_obj = Votingpoll.objects.get(poll_id=poll_id)
            print("ok", voter_obj, poll_obj)
            v = Voted(poll_id=poll_obj,
                      voter_adhar=voter_obj)
            v.save()
            print("ok", voter_obj, poll_obj)
        except Exception as e:
            print(e)


# voter logout
def VoterLogout(request):
    if request.method == "GET":
        if request.session.get('voter') != None:
            del request.session['voter']
            return redirect("/")
        else:
            return redirect("/")

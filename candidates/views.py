from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from candidates.models import Candidate
from datetime import datetime, date
import random
from django.core.mail import EmailMessage
from django.conf import settings
import base64
from PIL import Image
import io
# Create your views here.


# candidate registration
class CandidateRegistration(View):

    def get(self, request):
        try:
            return render(request, "candidates/registration.html")
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
            adhar_photo = request.FILES.get('adhar_img')
            symbol_photo = request.FILES.get('symbol_img')

            age = self.getAge(birth_date)
            pwd = self.getPassword(first_name)

            candidate_data = {'adhar': adhar, 'first_name': first_name,
                              'last_name': last_name, 'username': email, 'password': pwd, 'phone': phone, 'email': email, 'birth_date': birth_date, 'age': age, 'gender': gender, 'city': city, 'adhar_photo': adhar_photo, 'symbol_photo': symbol_photo}
            # print(first_name, last_name, adhar, phone,
            #   email, birth_date, age, pwd, gender, city, profile_photo,  adhar_photo, symbol_photo)
            return_msg = self.validateData(candidate_data)
            # print(return_msg)
            if return_msg == None:
                profile_photo = self.uploadProfile(profile_img, adhar)
                v = Candidate(adhar=adhar, first_name=first_name,
                              last_name=last_name, username=email, password=pwd, phone=phone, email=email, profile_photo=profile_photo, birth_date=birth_date, age=age, gender=gender, city=city, adhar_photo=adhar_photo, symbol_photo=symbol_photo)
                v.save()

                self.sendEmail(candidate_data)

                data = {
                    'msg': 'registered successfully'
                }
                return render(request, "candidates/registration.html", data)
            else:
                data = {
                    'msg': return_msg
                }
                return render(request, "candidates/registration.html", data)
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
        try:
            small_char = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                          'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z')
            capital_char = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                            'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z')
            special_symbol = ('!', '@', '#', '$', '%', '&', '*')

            name = name.lower()
            pwd = name.capitalize()+str(random.choice(special_symbol))+str(random.choice(small_char) +
                                                                           str(random.choice(capital_char))+str(random.randint(1, 1000)))
            return pwd
        except Exception as e:
            print(e)

    def validateData(self, data):
        try:
            # print("validate data:", data)
            msg = None
            if Candidate.objects.filter(adhar=data.get('adhar')).exists():
                msg = "already registered with this adhar"
            elif Candidate.objects.filter(phone=data.get('phone')).exists():
                msg = "phone already taken"
            elif Candidate.objects.filter(username=data.get('username')).exists():
                msg = "email already taken"
            elif Candidate.objects.filter(email=data.get('email')).exists():
                msg = "email already taken"
            else:
                msg = None
            return msg
        except Exception as e:
            print(e)

    def sendEmail(self, candidate):
        try:
            sub = "Dear candidate,your credentials to vote"
            msg_to = candidate.get('email')
            msg = "username: "+candidate.get('username') + "\n"+"password: "+candidate.get(
                'password') + "\n"+"This is an system generated mail, do not reply"

            email = EmailMessage(
                sub,  # subject
                msg,  # body
                settings.EMAIL_HOST_USER,  # sender
                [msg_to],  # recievers
            )
            email.fail_silently = False
            email.send()
            # return HttpResponse("<h1>Email sent</h1>")
        except Exception as e:
            print(e)


# candidate login
class CandidateLogin(View):

    def get(self, request):
        try:
            if request.session.get('candidate') != None:
                if Candidate.objects.filter(username=request.session.get('candidate')).exists():
                    return render(request, "votingPoll.html")
                else:
                    return render(request, "candidates/login.html")
            else:
                return render(request, "candidates/login.html")
        except Exception as e:
            print(e)

    def post(self, request):
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            print(username, password)
            if Candidate.objects.filter(username=username, password=password).exists():
                request.session['candidate'] = username
                return render(request, "votingPoll.html")
            else:
                data = {
                    "msg": "invalid credentials"
                }
                return render(request, "candidates/login.html", data)
        except Exception as e:
            print(e)


# candidate logout
def CandidateLogout(request):
    if request.method == "GET":
        del request.session['candidate']
        return redirect("/")

from django.db import models

# Create your models here.


class Administration(models.Model):
    adhar = models.BigIntegerField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=254, unique=True)
    password = models.CharField(max_length=50, unique=True)
    phone = models.BigIntegerField(unique=True)
    email = models.CharField(max_length=254, unique=True)

    def __int__(self):
        return self.adhar


class Votingpoll(models.Model):
    poll_id = models.AutoField(primary_key=True)
    poll_name = models.CharField(max_length=50)
    voting_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    result_date = models.DateField()
    result_time = models.TimeField()

    def __str__(self):
        return str(self.poll_id)+" "+self.poll_name


class Voted (models.Model):
    id = models.AutoField(primary_key=True)
    poll_id = models.ForeignKey(
        "voting.Votingpoll", on_delete=models.CASCADE)
    voter_adhar = models.ForeignKey(
        "voters.Voter", on_delete=models.CASCADE)

    def __int__(self):
        return self.id


class Result(models.Model):
    id = models.AutoField(primary_key=True)
    poll_id = models.ForeignKey(
        "voting.Votingpoll", on_delete=models.CASCADE)
    candidate_adhar = models.ForeignKey(
        "candidates.Candidate", on_delete=models.CASCADE)
    votes = models.BigIntegerField(default=0)

    def __int_(self):
        return self.id

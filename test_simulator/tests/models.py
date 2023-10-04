from django.db import models
from django.contrib.auth.models import User

class TestQuerySet(models.QuerySet):
    pass

class TestManager(models.Manager):
    pass


class Test(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200, null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    def getQuestionsToTest(self):
        return Question.objects.filter(test=self)[:70]
    
class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=2000)
    user_question_data = models.ManyToManyField(User, through='UserQuestionData')

    def getOptions(self):
        return Option.objects.filter(question=self)
    
    def get_user_question_data(self, user):
        return UserQuestionData.objects.filter(user__username=user, question=self)

    def get_user_question_data_now(self, user):
        return self.get_user_question_data(user)[0]

    def __str__(self):
        return self.question_text
    
class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option_text = models.CharField(max_length=1000)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.option_text

class UserQuestionData(models.Model):
    READ = 'READ'
    UNREAD = 'UNREAD'
    IMPORTANT = 'IMPORTANT'
    OK = 'OK'
    STUDY = 'STUDY'
    
    TAGS = [
        (READ, 'Lida'),
        (UNREAD, 'Não lida'),
        (IMPORTANT, 'Importante'),
        (OK, 'OK'),
        (STUDY, 'Estudar'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    annotation = models.TextField(blank=True)
    tag = models.CharField(max_length=10, choices=TAGS, default=READ, null=True)

    class Meta:
        unique_together = ('user', 'question')

    def __str__(self):
        return "Username:{}".format(self.user.username, self.question.question_text)

import datetime
from django.db import models
from django.utils import timezone

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('date ended')
    now = timezone.now()
    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_published(self):
        return now >= self.pub_date

    def can_vote(self):
        return (is_published()) and (now < self.end_date)

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'
    

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text


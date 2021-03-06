import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Question(models.Model):
    """Class to create question in KU polls."""

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField(
        'date ended', default=timezone.now() + datetime.timedelta(days=1))

    def __str__(self):
        """Return question text."""
        return self.question_text

    def was_published_recently(self):
        """Check that the poll has been published recently."""
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_published(self):
        """Check that the poll has been published."""
        now = timezone.now()
        return now >= self.pub_date

    def can_vote(self):
        """Check that the poll can vote."""
        now = timezone.now()
        return (self.is_published()) and (now < self.end_date)

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    """Class to create choices in ku poll."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        """Show the choice text."""
        return self.choice_text


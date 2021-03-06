import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question
from django.urls import reverse
from django.contrib.auth import get_user_model


class QuestionModelTests(TestCase):
    """Test case for question."""

    def test_was_published_recently_with_future_question(self):
        """was_published_recently() returns False for questions whose pub_date is in the future."""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """was_published_recently() returns False for questions whose pub_date is older than 1 day."""
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """was_published_recently() returns True for questions whose pub_date is within the last day."""
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    """Test case for redirect and response."""

    def test_no_questions(self):
        """If no questions exist, an appropriate message is displayed."""
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(
            question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(
            question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_two_past_questions(self):
        """The questions index page may display multiple questions."""
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )


class PublishedTimeTests(TestCase):
    """Test time for poll model."""

    def test_is_published(self):
        """Test that the poll has been published."""
        time = timezone.now() - datetime.timedelta(days=1)
        question = Question(pub_date=time)
        self.assertTrue(question.is_published())

    def test_can_vote(self):
        """Test that the poll can vote or not."""
        time = timezone.now() - datetime.timedelta(days=1)
        question = Question(pub_date=time)
        self.assertTrue(question.can_vote())

class AuthenticationTest(TestCase):
    """Test Authenticaton"""

    def setUp(self):
        """setup method for testing"""
        User = get_user_model()
        user = User.objects.create_user("Raikirieiei", email="thornthep.c@ku.th", password="Bloodedge")
        user.first_name = "Thornthep"
        user.last_name = "Chomchuen"
        user.save()

    # def test_logged_in(self):
    #     """Test the user login."""
    #     self.client.login(username="Raikirieiei", password="Bloodedge")
    #     url = reverse("polls:index")
    #     response = self.client.get(url)
    #     self.assertContains(response, "Thornthep")

    def test_logged_out(self):
        """Test the user logout."""
        self.client.login(username="Raikirieiei", password="Bloodedge")
        self.client.logout()
        url = reverse("polls:index")
        response = self.client.get(url)
        self.assertNotContains(response, "Thornthep")

    

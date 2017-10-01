from django.db import models
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

# Create your models here.


def user_competition_path(instance, filename):
    return "competition_{}/{}".format(instance.uuid, filename)


class Competition(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    training_file = models.FileField(
        upload_to=user_competition_path, null=False, blank=False)
    test_file = models.FileField(
        upload_to=user_competition_path, null=False, blank=False)
    test_answer_file = models.FileField(
        upload_to=user_competition_path, null=False, blank=False)

    def __str__(self):
        return str(self.title)

    def get_training_data(self):
        return reverse_lazy(
            "competition:download",
            kwargs={"filepath": str(self.training_file.name)})

    def get_test_data(self):
        return reverse_lazy(
            "competition:download",
            kwargs={"filepath": str(self.test_file.name)})

class Rank(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    score = models.FloatField()

    class Meta:
        ordering = ["-score"]

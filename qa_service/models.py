from django.db import models
from vote import models as votemodel
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
        
class Question(votemodel.VoteModel, models.Model):
    question = models.TextField(unique=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    status = models.BooleanField(default=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    tags = models.ManyToManyField(Tag)
    tags_text = models.CharField(max_length=120,null=True)
    def __str__(self):
        return self.question

    class Meta:
        ordering = ["-created", "-updated", 'question']

class Answer(votemodel.VoteModel, models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE, db_column = 'question')
    
    answer = models.TextField()
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    #status = models.BooleanField(default=True)
    def __str__(self):
        return str(self.question)

    class Meta:
        ordering = ["-updated", 'question']




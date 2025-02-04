from django.db import models

# Create your models here.
class ProblemSolution(models.Model):
    problem = models.TextField()
    solution = models.TextField()

    def __str__(self):
        return self.problem
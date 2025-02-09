from django.db import models
from collections import Counter
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class ProblemSolution(models.Model):
    problem_id = models.AutoField(primary_key=True)
    problem = models.TextField()
    solution = models.TextField()
    categories = models.ManyToManyField(Category, blank=True)

    # Method to get the most voted category for a problem
    def most_voted_category(self):
        category_counts = Counter(self.problemstatus_set.values_list('selected_category', flat=True))
        if category_counts:
            most_common_category_id = category_counts.most_common(1)[0][0]
            return Category.objects.get(name=most_common_category_id) if most_common_category_id else None
        return None
    
    def __str__(self):
        return self.problem[:50]  # Show only the first 50 characters

class ProblemStatus(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(ProblemSolution, on_delete=models.CASCADE, related_name="problemstatus_set")
    selected_category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'problem')

    def __str__(self):
        return f"{self.user.username} - {self.problem.problem[:50]}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

from django.db import models

class Review(models.Model):
    photo_url = models.URLField(max_length=500)
    name = models.CharField(max_length=100)
    date = models.DateField()
    stars = models.PositiveIntegerField(default=1)
    content = models.TextField()

    def __str__(self):
        return self.name

class Reply(models.Model):
    review = models.ForeignKey(Review, related_name='replies', on_delete=models.CASCADE)
    reply_content = models.TextField()

    def __str__(self):
        return f'Reply to {self.review.name}'


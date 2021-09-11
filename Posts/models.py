from django.db import models
from django.core.validators import FileExtensionValidator
from Profiles.models import Profile

# Posts
class Post(models.Model):
    context=models.TextField()
    image=models.ImageField(upload_to='posts',validators=[FileExtensionValidator(['jpg','png','jpeg'])],blank=True)
    liked=models.ManyToManyField(Profile,blank=True,related_name="likes")
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)
    author=models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='posts')

    def __str__(self):
        return str(self.context[:20])

    def num_likes(self):
        return self.liked.all().count()
    #using reverse relation
    def num_comment(self):
        return self.comment_post.all().count() 

    class Meta:
        ordering=('-created',)

class Comment(models.Model):
    user=models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="comment_user")
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name="comment_post")
    body=models.TextField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)

    #left value for db and right fir us
choices=(('Like','Like'),('Unlike','Unlike'),)
class Like(models.Model):
    user=models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="user_like")
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name="like_post")
    value=models.CharField(choices=choices,max_length=8)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)

    def str(self):
        return f"{self.user}-{self.post}-{self.value}"


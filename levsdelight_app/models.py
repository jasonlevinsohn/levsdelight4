from django.db import models

class Slideshow(models.Model):
    title = models.CharField(max_length=1000)
    desc = models.CharField(max_length=2000)
    pictureLocation = models.CharField(max_length=200)
    isActive = models.BooleanField()
    slideshow_id = models.IntegerField()
    order_id = models.IntegerField()
    pub_date = models.DateTimeField('date_pubished')

    def __unicode__(self):
        return "Id: \"%s\" - Title: \"%s\" for Slideshow: \"%s\" - Order: \"%s\"" % (self.slideshow_id, self.title, str(self.slideshow_id), str(self.order_id))


class MonthMap(models.Model):
    slideshow_id = models.IntegerField()
    month = models.CharField(max_length=20)
    year = models.IntegerField()

    def __unicode__(self):
        return "Id: \"%s\" - Month: \"%s\" - Year: \"%s\"" % (self.slideshow_id, self.month, self.year)

class Author(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    email = models.EmailField()

    def __unicode__(self):
        return "Id: %s - %s %s" % (self.id, self.first_name, self.last_name)

    # We need these two definitions for getting first_name & last_name
    # as foreign keys when querying BlogPost
    def natural_key(self):
        return (self.first_name, self.last_name)

    class Meta:
        unique_together = (('first_name', 'last_name'),)


class BlogPost(models.Model):
    postText = models.CharField(max_length=10000)
    title = models.CharField(max_length=2000)
    images_id = models.IntegerField()
    author_id = models.ForeignKey(Author, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return "Id: \"%s\" - Title: \"%s\"" % (self.id, self.title)


class Comment(models.Model):
    commenter_name = models.CharField(max_length=50)
    comment = models.CharField(max_length=7000)
    post = models.ForeignKey(BlogPost)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "Id: %s - %s Title: %s" % (self.id, self.commenter_name, self.post.title)

class PendingComment(models.Model):
    commenter_name = models.CharField(max_length=50)
    comment = models.CharField(max_length=7000)
    post = models.ForeignKey(BlogPost)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "PENDING - Id: %s | Name: %s | Post Id: %s | Post Title: %s" % (self.id, self.commenter_name, self.post.id, self.post.title)

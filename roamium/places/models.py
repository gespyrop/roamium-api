from django.contrib.gis.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category-detail", kwargs={"pk": self.pk})


class Place(models.Model):
    WHEELCHAIR_CHOICES = (
        ('no', 'No'),
        ('limited', 'Limited'),
        ('yes', 'Yes'),
    )

    name = models.CharField(max_length=50)
    location = models.PointField()
    time = models.DurationField()
    wheelchair = models.CharField(choices=WHEELCHAIR_CHOICES, default='no', max_length=7)
    is_bike = models.BooleanField(default=False)
    is_family = models.BooleanField(default=False)
    is_friends = models.BooleanField(default=False)
    categories = models.ManyToManyField(Category)

    objects = models.Manager()

    class Meta:
        verbose_name = "place"
        verbose_name_plural = "places"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("place-detail", kwargs={"pk": self.pk})

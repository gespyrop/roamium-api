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


WHEELCHAIR_CHOICES = (
    ('no', 'No'),
    ('limited', 'Limited'),
    ('yes', 'Yes'),
)


class Place(models.Model):
    name = models.CharField(max_length=50)
    location = models.PointField()
    time = models.DurationField()
    wheelchair = models.CharField(choices=WHEELCHAIR_CHOICES, blank=True, null=True, max_length=7)
    categories = models.ManyToManyField(Category)

    objects = models.Manager()

    class Meta:
        verbose_name = "place"
        verbose_name_plural = "places"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("place-detail", kwargs={"pk": self.pk})


class OSMPlace(models.Model):
    osm_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    wheelchair = models.CharField(choices=WHEELCHAIR_CHOICES, max_length=7, blank=True, null=True)
    categories = models.ManyToManyField(Category)

    class Meta:
        verbose_name = "OSM Place"
        verbose_name_plural = "OSM Places"

    def __str__(self):
        return f'{self.name} ({self.osm_id})' if self.name else f'({self.osm_id})'

    def get_absolute_url(self):
        return reverse("osmplace-detail", kwargs={"pk": self.pk})

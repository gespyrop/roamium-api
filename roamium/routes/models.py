from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Route(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    finished = models.BooleanField(default=False)


PLACE_SOURCES = (
    ('roamium', 'Roamium'),
    ('osm', 'Open Street Maps'),
)


class Visit(models.Model):
    place_id = models.BigIntegerField()
    place_source = models.CharField(
        choices=PLACE_SOURCES, max_length=7, blank=False, null=False
    )
    name = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.name} {self.timestamp}'


class Review(models.Model):
    visit = models.OneToOneField(Visit, on_delete=models.CASCADE)
    text = models.TextField()
    stars = models.IntegerField(
        validators=(MinValueValidator(1), MaxValueValidator(5))
    )

    def __str__(self) -> str:
        return f'{self.visit.name} {self.visit.timestamp} ({self.stars})'

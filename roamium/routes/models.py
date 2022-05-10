from django.db import models


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

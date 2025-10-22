from django.db import models

# Create your models here.
class Player(models.Model):
    player_name = models.CharField(max_length=50)
    best_role = models.CharField(max_length = 50)
    corners = models.SmallIntegerField(default = 0, null = False, blank = False)
    crossing = models.SmallIntegerField(default = 0, null = False, blank = False)
    dribbling = models.SmallIntegerField(default = 0, null = False, blank = False)
    finishing = models.SmallIntegerField(default = 0, null = False, blank = False)
    first_touch = models.SmallIntegerField(default = 0, null = False, blank = False)
    free_kicks = models.SmallIntegerField(default = 0, null = False, blank = False)
    heading = models.SmallIntegerField(default = 0, null = False, blank = False)
    long_shots = models.SmallIntegerField(default = 0, null = False, blank = False)
    long_throws = models.SmallIntegerField(default = 0, null = False, blank = False)
    marking = models.SmallIntegerField(default = 0, null = False, blank = False)
    passing = models.SmallIntegerField(default = 0, null = False, blank = False)
    penalty_taking = models.SmallIntegerField(default = 0, null = False, blank = False)
    tackling = models.SmallIntegerField(default = 0, null = False, blank = False)
    technique = models.SmallIntegerField(default = 0, null = False, blank = False)
    aggression = models.SmallIntegerField(default = 0, null = False, blank = False)
    anticipation = models.SmallIntegerField(default = 0, null = False, blank = False)
    bravery = models.SmallIntegerField(default = 0, null = False, blank = False)
    composure = models.SmallIntegerField(default = 0, null = False, blank = False)
    concetration = models.SmallIntegerField(default = 0, null = False, blank = False)
    decisions = models.SmallIntegerField(default = 0, null = False, blank = False)
    determination = models.SmallIntegerField(default = 0, null = False, blank = False)
    flair = models.SmallIntegerField(default = 0, null = False, blank = False)
    leadership = models.SmallIntegerField(default = 0, null = False, blank = False)
    off_the_ball = models.SmallIntegerField(default = 0, null = False, blank = False)
    positioning = models.SmallIntegerField(default = 0, null = False, blank = False)
    teamwork = models.SmallIntegerField(default = 0, null = False, blank = False)
    vision = models.SmallIntegerField(default = 0, null = False, blank = False)
    work_rate = models.SmallIntegerField(default = 0, null = False, blank = False)
    acceleration = models.SmallIntegerField(default = 0, null = False, blank = False)
    pace = models.SmallIntegerField(default = 0, null = False, blank = False)
    agility = models.SmallIntegerField(default = 0, null = False, blank = False)
    balance = models.SmallIntegerField(default = 0, null = False, blank = False)
    jumping_reach = models.SmallIntegerField(default = 0, null = False, blank = False)
    stamina = models.SmallIntegerField(default = 0, null = False, blank = False)
    strength = models.SmallIntegerField(default = 0, null = False, blank = False)
    natural_fitness = models.SmallIntegerField(default = 0, null = False, blank = False)
    gk_diving = models.SmallIntegerField(default = 0, null = False, blank = False)
    gk_handling = models.SmallIntegerField(default = 0, null = False, blank = False)
    gk_kicking = models.SmallIntegerField(default = 0, null = False, blank = False)
    gk_reflexes = models.SmallIntegerField(default = 0, null = False, blank = False)
    gk_positioning = models.SmallIntegerField(default = 0, null = False, blank = False)





    
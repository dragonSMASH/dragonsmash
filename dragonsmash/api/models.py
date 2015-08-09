from django.contrib.gis.db import models  # inherits from django.db.models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import transaction


PhoneRegex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                            message="Phone number must be entered in the format: '+999999999'. \
                                     Up to 15 digits allowed.")


class BaseModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.full_clean()
        super(BaseModel, self).save(*args, **kwargs)


class Player(BaseModel):
    user = models.OneToOneField(User, related_name="player")
    phone = models.CharField(max_length=15, validators=[PhoneRegex], unique=True)

    @property
    def username(self):
        return self.user.username

    @property
    def email(self):
        return self.user.email

    @property
    def auth_token(self):
        return self.user.auth_token

    def delete(self, *args, **kwargs):
        super(Player, self).delete(*args, **kwargs)
        self.user.delete(*args, **kwargs)

    class PlayerManager(models.Manager):
        @transaction.atomic()
        def create_player(self, username, password, phone, email=None):
            user = User(username=username)
            if email:
                user.email = email
            user.set_password(password)
            user.full_clean()
            user.save()

            player = self.create(user=user, phone=phone)
            return player

    objects = PlayerManager()


class PlayerData(BaseModel):
    player = models.OneToOneField(Player, related_name="data")
    location = models.PointField(geography=True)
    money = models.IntegerField()

    objects = models.GeoManager()


class Dragon(BaseModel):
    name = models.CharField(max_length=50, unique=True)
    # TODO: implement various base stats


class Effect(BaseModel):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()


class PlayerDragon(BaseModel):
    player = models.ForeignKey(Player, related_name='dragon')
    base_dragon = models.ForeignKey(Dragon)
    experience = models.IntegerField()
    last_laid = models.DateTimeField()
    effect = models.ManyToManyField(Effect)
    # TODO: implement various stats


class Egg(BaseModel):
    player = models.ForeignKey(Player, related_name='egg')
    dragon = models.ForeignKey(PlayerDragon, related_name='egg')
    location = models.PointField(geography=True)
    lays_dragon_type = models.ForeignKey(Dragon)
    # TODO: add time
    # TODO: implement various stats

    objects = models.GeoManager()

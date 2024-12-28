from uuid import uuid4

from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model
from tortoise.fields import (
    CharField,
    DatetimeField,
    FloatField,
    UUIDField,
)


class Ping(Model):
    """ping model"""
    id = UUIDField(primary_key=True, default=uuid4)
    latency = FloatField(null=True)
    status = CharField(max_length=255)
    timestamp = DatetimeField(auto_now_add=True)

    class Meta:
        table = "ping"
        ordering = ["-timestamp"]


# create ping pydantic data validator from model
PingPydantic = pydantic_model_creator(Ping)

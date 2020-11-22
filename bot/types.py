"""Aggregate file for different base-classes to enable typehints."""

from uuid import UUID

from discord import Message #type: ignore
from discord.channel import DMChannel, TextChannel #type: ignore
from sqlalchemy.ext.declarative.api import DeclarativeMeta #type: ignore

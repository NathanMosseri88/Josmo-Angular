from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .presets import Preset
from .users import User
from .proposals import Proposal

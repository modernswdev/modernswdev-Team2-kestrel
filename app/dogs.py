from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from app.auth import login_required
from app.db import get_db

bp = Blueprint('dogs', __name__, url_prefix='/dogs')

SIZES = {
    1: 'X-Small (under 10 lbs)',
    2: 'Small (10-25 lbs)',
    3: 'Medium (26-60 lbs)',
    4: 'Large (61-90 lbs)',
    5: 'X-Large (over 90 lbs)',
}
ENERGY_LEVELS = {
    1: 'Low - prefers lounging',
    2: 'Gentle - short, casual walks',
    3: 'Balanced - steady on/off switch',
    4: 'Athletic - needs daily vigorous exercise',
    5: 'Intense - non-stop stamina',
}
TEMPERAMENTS = {
    1: 'Clingy - anxious or timid',
    2: 'Cautious - slow to warm up',
    3: 'Neutral - balanced, easygoing',
    4: 'Outgoing - friendly, loves group play',
    5: 'Assertive - bold, high-intensity',
}
SEXES = ('Male', 'Female')
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


def _scale_value(raw, scale):
    return int(raw) if raw.isdigit() and int(raw) in scale else None


@bp.route('/')
@login_required
def index():
    dogs = get_db().execute(
        'SELECT * FROM dogs WHERE owner_id = ? ORDER BY created_at DESC',
        (g.user['id'],)
    ).fetchall()
    return render_template(
        'dogs/index.html', dogs=dogs, sizes=SIZES,
        energy_levels=ENERGY_LEVELS, temperaments=TEMPERAMENTS
    )


@bp.route('/new', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        age = request.form.get('age', '').strip()
        sex = request.form.get('sex', '')
        zip_code = request.form.get('zip_code', '').strip()
        size = _scale_value(request.form.get('size', ''), SIZES)
        energy_level = _scale_value(request.form.get('energy_level', ''), ENERGY_LEVELS)
        temperament = _scale_value(request.form.get('temperament', ''), TEMPERAMENTS)
        error = None

        if not name:
            error = 'Name is required.'
        elif not age.isdigit():
            error = 'Age is required.'
        elif sex not in SEXES:
            error = 'Sex is required.'
        elif not (zip_code.isdigit() and len(zip_code) == 5):
            error = 'ZIP code must be 5 digits.'
        elif size is None:
            error = 'Size is required.'
        elif energy_level is None:
            error = 'Energy level is required.'
        elif temperament is None:
            error = 'Temperament is required.'

        if error is None:
            db = get_db()
            db.execute(
                'INSERT INTO dogs (owner_id, name, age, sex, zip_code, size, energy_level, temperament)'
                ' VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                (g.user['id'], name, int(age), sex, zip_code, size, energy_level, temperament)
            )
            db.commit()
            return redirect(url_for('dogs.index'))

        flash(error)

    return render_template(
        'dogs/create.html', sexes=SEXES, sizes=SIZES,
        energy_levels=ENERGY_LEVELS, temperaments=TEMPERAMENTS
    )

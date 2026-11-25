from flask import (
    Blueprint, abort, flash, g, redirect, render_template, request, url_for
)

from app.auth import login_required
from app.compatibility import calculate_miles, lookup_coordinates, score
from app.db import get_db

bp = Blueprint('matches', __name__, url_prefix='/matches')


def _best_matches(db, user_id, owner_ids):
    """Best compatibility score for each dog owned by `owner_ids`, measured
    against every dog the logged-in user owns. Highest score first."""
    if not owner_ids:
        return []
    my_dogs = db.execute(
        'SELECT * FROM dogs WHERE owner_id = ?', (user_id,)
    ).fetchall()
    marks = ','.join('?' * len(owner_ids))
    others = db.execute(
        'SELECT d.*, u.username AS owner_name FROM dogs d'
        ' JOIN users u ON u.id = d.owner_id'
        f' WHERE d.owner_id IN ({marks})',
        tuple(owner_ids)
    ).fetchall()

    coords = {}

    def coord(zip_code):
        if zip_code not in coords:
            coords[zip_code] = lookup_coordinates(zip_code)
        return coords[zip_code]

    matches = []
    for other in others:
        best = None
        for mine in my_dogs:
            miles = calculate_miles(coord(mine['zip_code']), coord(other['zip_code']))
            value = score(mine, other, miles)
            if best is None or value > best:
                best = value
        if best is not None:
            matches.append({'dog': other, 'score': best})
    matches.sort(key=lambda m: m['score'], reverse=True)
    return matches


@bp.route('/')
@login_required
def index():
    db = get_db()
    show_blocked = request.args.get('show') == 'blocked'

    if show_blocked:
        # Only people *I* blocked; people who blocked me stay hidden.
        owners = db.execute(
            'SELECT u.id, u.username FROM blocks b'
            ' JOIN users u ON u.id = b.blocked_id'
            ' WHERE b.blocker_id = ? ORDER BY u.username',
            (g.user['id'],)
        ).fetchall()
    else:
        # Hide anyone I blocked AND anyone who blocked me, so a blocked
        # user also stops seeing me as a match.
        owners = db.execute(
            'SELECT id, username FROM users WHERE id != ?'
            ' AND id NOT IN (SELECT blocked_id FROM blocks WHERE blocker_id = ?)'
            ' AND id NOT IN (SELECT blocker_id FROM blocks WHERE blocked_id = ?)'
            ' ORDER BY username',
            (g.user['id'], g.user['id'], g.user['id'])
        ).fetchall()

    matches = _best_matches(db, g.user['id'], [o['id'] for o in owners])
    return render_template('matches/index.html', matches=matches, show_blocked=show_blocked)


@bp.route('/block/<int:user_id>', methods=('POST',))
@login_required
def block(user_id):
    db = get_db()
    if user_id == g.user['id']:
        flash('You cannot block yourself.')
        return redirect(url_for('matches.index'))
    if db.execute('SELECT 1 FROM users WHERE id = ?', (user_id,)).fetchone() is None:
        abort(404)
    db.execute(
        'INSERT OR IGNORE INTO blocks (blocker_id, blocked_id) VALUES (?, ?)',
        (g.user['id'], user_id)
    )
    db.commit()
    flash('User blocked.')
    return redirect(url_for('matches.index'))


@bp.route('/unblock/<int:user_id>', methods=('POST',))
@login_required
def unblock(user_id):
    db = get_db()
    db.execute(
        'DELETE FROM blocks WHERE blocker_id = ? AND blocked_id = ?',
        (g.user['id'], user_id)
    )
    db.commit()
    flash('User unblocked.')
    return redirect(url_for('matches.index', show='blocked'))

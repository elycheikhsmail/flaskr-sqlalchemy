from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required

from flaskr.database import db_session
from flaskr.models import User ,Post

bp = Blueprint('blog', __name__)


@bp.route('/')
def index():
    """Show all the posts, most recent first."""
    # et = session.query(DatasetRevision).order_by(desc(DatasetRevision.revision))
    posts = db_session.query(Post).all()
    #posts = db_session.query(Post).order_by(desc(Post.created)).all()
  
    return render_template('blog/index.html', posts=posts)


def get_post(id , check_author=True):
    """Get a post and its author by id.

    Checks that the id exists and optionally that the current user is
    the author.

    :param id: id of post to get
    :param check_author: require the current user to be the author
    :return: the post with author information
    :raise 404: if a post with the given id doesn't exist
    :raise 403: if the current user isn't the author
    """
    #u = User.query(User ).filter(User.posts.id == id ).first()
    post = db_session.query(Post).filter(Post.id == id).first()
    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))
    
    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    """Create a new post for the current user."""
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            # for u, a in session.query(User, Address).
             # filter(User.id==Address.user_id).\
             #filter(Address.email_address=='jack@google.com').\ all():
            u1 = g.user.id
            u = db_session.query(User).filter(User.id == u1).first()
            # p = Post( title, body, g.user['id'] )
            # Post(user_id=None , user = None ,created =None, body=None )
            # Post(title =title , body=body)
            # user = u ,
            p=Post(title =title , body=body)
            u.posts=[p]
    
            #db_session.add(p)
            db_session.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    """Update a post if the current user is the author."""
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            p = db_session.query(Post).filter(Post.id == id).all()
            p.title = title
            p.body = body
            db_session.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    """Delete a post.

    Ensures that the post exists and that the logged in user is the
    author of the post.
    """
    get_post(id)
    p = db_session.query(Post).filter(Post.id == id).all()
    db_session.delete(p)
    db_session.commit()
   
    return redirect(url_for('blog.index'))

from flask import Flask, render_template, request, redirect, url_for, jsonify,\
     flash, session as login_session
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Category, Item
from jinja2 import Environment, PackageLoader
from oauth2client import client, crypt
from functools import wraps


app = Flask(__name__)
app.secret_key = "VDQx8BEDn7clDzn8I80WH1Mp2apV69qL"
engine = create_engine('sqlite:///database.sqlite')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
google_client_id = "702305718162-pkoufeo9l51m6rj29sed66h7hbtmm5c0.apps."\
                   "googleusercontent.com"


def app_template(tmpl_name, **kwargs):
    return render_template(tmpl_name, gcid=google_client_id,
                           logged_in=login_session.get('id') is not None,
                           **kwargs)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if login_session.get('id') is None:
            return redirect(url_for('showLogin'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def index():
    """Lists the latest items in our catalog"""
    categories = session.query(Category).all()
    items = session.query(Item).order_by(Item.id.desc()).limit(10).all()
    return app_template('index.html', categories=categories, items=items)


@app.route('/login')
def showLogin():
    """Displays login button"""
    return app_template('login.html')


@app.route('/oauth2callback', methods=['POST'])
def processLogin():
    """Handles callback from Google for OAuth2"""
    try:
        idinfo = client.verify_id_token(request.form["idtoken"],
                                        google_client_id)
        if idinfo['iss'] not in ['accounts.google.com',
                                 'https://accounts.google.com']:
            raise crypt.AppIdentityError("Wrong issuer.")
    except crypt.AppIdentityError:
        return "Authentication error."
    user = session.query(User).filter_by(google_id=idinfo['sub']).first()
    if not user:
        user = User(google_id = idinfo['sub'])
        session.add(user)
        session.commit()
    login_session['id'] = user.id
    return "valid"


@app.route('/logout')
def processLogout():
    """Displays login button"""
    login_session['id'] = None
    return redirect(url_for('index'))


@app.route('/catalog/<string:category_name>/items')
def showCategory(category_name):
    """Returns a list of the items within a category"""
    category = session.query(Category).filter_by(name=category_name).one()
    categories = session.query(Category).all()
    items = session.query(Item).filter_by(category_id=category.id).all()
    return app_template('category.html', categories=categories,
                        category=category, items=items)


@app.route('/catalog/<string:category_name>/<string:item_name>')
def showItem(category_name, item_name):
    """Returns the description of an item"""
    item = session.query(Item).filter_by(name=item_name).one()
    return app_template('item.html', item=item, 
                        is_owner=item.user.id is login_session['id'])


@app.route('/new/item/')
@login_required
def newItemForm():
    """Displays form to create a new item"""
    categories = session.query(Category).all()
    return app_template('new_item.html', categories=categories)


@app.route('/new/item/submit', methods=['POST'])
@login_required
def newItem():
    """Receives POST for new item"""
    item = Item(name=request.form["name"],
                description=request.form["description"],
                category_id=request.form["category"])
    session.add(item)
    session.commit()
    flash('Item successfully added!', 'success')
    return redirect(url_for('index'))


@app.route('/edit/item/<string:item_name>')
@login_required
def editItemForm(item_name):
    """Displays form to edit item"""
    item = session.query(Item).filter_by(name=item_name).one()
    categories = session.query(Category).all()
    return app_template('edit_item.html', item=item, categories=categories)


@app.route('/edit/item/<string:item_name>/submit', methods=['POST'])
@login_required
def editItem(item_name):
    """Receives POST for edit item"""
    item = session.query(Item).filter_by(name=item_name).one()
    if item.user.id is not login_session['id']:
        flash ('You do not have permission to edit this item!', 'danger')
    else:
        item.name = request.form["name"]
        item.description = request.form["description"]
        item.category_id = request.form["category"]
        session.commit()
        flash('Item successfully edited!', 'success')
    return redirect(url_for('index'))


@app.route('/delete/item/<string:item_name>')
@login_required
def deleteItemForm(item_name):
    """Displays a confirmation to delete an item"""
    item = session.query(Item).filter_by(name=item_name).one()
    return app_template('delete_item.html', item=item)


@app.route('/delete/item/<string:item_name>/submit')
@login_required
def deleteItem(item_name):
    """Receives POST to delete item"""
    item = session.query(Item).filter_by(name=item_name).one()
    if item.user.id is not login_session['id']:
        flash ('You do not have permission to edit this item!', 'danger')
    else:
        session.delete(item)
        session.commit()
        flash('Item successfully deleted!', 'success')
    return redirect(url_for('index'))


@app.route('/catalog.json')
def json():
    """JSON dump of the catalog."""
    categories = session.query(Category).all()
    return jsonify(Categories=[category.serialize for category in categories])


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

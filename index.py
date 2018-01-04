from flask import Flask, render_template, abort, session, request, flash, redirect, url_for
from orvSecurity import generate_csrf_token
from orvData import user, categories, next_category_id
from orvTools import get_category, get_item

app = Flask(__name__) 
app.secret_key = 'KJKxXXPKSks75g4W'

@app.route('/', methods = ['GET'])
def index_route():
    return render_template('index.html', page={
        'title': 'Homepage',
        'has_sidebar': True
    }, user=user, content={
        'categories': categories
    })

@app.route('/categories', methods = ['GET'])
def categories_route():
    return render_template('categories.html', page={
        'title': 'Categories'
    }, user=user, content={
        'categories': categories
    })

@app.route('/category/add', methods = ['GET', 'POST'])
def category_add_route():
    csrf = generate_csrf_token()

    if request.method == 'POST':
        if csrf != request.form['csrf_token']:
            abort(403)
        else:
            add_category()
            flash('Category added')
            return redirect(url_for('categories_route'))

    if request.method == 'GET':
        return render_template('category_edit.html', page={
            'title': 'Add category'
        }, user=user, content={
            'is_edit': False,
            'csrf_token': csrf
        })

@app.route('/category/<int:category_id>/edit', methods = ['GET', 'POST'])
def category_edit_route(category_id):
    target_category = get_category(category_id)

    if target_category is None:
        abort(404)

    csrf = generate_csrf_token()

    if request.method == 'POST':
        if csrf != request.form['csrf_token']:
            abort(403)
        else:
            update_category(category_id)
            flash('Category updated')
            return redirect(url_for('categories_route'))
    
    if request.method == 'GET':
        return render_template('category_edit.html', page={
            'title': 'Add category'
        }, user=user, content={
            'is_edit': True,
            'csrf_token': csrf,
            'category': target_category
        })

@app.route('/category/<int:category_id>/delete', methods = ['GET', 'POST'])
def category_delete_route(category_id):
    target_category = get_category(category_id)

    if target_category is None:
        abort(404)

    csrf = generate_csrf_token()

    if request.method == 'POST':
        if csrf != request.form['csrf_token']:
            abort(403)
        else:
            delete_category(category_id)
            flash('Category deleted')
            return redirect(url_for('categories_route'))

    if request.method == 'GET':
        return render_template('confirm.html', page={
            'title': 'Delete category'
        }, user=user, content={
            'csrf_token': csrf,
            'message': 'Do you really want delete category ' + target_category['name'] + '?'
        })

@app.route('/category/<int:category_id>', methods = ['GET'])
def category_route(category_id):
    target_category = get_category(category_id)

    if target_category is None:
        abort(404)

    return render_template('category.html', page={
        'title': 'Category ' + target_category['name'],
        'has_sidebar': True
    }, user=user, content={
        'categories': categories,
        'category': target_category
    })

@app.route('/item/<int:item_id>', methods = ['GET'])
def item_route(item_id):
    target_item = get_item(item_id)

    if target_item is None:
        abort(404)

    return render_template('item.html', page={
        'title': 'Item ' + target_item['name'],
        'has_sidebar': True
    }, user=user, content={
        'categories': categories,
        'item': target_item
    })

def add_category():
    global next_category_id, categories
    name = request.form['name']
    
    categories.append({
        'id': next_category_id,
        'name': name,
        'items': []
    })
    next_category_id += 1

def update_category(category_id):
    global categories
    name = request.form['name']

    for index, category in enumerate(categories):
        if category['id'] == category_id:
            categories[index]['name'] = name

def delete_category(category_id):
    global categories

    for index, category in enumerate(categories):
        if category['id'] == category_id:
            del categories[index]

if __name__ == '__main__':
    app.debug = True #False
    app.run(host='0.0.0.0', port=5000)	
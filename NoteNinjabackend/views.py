from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .models import *  

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    data = request.form
    submitType = request.form.get("submitType")
    docID = request.form.get("docID")
    var = {"docID":docID}
    # print(data)
    if request.method == "GET":
        # print(db.session.get(User,current_user.id).documents)
        return render_template("home.html", query=db.session.get(User,current_user.id).documents)
    if request.method == "POST":
        if submitType == "create":
            new_doc = Document(name="New Document", user_id=current_user.id)
            db.session.add(new_doc)
            db.session.commit()
            print("Made Document")
            return redirect("/")
        if submitType == "title":
            doc = db.session.get(Document, docID)
            doc.name = "Changed Title"
            doc.date = func.now()
            db.session.commit()
            return redirect("/")
        if submitType == "edit":
            return redirect(url_for("views.show_editor", **var))
        if submitType == "delete":
            doc = db.session.get(Document, docID)
            db.session.delete(doc)
            db.session.commit()
            return redirect("/")
    return render_template("home.html")

@views.route('/edit', methods=['GET', 'POST'])
@login_required
def show_editor():
    docID = request.args.get("docID")
    doc = db.session.get(Document, docID)
    if request.method == "POST":
        symbol = request.form.get("greater-than-button")
        docID = request.form.get("docID")
        write = request.form.get("edit-box")
        data = request.form
        if(symbol != None):
            write+=symbol
        doc = db.session.get(Document, docID)
        doc.data = write
        db.session.commit()
        print(data)
    #if request.method == "GET":    
        
    print(doc.data)
    return render_template("edit.html", query=docID, write=doc.data, theDoc=doc)

@views.route('/test', methods=['POST'])
@login_required
def test():
    if request.method == 'POST':
        print(request.form)
        docID = request.form.get("docID")
        title = request.form.get("title")
        doc = db.session.get(Document, docID)
        if(doc != None):
            doc.name = title
            db.session.commit()
            print("title changed")
        return('', 204)
    pass

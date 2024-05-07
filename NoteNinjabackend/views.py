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
        return render_template("home.html", query=db.session.get(User,current_user.id).documents, user=db.session.get(User,current_user.id))
    if request.method == "POST":
        if submitType == "create":
            new_doc = Document(name="New Document", user_id=current_user.id)
            #new_doc.font_size = 12
            db.session.add(new_doc)
            db.session.commit()
            print("Made Document")
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
        doc.date = func.now()
        db.session.commit()
        print(data)
    #if request.method == "GET":    
        
    print(doc.data)
    return render_template("edit.html", query=docID, write=doc.data, theDoc=doc, user=db.session.get(User,current_user.id))

@views.route('/update-title', methods=['GET','POST'])
@login_required
def update_title():
    if(request.method == 'GET'):
        #Just in case someone manually tries to go to this url, send them back home
        return redirect(url_for("views.home"))
    if request.method == 'POST':
        print(request.form)
        docID = request.form.get("docID")
        title = request.form.get("title")
        doc = db.session.get(Document, docID)
        if(doc != None):
            doc.date = func.now()
            doc.name = title
            db.session.commit()
            print("title changed to " + title)
            return('', 204)

@views.route('/update-font-size', methods=['GET','POST'])
@login_required
def update_font_size():
    if(request.method == 'GET'):
        #Just in case someone manually tries to go to this url, send them back home
        return redirect(url_for("views.home"))
    if request.method == 'POST':
        print(request.form)
        docID = request.form.get("docID")
        fontSize = request.form.get("fontSize")
        doc = db.session.get(Document, docID)
        if(doc != None):
            doc.date = func.now()
            doc.font_size = int(fontSize)
            db.session.commit()
            print("font size changed to " + fontSize)
            return('', 204)

@views.route('/update-font', methods=['GET','POST'])
@login_required
def update_font():
    if(request.method == 'GET'):
        #Just in case someone manually tries to go to this url, send them back home
        return redirect(url_for("views.home"))
    if request.method == 'POST':
        print(request.form)
        docID = request.form.get("docID")
        font = request.form.get("font")
        doc = db.session.get(Document, docID)
        if(doc != None):
            doc.date = func.now()
            doc.font = font
            db.session.commit()
            print("font changed to " + font)
            return('', 204)

@views.route('/update-align', methods=['GET','POST'])
@login_required
def update_align():
    if(request.method == 'GET'):
        #Just in case someone manually tries to go to this url, send them back home
        return redirect(url_for("views.home"))
    if request.method == 'POST':
        print(request.form)
        docID = request.form.get("docID")
        align = request.form.get("align")
        doc = db.session.get(Document, docID)
        if(doc != None):
            doc.date = func.now()
            doc.align = align
            db.session.commit()
            print("alignment changed to " + align)
            return('', 204)

@views.route('/update-tag', methods=['GET','POST'])
@login_required
def update_tag():
    if(request.method == 'GET'):
        #Just in case someone manually tries to go to this url, send them back home
        return redirect(url_for("views.home"))
    if request.method == 'POST':
        print(request.form)
        docID = request.form.get("docID")
        tag = request.form.get("tag")
        doc = db.session.get(Document, docID)
        if(doc != None):
            doc.date = func.now()
            doc.tag = tag
            db.session.commit()
            print("tag changed to " + tag)
            return('', 204)
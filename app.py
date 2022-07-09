

from flask import Flask, make_response, render_template, request, url_for, redirect
import sqlite3, os
from functions import *
from sql_script import *


if not os.path.isfile("hotelms.db"):
    conn = sqlite3.connect("hotelms.db")
    c = conn.cursor()
    c.executescript(CREATE_TABLES)
    conn.commit()
    conn.close()


app = Flask(__name__)
# app.config["DEBUG"] = True

@app.route("/")
def home():
    logged_in = False
    cookie = request.cookies.get("user_session")
    if cookie != None:
        logged_in = True
    return render_template("index.html",logged_in=logged_in)

@app.route("/login/", methods=["GET","POST"])
def login():
    if request.method == "POST":
        valid, cookie, error = validUser(request.form["username"],request.form["password"])
        if not valid:
            return render_template("login.html",error=error)
        else:
            resp = make_response(redirect(url_for("home")))
            resp.set_cookie("user_session",cookie)
            return resp
    else:
        return render_template("login.html")


@app.route("/signup/",methods=["GET","POST"])
def signup():
    if request.method == "POST":
        valid, error = createUser(request.form)
        if not valid:
            return render_template("user.html",error=error)
        else:
            return redirect(url_for("login"))
    else:
        return render_template("user.html")

@app.route("/admin/login/", methods=["GET","POST"])
def admin_login():
    error = None
    if request.method == "POST":
        valid, cookie, error = validUser(request.form["username"],request.form["password"],admin=True)
        if not valid:
            return render_template("login.html",error=error,admin=True)
        else:
            resp = make_response(redirect(url_for("adminDashboard")))
            resp.set_cookie("admin_session",cookie)
            return resp

    else:
        return render_template("login.html",admin=True)

@app.route("/admin/")
@app.route("/admin/dashboard/")
def adminDashboard():
    cookie = request.cookies.get("admin_session")
    if cookie == None:
        return redirect(url_for("admin_login"))
    else:
        return render_template("admin_dashboard.html")


@app.route("/hotels/")
def hotels():
    admin = False
    cookie = request.cookies.get("admin_session")
    if cookie != None:
        admin = True
    return render_template("hotels_page.html",admin=admin,hotels=getHotels())


@app.route("/hotels/<int:hotel_id>/")
def hotel(hotel_id):
    return render_template("hotel_rooms.html",rooms=getRooms(hotel_id))


@app.route("/admin/hotels/add/",methods=["GET","POST"])
def addHotel():
    cookie = request.cookies.get("admin_session")
    if cookie == None:
        return redirect(url_for("admin_login"))
    if request.method == "POST":
        valid, error = addHotelF(request.form)
        return render_template("hotels.html",valid=valid,error=error)
    else:
        return render_template("hotels.html")


@app.route("/admin/room/add/",methods=["GET","POST"])
def addRoom():
    cookie = request.cookies.get("admin_session")
    if cookie == None:
        return redirect(url_for("admin_login"))
    if request.method == "POST":
        valid, error = addRoomF(request.form)
        return render_template("room.html",valid=valid,error=error,hotels=getHotels(),room_types=getRoomsType()) 
    else:
        return render_template("room.html",hotels=getHotels(),room_types=getRoomsType())


@app.route("/admin/room/type/add/",methods=["GET","POST"])
def addRoomType():
    cookie = request.cookies.get("admin_session")
    if cookie == None:
        return redirect(url_for("admin_login"))
    if request.method == "POST":
        valid, error = addRoomTypeF(request.form)
        return render_template("roomtype.html",valid=valid,error=error)
    else:    
        return render_template("roomtype.html")

@app.route("/logout/")
def logout():
    resp = make_response(redirect(url_for("home")))
    resp.delete_cookie("admin_session")
    resp.delete_cookie("user_session")
    return resp

@app.route("/profile/")
def profile():
    logged_in = False
    cookie = request.cookies.get("user_session")
    if cookie != None:
        logged_in = True
    return render_template("profile.html",logged_in=logged_in)

@app.route("/rooms/book/<int:room_id>",methods=["POST"])
def bookRoom(room_id):
    logged_in = False
    cookie = request.cookies.get("user_session")
    if cookie == None:
        return redirect(url_for("login"))
    else:
        valid,error = book(room_id,cookie,request.form)
        if valid:
            return redirect(url_for("bookings"))
        else:
            return "<h1>"+error+"</h1>"


@app.route("/bookings/")
def bookings():
    if request.cookies.get("user_session") == None:
        if request.cookies.get("admin_session") == None:
            return redirect(url_for("login"))
        else:
            return render_template("bookings.html",bookings=getBookings(),admin=True)
    else:
        user_id = request.cookies.get("user_session").split("|")[0]
        return render_template("bookings.html",bookings=getBookings(user_id=user_id,admin=False),admin=False)


@app.route("/admin/approve/<int:booking_id>/")
def approveBooking(booking_id):
    cookie = request.cookies.get("admin_session")
    if cookie == None:
        return redirect(url_for("admin_login"))
    else:
        valid,error = approve(booking_id)
        if valid:
            return redirect(url_for("bookings"))
        else:
            return "<h1>"+error+"</h1>"


@app.route("/admin/decline/<int:booking_id>/")
def declineBooking(booking_id):
    cookie = request.cookies.get("admin_session")
    if cookie == None:
        return redirect(url_for("admin_login"))
    else:
        valid,error = decline(booking_id)
        if valid:
            return redirect(url_for("bookings"))
        else:
            return "<h1>"+error+"</h1>"


@app.route("/payment/<int:booking_id>/")
def payBooking(booking_id):
    cookie = request.cookies.get("user_session")
    user_id = cookie.split("|")[0]
    if cookie == None:
        return redirect(url_for("login"))
    else:
        valid, error = pay(booking_id,user_id)
        if valid:
            return redirect(url_for("bookings"))
        else:
            return "<h1>"+error+"</h1>"
    

@app.route("/cancel/<int:booking_id>/")
def cancelBooking(booking_id):
    cookie = request.cookies.get("user_session")
    user_id = cookie.split("|")[0]
    if cookie == None:
        return redirect(url_for("login"))
    else:
        valid, error = cancel(booking_id,user_id)
        if valid:
            return redirect(url_for("bookings"))
        else:
            return "<h1>"+error+"</h1>"

# app.run(host= 'localhost', port=5000)   

# if __name__ == "__main__":
#         app.run(host='0.0.0.0', port=80, DEBUG=True)
import sqlite3,datetime

def sqlConnection():
    db_name = "hotelms.db"
    return sqlite3.connect(db_name)


def generateCookie(user_id,username):
    return str(user_id)+"|"+username+"|COOKIE_TEMP"

def validUser(username,password,admin=False):
    if admin:
        if username == "admin":
            if password == "admin":
                return True, generateCookie(0,username),None
            else:
                return False, None, "Incorrect Password!"
        else:
            return False, None, "Incorrect Username!"
    else:
        conn = sqlConnection()
        c = conn.cursor()
        c.execute("SELECT Customer_ID, Password FROM customer WHERE User_ID=?",(username,))
        data = c.fetchone()
        conn.close()
        if data == None:
            return False, None, "Incorrect Username!"
        elif data[1] != password:
            return False, None, "Incorrect Password!"
        else:
            return True, generateCookie(data[0],username), None
        

def createUser(formData):
    conn = sqlConnection()
    c = conn.cursor()
    c.execute("SELECT * FROM customer WHERE Phone=?;",(formData["phone"],))
    if c.fetchone() != None:
        conn.close()
        return False, "Phone Number Already Registered!"
    c.execute("SELECT * FROM customer WHERE Email=?;",(formData["email"],))
    if c.fetchone() != None:
        conn.close()
        return False, "Email Already Registered!"
    c.execute("SELECT * FROM customer WHERE User_ID=?;",(formData["username"],))
    if c.fetchone() != None:
        conn.close()
        return False, "Username Already Taken!"
    
    query = "INSERT INTO customer (Name,Age,Gender,Type,Phone,Email,Address,User_ID,Password) VALUES (?,?,?,?,?,?,?,?,?);"
    data = list(formData.values())
    c.execute(query,data)
    conn.commit()
    conn.close()
    return True, None

def addHotelF(formData):
    try:
        conn = sqlConnection()
        c = conn.cursor()
        query = "INSERT INTO hotels (Hotel_Name,Hotels_Type,Capacity,Phone,Email,City,Address,Decription) VALUES (?,?,?,?,?,?,?,?);" 
        data = list(formData.values())
        c.execute(query,data)
        conn.commit()
        conn.close()
        return "Hotel Added Succesfully...",None
    except:
        return None,"Some Error Happened While Adding Hotel!"

def addRoomTypeF(formData):
    try:
        conn = sqlConnection()
        c = conn.cursor()
        query = "INSERT INTO room_type (Room_Type,Rent_Price_Per_Day,Descrption) VALUES (?,?,?);" 
        data = list(formData.values())
        c.execute(query,data)
        conn.commit()
        conn.close()
        return "Room Type Added Succesfully...",None
    except:
        return None,"Some Error Happened While Adding Room Type!"


def addRoomF(formData):
    try:
        conn = sqlConnection()
        c = conn.cursor()
        query = "INSERT INTO rooms (Hotel_ID,Type_ID,Rooms_Size,Location) VALUES (?,?,?,?);" 
        data = list(formData.values())
        c.execute(query,data)
        conn.commit()
        conn.close()
        return "Room Added Succesfully...",None
    except:
        return None,"Some Error Happened While Adding Room!"

def getHotels():
    conn = sqlConnection()
    c = conn.cursor()
    c.execute("SELECT * FROM hotels;")
    hotels = c.fetchall()
    conn.close()
    return hotels


def getRoomsType():
    conn = sqlConnection()
    c = conn.cursor()
    c.execute("SELECT * FROM room_type;")
    room_types = c.fetchall()
    conn.close()
    return room_types

def getRooms(hotel_id):
    conn = sqlConnection()
    c = conn.cursor()
    query = "SELECT * FROM rooms LEFT JOIN room_type ON rooms.Type_ID=room_type.Type_ID WHERE hotel_ID=?;"
    c.execute(query,(hotel_id,))
    rooms = c.fetchall()
    conn.close()
    return rooms


def book(room_id,cookie,formData):
    user_id = cookie.split("|")[0]
    date_format = "%Y-%m-%d"
    a = datetime.datetime.strptime(formData["from"], date_format)
    b = datetime.datetime.strptime(formData["to"], date_format)
    delta = b - a
    if delta.days <= 0:
        return False,"Cannot book Past Dates!"
    query = "INSERT INTO booking (Customer_ID,Room_ID,Booking_DateTime,Number_of_Booking_Days,Booking_Status) VALUES (?,?,?,?,?);"
    data = (user_id,room_id,datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),delta.days,"PENDING")
    try:
        conn = sqlConnection()
        c = conn.cursor()
        c.execute(query,data)
        conn.commit()
        conn.close()
        return True,None
    except:
        return False, "Error While Booking!"

def getBookings(user_id=None,admin=True):
    query = ""
    if admin:
        query = "SELECT * FROM booking LEFT JOIN customer ON booking.Customer_ID=customer.Customer_ID;"
    elif user_id != None:
        query = "SELECT * FROM booking LEFT JOIN customer ON booking.Customer_ID=customer.Customer_ID WHERE booking.Customer_ID="+str(user_id)+";"
    conn = sqlConnection()
    c = conn.cursor()
    c.execute(query)
    return c.fetchall()

def approve(booking_id):
    try:
        conn = sqlConnection()
        c = conn.cursor()
        c.execute("UPDATE booking SET Booking_Status=? WHERE Booking_ID=?;",("APPROVED",booking_id))
        conn.commit()
        conn.close()
        return True,None
    except:
        return False, "Error While Approving Booking!"


def decline(booking_id):
    try:
        conn = sqlConnection()
        c = conn.cursor()
        c.execute("UPDATE booking SET Booking_Status=? WHERE Booking_ID=?;",("DECLINED",booking_id))
        conn.commit()
        conn.close()
        return True,None
    except:
        return False, "Error While Declining Booking!"

def pay(booking_id,user_id):
    try:
        conn = sqlConnection()
        c = conn.cursor()
        c.execute("UPDATE booking SET Booking_Status=? WHERE Booking_ID=?;",("PAID",booking_id))
        c.execute("INSERT INTO payment (Booking_ID,Payment_Date_Time,Amount,Payment_Type,Status) VALUES (?,?,?,?,?);",(booking_id,datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),9999,"ONLINE","PAID"))
        conn.commit()
        conn.close()
        return True,None
    except:
        return False, "Error While Paying For Booking!"


def cancel(booking_id,user_id):
    try:
        conn = sqlConnection()
        c = conn.cursor()
        c.execute("UPDATE booking SET Booking_Status=? WHERE Booking_ID=?;",("CANCELLED",booking_id))
        conn.commit()
        conn.close()
        return True,None
    except:
        return False, "Error While Cancelling Booking!"

CREATE_TABLES = """
    CREATE TABLE `customer` (
        `Customer_ID` INTEGER PRIMARY KEY AUTOINCREMENT,
        `Name` NVARCHAR(150) NULL,
        `Age` TINYINT(10) NULL,
        `Gender` NVARCHAR(7) NULL,
        `Type` NVARCHAR(15) NULL,
        `Phone` NVARCHAR(10) NULL,
        `Email` NVARCHAR(180) NULL,
        `Address` NVARCHAR(250) NULL,
        `User_ID` NVARCHAR(50) NULL,
        `Password` NVARCHAR(16) NULL
    );
    CREATE TABLE `booking` (
        `Booking_ID` INTEGER PRIMARY KEY AUTOINCREMENT,
        `Customer_ID` BIGINT(45) NULL,
        `Room_ID` BIGINT(45) NULL,
        `Booking_DateTime` DATETIME NULL,
        `Number_Of_Booking_Days` INT NULL,
        `Booking_Status` NVARCHAR(50) NULL
    );
    CREATE TABLE `rooms` (
        `Rooms_ID` INTEGER PRIMARY KEY AUTOINCREMENT,
        `Hotel_ID` INT NULL,
        `Type_ID` SMALLINT(5) NULL,
        `Rooms_Size` NVARCHAR(15) NULL,
        `Location` NVARCHAR(100) NULL
    );
    CREATE TABLE `payment` (
        `Payment_ID` INTEGER PRIMARY KEY AUTOINCREMENT,
        `Booking_ID` BIGINT(45) NULL,
        `Payment_Date_Time` DATETIME NULL,
        `Amount` INT NULL,
        `Payment_Type` NVARCHAR(50) NULL,
        `Status` NVARCHAR(50) NULL
    );
    CREATE TABLE `room_type` (
        `Type_ID` INTEGER PRIMARY KEY AUTOINCREMENT,
        `Room_Type` NVARCHAR(150) NULL,
        `Rent_Price_Per_Day` INT NULL,
        `Descrption` NVARCHAR(1000) NULL
    ); 
    CREATE TABLE `hotels` (
        `Hotels_ID` INTEGER PRIMARY KEY AUTOINCREMENT,
        `Hotel_Name` NVARCHAR(150) NULL,
        `Hotels_Type` NVARCHAR(50) NULL,
        `Capacity` SMALLINT(7) NULL,
        `Phone` NVARCHAR(10) NULL,
        `Email` NVARCHAR(150) NULL,
        `City` NVARCHAR(150) NULL,
        `Address` NVARCHAR(250) NULL,
        `Decription` NVARCHAR(500) NULL
    );
"""
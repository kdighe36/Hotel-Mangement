CREATE SCHEMA `hotelms` ;

CREATE TABLE `hotelms`.`customer` (
  `Customer_ID` BIGINT(50) NOT NULL AUTO_INCREMENT,
  `Name` NVARCHAR(150) NULL,
  `Age` TINYINT(10) NULL,
  `Gender` NVARCHAR(7) NULL,
  `Type` NVARCHAR(15) NULL,
  `Phone` NVARCHAR(10) NULL,
  `Email` NVARCHAR(180) NULL,
  `Address` NVARCHAR(250) NULL,
  `User_ID` NVARCHAR(50) NULL,
  `Password` NVARCHAR(16) NULL,
  PRIMARY KEY (`Customer_ID`));
  
  CREATE TABLE `hotelms`.`booking` (
  `Booking_ID` BIGINT(45) NOT NULL AUTO_INCREMENT,
  `Customer_ID` BIGINT(45) NULL,
  `Room_ID` BIGINT(45) NULL,
  `Booking_DateTime` DATETIME NULL,
  `Number_Of_Booking_Days` INT NULL,
  `Booking_Status` NVARCHAR(50) NULL,
  PRIMARY KEY (`Booking_ID`));
  
  CREATE TABLE `hotelms`.`rooms` (
  `Rooms_ID` BIGINT(45) NOT NULL AUTO_INCREMENT,
  `Hotel_ID` INT NULL,
  `Type_ID` SMALLINT(5) NULL,
  `Rooms_Size` NVARCHAR(15) NULL,
  `Location` NVARCHAR(100) NULL,
  PRIMARY KEY (`Rooms_ID`));

CREATE TABLE `hotelms`.`payment` (
  `Payment_ID` BIGINT(45) NOT NULL AUTO_INCREMENT,
  `Booking_ID` BIGINT(45) NULL,
  `Payment_Date_Time` DATETIME NULL,
  `Amount` INT NULL,
  `Payment_Type` NVARCHAR(50) NULL,
  `Status` NVARCHAR(50) NULL,
  PRIMARY KEY (`Payment_ID`));

CREATE TABLE `hotelms`.`room_type` (
  `Type_ID` smallint NOT NULL AUTO_INCREMENT,
  `Room_Type` NVARCHAR(150) NULL,
  `Rent_Price_Per_Day` INT NULL,
  `Descrption` NVARCHAR(1000) NULL,
  PRIMARY KEY (`Type_ID`)); 

CREATE TABLE `hotelms`.`hotels` (
  `Hotels_ID` INT NOT NULL AUTO_INCREMENT,
  `Hotel_Name` NVARCHAR(150) NULL,
  `Hotels_Type` NVARCHAR(50) NULL,
  `Capacity` SMALLINT(7) NULL,
  `Phone` NVARCHAR(10) NULL,
  `Email` NVARCHAR(150) NULL,
  `City` NVARCHAR(150) NULL,
  `Address` NVARCHAR(250) NULL,
  `Decription` NVARCHAR(500) NULL,
  PRIMARY KEY (`Hotels_ID`));

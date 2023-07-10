import sqlite3
import os.path
class DatabaseHelper:
    _instance = None
    databasePath = "database/event.db"

    def __new__(self, *args, **kwargs):
        if not self._instance:
            self._instance = super().__new__(self, *args, **kwargs)
        return self._instance

    def __init__(self):
        databaseExists =self.checkIfDatabaseExists()
        self.con=sqlite3.connect(self.databasePath)
        # Default the cursor is Tuple ie returns tuple on fetchAll() or fetchOne(), changing to dict so that we can get name of column also
        self.con.row_factory = sqlite3.Row
        if(not databaseExists):
            self.__initializeTable()
    
    def __initializeTable(self):
        cur = self.con.cursor()
        try:
            cur.executescript('''BEGIN TRANSACTION;
                        CREATE TABLE if not exists "TicketStatus" (
                        	"id"	INTEGER,
                        	"name"	Text Not NULL,
                        	PRIMARY KEY("id" AUTOINCREMENT)
                        );
                        CREATE TABLE if not exists "Gender" (
                        	"id"	INTEGER,
                        	"name"	Text Not NULL,
                        	PRIMARY KEY("id" AUTOINCREMENT)
                        );
                        CREATE TABLE if not exists "User" (
                        	"id"	INTEGER,
                        	"name"	TEXT NOT NULL,
                        	"username"	TEXT NOT NULL,
                            "password"	TEXT NOT NULL,
                        	"address"	TEXT,
                            "isAdmin" INTEGER DEFAULT 0,
                        	"gender"	INTEGER NOT NULL REFERENCES "Gender"("id"),
                        	PRIMARY KEY("id" AUTOINCREMENT)
                        );
                        CREATE TABLE if not exists "Event" (
                        	"id"	INTEGER,
                        	"title"	TEXT NOT NULL,
                        	"description"	TEXT,
                        	"startDate"	Text Not NULL,
                        	"endDate"	Text Not NULL,
                        	"price"	REAL Not NULL DEFAULT 0.0,
                        	"address"	TEXT NOT NULL,
                        	"createdDate"	Text Not NULL DEFAULT (datetime('now','localtime')),
                        	PRIMARY KEY("id" AUTOINCREMENT)
                        );     
                        CREATE TABLE if not exists "Category" (
                        	"id"	INTEGER,
                        	"name"	Text Not NULL,
                        	PRIMARY KEY("id" AUTOINCREMENT)
                        );
                        CREATE TABLE if not exists "EventCategoryAssociation" (
                        	"id"	INTEGER,
                        	"categoryId"	INTEGER Not NULL,
                        	"eventId"	INTEGER Not NULL,
                        	FOREIGN KEY("EventId") REFERENCES "Event"("id"),
                        	FOREIGN KEY("CategoryId") REFERENCES "Category"("id"),
                        	PRIMARY KEY("id" AUTOINCREMENT)
                        );
                        CREATE TABLE if not exists "TicketPayment" (
                        	"id"	INTEGER,
                        	"ticketStatusId"	INTEGER NOT NULL,
                        	"eventId"	INTEGER NOT NULL,
                        	"userId"	INTEGER NOT NULL,
                        	"createdDate"	Text DEFAULT (datetime('now','localtime')),
                        	FOREIGN KEY("EventId") REFERENCES "Event"("id"),
                        	FOREIGN KEY("UserId") REFERENCES "User"("id"),
                        	FOREIGN KEY("TicketStatusId") REFERENCES "TicketStatus"("id"),
                        	PRIMARY KEY("id" AUTOINCREMENT)
                        );
                        INSERT INTO Category (id,name) VALUES (1,"Music"),(2,"Movies"),(3,"Football"),(4,"Drama");
                        INSERT INTO TicketStatus (id,name) VALUES (1,"Pending"),(2,"Approved"),(3,"Rejected");
                        INSERT INTO Gender (id,name) VALUES (1,"Male"),(2,"Female"),(3,"Other");
                        INSERT INTO User(name,username,password,address,isAdmin,gender) VALUES ("admin","admin","admin","",1,1);
                        COMMIT;
                        ''')   
        except:
            print("Error Initializing database")
            raise
        
    def checkIfDatabaseExists(self):
        return os.path.isfile(self.databasePath)
            
    def __del__(self):
        self.con.close()
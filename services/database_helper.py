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
                        	"name"	INTEGER,
                        	PRIMARY KEY("id" AUTOINCREMENT)
                        );
                        CREATE TABLE if not exists "Gender" (
                        	"id"	INTEGER,
                        	"name"	INTEGER,
                        	PRIMARY KEY("id" AUTOINCREMENT)
                        );
                        CREATE TABLE if not exists "User" (
                        	"id"	INTEGER,
                        	"name"	TEXT NOT NULL,
                        	"username"	TEXT NOT NULL,
                            "password"	TEXT NOT NULL,
                        	"address"	TEXT,
                        	"age"	INTEGER,
                        	"gender"	INTEGER NOT NULL REFERENCES "Gender"("id"),
                        	PRIMARY KEY("id" AUTOINCREMENT)
                        );
                        CREATE TABLE if not exists "Event" (
                        	"id"	INTEGER,
                        	"title"	TEXT NOT NULL,
                        	"description"	TEXT,
                        	"startDate"	Text,
                        	"endDate"	Text,
                        	"price"	REAL DEFAULT 0.0,
                        	"address"	TEXT NOT NULL,
                        	"createdDate"	INTEGER DEFAULT CURRENT_TIMESTAMP,
                        	PRIMARY KEY("id" AUTOINCREMENT)
                        );
                        CREATE TABLE if not exists "EventCategoryAssociation" (
                        	"id"	INTEGER,
                        	"categoryId"	INTEGER,
                        	"eventId"	INTEGER,
                        	FOREIGN KEY("EventId") REFERENCES "Event"("id"),
                        	FOREIGN KEY("CategoryId") REFERENCES "Category"("id"),
                        	PRIMARY KEY("id" AUTOINCREMENT)
                        );
                        CREATE TABLE if not exists "TicketPayment" (
                        	"id"	INTEGER,
                        	"ticketStatusId"	INTEGER NOT NULL,
                        	"eventId"	INTEGER NOT NULL,
                        	"userId"	INTEGER NOT NULL,
                        	"createdDate"	INTEGER DEFAULT CURRENT_TIMESTAMP,
                        	FOREIGN KEY("EventId") REFERENCES "Event"("id"),
                        	FOREIGN KEY("UserId") REFERENCES "User"("id"),
                        	FOREIGN KEY("TicketStatusId") REFERENCES "TicketStatus"("id"),
                        	PRIMARY KEY("id" AUTOINCREMENT)
                        );
                        INSERT INTO TicketStatus (id,Name) VALUES (1,"Pending"),(2,"Approved"),(3,"Rejected");
                        INSERT INTO Gender (id,Name) VALUES (1,"Male"),(2,"Female"),(3,"Other");
                        COMMIT;
                        ''')   
        except:
            print("Error Initializing database")
            raise
        
    def checkIfDatabaseExists(self):
        return os.path.isfile(self.databasePath)
            
    def __del__(self):
        self.con.close()
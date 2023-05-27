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
                        	"Id"	INTEGER,
                        	"Name"	INTEGER,
                        	PRIMARY KEY("Id" AUTOINCREMENT)
                        );
                        CREATE TABLE if not exists "Gender" (
                        	"Id"	INTEGER,
                        	"Name"	INTEGER,
                        	PRIMARY KEY("Id" AUTOINCREMENT)
                        );
                        CREATE TABLE if not exists "User" (
                        	"Id"	INTEGER,
                        	"Name"	TEXT NOT NULL,
                        	"Username"	TEXT NOT NULL,
                            "Password"	TEXT NOT NULL,
                        	"Address"	TEXT,
                        	"Age"	INTEGER,
                        	"Gender"	INTEGER NOT NULL REFERENCES "Gender"("Id"),
                        	PRIMARY KEY("Id" AUTOINCREMENT)
                        );
                        CREATE TABLE if not exists "Event" (
                        	"Id"	INTEGER,
                        	"Title"	TEXT NOT NULL,
                        	"Description"	TEXT,
                        	"StartDate"	INTEGER,
                        	"EndDate"	INTEGER,
                        	"Price"	REAL DEFAULT 0.0,
                        	"Address"	TEXT NOT NULL,
                        	"CreatedDate"	INTEGER DEFAULT CURRENT_TIMESTAMP,
                        	PRIMARY KEY("Id" AUTOINCREMENT)
                        );
                        CREATE TABLE if not exists "EventCategoryAssociation" (
                        	"Id"	INTEGER,
                        	"CategoryId"	INTEGER,
                        	"EventId"	INTEGER,
                        	FOREIGN KEY("EventId") REFERENCES "Event"("Id"),
                        	FOREIGN KEY("CategoryId") REFERENCES "Category"("Id"),
                        	PRIMARY KEY("Id" AUTOINCREMENT)
                        );
                        CREATE TABLE if not exists "TicketPayment" (
                        	"Id"	INTEGER,
                        	"TicketStatusId"	INTEGER NOT NULL,
                        	"EventId"	INTEGER NOT NULL,
                        	"UserId"	INTEGER NOT NULL,
                        	"CreatedDate"	INTEGER DEFAULT CURRENT_TIMESTAMP,
                        	FOREIGN KEY("EventId") REFERENCES "Event"("Id"),
                        	FOREIGN KEY("UserId") REFERENCES "User"("Id"),
                        	FOREIGN KEY("TicketStatusId") REFERENCES "TicketStatus"("Id"),
                        	PRIMARY KEY("Id" AUTOINCREMENT)
                        );
                        INSERT INTO TicketStatus (Id,Name) VALUES (1,"Pending"),(2,"Approved"),(3,"Rejected");
                        INSERT INTO Gender (Id,Name) VALUES (1,"Male"),(2,"Female"),(3,"Other");
                        COMMIT;
                        ''')   
        except:
            print("Error Initializing database")
            raise
        
    def checkIfDatabaseExists(self):
        return os.path.isfile(self.databasePath)
            
    def __del__(self):
        self.con.close()
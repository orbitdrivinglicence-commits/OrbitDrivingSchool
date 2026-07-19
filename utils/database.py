"""
=========================================================
ORBIT DRIVING SCHOOL MANAGEMENT SYSTEM
Developer : AMAL THIRUTHOOR
Version   : 1.0.0

Database  : SQLite
Framework : Flet
Mode      : Offline
=========================================================
"""

import sqlite3
import os
from datetime import datetime

# -------------------------------------------------------
# Database Location
# -------------------------------------------------------

import os
import sqlite3


def get_database_location():

	app_folder = os.path.join(
		os.path.expanduser("~"),
		".orbit_driving_school"
	)

	os.makedirs(
		app_folder,
		exist_ok=True
	)

	return os.path.join(
		app_folder,
		"database.db"
	)


DATABASE_FILE = get_database_location()


class OrbitDatabase:

	def __init__(self):

		self.connection = sqlite3.connect(
			DATABASE_FILE
		)

		self.connection.execute(
			"PRAGMA foreign_keys = ON"
		)

		self.cursor = self.connection.cursor()


    # ---------------------------------------------------
    # Create All Tables
    # ---------------------------------------------------

    def create_tables(self):

        self.create_students_table()

        # Remaining tables will be added
        # in Part-2

        self.connection.commit()

    # ---------------------------------------------------
    # STUDENTS TABLE
    # ---------------------------------------------------

    def create_students_table(self):

        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS students(

            registration_id TEXT PRIMARY KEY,

            registration_date TEXT NOT NULL,

            name TEXT NOT NULL,

            phone TEXT NOT NULL,

            address TEXT,

            course_type TEXT,

            registration_fee REAL DEFAULT 0,

            registration_payment_method TEXT,

            total_fee REAL DEFAULT 0,

            status TEXT DEFAULT 'ACTIVE',

            created_at TEXT,

            updated_at TEXT

        )

        """)

        # Fast Search

        self.cursor.execute("""

        CREATE INDEX IF NOT EXISTS idx_student_name

        ON students(name)

        """)

    # ---------------------------------------------------
    # Close Database
    # ---------------------------------------------------

    def close(self):

        self.connection.commit()

        self.connection.close()

    # ---------------------------------------------------
    # STUDENT PAYMENTS TABLE
    # ---------------------------------------------------

    def create_student_payments_table(self):

        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS student_payments(

            payment_id INTEGER PRIMARY KEY AUTOINCREMENT,

            registration_id TEXT NOT NULL,

            payment_date TEXT NOT NULL,

            payment_type TEXT NOT NULL,

            amount REAL NOT NULL,

            payment_method TEXT NOT NULL,

            remarks TEXT,

            created_at TEXT,

            FOREIGN KEY(registration_id)
                REFERENCES students(registration_id)
                ON DELETE CASCADE

        )

        """)

        self.cursor.execute("""

        CREATE INDEX IF NOT EXISTS idx_payment_registration

        ON student_payments(registration_id)

        """)

    # ---------------------------------------------------
    # INCOMES TABLE
    # ---------------------------------------------------

    def create_incomes_table(self):

        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS incomes(

            income_id INTEGER PRIMARY KEY AUTOINCREMENT,

            income_date TEXT NOT NULL,

            amount REAL NOT NULL,

            remarks TEXT,

            created_at TEXT

        )

        """)

    # ---------------------------------------------------
    # EXPENSES TABLE
    # ---------------------------------------------------

    def create_expenses_table(self):

        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS expenses(

            expense_id INTEGER PRIMARY KEY AUTOINCREMENT,

            expense_date TEXT NOT NULL,

            amount REAL NOT NULL,

            remarks TEXT,

            created_at TEXT

        )

        """)

    # ---------------------------------------------------
    # APP SETTINGS TABLE
    # ---------------------------------------------------

    def create_settings_table(self):

        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS app_settings(

            setting_key TEXT PRIMARY KEY,

            setting_value TEXT

        )

        """)

    # ---------------------------------------------------
    # AUDIT LOG TABLE
    # ---------------------------------------------------

    def create_audit_log_table(self):

        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS audit_log(

            log_id INTEGER PRIMARY KEY AUTOINCREMENT,

            log_date TEXT,

            module TEXT,

            action TEXT,

            description TEXT

        )

        """)

    # ---------------------------------------------------
    # UPDATE create_tables()
    # ---------------------------------------------------

    def create_tables(self):

        self.create_students_table()

        self.create_student_payments_table()

        self.create_incomes_table()

        self.create_expenses_table()

        self.create_settings_table()

        self.create_audit_log_table()

        self.connection.commit()

    # ---------------------------------------------------
    # DEFAULT APPLICATION SETTINGS
    # ---------------------------------------------------

    def initialize_settings(self):

        defaults = {

            "company_name": "ORBIT DRIVING SCHOOL",

            "application_name": "Driving School Management System",

            "version": "1.0.0",

            "registration_counter": "1000"

        }

        for key, value in defaults.items():

            self.cursor.execute("""

            INSERT OR IGNORE INTO app_settings
            (setting_key, setting_value)

            VALUES (?, ?)

            """, (key, value))

        self.connection.commit()


# -------------------------------------------------------
# CREATE DATABASE
# -------------------------------------------------------

def create_database():

    db = OrbitDatabase()

    db.create_tables()

    db.initialize_settings()

    db.close()

    print("=" * 45)
    print(" ORBIT DRIVING SCHOOL")
    print(" Database Created Successfully")
    print("=" * 45)


# -------------------------------------------------------
# MAIN
# -------------------------------------------------------

if __name__ == "__main__":

    create_database()



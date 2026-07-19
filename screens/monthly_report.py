"""
=========================================================
ORBIT DRIVING SCHOOL MANAGEMENT SYSTEM

Monthly Report

Framework : Flet
Database  : SQLite
Mode      : Offline

Developer : AMAL THIRUTHOOR
=========================================================
"""


import sqlite3
import flet as ft

from datetime import datetime

from utils.pdf_report import PDFReport


DB_PATH = "database/database.db"



class MonthlyReport:


    def __init__(self, page):

        self.page = page

        self.pdf = PDFReport()



    # -------------------------
    # Database Helper
    # -------------------------


    def get_value(self, query):

        try:

            conn = sqlite3.connect(DB_PATH)

            cur = conn.cursor()

            cur.execute(query)

            result = cur.fetchone()[0]

            conn.close()

            return result


        except Exception:

            return 0



    # -------------------------
    # Current Month
    # -------------------------


    def month_value(self):

        return datetime.now().strftime(
            "%Y-%m"
        )



    # -------------------------
    # Monthly Income
    # -------------------------


    def monthly_registration_fee(self):

        return self.get_value(

            """
            SELECT IFNULL(SUM(registration_fee),0)

            FROM students

            WHERE strftime('%Y-%m', registration_date)
            =
            strftime('%Y-%m','now')

            """

        )



    def monthly_student_payment(self):

        return self.get_value(

            """
            SELECT IFNULL(SUM(amount),0)

            FROM student_payments

            WHERE strftime('%Y-%m', payment_date)
            =
            strftime('%Y-%m','now')

            """

        )



    def monthly_other_income(self):

        return self.get_value(

            """
            SELECT IFNULL(SUM(amount),0)

            FROM incomes

            WHERE strftime('%Y-%m', income_date)
            =
            strftime('%Y-%m','now')

            """

        )

    # -------------------------
    # Monthly Total Income
    # -------------------------


    def total_income(self):

        return (

            self.monthly_registration_fee()

            +

            self.monthly_student_payment()

            +

            self.monthly_other_income()

        )



    # -------------------------
    # Monthly Expense
    # -------------------------


    def monthly_expense(self):

        return self.get_value(

            """
            SELECT IFNULL(SUM(amount),0)

            FROM expenses

            WHERE strftime('%Y-%m', expense_date)
            =
            strftime('%Y-%m','now')

            """

        )



    def monthly_balance(self):

        return (

            self.total_income()

            -

            self.monthly_expense()

        )



    # -------------------------
    # Daily Summary
    # 01 - 31 Days
    # -------------------------


    def daily_summary(self):

        summary = []


        year = datetime.now().strftime("%Y")

        month = datetime.now().strftime("%m")



        for day in range(1, 32):


            date_value = (

                f"{year}-{month}-{day:02d}"

            )



            income = self.get_value(

                f"""

                SELECT IFNULL(SUM(amount),0)

                FROM

                (

                    SELECT amount

                    FROM student_payments

                    WHERE payment_date='{date_value}'


                    UNION ALL


                    SELECT amount

                    FROM incomes

                    WHERE income_date='{date_value}'


                    UNION ALL


                    SELECT registration_fee AS amount

                    FROM students

                    WHERE registration_date='{date_value}'

                )

                """

            )



            expense = self.get_value(

                f"""

                SELECT IFNULL(SUM(amount),0)

                FROM expenses

                WHERE expense_date='{date_value}'

                """

            )



            # No transaction day = blank


            if income == 0 and expense == 0:


                summary.append(

                    [

                        date_value,

                        "",

                        "",

                        ""

                    ]

                )


            else:


                summary.append(

                    [

                        date_value,

                        income,

                        expense,

                        income - expense

                    ]

                )


        return summary

    # -------------------------
    # Monthly Transactions
    # -------------------------


    def get_transactions(self):

        data = []


        try:

            conn = sqlite3.connect(DB_PATH)

            cur = conn.cursor()



            # Student Payments

            cur.execute(

                """
                SELECT

                    payment_date,
                    amount,
                    payment_method,
                    remarks

                FROM student_payments

                WHERE strftime('%Y-%m', payment_date)
                =
                strftime('%Y-%m','now')

                """

            )


            for row in cur.fetchall():

                data.append(

                    [

                        row[0],

                        "Student Payment",

                        row[1],

                        row[2] or "-",

                        row[3] or "-"

                    ]

                )



            # Other Income

            cur.execute(

                """
                SELECT

                    income_date,
                    amount,
                    payment_method,
                    remarks

                FROM incomes

                WHERE strftime('%Y-%m', income_date)
                =
                strftime('%Y-%m','now')

                """

            )


            for row in cur.fetchall():

                data.append(

                    [

                        row[0],

                        "Other Income",

                        row[1],

                        row[2] or "-",

                        row[3] or "-"

                    ]

                )



            # Expenses

            cur.execute(

                """
                SELECT

                    expense_date,
                    amount,
                    payment_method,
                    remarks

                FROM expenses

                WHERE strftime('%Y-%m', expense_date)
                =
                strftime('%Y-%m','now')

                """

            )


            for row in cur.fetchall():

                data.append(

                    [

                        row[0],

                        "Expense",

                        row[1],

                        row[2] or "-",

                        row[3] or "-"

                    ]

                )



            conn.close()



        except Exception:

            pass



        return data





    # -------------------------
    # PRINT REPORT
    # -------------------------


    def print_report(self, e):


        transactions = self.get_transactions()



        file_path = self.pdf.create_report_pdf(

            "Monthly Report",

            self.month_value(),

            self.total_income(),

            self.monthly_expense(),

            self.monthly_balance(),

            transactions

        )



        self.pdf.print_pdf(

            file_path

        )



        self.page.update()




    # -------------------------
    # Summary Card
    # -------------------------


    def card(self, title, value, icon):

        return ft.Container(

            width=220,

            height=120,

            bgcolor="white",

            border_radius=15,

            padding=20,


            shadow=ft.BoxShadow(

                blur_radius=8,

                spread_radius=1,

                color="#DDDDDD"

            ),


            content=ft.Column(

                [

                    ft.Icon(

                        icon,

                        size=30,

                        color="#F57C00"

                    ),


                    ft.Text(

                        title,

                        size=14,

                        color="#666666"

                    ),


                    ft.Text(

                        value,

                        size=22,

                        weight=ft.FontWeight.BOLD

                    )

                ]

            )

        )

    # -------------------------
    # Build Monthly Report
    # -------------------------


    def build(self):


        daily_data = self.daily_summary()

        transactions = self.get_transactions()



        daily_rows = []


        for item in daily_data:


            daily_rows.append(

                ft.DataRow(

                    cells=[


                        ft.DataCell(
                            ft.Text(item[0])
                        ),


                        ft.DataCell(
                            ft.Text(
                                f"₹ {item[1]}"
                                if item[1] != ""
                                else ""
                            )
                        ),


                        ft.DataCell(
                            ft.Text(
                                f"₹ {item[2]}"
                                if item[2] != ""
                                else ""
                            )
                        ),


                        ft.DataCell(
                            ft.Text(
                                f"₹ {item[3]}"
                                if item[3] != ""
                                else ""
                            )
                        )

                    ]

                )

            )



        transaction_rows = []


        for item in transactions:


            transaction_rows.append(

                ft.DataRow(

                    cells=[


                        ft.DataCell(
                            ft.Text(item[0])
                        ),


                        ft.DataCell(
                            ft.Text(item[1])
                        ),


                        ft.DataCell(
                            ft.Text(
                                f"₹ {item[2]}"
                            )
                        ),


                        ft.DataCell(
                            ft.Text(item[3])
                        ),


                        ft.DataCell(
                            ft.Text(item[4])
                        )

                    ]

                )

            )



        return ft.Container(

            expand=True,

            padding=30,

            bgcolor="#F7F7F7",


            content=ft.Column(

                [

                    ft.Text(

                        "Monthly Report",

                        size=30,

                        weight=ft.FontWeight.BOLD

                    ),



                    ft.Text(

                        f"Month : {self.month_value()}",

                        size=16,

                        color="#666666"

                    ),



                    ft.Divider(),



                    ft.Row(

                        [

                            self.card(

                                "Monthly Income",

                                f"₹ {self.total_income()}",

                                ft.Icons.ADD_CIRCLE

                            ),



                            self.card(

                                "Monthly Expense",

                                f"₹ {self.monthly_expense()}",

                                ft.Icons.REMOVE_CIRCLE

                            ),



                            self.card(

                                "Monthly Balance",

                                f"₹ {self.monthly_balance()}",

                                ft.Icons.SAVINGS

                            )


                        ],

                        wrap=True,

                        spacing=20

                    ),



                    ft.Container(

                        height=25

                    ),



                    ft.Text(

                        "Daily Summary (01 - 31)",

                        size=22,

                        weight=ft.FontWeight.BOLD

                    ),



                    ft.DataTable(

                        columns=[


                            ft.DataColumn(
                                ft.Text("Date")
                            ),


                            ft.DataColumn(
                                ft.Text("Income")
                            ),


                            ft.DataColumn(
                                ft.Text("Expense")
                            ),


                            ft.DataColumn(
                                ft.Text("Balance")
                            )


                        ],

                        rows=daily_rows

                    ),



                    ft.Container(

                        height=25

                    ),



                    ft.Text(

                        "Transactions",

                        size=22,

                        weight=ft.FontWeight.BOLD

                    ),



                    ft.DataTable(

                        columns=[


                            ft.DataColumn(
                                ft.Text("Date")
                            ),


                            ft.DataColumn(
                                ft.Text("Type")
                            ),


                            ft.DataColumn(
                                ft.Text("Amount")
                            ),


                            ft.DataColumn(
                                ft.Text("Payment")
                            ),


                            ft.DataColumn(
                                ft.Text("Remarks")
                            )


                        ],

                        rows=transaction_rows

                    ),



                    ft.Container(

                        height=20

                    ),



                    ft.ElevatedButton(

                        "PRINT",

                        icon=ft.Icons.PRINT,

                        width=180,

                        height=50,

                        on_click=self.print_report

                    )


                ],

                scroll=ft.ScrollMode.AUTO,

                expand=True

            )

        )



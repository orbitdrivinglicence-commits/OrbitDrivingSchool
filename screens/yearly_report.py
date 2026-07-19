"""
=========================================================
ORBIT DRIVING SCHOOL MANAGEMENT SYSTEM

Yearly Report

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



class YearlyReport:


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
    # Current Year
    # -------------------------


    def year_value(self):

        return datetime.now().strftime(
            "%Y"
        )



    # -------------------------
    # Yearly Income
    # -------------------------


    def yearly_registration_fee(self):

        return self.get_value(

            """
            SELECT IFNULL(SUM(registration_fee),0)

            FROM students

            WHERE strftime('%Y', registration_date)
            =
            strftime('%Y','now')

            """

        )



    def yearly_student_payment(self):

        return self.get_value(

            """
            SELECT IFNULL(SUM(amount),0)

            FROM student_payments

            WHERE strftime('%Y', payment_date)
            =
            strftime('%Y','now')

            """

        )



    def yearly_other_income(self):

        return self.get_value(

            """
            SELECT IFNULL(SUM(amount),0)

            FROM incomes

            WHERE strftime('%Y', income_date)
            =
            strftime('%Y','now')

            """

        )

    # -------------------------
    # Yearly Total Income
    # -------------------------


    def total_income(self):

        return (

            self.yearly_registration_fee()

            +

            self.yearly_student_payment()

            +

            self.yearly_other_income()

        )



    # -------------------------
    # Yearly Expense
    # -------------------------


    def yearly_expense(self):

        return self.get_value(

            """
            SELECT IFNULL(SUM(amount),0)

            FROM expenses

            WHERE strftime('%Y', expense_date)
            =
            strftime('%Y','now')

            """

        )



    def yearly_balance(self):

        return (

            self.total_income()

            -

            self.yearly_expense()

        )



    # -------------------------
    # 12 Months Summary
    # -------------------------


    def monthly_summary(self):

        summary = []


        year = datetime.now().strftime(
            "%Y"
        )



        months = [

            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December"

        ]



        for index, month in enumerate(months, start=1):


            month_value = f"{index:02d}"



            income = self.get_value(

                f"""

                SELECT IFNULL(SUM(amount),0)

                FROM

                (

                    SELECT amount

                    FROM student_payments

                    WHERE strftime('%Y-%m', payment_date)
                    =
                    '{year}-{month_value}'


                    UNION ALL


                    SELECT amount

                    FROM incomes

                    WHERE strftime('%Y-%m', income_date)
                    =
                    '{year}-{month_value}'


                    UNION ALL


                    SELECT registration_fee AS amount

                    FROM students

                    WHERE strftime('%Y-%m', registration_date)
                    =
                    '{year}-{month_value}'

                )

                """

            )



            expense = self.get_value(

                f"""

                SELECT IFNULL(SUM(amount),0)

                FROM expenses

                WHERE strftime('%Y-%m', expense_date)
                =
                '{year}-{month_value}'

                """

            )



            if income == 0 and expense == 0:


                summary.append(

                    [

                        month,

                        "",

                        "",

                        ""

                    ]

                )


            else:


                summary.append(

                    [

                        month,

                        income,

                        expense,

                        income - expense

                    ]

                )


        return summary

    # -------------------------
    # Yearly Transactions
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

                WHERE strftime('%Y', payment_date)
                =
                strftime('%Y','now')

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

                WHERE strftime('%Y', income_date)
                =
                strftime('%Y','now')

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

                WHERE strftime('%Y', expense_date)
                =
                strftime('%Y','now')

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

            "Yearly Report",

            self.year_value(),

            self.total_income(),

            self.yearly_expense(),

            self.yearly_balance(),

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
    # Build Yearly Report
    # -------------------------


    def build(self):


        monthly_data = self.monthly_summary()

        transactions = self.get_transactions()



        month_rows = []



        for item in monthly_data:


            month_rows.append(

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

                        "Yearly Report",

                        size=30,

                        weight=ft.FontWeight.BOLD

                    ),



                    ft.Text(

                        f"Year : {self.year_value()}",

                        size=16,

                        color="#666666"

                    ),



                    ft.Divider(),



                    ft.Row(

                        [

                            self.card(

                                "Yearly Income",

                                f"₹ {self.total_income()}",

                                ft.Icons.ADD_CIRCLE

                            ),



                            self.card(

                                "Yearly Expense",

                                f"₹ {self.yearly_expense()}",

                                ft.Icons.REMOVE_CIRCLE

                            ),



                            self.card(

                                "Yearly Balance",

                                f"₹ {self.yearly_balance()}",

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

                        "Monthly Summary (January - December)",

                        size=22,

                        weight=ft.FontWeight.BOLD

                    ),



                    ft.DataTable(

                        columns=[


                            ft.DataColumn(

                                ft.Text("Month")

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

                        rows=month_rows

                    ),



                    ft.Container(

                        height=25

                    ),



                    ft.Text(

                        "Yearly Transactions",

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


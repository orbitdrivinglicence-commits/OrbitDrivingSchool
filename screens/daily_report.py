import sqlite3
import flet as ft

from datetime import datetime

from utils.pdf_report import PDFReport


DB_PATH = "database/database.db"



class DailyReport:


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
    # Date
    # -------------------------


    def today_date(self):

        return datetime.now().strftime(
            "%Y-%m-%d"
        )



    # -------------------------
    # Income
    # -------------------------


    def today_registration_fee(self):

        return self.get_value(

            """
            SELECT IFNULL(SUM(registration_fee),0)
            FROM students
            WHERE registration_date=date('now')
            """

        )



    def today_student_payment(self):

        return self.get_value(

            """
            SELECT IFNULL(SUM(amount),0)
            FROM student_payments
            WHERE payment_date=date('now')
            """

        )



    def today_other_income(self):

        return self.get_value(

            """
            SELECT IFNULL(SUM(amount),0)
            FROM incomes
            WHERE income_date=date('now')
            """

        )



    def total_income(self):

        return (

            self.today_registration_fee()

            +

            self.today_student_payment()

            +

            self.today_other_income()

        )



    # -------------------------
    # Expense
    # -------------------------


    def today_expense(self):

        return self.get_value(

            """
            SELECT IFNULL(SUM(amount),0)
            FROM expenses
            WHERE expense_date=date('now')
            """

        )



    def today_balance(self):

        return (

            self.total_income()

            -

            self.today_expense()

        )

    # -------------------------
    # Card
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
    # Transactions
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

                WHERE payment_date=date('now')

                """

            )


            for row in cur.fetchall():

                data.append(

                    [

                        row[0],

                        "Student Payment",

                        row[1],

                        row[2],

                        row[3] or ""

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

                WHERE income_date=date('now')

                """

            )


            for row in cur.fetchall():

                data.append(

                    [

                        row[0],

                        "Other Income",

                        row[1],

                        row[2],

                        row[3] or ""

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

                WHERE expense_date=date('now')

                """

            )


            for row in cur.fetchall():

                data.append(

                    [

                        row[0],

                        "Expense",

                        row[1],

                        row[2],

                        row[3] or ""

                    ]

                )


            conn.close()



        except Exception:

            pass



        return data




    # -------------------------
    # Print Report
    # -------------------------


    def print_report(self, e):


        transactions = self.get_transactions()


        file_path = self.pdf.create_report_pdf(

            "Daily Report",

            self.today_date(),

            self.total_income(),

            self.today_expense(),

            self.today_balance(),

            transactions

        )


        self.pdf.print_pdf(

            file_path

        )


        self.page.update()

    # -------------------------
    # Build
    # -------------------------


    def build(self):


        transactions = self.get_transactions()



        rows = []


        for item in transactions:


            rows.append(

                ft.DataRow(

                    cells=[

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

                            ft.Container(

                                width=250,

                                content=ft.Text(

                                    item[4]
                                    if item[4]
                                    else "-",

                                    max_lines=3

                                )

                            )

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

                        "Daily Report",

                        size=30,

                        weight=ft.FontWeight.BOLD

                    ),



                    ft.Text(

                        f"Date : {self.today_date()}",

                        size=16,

                        color="#666666"

                    ),



                    ft.Divider(),



                    ft.Row(

                        [


                            self.card(

                                "Total Income",

                                f"₹ {self.total_income()}",

                                ft.Icons.ADD_CIRCLE

                            ),



                            self.card(

                                "Total Expense",

                                f"₹ {self.today_expense()}",

                                ft.Icons.REMOVE_CIRCLE

                            ),



                            self.card(

                                "Balance",

                                f"₹ {self.today_balance()}",

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

                        "Today's Transactions",

                        size=22,

                        weight=ft.FontWeight.BOLD

                    ),



                    ft.DataTable(

                        column_spacing=30,


                        columns=[


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


                        rows=rows

                    ),



                    ft.Container(

                        height=20

                    ),



                    ft.ElevatedButton(

                        "PRINT",

                        icon=ft.Icons.PRINT,

                        on_click=self.print_report,

                        width=180,

                        height=50

                    )


                ],

                scroll=ft.ScrollMode.AUTO,

                expand=True

            )

        )



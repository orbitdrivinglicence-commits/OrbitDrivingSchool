"""
=========================================================
ORBIT DRIVING SCHOOL MANAGEMENT SYSTEM

Report Search

Framework : Flet
Database  : SQLite
Mode      : Offline

Features:
- Date Search
- Month Search
- Year Search
- Transaction Details
=========================================================
"""


import sqlite3
import flet as ft

from datetime import datetime, date

from utils.pdf_report import PDFReport

DB_PATH = "database/database.db"



class ReportSearch:


    def __init__(self, page):

        self.page = page

        self.selected_date = None

        self.current_report_data = {}

        self.pdf = PDFReport()


    # -------------------------
    # Database
    # -------------------------


    def get_connection(self):

        return sqlite3.connect(DB_PATH)



    def get_value(self, query, params=()):


        try:


            conn = self.get_connection()

            cur = conn.cursor()


            cur.execute(

                query,

                params

            )


            result = cur.fetchone()[0]


            conn.close()


            return result or 0



        except Exception as e:


            print(e)

            return 0



    # -------------------------
    # Date Income
    # -------------------------


    def date_income(self, search_date):


        total = 0



        total += self.get_value(

            """
            SELECT IFNULL(SUM(registration_fee),0)
            FROM students
            WHERE registration_date=?
            """,

            (search_date,)

        )



        total += self.get_value(

            """
            SELECT IFNULL(SUM(amount),0)
            FROM student_payments
            WHERE payment_date=?
            """,

            (search_date,)

        )



        total += self.get_value(

            """
            SELECT IFNULL(SUM(amount),0)
            FROM incomes
            WHERE income_date=?
            """,

            (search_date,)

        )


        return total




    # -------------------------
    # Date Expense
    # -------------------------


    def date_expense(self, search_date):


        return self.get_value(

            """
            SELECT IFNULL(SUM(amount),0)
            FROM expenses
            WHERE expense_date=?
            """,

            (search_date,)

        )



    def balance(self, income, expense):

        return income - expense

    # -------------------------
    # Date Search Section
    # -------------------------


    def date_search_section(self):


        day_dropdown = ft.Dropdown(

            label="Day",

            width=120,

            options=[


                ft.dropdown.Option(

                    str(i)

                )

                for i in range(1,32)


            ]

        )



        month_dropdown = ft.Dropdown(

            label="Month",

            width=160,

            options=[


                ft.dropdown.Option(

                    str(i),

                    datetime(

                        2000,

                        i,

                        1

                    ).strftime("%B")

                )

                for i in range(1,13)


            ]

        )



        year_dropdown = ft.Dropdown(

            label="Year",

            width=140,

            options=[


                ft.dropdown.Option(

                    str(y)

                )

                for y in range(

                    2020,

                    datetime.now().year + 1

                )


            ]

        )



        result_area = ft.Column()



        def search_date(e):


            if not day_dropdown.value or not month_dropdown.value or not year_dropdown.value:


                result_area.controls = [


                    ft.Text(

                        "Select Day, Month and Year",

                        color="red"

                    )


                ]


                self.page.update()

                return




            search_date = (

                f"{year_dropdown.value}-"

                f"{int(month_dropdown.value):02d}-"

                f"{int(day_dropdown.value):02d}"

            )



            income = self.date_income(

                search_date

            )



            expense = self.date_expense(

                search_date

            )



            balance = self.balance(

                income,

                expense

            )



            self.current_report_data = {

                "title": "Date Report",

                "date": search_date,

                "income": income,

                "expense": expense,

                "balance": balance

            }



            result_area.controls=[



                ft.Text(

                    f"Date : {search_date}",

                    size=18,

                    weight=ft.FontWeight.BOLD

                ),



                ft.Text(

                    f"Income : ₹ {income}"

                ),



                ft.Text(

                    f"Expense : ₹ {expense}"

                ),



                ft.Text(

                    f"Balance : ₹ {balance}"

                ),



                ft.Divider(),



                self.transaction_table(

                    search_date,

                    search_date

                )



            ]



            self.page.update()





        return ft.Container(


            padding=20,


            bgcolor="white",


            border_radius=15,



            content=ft.Column(

                [

                    ft.Text(

                        "DATE SEARCH",

                        size=22,

                        weight=ft.FontWeight.BOLD

                    ),



                    ft.Row(

                        [


                            day_dropdown,


                            month_dropdown,


                            year_dropdown,



                            ft.ElevatedButton(

                                "SEARCH",

                                icon=ft.Icons.SEARCH,

                                on_click=search_date

                            ),

                            ft.ElevatedButton(

                                "PRINT DATE REPORT",

                                icon=ft.Icons.PRINT,

                                on_click=self.print_date_report

                             )


                        ],


                        wrap=True

                    ),


                    ft.Divider(),



                    result_area



                ]

            )


        )

    # -------------------------
    # Month Search
    # -------------------------


    def month_income(self, year, month):


        total = 0



        total += self.get_value(

            """
            SELECT IFNULL(SUM(registration_fee),0)
            FROM students
            WHERE strftime('%Y',registration_date)=?
            AND strftime('%m',registration_date)=?
            """,

            (

                str(year),

                f"{month:02d}"

            )

        )



        total += self.get_value(

            """
            SELECT IFNULL(SUM(amount),0)
            FROM student_payments
            WHERE strftime('%Y',payment_date)=?
            AND strftime('%m',payment_date)=?
            """,

            (

                str(year),

                f"{month:02d}"

            )

        )



        total += self.get_value(

            """
            SELECT IFNULL(SUM(amount),0)
            FROM incomes
            WHERE strftime('%Y',income_date)=?
            AND strftime('%m',income_date)=?
            """,

            (

                str(year),

                f"{month:02d}"

            )

        )


        return total




    def month_expense(self, year, month):


        return self.get_value(

            """
            SELECT IFNULL(SUM(amount),0)
            FROM expenses
            WHERE strftime('%Y',expense_date)=?
            AND strftime('%m',expense_date)=?
            """,

            (

                str(year),

                f"{month:02d}"

            )

        )





    def month_search_section(self):


        month_dropdown = ft.Dropdown(

            label="Month",

            width=180,


            options=[


                ft.dropdown.Option(

                    str(i),

                    datetime(

                        2000,

                        i,

                        1

                    ).strftime("%B")

                )

                for i in range(1,13)


            ]

        )




        year_dropdown = ft.Dropdown(

            label="Year",

            width=150,


            options=[


                ft.dropdown.Option(

                    str(y)

                )

                for y in range(

                    2020,

                    datetime.now().year + 1

                )

            ]

        )



        result_area = ft.Column()



        def search_month(e):


            if not month_dropdown.value or not year_dropdown.value:


                result_area.controls=[


                    ft.Text(

                        "Select month and year",

                        color="red"

                    )

                ]


                self.page.update()


                return




            month = int(

                month_dropdown.value

            )


            year = int(

                year_dropdown.value

            )



            rows=[]



            for day in range(1,32):


                try:


                    current = date(

                        year,

                        month,

                        day

                    )


                except ValueError:


                    continue




                current_date = current.strftime(

                    "%Y-%m-%d"

                )



                income = self.date_income(

                    current_date

                )



                expense = self.date_expense(

                    current_date

                )



                rows.append(

                    ft.DataRow(

                        cells=[


                            ft.DataCell(

                                ft.Text(

                                    current.strftime(

                                        "%d-%m-%Y"

                                    )

                                )

                            ),



                            ft.DataCell(

                                ft.Text(

                                    f"₹ {income}"

                                )

                            ),



                            ft.DataCell(

                                ft.Text(

                                    f"₹ {expense}"

                                )

                            ),



                            ft.DataCell(

                                ft.Text(

                                    f"₹ {income-expense}"

                                )

                            )


                        ]

                    )

                )


            self.current_report_data = {

                "title": "Month Report",

                "date": f"{month}-{year}",

                "income": self.month_income(

                    year,

                    month

                ),

                "expense": self.month_expense(

                    year,

                    month

                ),

                "balance": (

                    self.month_income(

                        year,

                        month

                    )

                    -

                    self.month_expense(

                        year,

                        month

                    )

                )

            }

            result_area.controls=[


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


                    rows=rows

                )

            ]



            self.page.update()





        return ft.Container(


            padding=20,


            bgcolor="white",


            border_radius=15,


            content=ft.Column(

                [

                    ft.Text(

                        "MONTH SEARCH",

                        size=22,

                        weight=ft.FontWeight.BOLD

                    ),



                    ft.Row(

                        [

                            month_dropdown,


                            year_dropdown,



                            ft.ElevatedButton(

                                "SEARCH",

                                icon=ft.Icons.SEARCH,

                                on_click=search_month

                            ),


                            ft.ElevatedButton(

                                "PRINT MONTH REPORT",

                                icon=ft.Icons.PRINT,

                                on_click=self.print_month_report

                            )


                        ]

                    ),



                    ft.Divider(),



                    result_area


                ]

            )

        )

    # -------------------------
    # Year Search
    # -------------------------


    def yearly_search_section(self):


        year_dropdown = ft.Dropdown(

            label="Year",

            width=180,


            options=[


                ft.dropdown.Option(

                    str(y)

                )

                for y in range(

                    2020,

                    datetime.now().year + 1

                )


            ]

        )



        result_area = ft.Column()



        def search_year(e):


            if not year_dropdown.value:


                result_area.controls = [


                    ft.Text(

                        "Select year first",

                        color="red"

                    )


                ]


                self.page.update()


                return




            year = int(

                year_dropdown.value

            )



            rows = []



            for month in range(1,13):


                income = self.month_income(

                    year,

                    month

                )



                expense = self.month_expense(

                    year,

                    month

                )



                month_name = datetime(

                    year,

                    month,

                    1

                ).strftime("%B")



                rows.append(


                    ft.DataRow(

                        cells=[



                            ft.DataCell(

                                ft.Text(

                                    month_name

                                )

                            ),



                            ft.DataCell(

                                ft.Text(

                                    f"₹ {income}"

                                )

                            ),



                            ft.DataCell(

                                ft.Text(

                                    f"₹ {expense}"

                                )

                            ),



                            ft.DataCell(

                                ft.Text(

                                    f"₹ {income-expense}"

                                )

                            )



                        ]

                    )

                )


            self.current_report_data = {

                "title": "Year Report",

                "date": str(year),

                "income": sum(

                    self.month_income(

                        year,

                        month

                    )

                    for month in range(1, 13)

                ),

                "expense": sum(

                    self.month_expense(

                        year,

                        month

                    )

                    for month in range(1, 13)

                ),

                "balance": (

                    sum(

                        self.month_income(

                            year,

                            month

                        )

                        for month in range(1, 13)

                    )

                    -

                    sum(

                        self.month_expense(

                            year,

                            month

                        )

                        for month in range(1, 13)

                    )

                )

            }


            result_area.controls=[



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


                    rows=rows


                )



            ]



            self.page.update()





        return ft.Container(


            padding=20,


            bgcolor="white",


            border_radius=15,



            content=ft.Column(

                [



                    ft.Text(

                        "YEAR SEARCH",

                        size=22,

                        weight=ft.FontWeight.BOLD

                    ),



                    ft.Row(

                        [


                            year_dropdown,



                            ft.ElevatedButton(

                                "SEARCH",

                                icon=ft.Icons.SEARCH,

                                on_click=search_year

                            ),

                            ft.ElevatedButton(

                                "PRINT YEAR REPORT",

                                icon=ft.Icons.PRINT,

                                on_click=self.print_year_report

                            )


                        ]

                    ),



                    ft.Divider(),



                    result_area



                ]

            )

        )

    # -------------------------
    # PDF Transaction Data
    # -------------------------

    def get_pdf_transactions(self, start_date, end_date):

        transactions = []

        try:

            conn = self.get_connection()

            cur = conn.cursor()


            cur.execute(

                """
                SELECT

                    payment_date,

                    'Student Payment',

                    amount,

                    payment_method,

                    remarks

                FROM student_payments

                WHERE payment_date BETWEEN ? AND ?

                ORDER BY payment_date

                """,

                (

                    start_date,

                    end_date

                )

            )


            for row in cur.fetchall():

                transactions.append(

                    [

                        row[0],

                        row[1],

                        row[2],

                        row[3] or "-",

                        row[4] or "-"

                    ]

                )


            cur.execute(

                """
                SELECT

                    income_date,

                    'Income',

                    amount,

                    payment_method,

                    remarks

                FROM incomes

                WHERE income_date BETWEEN ? AND ?

                ORDER BY income_date

                """,

                (

                    start_date,

                    end_date

                )

            )


            for row in cur.fetchall():

                transactions.append(

                    [

                        row[0],

                        row[1],

                        row[2],

                        row[3] or "-",

                        row[4] or "-"

                    ]

                )


            cur.execute(

                """
                SELECT

                    expense_date,

                    'Expense',

                    amount,

                    payment_method,

                    remarks

                FROM expenses

                WHERE expense_date BETWEEN ? AND ?

                ORDER BY expense_date

                """,

                (

                    start_date,

                    end_date

                )

            )


            for row in cur.fetchall():

                transactions.append(

                    [

                        row[0],

                        row[1],

                        row[2],

                        row[3] or "-",

                        row[4] or "-"

                    ]

                )


            conn.close()


        except Exception as e:

            print(e)


        return transactions

    # -------------------------
    # Transaction Table
    # -------------------------


    def transaction_table(self, start_date, end_date):


        rows = []



        try:


            conn = self.get_connection()

            cur = conn.cursor()



            # Student Payments

            cur.execute(

                """

                SELECT

                    payment_date,

                    'Student Payment',

                    amount,

                    payment_method,

                    remarks

                FROM student_payments

                WHERE payment_date BETWEEN ? AND ?

                ORDER BY payment_date


                """,

                (

                    start_date,

                    end_date

                )

            )



            for row in cur.fetchall():


                rows.append(

                    ft.DataRow(

                        cells=[


                            ft.DataCell(

                                ft.Text(

                                    row[0]

                                )

                            ),



                            ft.DataCell(

                                ft.Text(

                                    row[1]

                                )

                            ),



                            ft.DataCell(

                                ft.Text(

                                    f"₹ {row[2]}"

                                )

                            ),



                            ft.DataCell(

                                ft.Text(

                                    row[3] or "-"

                                )

                            ),



                            ft.DataCell(

                                ft.Text(

                                    row[4] or "-"

                                )

                            )


                        ]

                    )

                )





            # Other Income

            cur.execute(

                """

                SELECT

                    income_date,

                    'Other Income',

                    amount,

                    payment_method,

                    remarks

                FROM incomes

                WHERE income_date BETWEEN ? AND ?

                ORDER BY income_date


                """,

                (

                    start_date,

                    end_date

                )

            )



            for row in cur.fetchall():


                rows.append(


                    ft.DataRow(

                        cells=[


                            ft.DataCell(

                                ft.Text(row[0])

                            ),


                            ft.DataCell(

                                ft.Text(row[1])

                            ),


                            ft.DataCell(

                                ft.Text(

                                    f"₹ {row[2]}"

                                )

                            ),


                            ft.DataCell(

                                ft.Text(

                                    row[3] or "-"

                                )

                            ),


                            ft.DataCell(

                                ft.Text(

                                    row[4] or "-"

                                )

                            )


                        ]

                    )

                )





            # Expenses

            cur.execute(

                """

                SELECT

                    expense_date,

                    'Expense',

                    amount,

                    payment_method,

                    remarks

                FROM expenses

                WHERE expense_date BETWEEN ? AND ?

                ORDER BY expense_date


                """,

                (

                    start_date,

                    end_date

                )

            )



            for row in cur.fetchall():


                rows.append(


                    ft.DataRow(

                        cells=[


                            ft.DataCell(

                                ft.Text(row[0])

                            ),


                            ft.DataCell(

                                ft.Text(row[1])

                            ),


                            ft.DataCell(

                                ft.Text(

                                    f"₹ {row[2]}"

                                )

                            ),


                            ft.DataCell(

                                ft.Text(

                                    row[3] or "-"

                                )

                            ),


                            ft.DataCell(

                                ft.Text(

                                    row[4] or "-"

                                )

                            )


                        ]

                    )

                )



            conn.close()



        except Exception as e:


            print(

                "TRANSACTION ERROR:",

                e

            )



        return ft.DataTable(


            column_spacing=30,


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



            rows=rows


        )


    # -------------------------
    # Print Date Report
    # -------------------------

    def print_date_report(self, e=None):

        if not self.current_report_data:
            return

        data = self.current_report_data

        self.pdf.create_report_pdf(

            data["title"],

            data["date"],

            data["income"],

            data["expense"],

            data["balance"],

        self.get_pdf_transactions(

            data["date"],

            data["date"]

        )

        )


    # -------------------------
    # Print Month Report
    # -------------------------

    def print_month_report(self, e=None):

        if not self.current_report_data:
            return

        data = self.current_report_data

        self.pdf.create_report_pdf(

            data["title"],

            data["date"],

            data["income"],

            data["expense"],

            data["balance"],

        self.get_pdf_transactions(

            data["date"] + "-01",

            data["date"] + "-31"

        )

        )


    # -------------------------
    # Print Year Report
    # -------------------------

    def print_year_report(self, e=None):

        if not self.current_report_data:
            return

        data = self.current_report_data

        self.pdf.create_report_pdf(

            data["title"],

            data["date"],

            data["income"],

            data["expense"],

            data["balance"],

        self.get_pdf_transactions(

            data["date"] + "-01-01",

            data["date"] + "-12-31"

        )


        )


    # -------------------------
    # Build Report Search Page
    # -------------------------


    def build(self):


        return ft.Container(


            expand=True,


            padding=30,


            bgcolor="#F7F7F7",



            content=ft.Column(


                [



                    ft.Text(


                        "REPORT SEARCH",


                        size=30,


                        weight=ft.FontWeight.BOLD

                    ),



                    ft.Text(


                        "Search reports manually by Date, Month and Year",


                        size=15,


                        color="#666666"

                    ),



                    ft.Divider(),




                    self.date_search_section(),




                    ft.Container(

                        height=20

                    ),




                    self.month_search_section(),




                    ft.Container(

                        height=20

                    ),




                    self.yearly_search_section()



                ],


                scroll=ft.ScrollMode.AUTO,


                expand=True


            )

        )



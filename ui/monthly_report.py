"""
=========================================================
ORBIT DRIVING SCHOOL MANAGEMENT SYSTEM

Monthly Report UI

Framework : Flet
Database  : SQLite
Mode      : Offline
=========================================================
"""

import flet as ft
import sqlite3
from datetime import datetime


DB_PATH = "database/database.db"


class MonthlyReport:

    def __init__(self, page):

        self.page = page

        self.report_area = ft.Column()



    def get_monthly_report(self):

        current_month = datetime.now().strftime(
            "%Y-%m"
        )


        conn = sqlite3.connect(DB_PATH)

        cursor = conn.cursor()


        # Students this month

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM students
            WHERE registration_date LIKE ?
            """,
            (
                current_month + "%",
            )
        )

        students = cursor.fetchone()[0]


        # Income this month

        cursor.execute(
            """
            SELECT SUM(amount)
            FROM incomes
            WHERE income_date LIKE ?
            """,
            (
                current_month + "%",
            )
        )

        income = cursor.fetchone()[0]

        if income is None:
            income = 0



        # Expense this month

        cursor.execute(
            """
            SELECT SUM(amount)
            FROM expenses
            WHERE expense_date LIKE ?
            """,
            (
                current_month + "%",
            )
        )

        expense = cursor.fetchone()[0]

        if expense is None:
            expense = 0


        conn.close()


        balance = income - expense


        return (
            students,
            income,
            expense,
            balance
        )



    def load_report(self, e=None):

        students, income, expense, balance = (
            self.get_monthly_report()
        )


        self.report_area.controls.clear()


        reports = [

            (
                "Monthly Students",
                str(students),
                ft.Icons.PERSON
            ),

            (
                "Monthly Income",
                f"₹ {income}",
                ft.Icons.ADD_CIRCLE
            ),

            (
                "Monthly Expense",
                f"₹ {expense}",
                ft.Icons.REMOVE_CIRCLE
            ),

            (
                "Monthly Balance",
                f"₹ {balance}",
                ft.Icons.ACCOUNT_BALANCE
            )

        ]


        for title, value, icon in reports:


            self.report_area.controls.append(

                ft.Container(

                    padding=20,

                    bgcolor="#FFFFFF",

                    border_radius=15,

                    content=ft.Column(

                        [

                            ft.Icon(
                                icon,
                                size=30
                            ),

                            ft.Text(
                                title,
                                size=16
                            ),

                            ft.Text(
                                value,
                                size=24,
                                weight=ft.FontWeight.BOLD
                            )

                        ]

                    )

                )

            )


        self.page.update()



    def build(self):

        self.load_report()


        return ft.Container(

            padding=30,

            content=ft.Column(

                [

                    ft.Text(

                        "Monthly Report",

                        size=28,

                        weight=ft.FontWeight.BOLD

                    ),


                    ft.ElevatedButton(

                        "Refresh Report",

                        icon=ft.Icons.REFRESH,

                        on_click=self.load_report

                    ),


                    ft.Divider(),


                    self.report_area


                ]

            )

        )

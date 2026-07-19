"""
=========================================================
ORBIT DRIVING SCHOOL MANAGEMENT SYSTEM

Daily Report UI

Framework : Flet
Database  : SQLite
Mode      : Offline
=========================================================
"""

import flet as ft
import sqlite3
from datetime import datetime


DB_PATH = "database/database.db"


class DailyReport:

    def __init__(self, page):

        self.page = page

        self.report_area = ft.Column()



    def get_today_report(self):

        today = datetime.now().strftime(
            "%Y-%m-%d"
        )

        conn = sqlite3.connect(DB_PATH)

        cursor = conn.cursor()


        # Total Students Registered Today

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM students
            WHERE registration_date = ?
            """,
            (today,)
        )

        students = cursor.fetchone()[0]


        # Today's Income

        cursor.execute(
            """
            SELECT SUM(amount)
            FROM incomes
            WHERE income_date = ?
            """,
            (today,)
        )

        income = cursor.fetchone()[0]

        if income is None:
            income = 0


        # Today's Expense

        cursor.execute(
            """
            SELECT SUM(amount)
            FROM expenses
            WHERE expense_date = ?
            """,
            (today,)
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
            self.get_today_report()
        )


        self.report_area.controls.clear()


        cards = [

            (
                "New Students",
                str(students),
                ft.Icons.PERSON
            ),

            (
                "Today's Income",
                f"₹ {income}",
                ft.Icons.ADD_CIRCLE
            ),

            (
                "Today's Expense",
                f"₹ {expense}",
                ft.Icons.REMOVE_CIRCLE
            ),

            (
                "Balance",
                f"₹ {balance}",
                ft.Icons.ACCOUNT_BALANCE
            )

        ]


        for title, value, icon in cards:


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

                        "Daily Report",

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

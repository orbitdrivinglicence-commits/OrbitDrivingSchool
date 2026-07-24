"""
=========================================================
ORBIT DRIVING SCHOOL MANAGEMENT SYSTEM

REPORT SEARCH MODULE

Date Search
Month Search
Year Search

Framework : Flet
Database  : SQLite
Mode      : Offline

Developer : AMAL THIRUTHOOR
=========================================================
"""

import sqlite3
import flet as ft

from utils.theme import (
    APP_NAME,
    DEVELOPER,
    PRIMARY_COLOR
)


DB_PATH = "database/database.db"


class Home:


    def __init__(
        self,
        page,
        change_screen,
        refresh_app
    ):

        self.page = page

        self.change_screen = change_screen

        self.refresh_app = refresh_app

        self.stats_container = ft.Container()


    # -------------------------
    # Database
    # -------------------------


    def get_value(self, query):

        try:

            conn = sqlite3.connect(
                DB_PATH
            )

            cur = conn.cursor()

            cur.execute(
                query
            )


            result = cur.fetchone()[0]


            conn.close()


            return result or 0


        except Exception:

            return 0




    # -------------------------
    # Student Statistics
    # -------------------------


    def total_students(self):

        return str(

            self.get_value(

                """
                SELECT COUNT(*)
                FROM students
                """

            )

        )




    def active_students(self):

        return str(

            self.get_value(

                """
                SELECT COUNT(*)
                FROM students
                WHERE status='ACTIVE'
                """

            )

        )




    def completed_students(self):

        return str(

            self.get_value(

                """
                SELECT COUNT(*)
                FROM students
                WHERE status='COMPLETED'
                """

            )

        )

    # -------------------------
    # Today's Income
    # -------------------------


    def today_income(self):


        registration = self.get_value(

            """
            SELECT IFNULL(SUM(registration_fee),0)
            FROM students
            WHERE registration_date = date('now')
            """

        )


        payments = self.get_value(

            """
            SELECT IFNULL(SUM(amount),0)
            FROM student_payments
            WHERE payment_date = date('now')
            """

        )


        manual_income = self.get_value(

            """
            SELECT IFNULL(SUM(amount),0)
            FROM incomes
            WHERE income_date = date('now')
            """

        )


        return f"₹ {registration + payments + manual_income}"





    # -------------------------
    # Today's Expense
    # -------------------------


    def today_expense(self):


        expense = self.get_value(

            """
            SELECT IFNULL(SUM(amount),0)
            FROM expenses
            WHERE expense_date = date('now')
            """

        )


        return f"₹ {expense}"





    # -------------------------
    # Today's Balance
    # -------------------------


    def today_balance(self):


        income = self.get_value(

            """
            SELECT IFNULL(SUM(registration_fee),0)
            FROM students
            WHERE registration_date = date('now')
            """

        )


        income += self.get_value(

            """
            SELECT IFNULL(SUM(amount),0)
            FROM student_payments
            WHERE payment_date = date('now')
            """

        )


        income += self.get_value(

            """
            SELECT IFNULL(SUM(amount),0)
            FROM incomes
            WHERE income_date = date('now')
            """

        )


        expense = self.get_value(

            """
            SELECT IFNULL(SUM(amount),0)
            FROM expenses
            WHERE expense_date = date('now')
            """

        )


        return f"₹ {income - expense}"





    # -------------------------
    # Dashboard Card
    # -------------------------


    def card(self, title, value, icon):

        return ft.Container(

            width=220,

            height=135,

            bgcolor="white",

            border_radius=18,

            padding=20,

            shadow=ft.BoxShadow(

                blur_radius=10,

                spread_radius=1,

                color="#D9D9D9"

            ),

            content=ft.Column(

                [

                    ft.Container(

                        width=42,

                        height=42,

                        border_radius=21,

                        bgcolor="#FFF1E6",

                        alignment=ft.Alignment(0, 0),

                        content=ft.Icon(

                            icon,

                            size=24,

                            color=PRIMARY_COLOR

                        )

                    ),


                    ft.Container(

                        height=5

                    ),


                    ft.Text(

                        title,

                        size=13,

                        color="#777777"

                    ),


                    ft.Text(

                        value,

                        size=26,

                        weight=ft.FontWeight.BOLD,

                        color="#111111"

                    )

                ],

                spacing=3

            )

        )



    # -------------------------
    # Statistics
    # -------------------------


    def statistics(self):


        self.stats_container.content = ft.Row(

            [

                self.card(

                    "Total Students",

                    self.total_students(),

                    ft.Icons.PEOPLE

                ),



                self.card(

                    "Active Students",

                    self.active_students(),

                    ft.Icons.VERIFIED_USER

                ),



                self.card(

                    "Completed",

                    self.completed_students(),

                    ft.Icons.SCHOOL

                ),



                self.card(

                    "Today's Income",

                    self.today_income(),

                    ft.Icons.ADD_CIRCLE

                ),



                self.card(

                    "Today's Expense",

                    self.today_expense(),

                    ft.Icons.REMOVE_CIRCLE

                ),



                self.card(

                    "Today's Balance",

                    self.today_balance(),

                    ft.Icons.SAVINGS

                )

            ],


            wrap=True,

            spacing=20

        )

        return self.stats_container

    def refresh_dashboard(self):

        print("DASHBOARD REFRESH CALLED")

        self.statistics()

        self.stats_container.update()

        self.page.update()

    def refresh_application(self, e=None):

        self.refresh_app()


    # -------------------------
    # Action Button
    # -------------------------


    def action_button(self, text, icon, action=None):


        return ft.ElevatedButton(

            text,


            icon=icon,


            width=180,


            height=50,


            style=ft.ButtonStyle(

                bgcolor=PRIMARY_COLOR,

                color="white"

            ),


            on_click=action

        )

    # -------------------------
    # Open Report Search
    # -------------------------


    def open_report_search(self, e=None):


        from screens.report_search import ReportSearch


        self.change_screen(

            ReportSearch(

                self.page

            ).build()

        )


    # -------------------------
    # Open Student Registration
    # -------------------------

    def open_student_registration(self, e=None):

        from ui.student_registration import StudentRegistration

        self.change_screen(
            StudentRegistration(self.page).build()
        )


    # -------------------------
    # Open Student Search
    # -------------------------

    def open_student_search(self, e=None):

        from ui.student_search import StudentSearch


        self.change_screen(

            StudentSearch(

                self.page,

                self.change_screen,

                self.refresh_app

            ).build()

        )


    # -------------------------
    # Open Income
    # -------------------------

    def open_income(self, e=None):

        from ui.incomes import Income

        self.change_screen(
            Income(self.page).build()
        )


    # -------------------------
    # Open Expenses
    # -------------------------

    def open_expenses(self, e=None):

        from ui.expenses import Expenses

        self.change_screen(
            Expenses(self.page).build()
        )


    # -------------------------
    # Open Reports Menu
    # -------------------------

    def open_reports(self, e=None):

        from screens.daily_report import DailyReport
        from screens.monthly_report import MonthlyReport
        from screens.yearly_report import YearlyReport
        from screens.report_search import ReportSearch


        self.change_screen(

            ft.Container(

                padding=30,

                content=ft.Column(

                    [

                        ft.Text(
                            "REPORTS",
                            size=28,
                            weight=ft.FontWeight.BOLD,
                        ),


                        ft.ElevatedButton(
                            "Daily Report",
                            icon=ft.Icons.TODAY,
                            on_click=lambda x:
                                self.change_screen(
                                    DailyReport(self.page).build()
                                ),
                        ),


                        ft.ElevatedButton(
                            "Monthly Report",
                            icon=ft.Icons.CALENDAR_MONTH,
                            on_click=lambda x:
                                self.change_screen(
                                    MonthlyReport(self.page).build()
                                ),
                        ),


                        ft.ElevatedButton(
                            "Yearly Report",
                            icon=ft.Icons.INSERT_CHART,
                            on_click=lambda x:
                                self.change_screen(
                                    YearlyReport(self.page).build()
                                ),
                        ),


                        ft.ElevatedButton(
                            "Report Search",
                            icon=ft.Icons.SEARCH,
                            on_click=lambda x:
                                self.change_screen(
                                    ReportSearch(self.page).build()
                                ),
                        ),

                    ]

                )

            )

        )


    # -------------------------
    # Quick Actions
    # -------------------------


    def quick_actions(self):


        return ft.Column(

            [

                ft.Text(

                    "Quick Actions",

                    size=22,

                    weight=ft.FontWeight.BOLD

                ),



                ft.Row(

                    [

                        self.action_button(

                            "Add Student",

                            ft.Icons.PERSON_ADD,

                            self.open_student_registration

                        ),



                        self.action_button(

                            "Student Search",

                            ft.Icons.SEARCH,

                            self.open_student_search

                        ),



                        self.action_button(

                            "Add Incomes",

                            ft.Icons.ADD_CIRCLE,

                            self.open_income

                        ),



                        self.action_button(

                            "Add Expenses",

                            ft.Icons.REMOVE_CIRCLE,

                            self.open_expenses

                        ),


                        self.action_button(

                            "Search Report",

                            ft.Icons.SEARCH,

                            self.open_report_search

                        ),


                    ],


                    wrap=True,


                    spacing=15

                )

            ]

        )

    # -------------------------
    # System Information
    # -------------------------


    def information_panel(self):


        return ft.Container(


            padding=20,


            bgcolor="white",


            border_radius=15,


            shadow=ft.BoxShadow(

                blur_radius=8,

                spread_radius=1,

                color="#DDDDDD"

            ),



            content=ft.Column(

                [


                    ft.Text(

                        "System Information",

                        size=20,

                        weight=ft.FontWeight.BOLD

                    ),



                    ft.Divider(),



                    ft.Text(

                        "Offline Driving School Management System"

                    ),



                    ft.Text(

                        "Student Registration & Fee Management"

                    ),



                    ft.Text(

                        "Income, Expense and Report Management"

                    ),



                    ft.Text(

                        "System Status : READY",

                        color="green",

                        weight=ft.FontWeight.BOLD

                    )


                ],


                spacing=8

            )

        )





    # -------------------------
    # Footer
    # -------------------------


    def footer(self):


        return ft.Container(


            padding=10,


            content=ft.Column(

                [


                    ft.Text(

                        APP_NAME,

                        size=13,

                        color=PRIMARY_COLOR,

                        weight=ft.FontWeight.BOLD

                    ),



                    ft.Text(

                        f"Developed by {DEVELOPER}",

                        size=12,

                        color="#777777"

                    ),



                    ft.Text(

                        "© 2026 All Rights Reserved",

                        size=11,

                        color="#999999"

                    )


                ],



                horizontal_alignment=ft.CrossAxisAlignment.CENTER,


                spacing=2

            )

        )





    # -------------------------
    # Build Dashboard
    # -------------------------


    def build(self):


        return ft.Container(


            expand=True,


            padding=30,


            bgcolor="#F7F7F7",



            content=ft.Column(


                [

                    ft.Image(

                        src="assets/images/logo.png",

                        width=120,

                        height=120,

                    ),


                    ft.Text(

                        APP_NAME,

                        size=30,

                        weight=ft.FontWeight.BOLD,

                        color=PRIMARY_COLOR

                    ),



                    ft.Text(

                        "Daily Driving School Dashboard",

                        size=16,

                        color="#666666"

                    ),



                    ft.Divider(),




                    self.statistics(),




                    ft.Container(

                        height=25

                    ),




                    self.quick_actions(),




                    ft.Container(

                        height=25

                    ),




                    self.information_panel(),




                    ft.Container(

                        expand=True

                    ),




                    ft.Divider(),




                    self.footer()


                ],



                scroll=ft.ScrollMode.AUTO,


                expand=True

            )

        )



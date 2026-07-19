"""
=========================================================
ORBIT DRIVING SCHOOL MANAGEMENT SYSTEM

Expense Entry UI

Framework : Flet
Database  : SQLite
Mode      : Offline
=========================================================
"""

import flet as ft
import sqlite3
from datetime import datetime


DB_PATH = "database/database.db"


class Expenses:

    def __init__(self, page):

        self.page = page


        self.amount = ft.TextField(

            label="Expense Amount",

            keyboard_type=ft.KeyboardType.NUMBER

        )


        self.remarks = ft.TextField(

            label="Remarks",

            multiline=True

        )


        self.payment_method = ft.Dropdown(

            label="Payment Method",

            options=[

                ft.dropdown.Option("Cash"),

                ft.dropdown.Option("UPI"),

                ft.dropdown.Option("Google Pay"),

                ft.dropdown.Option("Bank")

            ],

            value="Cash"

        )


        self.message = ft.Text()



    # -------------------------
    # Save Expense
    # -------------------------

    def save_expense(self, e):

        if not self.amount.value or float(self.amount.value) <= 0:

             self.message.value = "Enter valid expense amount"

             self.message.color = "red"

             self.page.update()

             return

        try:

            conn = sqlite3.connect(DB_PATH)

            cursor = conn.cursor()


            now = datetime.now()


            cursor.execute(

                """
                INSERT INTO expenses(

                    expense_date,
                    amount,
                    remarks,
                    created_at,
                    payment_method

                )

                VALUES(?,?,?,?,?)

                """,

                (

                    now.strftime("%Y-%m-%d"),

                    float(
                        self.amount.value or 0
                    ),

                    self.remarks.value,

                    now.strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),

                    self.payment_method.value

                )

            )


            conn.commit()

            conn.close()


            self.message.value = (
                "Expense Saved Successfully"
            )

            self.message.color = "green"


            self.amount.value = ""

            self.remarks.value = ""

            self.payment_method.value = "Cash"


            self.page.update()



        except Exception as ex:


            self.message.value = str(ex)

            self.message.color = "red"


            self.page.update()



    # -------------------------
    # Build UI
    # -------------------------

    def build(self):

        return ft.Container(

            padding=30,

            content=ft.Column(

                [

                    ft.Text(

                        "Expense Entry",

                        size=28,

                        weight=ft.FontWeight.BOLD

                    ),


                    self.amount,


                    self.remarks,


                    self.payment_method,


                    ft.ElevatedButton(

                        "Save Expense",

                        icon=ft.Icons.SAVE,

                        on_click=self.save_expense

                    ),


                    self.message


                ]

            )

        )

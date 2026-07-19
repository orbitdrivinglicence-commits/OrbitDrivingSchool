import flet as ft
import sqlite3
from datetime import datetime

DB_PATH = "database/database.db"


class Income:

    def __init__(self, page):

        self.page = page

        self.amount = ft.TextField(
            label="Income Amount",
            keyboard_type=ft.KeyboardType.NUMBER
        )

        self.remarks = ft.TextField(
            label="Remarks",
            multiline=True
        )

        self.payment_method = ft.Dropdown(
            label="Payment Method",
            value="Cash",
            options=[
                ft.dropdown.Option("Cash"),
                ft.dropdown.Option("UPI"),
                ft.dropdown.Option("Bank"),
                ft.dropdown.Option("Google Pay"),
            ],
        )

        self.message = ft.Text()

    def save_income(self, e):

        if not self.amount.value or float(self.amount.value) <= 0:

           self.message.value = "Enter valid income amount"

           self.message.color = "red"

           self.page.update()

           return

        try:

            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()

            now = datetime.now()

            cursor.execute(
                """
                INSERT INTO incomes(
                    income_date,
                    amount,
                    remarks,
                    payment_method,
                    created_at
                )
                VALUES(?,?,?,?,?)
                """,
                (
                    now.strftime("%Y-%m-%d"),
                    float(self.amount.value or 0),
                    self.remarks.value,
                    self.payment_method.value,
                    now.strftime("%Y-%m-%d %H:%M:%S"),
                ),
            )

            conn.commit()
            conn.close()

            self.message.value = "Income Saved Successfully"
            self.message.color = "green"

            self.amount.value = ""
            self.remarks.value = ""
            self.payment_method.value = "Cash"

            self.page.update()

        except Exception as ex:

            self.message.value = str(ex)
            self.message.color = "red"
            self.page.update()

    def build(self):

        return ft.Container(
            padding=30,
            content=ft.Column(
                [
                    ft.Text(
                        "Income Entry",
                        size=28,
                        weight=ft.FontWeight.BOLD,
                    ),

                    self.amount,

                    self.remarks,

                    self.payment_method,

                    ft.ElevatedButton(
                        "Save Income",
                        icon=ft.Icons.SAVE,
                        on_click=self.save_income,
                    ),

                    self.message,
                ],
                scroll=ft.ScrollMode.AUTO,
            ),
        )

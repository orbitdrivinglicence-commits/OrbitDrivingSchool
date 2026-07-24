import flet as ft
from datetime import datetime
import sqlite3

from utils.auto_id import generate_registration_id


DB_PATH = "database/database.db"


class StudentRegistration:

    def __init__(self, page):

        self.page = page


        self.registration_id = ft.TextField(
            label="Registration ID",
            value=generate_registration_id(),
            read_only=True
        )


        self.name = ft.TextField(
            label="Student Name"
        )


        self.phone = ft.TextField(
            label="Phone Number",
            keyboard_type=ft.KeyboardType.PHONE
        )


        self.address = ft.TextField(
            label="Address",
            multiline=True
        )


        self.course_type = ft.Dropdown(
            label="Course Type",
            options=[
                ft.dropdown.Option("Car"),
                ft.dropdown.Option("Bike"),
                ft.dropdown.Option("Car + Bike")
            ]
        )


        self.registration_fee = ft.TextField(
            label="Registration Fee",
            keyboard_type=ft.KeyboardType.NUMBER
        )


        self.payment_method = ft.Dropdown(
            label="Registration Payment Method",
            options=[
                ft.dropdown.Option("Cash"),
                ft.dropdown.Option("UPI"),
                ft.dropdown.Option("Google Pay"),
                ft.dropdown.Option("Bank")
            ]
        )


        self.total_fee = ft.TextField(
            label="Total Course Fee",
            keyboard_type=ft.KeyboardType.NUMBER
        )


        self.message = ft.Text()



    def save_student(self, e):

        if not self.name.value.strip():

            self.message.value = "Enter Student Name"

            self.message.color = "red"

            self.page.update()

            return


        if not self.phone.value.strip():

            self.message.value = "Enter Phone Number"

            self.message.color = "red"

            self.page.update()

            return


        if not self.course_type.value:

            self.message.value = "Select Course Type"

            self.message.color = "red"

            self.page.update()

            return


        if not self.total_fee.value or float(self.total_fee.value) <= 0:

            self.message.value = "Enter Valid Total Fee"

            self.message.color = "red"

            self.page.update()

            return


        try:

            conn = sqlite3.connect(DB_PATH)

            cursor = conn.cursor()


            now = datetime.now()


            registration_id = self.registration_id.value

            registration_fee = float(
                self.registration_fee.value or 0
            )

            total_fee = float(
                self.total_fee.value or 0
            )


            # Save Student

            cursor.execute(
                """
                INSERT INTO students
                (
                registration_id,
                registration_date,
                name,
                phone,
                address,
                course_type,
                registration_fee,
                registration_payment_method,
                total_fee,
                status,
                created_at,
                updated_at
                )

                VALUES(?,?,?,?,?,?,?,?,?,?,?,?)
                """,

                (

                registration_id,

                now.strftime("%Y-%m-%d"),

                self.name.value,

                self.phone.value,

                self.address.value,

                self.course_type.value,

                registration_fee,

                self.payment_method.value,

                total_fee,

                "ACTIVE",

                now.strftime("%Y-%m-%d %H:%M:%S"),

                now.strftime("%Y-%m-%d %H:%M:%S")

                )

            )


            # Automatic Registration Payment Entry

            if registration_fee > 0:


                cursor.execute(
                    """
                    INSERT INTO student_payments
                    (
                    registration_id,
                    payment_date,
                    payment_type,
                    amount,
                    payment_method,
                    remarks,
                    created_at
                    )

                    VALUES(?,?,?,?,?,?,?)
                    """,

                    (

                    registration_id,

                    now.strftime("%Y-%m-%d"),

                    "Registration Fee",

                    registration_fee,

                    self.payment_method.value,

                    "Initial Registration Fee",

                    now.strftime("%Y-%m-%d %H:%M:%S")

                    )

                )


            conn.commit()
            conn.close()

            if hasattr(self.page, "student_payment"):
                self.page.student_payment.load_students()

            if hasattr(self.page, "student_search"):
                self.page.student_search.load_students()

            self.message.value = "Student Saved Successfully"


            self.message.color = "green"

            # Refresh Dashboard

            if hasattr(self.page, "home"):

                 self.page.home.refresh_dashboard()


            self.registration_id.value = generate_registration_id()

            self.name.value = ""

            self.phone.value = ""

            self.address.value = ""

            self.course_type.value = None

            self.registration_fee.value = ""

            self.payment_method.value = None

            self.total_fee.value = ""



            self.page.update()



        except Exception as ex:


            try:
                conn.rollback()
                conn.close()
            except:
                pass


            self.message.value = str(ex)

            self.message.color = "red"

            self.page.update()



    def build(self):


        return ft.Container(

            padding=30,


            content=ft.Column(

                [

                ft.Text(
                    "Student Registration",
                    size=28,
                    weight=ft.FontWeight.BOLD
                ),


                self.registration_id,

                self.name,

                self.phone,

                self.address,

                self.course_type,

                self.registration_fee,

                self.payment_method,

                self.total_fee,


                ft.ElevatedButton(

                    "Save Student",

                    icon=ft.Icons.SAVE,

                    on_click=self.save_student

                ),


                self.message

                ],

                scroll=ft.ScrollMode.AUTO

            )

        )

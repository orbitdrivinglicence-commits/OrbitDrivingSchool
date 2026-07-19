import flet as ft
import sqlite3

from datetime import datetime


DB_PATH = "database/database.db"



class StudentPayment:


    def __init__(self, page):

        self.page = page


        self.registration_id = ""


        # -------------------------
        # Search Fields
        # -------------------------

        self.search_id = ft.TextField(

            label="Registration ID"

        )


        self.search_name = ft.TextField(

            label="Student Name"

        )



        # -------------------------
        # Student Dropdown
        # -------------------------

        self.student_dropdown = ft.Dropdown(

            label="Select Student",

            options=[]

        )


        self.student_dropdown.on_select = self.load_student



        # -------------------------
        # Student Details
        # -------------------------

        self.total_fee_text = ft.Text(

            "Total Fee : ₹0"

        )


        self.registration_fee_text = ft.Text(

            "Registration Fee : ₹0"

        )


        self.paid_text = ft.Text(

            "Paid Amount : ₹0"

        )


        self.balance_text = ft.Text(

            "Balance : ₹0"

        )



        # -------------------------
        # Payment Fields
        # -------------------------

        self.payment_type = ft.Dropdown(

            label="Payment Type",

            options=[

                ft.dropdown.Option("Course Fee"),

                ft.dropdown.Option("Registration Fee")

            ]

        )



        self.amount = ft.TextField(

            label="Payment Amount",

            keyboard_type=ft.KeyboardType.NUMBER

        )



        self.payment_method = ft.Dropdown(

            label="Payment Method",

            options=[

                ft.dropdown.Option("Cash"),

                ft.dropdown.Option("UPI"),

                ft.dropdown.Option("Bank")

            ]

        )



        self.remarks = ft.TextField(

            label="Remarks"

        )



        self.message = ft.Text()



        self.load_students()



    # -------------------------
    # Load Students Dropdown
    # -------------------------


    def load_students(self):


        conn = sqlite3.connect(DB_PATH)

        cursor = conn.cursor()



        cursor.execute(

            """

            SELECT registration_id,name

            FROM students

            ORDER BY name

            """

        )


        rows = cursor.fetchall()


        conn.close()



        for row in rows:


            self.student_dropdown.options.append(

                ft.dropdown.Option(

                    row[0],

                    text=f"{row[0]} - {row[1]}"

                )

            )

    # -------------------------
    # Search Student
    # -------------------------


    def search_student(self, e):


        conn = sqlite3.connect(DB_PATH)

        cursor = conn.cursor()



        search_id = self.search_id.value.strip()

        search_name = self.search_name.value.strip()



        if search_id:


            cursor.execute(

                """

                SELECT registration_id

                FROM students

                WHERE registration_id=?

                """,

                (

                    search_id,

                )

            )


        elif search_name:


            cursor.execute(

                """

                SELECT registration_id

                FROM students

                WHERE LOWER(name) LIKE LOWER(?)

                """,

                (

                    "%" + search_name + "%",

                )

            )


        else:


            conn.close()

            return



        row = cursor.fetchone()


        conn.close()



        if row:


            self.registration_id = row[0]


            self.student_dropdown.value = row[0]


            self.load_student(None)



            self.search_id.value = ""

            self.search_name.value = ""



            self.page.update()



        else:


            self.message.value = "Student Not Found"

            self.message.color = "red"


            self.page.update()





    # -------------------------
    # Load Selected Student
    # -------------------------


    def load_student(self, e):


        if not self.student_dropdown.value:

            return



        self.registration_id = self.student_dropdown.value



        conn = sqlite3.connect(DB_PATH)

        cursor = conn.cursor()



        cursor.execute(

            """

            SELECT registration_fee,total_fee

            FROM students

            WHERE registration_id=?

            """,

            (

                self.registration_id,

            )

        )


        student = cursor.fetchone()




        cursor.execute(

            """

            SELECT SUM(amount)

            FROM student_payments

            WHERE registration_id=?

            """,

            (

                self.registration_id,

            )

        )



        paid = cursor.fetchone()[0] or 0



        conn.close()




        if student:


            registration_fee = student[0] or 0


            total_fee = student[1] or 0



            total_paid = registration_fee + paid


            balance = total_fee - total_paid



            self.registration_fee_text.value = (

                f"Registration Fee : ₹{registration_fee}"

            )



            self.total_fee_text.value = (

                f"Total Fee : ₹{total_fee}"

            )



            self.paid_text.value = (

                f"Paid Amount : ₹{total_paid}"

            )



            self.balance_text.value = (

                f"Balance : ₹{balance}"

            )



            self.page.update()

    # -------------------------
    # Save Payment
    # -------------------------


    def save_payment(self, e):


        if not self.registration_id:


            self.message.value = "Select Student First"

            self.message.color = "red"

            self.page.update()

            return




        conn = sqlite3.connect(DB_PATH)

        cursor = conn.cursor()



        now = datetime.now()



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

                self.registration_id,

                now.strftime("%Y-%m-%d"),

                self.payment_type.value,

                float(self.amount.value or 0),

                self.payment_method.value,

                self.remarks.value,

                now.strftime("%Y-%m-%d %H:%M:%S")

            )

        )



        conn.commit()

        conn.close()




        self.message.value = "Payment Saved Successfully"

        self.message.color = "green"



        self.amount.value = ""

        self.remarks.value = ""



        self.load_student(None)



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

                    "Student Payment",

                    size=28,

                    weight=ft.FontWeight.BOLD

                ),



                # Search Options

                self.search_id,


                self.search_name,



                ft.ElevatedButton(

                    "Search",

                    icon=ft.Icons.SEARCH,

                    on_click=self.search_student

                ),



                ft.Divider(),



                # Existing Dropdown

                self.student_dropdown,



                self.registration_fee_text,


                self.total_fee_text,


                self.paid_text,


                self.balance_text,



                ft.Divider(),



                self.payment_type,


                self.amount,


                self.payment_method,


                self.remarks,



                ft.ElevatedButton(

                    "Save Payment",

                    icon=ft.Icons.SAVE,

                    on_click=self.save_payment

                ),



                self.message



                ],


                scroll=ft.ScrollMode.AUTO

            )

        )



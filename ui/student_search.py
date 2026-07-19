import flet as ft
import sqlite3
from ui.home import Home

DB_PATH = "database/database.db"


class StudentSearch:

    def __init__(self, page, change_screen, refresh_app):

        self.page = page

        self.change_screen = change_screen

        self.refresh_app = refresh_app

        self.edit_mode = False

        self.current_registration_id = None


        # -------------------------
        # Search Controls
        # -------------------------

        self.student_dropdown = ft.Dropdown(
            label="Select Student",
            options=[]
        )

        self.student_dropdown.on_select = self.dropdown_changed


        self.search_id = ft.TextField(
            label="Registration ID"
        )


        self.search_name = ft.TextField(
            label="Student Name"
        )


        # -------------------------
        # Edit Controls
        # -------------------------

        self.name_field = ft.TextField(
            label="Name",
            read_only=True
        )


        self.phone_field = ft.TextField(
            label="Phone",
            read_only=True
        )


        self.address_field = ft.TextField(
            label="Address",
            read_only=True
        )


        self.course_field = ft.TextField(
            label="Course Type",
            read_only=True
        )


        self.total_fee_field = ft.TextField(
            label="Total Fee",
            read_only=True
        )


        self.paid_fee_field = ft.TextField(
            label="Paid Fee",
            read_only=True
        )


        self.balance_field = ft.TextField(
            label="Balance",
            read_only=True
        )


        self.status_dropdown = ft.Dropdown(
            label="Status",
            options=[
                ft.dropdown.Option("ACTIVE"),
                ft.dropdown.Option("COMPLETED")
            ],
            disabled=True
        )


        self.edit_button = ft.ElevatedButton(
            "EDIT",
            icon=ft.Icons.EDIT,
            on_click=self.enable_edit
        )


        self.save_button = ft.ElevatedButton(
            "SAVE CHANGES",
            icon=ft.Icons.SAVE,
            on_click=self.save_changes,
            visible=False
        )


        self.result_area = ft.Column(
            scroll=ft.ScrollMode.AUTO
        )


        self.load_student_list()

    # -------------------------
    # Load Students
    # -------------------------

    def load_student_list(self):

        conn = sqlite3.connect(DB_PATH)

        cursor = conn.cursor()


        cursor.execute(
            """
            SELECT registration_id, name
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
    # Dropdown Changed
    # -------------------------

    def dropdown_changed(self, e):

        if self.student_dropdown.value:

            self.show_student_details(
                self.student_dropdown.value
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


        else:

            cursor.execute(

                """
                SELECT registration_id
                FROM students
                WHERE name LIKE ?
                """,

                (
                    "%" + search_name + "%",
                )

            )

        row = cursor.fetchone()


        conn.close()


        if row:

            self.show_student_details(
                row[0]
            )

            self.search_id.value = ""

            self.search_name.value = ""

            self.student_dropdown.value = None

            self.page.update()

        else:

            self.result_area.controls.clear()

            self.result_area.controls.append(

                ft.Text(
                    "Student Not Found",
                    color="red"
                )

            )

            self.page.update()



    # -------------------------
    # Show Student Details
    # -------------------------

    def show_student_details(self, registration_id):

        self.current_registration_id = registration_id


        conn = sqlite3.connect(DB_PATH)

        cursor = conn.cursor()


        cursor.execute(
            """
            SELECT
            registration_id,
            registration_date,
            name,
            phone,
            address,
            course_type,
            registration_fee,
            total_fee,
            status

            FROM students

            WHERE registration_id=?
            """,

            (registration_id,)

        )


        student = cursor.fetchone()



        cursor.execute(
            """
            SELECT
            payment_date,
            payment_type,
            amount,
            payment_method,
            remarks

            FROM student_payments

            WHERE registration_id=?

            ORDER BY payment_id DESC
            """,

            (registration_id,)

        )


        payments = cursor.fetchall()


        conn.close()


        if not student:

            return



        registration_fee = student[6] or 0


        paid_amount = registration_fee


        for payment in payments:

            paid_amount += payment[2]



        total_fee = student[7] or 0


        balance = total_fee - paid_amount



        # Fill Edit Fields

        self.name_field.value = student[2]

        self.phone_field.value = student[3]

        self.address_field.value = student[4]

        self.course_field.value = student[5]

        self.total_fee_field.value = str(total_fee)

        self.paid_fee_field.value = str(paid_amount)

        self.balance_field.value = str(balance)

        self.status_dropdown.value = student[8]



        self.result_area.controls.clear()


        self.result_area.controls.append(

            ft.Container(

                padding=20,

                border_radius=15,

                bgcolor="white",

                content=ft.Column(

                    [

                        ft.Text(

                            "Student Details",

                            size=22,

                            weight=ft.FontWeight.BOLD

                        ),


                        ft.Text(

                            f"Registration ID : {student[0]}"

                        ),


                        self.name_field,

                        self.phone_field,

                        self.address_field,

                        self.course_field,

                        self.total_fee_field,

                        self.paid_fee_field,

                        self.balance_field,

                        self.status_dropdown,


                        ft.Row(

                            [

                                self.edit_button,

                                self.save_button

                            ]

                        )

                    ]

                )

            )

        )


        self.page.update()

    # -------------------------
    # Enable Edit Mode
    # -------------------------

    def enable_edit(self, e):

        self.edit_mode = True


        self.name_field.read_only = False

        self.phone_field.read_only = False

        self.address_field.read_only = False

        self.course_field.read_only = False

        self.total_fee_field.read_only = False

        self.paid_fee_field.read_only = False


        self.status_dropdown.disabled = False


        self.edit_button.visible = False

        self.save_button.visible = True


        self.page.update()



    # -------------------------
    # Save Changes
    # -------------------------

    def save_changes(self, e):

        if not self.current_registration_id:

            return



        try:

            total_fee = float(
                self.total_fee_field.value
            )


            paid_fee = float(
                self.paid_fee_field.value
            )


        except:

            return



        balance = total_fee - paid_fee


        conn = sqlite3.connect(DB_PATH)

        cursor = conn.cursor()



        cursor.execute(

            """

            UPDATE students

            SET

            name=?,

            phone=?,

            address=?,

            course_type=?,

            total_fee=?,

            status=?

            WHERE registration_id=?

            """,

            (

                self.name_field.value,

                self.phone_field.value,

                self.address_field.value,

                self.course_field.value,

                total_fee,

                self.status_dropdown.value,

                self.current_registration_id

            )

        )


        conn.commit()

        conn.close()



        # Return to view mode

        self.name_field.read_only = True

        self.phone_field.read_only = True

        self.address_field.read_only = True

        self.course_field.read_only = True

        self.total_fee_field.read_only = True

        self.paid_fee_field.read_only = True


        self.balance_field.value = str(balance)


        self.status_dropdown.disabled = True


        self.edit_button.visible = True

        self.save_button.visible = False


        self.page.snack_bar = ft.SnackBar(

            ft.Text(
                "Student Updated Successfully"
            )

        )

        self.page.snack_bar.open = True


        self.page.update()

        self.change_screen(
           Home(
               self.page,
               self.change_screen,
               self.refresh_app
           ).build()
        )


    # -------------------------
    # Build Page
    # -------------------------

    def build(self):

        return ft.Container(

            padding=30,

            content=ft.Column(

                [

                    ft.Text(

                        "Student Search",

                        size=28,

                        weight=ft.FontWeight.BOLD

                    ),



                    self.student_dropdown,


                    ft.Divider(),


                    self.search_id,


                    self.search_name,



                    ft.ElevatedButton(

                        "Search",

                        icon=ft.Icons.SEARCH,

                        on_click=self.search_student

                    ),



                    ft.Divider(),


                    self.result_area


                ],

                scroll=ft.ScrollMode.AUTO

            )

        )



import flet as ft


from ui.expenses import Expenses
from ui.student_payment import StudentPayment
from ui.student_registration import StudentRegistration
from ui.student_search import StudentSearch
from ui.incomes import Income


from screens.daily_report import DailyReport
from screens.monthly_report import MonthlyReport
from screens.yearly_report import YearlyReport
from screens.report_search import ReportSearch
from screens.backup_restore import BackupRestore



from utils.theme import (

    APP_NAME,

    DEVELOPER,

    PRIMARY_COLOR

)

home = None


def main(page: ft.Page):


    # -----------------------------
    # Window Configuration
    # -----------------------------


    page.title = APP_NAME


    page.theme_mode = ft.ThemeMode.LIGHT


    page.window_width = 1200


    page.window_height = 750


    page.padding = 0


    page.bgcolor = "#F7F7F7"





    # -----------------------------
    # Main Content Area
    # -----------------------------


    content_area = ft.Container(


        expand=True,


        bgcolor="#F7F7F7"


    )

    current_screen = None



    # -----------------------------
    # Screen Change Handler
    # -----------------------------


    def change_screen(screen):

        nonlocal current_screen

        current_screen = screen

        content_area.content = screen

        page.update()


    def refresh_app():

        page.update()


    # -----------------------------
    # Top Bar
    # -----------------------------

    def top_bar():

        return ft.Container(

            height=75,

            bgcolor="#121212",

            padding=10,

            content=ft.Row(

                [

                    ft.Image(

                        src="images/logo.png",

                        width=55,

                        height=55,

                    ),


                    ft.Column(

                        [

                            ft.Text(

                                "ORBIT DRIVING SCHOOL",

                                size=22,

                                weight=ft.FontWeight.BOLD,

                                color="white"

                            ),


                            ft.Text(

                                "Driving School Management System",

                                size=12,

                                color="#BBBBBB"

                            )

                        ],

                        spacing=0,

                        alignment=ft.MainAxisAlignment.CENTER

                    ),


                    ft.Container(

                        expand=True

                    ),


                    ft.IconButton(

                        icon=ft.Icons.REFRESH,

                        icon_color="white",

                        tooltip="Refresh App",

                        on_click=lambda e: refresh_app()

                    )

                ],

                vertical_alignment=ft.CrossAxisAlignment.CENTER

            )

        )


    # -----------------------------
    # Navigation Button
    # -----------------------------


    def nav_button(title, icon, screen):


        return ft.ElevatedButton(


            content=ft.Row(

                [

                    ft.Icon(icon),


                    ft.Text(

                        title,

                        expand=True,

                        overflow=ft.TextOverflow.VISIBLE

                    )

                ],


                alignment=ft.MainAxisAlignment.START

            ),



            width=320,


            height=45,



            style=ft.ButtonStyle(


                color="white",


                bgcolor=PRIMARY_COLOR


            ),



            on_click=lambda e:

            change_screen(screen)


        )





    # -----------------------------
    # Reports Menu
    # -----------------------------


    def reports_menu():


        return ft.Container(


            padding=30,


            content=ft.Column(


                [


                    ft.Text(


                        "Reports",


                        size=30,


                        weight=ft.FontWeight.BOLD


                    ),



                    ft.ElevatedButton(


                        "Daily Report",


                        icon=ft.Icons.TODAY,


                        on_click=lambda e:

                        change_screen(

                            DailyReport(page).build()

                        )


                    ),




                    ft.ElevatedButton(


                        "Monthly Report",


                        icon=ft.Icons.CALENDAR_MONTH,


                        on_click=lambda e:

                        change_screen(

                            MonthlyReport(page).build()

                        )


                    ),




                    ft.ElevatedButton(


                        "Yearly Report",


                        icon=ft.Icons.INSERT_CHART,


                        on_click=lambda e:

                        change_screen(

                            YearlyReport(page).build()

                        )


                    ),


                    ft.ElevatedButton(

                        "Report Search",

                        icon=ft.Icons.SEARCH,

                        on_click=lambda e:

                        change_screen(

                            ReportSearch(page).build()

                        )


                    )


                ]


            )


        )


    # -----------------------------
    # Home Screen
    # -----------------------------


    try:


        from ui.home import Home

        global home

        home = Home(

            page,

            change_screen,

            refresh_app

        )

        page.home = home

        home_screen = home.build()



    except Exception as e:


        print(

            "HOME ERROR:",

            e

        )



        home_screen = ft.Container(


            expand=True,


            content=ft.Text(


                str(e),


                size=18


            )


        )






    # -----------------------------
    # Sidebar
    # -----------------------------


    sidebar = ft.Container(


        width=250,


        bgcolor="white",


        padding=20,



        content=ft.Column(


            [



                ft.Divider(),





                nav_button(


                    "DASHBOARD",


                    ft.Icons.DASHBOARD,

                    Home(
                        page,
                        change_screen,
                        refresh_app
                    ).build()

                ),




                nav_button(


                    "STUDENT REGISTRATION",


                    ft.Icons.PERSON,


                    StudentRegistration(page).build()


                ),




                nav_button(


                    "ADD STUDENT'S PAYMENT",


                    ft.Icons.MONEY,


                    StudentPayment(page).build()


                ),




                nav_button(


                    "SEARCH STUDENT'S DETAILS",


                    ft.Icons.SEARCH,

                    StudentSearch(

                        page,

                        change_screen,

                        refresh_app

                    ).build()


                ),




                nav_button(


                    "ADD INCOMES",


                    ft.Icons.ADD_CIRCLE,


                    Income(page).build()


                ),




                nav_button(


                    "ADD EXPENSES",


                    ft.Icons.REMOVE_CIRCLE,


                    Expenses(page).build()


                ),



                nav_button(


                    "REPORTS",


                    ft.Icons.INSERT_CHART,


                    reports_menu()


                ),


                  nav_button(

                      "BACKUP & RESTORE",

                      ft.Icons.BACKUP,

                      BackupRestore(page).build()

                  ),


                ft.Container(


                    expand=True


                ),




                ft.Text(


                    f"Developer\n{DEVELOPER}",


                    size=12,


                    color="#777777"


                )


            ],


            scroll=ft.ScrollMode.AUTO,

            expand=True


        )


    )

    # -----------------------------
    # Main Layout
    # -----------------------------


    content_area.content = home_screen


    page.add(

        ft.Column(

            [

                top_bar(),

                ft.Row(

                    [

                        sidebar,

                        ft.VerticalDivider(

                            width=1

                        ),

                        content_area

                    ],

                    expand=True

                )

            ],

            expand=True,

            spacing=0

        )

    )

# -----------------------------
# Application Start
# -----------------------------

if __name__ == "__main__":

    ft.run(

        main,

        assets_dir="assets"

    )

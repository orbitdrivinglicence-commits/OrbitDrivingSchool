import flet as ft

from utils.theme import PRIMARY_COLOR

from utils.backup import (
    create_backup,
    list_backups,
    restore_backup
)


class BackupRestore:

    def __init__(self, page):

        self.page = page

        self.selected_backup = None

        self.status = ft.Text(
            "",
            color="green"
        )

        self.backup_list = ft.Column(
            spacing=10
        )


    # -----------------------------
    # Select Backup
    # -----------------------------

    def select_backup(self, backup_name):

        self.selected_backup = backup_name

        self.status.value = (
            f"Selected Backup: {backup_name}"
        )

        self.status.color = PRIMARY_COLOR

        self.load_backups()



    # -----------------------------
    # Load Backup List
    # -----------------------------

    def load_backups(self):

        self.backup_list.controls.clear()


        backups = list_backups()


        if not backups:

            self.backup_list.controls.append(

                ft.Text(
                    "No Backup Found"
                )

            )


        else:

                    for backup in backups:


                        self.backup_list.controls.append(

                            ft.Container(

                                padding=10,

                                bgcolor="white",

                                border_radius=10,


                                content=ft.Row(

                                    [

                                        ft.Checkbox(

                                            value=(

                                                self.selected_backup == backup

                                            ),


                                            on_change=lambda e, b=backup:

                                                self.select_backup(b)

                                        ),



                                        ft.Text(

                                            backup,

                                            size=16

                                        )

                                    ]

                                )

                            )

                        )


        self.page.update()



    # -----------------------------
    # Create Backup
    # -----------------------------

    def backup_now(self, e=None):

        try:

            file_path = create_backup()


            self.status.value = (

                f"Backup Created Successfully\n{file_path}"

            )

            self.status.color = "green"


            self.load_backups()



        except Exception as ex:


            self.status.value = (

                f"Backup Failed: {ex}"

            )

            self.status.color = "red"


        self.page.update()

    # -----------------------------
    # Restore Selected Backup
    # -----------------------------

    def restore_selected(self, e=None):

        try:

            if not self.selected_backup:

                self.status.value = (

                    "Please select a backup first"

                )

                self.status.color = "red"

                self.page.update()

                return



            result = restore_backup(

                self.selected_backup

            )


            if result:

                self.status.value = (

                    "Backup Restored Successfully"

                )

                self.status.color = "green"


            else:

                self.status.value = (

                    "Backup Restore Failed"

                )

                self.status.color = "red"



        except Exception as ex:


            self.status.value = (

                f"Restore Error: {ex}"

            )

            self.status.color = "red"



        self.page.update()



    # -----------------------------
    # Build UI
    # -----------------------------

    def build(self):

        self.load_backups()


        return ft.Container(

            expand=True,

            padding=30,

            bgcolor="#F7F7F7",


            content=ft.Column(

                [

                    ft.Text(

                        "Backup & Restore",

                        size=30,

                        weight=ft.FontWeight.BOLD,

                        color=PRIMARY_COLOR

                    ),


                    ft.Divider(),



                    ft.ElevatedButton(

                        "Create Backup",

                        icon=ft.Icons.BACKUP,

                        on_click=self.backup_now

                    ),



                    self.status,



                    ft.Text(

                        "Available Backups",

                        size=20,

                        weight=ft.FontWeight.BOLD

                    ),



                    ft.Container(

                        height=300,

                        bgcolor="white",

                        border_radius=10,

                        padding=10,

                        content=ft.ListView(

                            controls=self.backup_list.controls,

                            spacing=5

                        )

                    ),



                    ft.ElevatedButton(

                        "Restore Selected Backup",

                        icon=ft.Icons.RESTORE,

                        on_click=self.restore_selected

                    )

                ],

                scroll=ft.ScrollMode.AUTO

            )

        )



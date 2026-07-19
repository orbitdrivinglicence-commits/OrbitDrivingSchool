"""
=========================================================
ORBIT DRIVING SCHOOL MANAGEMENT SYSTEM

PDF Report Generator

Framework : Flet
Database  : SQLite
PDF       : ReportLab
Mode      : Offline

Developer : AMAL THIRUTHOOR
=========================================================
"""


import os
import platform
import subprocess

from datetime import datetime

from reportlab.lib.pagesizes import A4

from reportlab.platypus import (

    SimpleDocTemplate,

    Paragraph,

    Spacer,

    Table,

    TableStyle

)

from reportlab.lib.styles import getSampleStyleSheet

from reportlab.lib.styles import ParagraphStyle

from reportlab.lib import colors

from reportlab.lib.enums import TA_CENTER

from reportlab.platypus import Image


# -------------------------
# Report Folder
# -------------------------


BASE_DIR = os.path.dirname(

    os.path.dirname(

        os.path.abspath(__file__)

    )

)



REPORT_FOLDER = os.path.join(

    BASE_DIR,

    "reports"

)



os.makedirs(

    REPORT_FOLDER,

    exist_ok=True

)


LOGO_PATH = os.path.join(

    BASE_DIR,

    "assets",

    "images",

    "logo.png"

)



class PDFReport:


    def __init__(self):


        self.styles = getSampleStyleSheet()

        self.styles["Title"].alignment = TA_CENTER

        self.styles["Heading2"].alignment = TA_CENTER

        self.developer_style = ParagraphStyle(

            "Developer",

            parent=self.styles["Normal"],

            fontSize=8,

            alignment=TA_CENTER

        )

    # -------------------------
    # Student PDF
    # -------------------------

    def create_student_pdf(self, student_data):


        file_name = (

            "student_"

            + datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )

            + ".pdf"

        )


        file_path = os.path.join(

            REPORT_FOLDER,

            file_name

        )


        pdf = SimpleDocTemplate(

            file_path,

            pagesize=A4

        )


        content = []


        content.append(

            Paragraph(

                "ORBIT DRIVING SCHOOL",

                self.styles["Title"]

            )

        )


        content.append(

            Paragraph(

                "Driving School Management System",

                self.styles["Heading2"]

            )

        )


        content.append(

            Paragraph(

                "Developer : AMAL THIRUTHOOR",

                self.styles["Normal"]

            )

        )


        content.append(

            Spacer(

                1,

                20

            )

        )



        for key, value in student_data.items():


            content.append(

                Paragraph(

                    f"{key} : {value}",

                    self.styles["Normal"]

                )

            )


            content.append(

                Spacer(

                    1,

                    8

                )

            )


        pdf.build(content)


        return file_path




    # -------------------------
    # General Report PDF
    # -------------------------


    def create_report_pdf(

            self,

            report_title,

            report_date,

            income,

            expense,

            balance,

            transactions

    ):



        file_name = (

            report_title.replace(

                " ",

                "_"

            )

            +

            "_"

            +

            datetime.now().strftime(

                "%Y%m%d_%H%M%S"

            )

            +

            ".pdf"

        )



        file_path = os.path.join(

            REPORT_FOLDER,

            file_name

        )



        pdf = SimpleDocTemplate(

            file_path,

            pagesize=A4

        )


        content = []

        if os.path.exists(LOGO_PATH):

            content.append(

                Image(

                    LOGO_PATH,

                    width=80,

                    height=80

                )

            )

            content.append(

                Spacer(

                    1,

                    10

                )

            )

        content.append(

            Paragraph(

                "ORBIT DRIVING SCHOOL",

                self.styles["Title"]

            )

        )

        content.append(

            Paragraph(

                "Driving School Management System",

                self.styles["Heading2"]

            )

        )

        content.append(

            Paragraph(

                "DEVELOPED BY  AMAL THIRUTHOOR",

                self.developer_style

            )

        )

        content.append(

            Spacer(

                1,

                15

            )

        )


        content.append(

            Paragraph(

                f"{report_title}",

                self.styles["Heading2"]

            )

        )



        content.append(

            Paragraph(

                f"Date : {report_date}",

                self.styles["Normal"]

            )

        )



        content.append(

            Spacer(

                1,

                15

            )

        )



        summary_data = [

            [

                "Total Income",

                f"₹ {income}"

            ],

            [

                "Total Expense",

                f"₹ {expense}"

            ],

            [

                "Balance",

                f"₹ {balance}"

            ]

        ]


        summary_table = Table(

            summary_data,

            colWidths=[170, 170],

            hAlign="CENTER"

        )


        summary_table.setStyle(

            TableStyle(

                [

                    (

                        "GRID",

                        (0,0),

                        (-1,-1),

                        0.5,

                        colors.black

                    ),

                    (

                        "ALIGN",

                        (0,0),

                        (-1,-1),

                        "CENTER"

                    ),

                    (

                        "BACKGROUND",

                        (0,0),

                        (-1,0),

                        colors.lightgrey

                    )

                ]

            )

        )


        content.append(

            summary_table

        )


        content.append(

            Spacer(

                1,

                20

            )

        )



        # -------------------------
        # Transaction Table
        # -------------------------


        table_data = [

            [

                "Date",

                "Type",

                "Amount",

                "Payment",

                "Remarks"

            ]

        ]



        for row in transactions:


            table_data.append(row)



        transaction_table = Table(

            table_data,

            repeatRows=1,

            hAlign="CENTER"

        )



        transaction_table.setStyle(

            TableStyle(

                [

                    (

                        "GRID",

                        (0,0),

                        (-1,-1),

                        0.5,

                        colors.black

                    ),


                    (

                        "BACKGROUND",

                        (0,0),

                        (-1,0),

                        colors.lightgrey

                    ),


                    (


                       "ALIGN",

                        (0,0),

                        (-1,-1),

                        "CENTER"

                    )

                ]

            )

        )


        content.append(

            transaction_table

        )



        content.append(

            Spacer(

                1,

                20

            )

        )



        content.append(

            Paragraph(

                "Generated by ORBIT DRIVING SCHOOL",

                self.styles["Normal"]

            )

        )



        pdf.build(

            content

        )


        return file_path




    # -------------------------
    # Print PDF
    # -------------------------


    def print_pdf(

            self,

            file_path

    ):


        try:


            system = platform.system()



            if system == "Windows":


                os.startfile(

                    file_path,

                    "print"

                )



            elif system == "Linux":


                subprocess.run(

                    [

                        "lp",

                        file_path

                    ]

                )



            else:


                subprocess.run(

                    [

                        "xdg-open",

                        file_path

                    ]

                )


            return True



        except Exception:


            return False



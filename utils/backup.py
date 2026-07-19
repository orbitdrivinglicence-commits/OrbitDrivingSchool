import os
import shutil
from datetime import datetime


DB_PATH = "database/database.db"

BACKUP_FOLDER = "backup"



def create_backup():

    if not os.path.exists(BACKUP_FOLDER):

        os.makedirs(BACKUP_FOLDER)


    timestamp = datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S"
    )


    backup_file = os.path.join(

        BACKUP_FOLDER,

        f"backup_{timestamp}.db"

    )


    shutil.copy2(

        DB_PATH,

        backup_file

    )


    cleanup_old_backups()


    return backup_file





def list_backups():

    if not os.path.exists(BACKUP_FOLDER):

        return []


    backups = []


    for file in os.listdir(BACKUP_FOLDER):

        if file.endswith(".db"):

            backups.append(file)


    backups.sort(reverse=True)


    return backups





def cleanup_old_backups():

    backups = list_backups()


    if len(backups) > 3:


        old_backups = backups[3:]


        for backup in old_backups:


            backup_file = os.path.join(

                BACKUP_FOLDER,

                backup

            )


            if os.path.exists(backup_file):

                os.remove(backup_file)





def restore_backup(backup_name):

    backup_file = os.path.join(

        BACKUP_FOLDER,

        backup_name

    )


    if not os.path.exists(backup_file):

        return False


    shutil.copy2(

        backup_file,

        DB_PATH

    )


    return True

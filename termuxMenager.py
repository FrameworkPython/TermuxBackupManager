import os
import asyncio
import subprocess

class Color:
   GREEN = '\033[92m'
   RED = '\033[91m'
   END = '\033[0m'

class BackupManager:
    def __init__(self, source_dir, backup_file):
        self.source_dir = source_dir
        self.backup_file = backup_file

    async def backup_data(self):
        cmd = ["tar", "-cvf", self.backup_file, "."]
        process = await asyncio.create_subprocess_exec(*cmd, cwd=self.source_dir)
        await process.communicate()
        if process.returncode == 0:
            print(Color.GREEN + "Backup successful." + Color.END)
        else:
            print(Color.RED + "Backup failed." + Color.END)

    async def restore_data(self):
        cmd = ["tar", "-xvf", self.backup_file, "-C", self.source_dir]
        process = await asyncio.create_subprocess_exec(*cmd)
        await process.communicate()
        if process.returncode == 0:
            print(Color.GREEN + "Data restoration successful." + Color.END)
        else:
            print(Color.RED + "Data restoration failed." + Color.END)

async def main():
    source_dir = "/data/data/com.termux"
    backup_file = input("Enter the path where you want to store the backup (default is /sdcard/termux_backup.tar): ")
    if not backup_file:
        backup_file = "/sdcard/termux_backup.tar"
        print("No path entered. The backup will be stored at /sdcard/termux_backup.tar by default.")
    backup_manager = BackupManager(source_dir, backup_file)
    while True:
        print("1. Backup data")
        print("2. Restore data")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            await backup_manager.backup_data()
        elif choice == '2':
            restore_file = input("Enter the path of the backup file you want to restore (default is /sdcard/termux_backup.tar): ")
            if not restore_file:
                restore_file = "/sdcard/termux_backup.tar"
                print("No path entered. The backup will be restored from /sdcard/termux_backup.tar by default.")
            backup_manager.backup_file = restore_file
            await backup_manager.restore_data()
        elif choice == '3':
            break
        else:
            print(Color.RED + "Invalid choice. Please try again." + Color.END)

if __name__ == "__main__":
    asyncio.run(main())

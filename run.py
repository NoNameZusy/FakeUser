import os
import time
import shutil
import subprocess
from colorama import Fore, Style, init

def main():
    # Dosya yolları
    current_dir = os.path.dirname(os.path.abspath(__file__))
    source_file = os.path.join(current_dir, "files", "fake_user.py")
    target_file = "/usr/local/bin/FakeUser"

    try:
        shutil.copy2(source_file, target_file)
        time.sleep(2)
        print(Fore.LIGHTBLUE_EX +  Style.BRIGHT + "\n[COPYING]" + Fore.WHITE + f" Copied {source_file} to {target_file}")

        subprocess.run(["chmod", "+x", target_file], check=True)
        time.sleep(2.5)
        print(Fore.LIGHTRED_EX + "\n[COMMAND]" + Fore.WHITE + f" Executed chmod +x {target_file}")

        # 2 saniye bekle
        time.sleep(2)

        # Komut satırına çıktıyı yazdır
        print("\nRun command :\n\n$ : " + Fore.LIGHTBLUE_EX + "FakeUser" + Fore.LIGHTGREEN_EX + " -h\n" + Fore.WHITE)

        # FakeUser komutunu çalıştır
        subprocess.run(["FakeUser", "-h"])
        print(Style.RESET_ALL + "")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

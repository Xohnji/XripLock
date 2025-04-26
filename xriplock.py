import pyzipper
import rarfile
import os
import threading
import time
from colorama import Fore, Style, init # aesthetic purposes only
init(autoreset=True)

# for_zip
def cracking_zip(zip_file, wordlist, start_line=0, end_line=None):
    with pyzipper.AESZipFile(zip_file) as zipfile:
        test_file = zipfile.namelist()[0]
        with open(wordlist, 'r', encoding='UTF-8', errors='ignore') as file:
            passes_list = file.readlines()[start_line:end_line]
            for password in passes_list:
                password = password.strip()
                try:
                    zipfile.read(test_file, pwd=password.encode('UTF-8'))
                    time.sleep(0.1)
                    print(Fore.YELLOW + f"[+] Valid: {password}")
                    return password
                except:
                    time.sleep(0.1)
                    print(Fore.LIGHTRED_EX + f"[~] Invalid: {password[:100]}", end="\n")
    return None

# for_rar
def cracking_rar(rar_file, wordlist, start_line=0, end_line=None):
    with rarfile.RarFile(rar_file) as rf:
        test_file = rf.namelist()[0]
        with open(wordlist, 'r', encoding='UTF-8', errors='ignore') as file:
            passes_list = file.readlines()[start_line:end_line]
            for password in passes_list:
                password = password.strip()
                try:
                    rf.read(test_file, pwd=password.encode('utf-8'))
                    print(Fore.YELLOW + f"[+] Valid: {password}")
                    return password
                except:
                    print(Fore.LIGHTRED_EX + f"[~] Invalid: {password[:100]}", end="\n")
    return None



print(
    Fore.BLUE + "██╗  ██╗██████╗ ██╗██████╗ ██╗      ██████╗  ██████╗██╗  ██╗" + "\n" +
    Fore.LIGHTBLUE_EX + "╚██╗██╔╝██╔══██╗██║██╔══██╗██║     ██╔═══██╗██╔════╝██║ ██╔╝" + "\n" +
    Fore.CYAN + " ╚███╔╝ ██████╔╝██║██████╔╝██║     ██║   ██║██║     █████╔╝ " + "\n" +
    Fore.LIGHTBLUE_EX + " ██╔██╗ ██╔══██╗██║██╔═══╝ ██║     ██║   ██║██║     ██╔═██╗ " + "\n" +
    Fore.BLUE + "██╔╝ ██╗██║  ██║██║██║     ███████╗╚██████╔╝╚██████╗██║  ██╗" + "\n" +
    Fore.BLUE + "╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝     ╚══════╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝" +
    Style.RESET_ALL
)




def main_cracking_process():
    print(Fore.LIGHTBLUE_EX + "        🔓 By Xohnji — (ZIP/RAR) Password Cracker 🔓")
    print("\n")

    while True:
        archive_file_path = input(Fore.LIGHTYELLOW_EX + "Enter the file path (zip/rar): " + Style.RESET_ALL).strip('"')
        if os.path.exists(archive_file_path):
            if archive_file_path.lower().endswith(('.zip', '.rar')):
                time.sleep(0.5)
                print(Fore.LIGHTCYAN_EX + "\n[+] File imported!\n")
                break
            else:
                print(Fore.LIGHTRED_EX + "\n[!] Invalid File Input.\n")
        else:
            print(Fore.LIGHTRED_EX + "\n[!] Invalid File Input.\n")

    while True:
        wordlist_file_path = input(Fore.LIGHTYELLOW_EX + "Enter wordlist path: " + Style.RESET_ALL).strip('"')
        if os.path.exists(wordlist_file_path) and wordlist_file_path.lower().endswith('.txt'):
            time.sleep(0.5)
            print(Fore.LIGHTCYAN_EX + "\n[+] Wordlist imported!\n")
            break
        else:
            print(Fore.LIGHTRED_EX + "\n[!] Invalid Wordlist.\n")

    while True:
        try:
            threads = int(input(Fore.LIGHTYELLOW_EX + "Threads [1-5] (recommended: 1): " + Style.RESET_ALL))
            if 1 <= threads <= 5:
                print(Fore.CYAN + r"""
    -------------------------
      >>> Brute-Forcing <<<
    -------------------------""")
                break
        except ValueError:
            print(Fore.LIGHTRED_EX + "[!] Invalid Input Thread." + Style.RESET_ALL)


# THREADS OPERATION (look messy, idk how i coded this, but trust me it works :> )
    with open(wordlist_file_path, 'r', encoding='UTF-8', errors='ignore') as file:
        total_lines = len(file.readlines())
    threads_lines = total_lines // threads

    passwords_storage = []
    threads_storage = []

    def with_thrds(target_file_archive, archive_file_path, wordlist_file_path, begin_t, end_t, passwords_storage):
        result = target_file_archive(archive_file_path, wordlist_file_path, begin_t, end_t)
        if result:
            passwords_storage.append(result)

    target_file_archive = cracking_zip if archive_file_path.lower().endswith('.zip') else cracking_rar

    for i in range(threads):
        begin_t = i * threads_lines
        end_t = (i + 1) * threads_lines if i != threads - 1 else total_lines

        thrds = threading.Thread(
            target=with_thrds,
            args=(target_file_archive, archive_file_path, wordlist_file_path, begin_t, end_t, passwords_storage)
        )

        threads_storage.append(thrds)
        thrds.start()
    
    for thrds in threads_storage:
        thrds.join()


    # checks if password is found correctly
    if passwords_storage:
        print(Fore.LIGHTGREEN_EX + f"\n[+] Password Found: {passwords_storage[0]}")
    else:
        print(Fore.RED + "\n[!] Password Not Found.")

if __name__ == "__main__":
    main_cracking_process()

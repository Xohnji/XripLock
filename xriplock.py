import subprocess
import pyzipper
import os
import threading
import time
import sys
from colorama import Fore, Style, init # aesthetic purposes only
init(autoreset = True)
gateway_exit = False # This will not gonna work once the threads start processing; it's either wait till the password cracks or wait for nothing.
invalid_attempts_counter = 0
invalid_attempts_LockedIn = threading.Lock()

# DISCLAIMER: If you don't trust this code, just use 'John the Ripper' Even I don't trust this lol.

# for_zip_set
def cracking_dat_zip(zip_file, wordlist, start_line=0, end_line=None):
    global invalid_attempts_counter
    with pyzipper.AESZipFile(zip_file) as zipfile:
        reader_file = zipfile.namelist()[0]
        with open(wordlist, 'r', encoding='UTF-8', errors='ignore') as file:
            passes_list = file.readlines()[start_line:end_line]
            for password in passes_list:
                if gateway_exit:
                    sys.exit(0)
                password = password.strip()
                try:
                    zipfile.read(reader_file, pwd=password.encode('UTF-8'))
                    print(Fore.LIGHTCYAN_EX + f"[+] Valid: {password}")
                    return password
                except:
                    with invalid_attempts_LockedIn:
                        invalid_attempts_counter += 1
                    print(Fore.LIGHTRED_EX + f"[~] Invalid: {password[:100]}", end="\n")
    return None


# for_rar_set
# RAR doesn't use pyzipper, which is sucks, so that's why cracking RAR is slow as hell compared to ZIP.
# Plus this is written in Python what do you expect lol.
def cracking_dat_rar(rar_file, wordlist, start_line=0, end_line=None):
    global invalid_attempts_counter
    with open(wordlist, 'r', encoding='UTF-8', errors='ignore') as file:
        passes_list = file.readlines()[start_line:end_line]
        for password in passes_list:
            if gateway_exit:
                sys.exit(0)
            password = password.strip()

            # I don't trust 'import unrar' because it's very broken. RAR4 & RAR5 have problem with each other.
            # So I decided to just execute the unrar program command directly using 'subprocess'
            # The UnRAR external program will then execute the command outside the script and then deliver the output into this script.  
            try:
                result = subprocess.run(
                    ['unrar', 't', '-p' + password, rar_file],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE
                )
                if result.returncode == 0:
                    print(Fore.LIGHTCYAN_EX + f"[+] Valid: {password}")
                    return password
                else:
                    with invalid_attempts_LockedIn:
                        invalid_attempts_counter += 1
                    print(Fore.LIGHTRED_EX + f"[~] Invalid: {password[:100]}", end="\n")
            except Exception as e:
                with invalid_attempts_LockedIn:
                    invalid_attempts_counter += 1
                print(Fore.LIGHTRED_EX + f"[!] Error: {str(e)}", end="\n")
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
    global invalid_attempts_counter
    invalid_attempts_counter = 0
    print(Fore.LIGHTBLUE_EX + "        🔓 By Xohnji — (ZIP/RAR) Password Cracker 🔓")
    print("\n")


    while True:
        try:
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
        except KeyboardInterrupt:
            print(Fore.LIGHTRED_EX + "\nTerminating... [2s]")
            time.sleep(2)
            sys.exit(0)


    while True:
        try:
            wordlist_file_path = input(Fore.LIGHTYELLOW_EX + "Enter wordlist path: " + Style.RESET_ALL).strip('"')
            if os.path.exists(wordlist_file_path) and wordlist_file_path.lower().endswith('.txt'):
                time.sleep(0.5)
                print(Fore.LIGHTCYAN_EX + "\n[+] Wordlist imported!\n")
                break
            else:
                print(Fore.LIGHTRED_EX + "\n[!] Invalid Wordlist.\n")
        except KeyboardInterrupt:
            print(Fore.LIGHTRED_EX + "\nTerminating... [2s]")
            time.sleep(2)
            sys.exit(0)


    while True:
        try:
            threads = int(input(Fore.LIGHTYELLOW_EX + "Threads [1-5] (recommended: 1): " + Style.RESET_ALL))
            if 1 <= threads <= 5:
                print(Fore.CYAN + r"""
    -------------------------
      >>> Brute-Forcing <<<
    -------------------------
          please wait...""")
                break
        except ValueError:
            print(Fore.LIGHTRED_EX + "[!] Invalid Input Thread." + Style.RESET_ALL)
        except KeyboardInterrupt:
            print(Fore.LIGHTRED_EX + "\nTerminating... [2s]")
            time.sleep(2)
            sys.exit(0)
    Process_Timer = time.time()

# THREADS OPERATION (look messy, idk how i coded this, but trust me it works :> )

    # The more larger the wordlist the more slower for it to starts cracking because it need to read the whole .TXT file.
    # Ex. rockyou.txt(139.92 MB) takes 3 seconds to starts cracking. It depends how big the size of your wordlist file.
    # I hate Buffering Reading even It improves performance :>
    with open(wordlist_file_path, 'r', encoding='UTF-8', errors='ignore') as file:
        total_lines = len(file.readlines())
    threads_lines = total_lines // threads

    passwords_storage_set = []
    threads_storage_set = []

    def with_thrds(target_file_archive, archive_file_path, wordlist_file_path, begin_t, end_t, passwords_storage):
        result = target_file_archive(archive_file_path, wordlist_file_path, begin_t, end_t)
        if result:
            passwords_storage.append(result)

    target_file_archive = cracking_dat_zip if archive_file_path.lower().endswith('.zip') else cracking_dat_rar

    for i in range(threads):
        begin_t = i * threads_lines
        end_t = (i + 1) * threads_lines if i != threads - 1 else total_lines

        thrds = threading.Thread(
            target=with_thrds,
            args=(target_file_archive, archive_file_path, wordlist_file_path, begin_t, end_t, passwords_storage_set)
        )

        threads_storage_set.append(thrds)
        thrds.start()

    for thrds in threads_storage_set:
        thrds.join()


# Timer to check how long it takes to process..
    ending = time.time()
    elapsed = ending - Process_Timer
    print(Fore.YELLOW + f"\n Timer: {elapsed:.2f} seconds")

    # Checks if the password is found correctly and also checks how many invalid attempts have been done.
    if passwords_storage_set:
        print(Fore.LIGHTYELLOW_EX + f" Total Invalid Attempts: {invalid_attempts_counter}")
        print(Fore.LIGHTGREEN_EX + f"\n[+] Password Found!: {passwords_storage_set[0]}")
    else:
        print(Fore.LIGHTYELLOW_EX + f" Total Invalid Attempts: {invalid_attempts_counter}")
        print(Fore.RED + "\n[!] Password Not Found.")

if __name__ == "__main__":
    main_cracking_process()

from colorama import init, Fore

init(autoreset=True)


"""
        This is a game hacking library created by the Vision team to bypass Anti-Cheats / Anti Tampers .
        
        Credits:
            - Nano (github.com/l4tt)
            
        PyGG API:
            - get_process_id(process_name: str): Grabs the process ID of an active window.
            - change_process_title(pid: int, title_length=5, random_title=True, window_title="VISION"): Changes the title of an active window process in a 5-second loop.
            - modify_privileges(current_process=None): Modifies the target process Security descriptor's.
            - set_window_icon(pid: int, icon_path: str): Sets a windows icon to an icon path.
            - create_junk_code(start_range=10, max_range=20): Creates Junkcode preventing some AC detecting whats going on.
            - write_bool(address, value): Writes a boolean value to a specific memory address.
            - write_string(address, value): Writes a string value to a specific memory address.
            - write_memory(address, value): Writes a value to a specific memory address.
            - write_float(address, value): Writes a float value to a specific memory address.
            - write_double(address, value): Writes a double value to a specific memory address.
            - write_longlong(address, value): Writes a long long value to a specific memory address.
            - read_string(address, is_obfuscated=True): Reads a string value from a specific memory address.
            - read_bool(address): Reads a boolean value from a specific memory address.
            - read_int(address): Reads an integer value from a specific memory address.
            - read_float(address): Reads a float value from a specific memory address.
            - read_qword(address): Reads a qword value from a specific memory address.
            - read_memory(address): Reads a value from a specific memory address.
            - read_double(address): Reads a double value from a specific memory address.
            - read_longlong(address): Reads a long long value from a specific memory address.
            - close_handle(): Closes the handle to the process.
            - allocate_memory(size): Allocates memory to the process (default is 124b).
            - handle_refresher(delay): Closes and reopens the handle that is open to trick AC.
            

"""


class Logger:
    def success(msg):
        print(f"[ {Fore.GREEN}SUCCESS{Fore.RESET} ] {msg}")

    def error(msg):
        print(f"[{Fore.RED}ERROR{Fore.RESET}] {msg}")

    def warning(msg):
        print(f"[{Fore.YELLOW}WARNING{Fore.RESET}] {msg}")
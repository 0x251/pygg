from libs.pygg_api import PyGG
from colorama import Fore, init

class PyggExample:
    def __init__(self) -> None:
        # Setting init
        self.pygg = PyGG() # PyGG class
        self._pid = 0
        self._process_name = "notepad.exe"
        self._target_address = 0x1A9AAEF0000
        # Class sets
        self._window_title = None
        self._str = None
        self._address_ex = None
        self._address = None
        self._encoded = None
        self._null_byte = None
        self._bool = None
        self._read_string = None
        self._read_bool = None
        # Colorama
        self._colorama = init(autoreset=True, convert=True)

    @property
    def process_pid(self):
        return self._pid

    @process_pid.setter
    def process_pid(self, _proc_name):
        self._pid = self.pygg.get_process_id(_proc_name)

    @property
    def set_process_window_title(self):
        return self._window_title

    @set_process_window_title.setter
    def set_process_window_title(self, value):
        _title, _length, _random_title = value
        self._window_title = _title

        if _random_title:
            self._window_title = "Random"
        
        self.pygg.change_process_title(self._pid, title_length=_length, random_title=_random_title, window_title=_title)

    @property
    def write_string(self):
        ...
    
    @write_string.setter
    def write_string(self, value):
        _address, _str, _encoded, _null_byte = value
        self._str, self._address, self._encoded, self._null_byte = _str, _address, _encoded, _null_byte
        self.pygg.write_string(address=_address, value=_str, is_obfuscated=_encoded, null_bytes=_null_byte) # write LOL

    
    @property
    def write_bool(self):
        ...
    
    @write_bool.setter
    def write_bool(self, value):
        _address, _bool = value
        self._bool, self._address = _bool, _address
        self.pygg.write_bool(address=_address, value=_bool)

    @property
    def read_string(self):
        return self._read_string

    @read_string.setter
    def read_string(self, value):
        _address, _encoded = value
        self._address, self._encoded = _address, _encoded
        self._read_string = self.pygg.read_string(address=_address, is_obfuscated=_encoded)


    @property
    def aob_scan(self):
        return self._address_ex
    
    @aob_scan.setter
    def aob_scan(self, pattern: bytes):
        self._address_ex = self.pygg.aob_scan(pattern=pattern, return_multiple=True)

    @property
    def read_bool(self):
        return self._read_bool

    @read_bool.setter
    def read_bool(self, _address):
        self._address = _address
        self._read_bool = self.pygg.read_bool(_address)

    def pygg_console_logging(self, _value, error=False):
        if error:
            print(f"[{Fore.RED}ERROR{Fore.RESET}] - {_value}")
        else:
            print(f"[{Fore.YELLOW}PyGG{Fore.RESET}] - {_value}")


    def pygg_ex(self):
        self.process_pid = self._process_name  # set proc name to setting property

        pid = self.process_pid

        if not pid:
            self.pygg_console_logging(f"Failed to grab pid from '{self._process_name}'", error=True)
            exit()
        
        self.pygg_console_logging(f"Grabbed pid: {Fore.YELLOW}{self._pid}{Fore.RESET} from {Fore.GREEN}'{self._process_name}'")

        self.pygg.init_memory(pid) # opens a handle for the pid it's set to

        self._target_address = self.pygg.allocate_memory(124)

        self.pygg_console_logging(f"Opened an handle to {Fore.LIGHTBLACK_EX}'{self._process_name}:{pid}'")

        self.set_process_window_title = ("PyGG Example", 0, False) # title, length, random_title

        self.pygg_console_logging(f"Set window title of {Fore.GREEN}'{self._process_name}' to '{self._window_title}'")

        #print(hex(self._target_address))

        
        self.write_string = (self._target_address, "visiontest", False, False) # address, str, encoded, null-byte

        self.pygg_console_logging(f"Wrote {Fore.GREEN}'{self._str}'{Fore.RESET} to {Fore.YELLOW}{hex(self._address)}{Fore.RESET} encoded: {Fore.BLUE}{self._encoded}{Fore.RESET}, null-byte: {Fore.LIGHTMAGENTA_EX}{self._null_byte}{Fore.RESET}")

        self.read_string = (self._target_address, False) # do note that if the string contains null bytes it will only read the first letter of the string as it will strip all null bytes if contained

        self.pygg_console_logging(f"Read from {Fore.YELLOW}{hex(self._address)}{Fore.RESET} str value: {Fore.GREEN}'{self._read_string}'{Fore.RESET} encoded: {Fore.BLUE}{self._encoded}\n")
        
        #pattern_bytes = self.pygg.create_pattern(self._target_address, len(self._read_string)).encode()

        #self.pygg_console_logging(f"Created Pattern for {Fore.GREEN}'{self._read_string}' {Fore.RESET}: {Fore.LIGHTRED_EX}{pattern_bytes.decode()}")
        
        self.aob_scan = b"\x76\x69\x73\x69\x6F\x6E\x74\x65\x73\??\??" # You can set this to pattern_bytes and uncomment it, but this was to test pattern masks like ?? or x00

        hook_addy = self.pygg.allocate_memory(124)
        self.write_string = (hook_addy, "you have jumped to me", False, False)
        self.pygg.hook_function(self._target_address, hook_addy, len(self._read_string))

        self.pygg_console_logging(f"Jumped from {Fore.YELLOW}{hex(self._target_address)}{Fore.RESET} to {Fore.CYAN}{hex(hook_addy)}")
        

        for _ in self.aob_scan:
            self.read_string = (_, False) # Since i added a jump function, it will fail to read the string since the instruction no longer points to a string, it will point to a jump
            if not self._read_string:
                self.pygg_console_logging(f"Hit a jump instruction or not a valid string at address {Fore.RED}{hex(self._address)}", True)
                exit()
            self.pygg_console_logging(f"Found address that matches pattern {Fore.YELLOW}{hex(_)}")        
             
            
            self.pygg_console_logging(f"Read from {Fore.YELLOW}{hex(self._address)}{Fore.RESET} str value: {Fore.GREEN}'{self._read_string}'{Fore.RESET} encoded: {Fore.BLUE}{self._encoded}")
            

        
        
        #self.write_bool = (self._target_address, True)

        #self.pygg_console_logging(f"Wrote {Fore.BLUE}{self._bool}{Fore.RESET} to {Fore.YELLOW}{hex(self._address)}")

        #self.read_bool = self._target_address

        #self.pygg_console_logging(f"Read from {Fore.YELLOW}{hex(self._address)}{Fore.RESET} bool value: {Fore.BLUE}{self._read_bool}")
        
        #print(self.pygg.create_junk_code(1, 100))
        self.pygg.close_handle()

        self.pygg_console_logging(f"Closed handle to {Fore.LIGHTBLACK_EX}'{self._process_name}:{pid}'")

if __name__ == "__main__":
    pygg_example = PyggExample()
    pygg_example.pygg_ex()

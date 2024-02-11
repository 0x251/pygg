import psutil
import ctypes
import threading
import random
import string
import time
import win32api
import win32con
import win32process
import win32security
import win32com.client

import ctypes.wintypes as wintypes
from ctypes import windll
from libs.memory import Memory
from libs.windows import Windows

from libs.logger import Logger
from libs.acls import SECURITY_DESCRIPTOR, SID_IDENTIFIER_AUTHORITY, ACL, ALACE




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

        PyGG Lua API:
            - lua_version(): Returns the lua Env version
            - lua_globals(): Returns lua set globals example: lua_globals().b will return the value of the set global b 
            - lua_set_memory(max_memory: int): It Will set lua vm max memory to the env
            - lua_memory_used(): Returns memory used by the lua env
            - lua_exec(str): Will execute lua, accepts multi line strings
            - lua_eval(str): Will execute lua, accepts multi line strings (same as exec kinda)

            

"""

class PyGG:
    
    def __init__(self) -> None:
        # Class init setting
        self.p_handle = None
        self.windows = Windows()
        self.memory = Memory(self.p_handle)
        #self.lua = Luavm()
        self.pid = None
        
        # kernel
        self.kernel32 = windll.kernel32

        # Open Process types
        self.PROCESS_VM_READ = 0x0010
        self.PROCESS_VM_WRITE = 0x0020
        self.PROCESS_VM_OPERATION = 0x0008

        # Open Process args
        self.kernel32.OpenProcess.restype = wintypes.HANDLE
        self.kernel32.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
        self.kernel32.CloseHandle.restype = wintypes.BOOL
        self.kernel32.CloseHandle.argtypes = [wintypes.HANDLE]

    
    def init_memory(self, pid: int):
        self.p_handle = self.kernel32.OpenProcess(self.PROCESS_VM_READ | self.PROCESS_VM_WRITE | self.PROCESS_VM_OPERATION, False, pid)
        self.pid = pid
        if not self.p_handle:
            error_code = self.kernel32.GetLastError()
            Logger.error(f"Failed to open process. Error code: {error_code}")
            exit()
        self.memory = Memory(self.p_handle)
    
    
    def handle_refresher(self, delay=.5):
        def refresh(delay):
            time.sleep(delay)
            self.kernel32.CloseHandle(self.p_handle)
            self.p_handle = self.kernel32.OpenProcess(self.PROCESS_VM_READ | self.PROCESS_VM_WRITE | self.PROCESS_VM_OPERATION, False, self.pid)
        threading.Thread(target=refresh, args=[delay], daemon=True).start()

    """

    def lua_version(self):
        return self.lua_version

    def lua_globals(self):
        return self.lua.lua_globals()
    
    def lua_set_memory(self, _value: int):
        return self.lua.lua_set_memory(_value)

    def lua_memory_used(self):
        return self.lua.lua_memory_used()

    def lua_exec(self, _str: str):
        return self.lua.lua_exec(_str)

    def lua_eval(self, _str: str):
        return self.lua.lua_eval(_str)
    """
    def get_process_id(self, process_name):
        return self.windows.get_process_id(process_name=process_name)
    
  

    def write_bool_undetected(self, address, value):
        return self.memory.write_bool_test(address=address, value=value)

    def change_process_title(self, pid, title_length, random_title, window_title):
        return self.windows.change_process_title(pid=pid, title_length=title_length, random_title=random_title, window_title=window_title)
    
    def create_junk_code(self, start_range, max_range):
        return self.windows.create_junk_code(start_range=start_range, max_range=max_range)
    
    def set_window_icon(self, pid, icon_path):
        return self.windows.set_window_icon(pid=pid, icon_path=icon_path)    

    def modify_privileges(self):
        return self.windows.modify_privileges()

    def write_bool(self, address, value):
        return self.memory.write_bool(address=address, value=value)
    
    def write_int(self, address, value):
        return self.memory.write_int(address=address, value=value)
    
    def GetModuleBaseAddress(self, pid, module_name):
        return self.memory.GetModuleBaseAddress(PID=pid, ModuleName=module_name)
    
    def GetPointerAddress(self, baseAddress, offsets):
        return self.memory.GetPointerAddress(baseAddress=baseAddress, offsets=offsets)
    
    def allocate_memory(self, size=124):
        return self.memory.allocate_memory(size=size)
    
    def create_pattern(self, address, size):
        return self.memory.create_pattern(address=address, length=size)
    
    def hook_function(self, target_address, new_address, original_bytes_length):
        return self.memory.hook_function(target_address, new_address, original_bytes_length)
    
    def aob_scan(self, pattern: str, return_multiple: bool = True):
        return self.memory.aob_scan(pattern=pattern, return_multiple=return_multiple)
    
    def write_string(self, address, value, is_obfuscated=True, null_bytes=True):
        return self.memory.write_string(address=address, value=value, is_obfuscated=is_obfuscated, null_byte_split=null_bytes)
    
    def write_memory(self, address, value):
        return self.memory.write_memory(address=address, value=value)
    
    def write_float(self, address, value):
        return self.memory.write_float(address=address, value=value)
    
    def write_double(self, address, value):
        return self.memory.write_double(address=address, value=value)
    
    def write_longlong(self, address, value):
        return self.memory.write_longlong(address=address, value=value)
    
    def read_string(self, address, is_obfuscated=True):
        return self.memory.read_string(address=address, is_obfuscated=is_obfuscated)
    
    def read_bool(self, address):
        return self.memory.read_bool(address=address)
    
    def read_bool_test(self, address):
        return self.memory.read_bool_test(address=address)
    
    def read_int(self, address):
        return self.memory.read_int(address=address)
    
    def read_ctype(self, address, ctype):
        return self.memory.read_ctype(address=address, ctype_type=ctype)
    
    def read_float(self, address):
        return self.memory.read_float(address=address)
    
    def read_qword(self, address):
        return self.memory.read_qword(address=address)

    def read_memory(self, address):
        return self.memory.read_memory(address=address)
    
    def read_double(self, address):
        return self.memory.read_double(address=address)
    
    def read_longlong(self, address):
        return self.memory.read_longlong(address=address)
    
    def close_handle(self):
        self.kernel32.CloseHandle(self.p_handle)
    
    
    
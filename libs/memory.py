import ctypes, random, re, struct
import ctypes.wintypes as wintypes
from ctypes import windll
from libs.logger import Logger

from ctypes.wintypes import *

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

class MEMORY_BASIC_INFORMATION(ctypes.Structure):
            _fields_ = [
                ("BaseAddress", ctypes.c_void_p),
                ("AllocationBase", ctypes.c_void_p),
                ("AllocationProtect", wintypes.DWORD),
                ("RegionSize", ctypes.c_size_t),
                ("State", wintypes.DWORD),
                ("Protect", wintypes.DWORD),
                ("Type", wintypes.DWORD),
            ]


class Memory:
    
    def __init__(self, phandle) -> None:
        self.p_handle = phandle 
        self.advapi32 = windll.advapi32
        self.kernel32 = windll.kernel32
        self.user32 = windll.user32
        self.obf_byte = 0
        self.byte_size = 0
        self.VirtualAllocEx = self.kernel32.VirtualAllocEx
        self.VirtualAllocEx.argtypes = (
            ctypes.c_void_p,
            ctypes.c_void_p,
            ctypes.c_ulong,
            ctypes.c_ulong,
            ctypes.c_ulong
        )
        
        self.PROCESS_ALL_ACCESS = 0xFFFF
        self.TH32CS_SNAPMODULE = 0x00000008
        self.TH32CS_SNAPMODULE32 = 0x00000010
        
        self.kernel32.ReadProcessMemory.restype = wintypes.BOOL
        self.kernel32.ReadProcessMemory.argtypes = [wintypes.HANDLE, wintypes.LPCVOID, wintypes.LPVOID, ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]
        
    
        self.VirtualAllocEx.restype = ctypes.c_void_p
        self.VirtualQueryEx = self.kernel32.VirtualQueryEx
        self.VirtualQueryEx.argtypes = [wintypes.HANDLE, wintypes.LPCVOID, ctypes.POINTER(MEMORY_BASIC_INFORMATION), ctypes.c_size_t]
        self.VirtualQueryEx.restype = ctypes.c_size_t


    def write_bytes(self, address, data):
        try:
            buffer = (ctypes.c_ubyte * len(data)).from_buffer_copy(data)
            bytes_written = ctypes.c_size_t()

            result = self.kernel32.WriteProcessMemory(
                self.p_handle,
                ctypes.c_void_p(address),
                buffer,
                len(data),
                ctypes.byref(bytes_written)
            )

            if result == 0:
                raise ctypes.WinError()

            return True

        except Exception as error:
            Logger.error(f"Failed to write bytes to memory. Error: {error}")
            return False
        
    def read_bytes(self, address, size) -> bytes:
        try:
            buffer = ctypes.create_string_buffer(size)
            read_bytes = ctypes.c_size_t()
            self.kernel32.ReadProcessMemory(
                self.p_handle,
                ctypes.c_void_p(address),
                buffer,
                size,
                ctypes.byref(read_bytes)
            )
            return buffer.raw
        except Exception as error:
            Logger.error(f"Failed to read bytes. Error: {error}")
            return None
        
    def read_memory(self, address):
        try:
           
            addy_value = ctypes.c_ulonglong()
            read_bytes = ctypes.c_size_t()
            
            self.kernel32.ReadProcessMemory(self.p_handle, 
            ctypes.c_void_p(address), 
            ctypes.byref(addy_value), 
            ctypes.sizeof(addy_value), 
            ctypes.byref(read_bytes))
            
            random_byte_val = random.randint(0, 255)
            obfuscated_val = addy_value.value ^ random_byte_val
            
            
            
            return (obfuscated_val, random_byte_val)
        except Exception as error:
            Logger.error(f"Failed to read memory. Error: {error}")
            
    def write_bool_test(self, address, value: bool) -> bool:
        try:
            bool_value = ctypes.c_bool(value)
            size = ctypes.sizeof(bool_value)
            old_protect = ctypes.c_ulong()
            new_protect = 0x40
            temp_protect = ctypes.c_ulong()

            status_change_protect = self.kernel32.VirtualProtectEx(self.p_handle, ctypes.c_void_p(address), ctypes.c_size_t(size), new_protect, ctypes.byref(temp_protect))
            if not status_change_protect:
                Logger.error("Failed to change memory protection.")
                return False

            written = ctypes.c_size_t()
            status_write_memory = self.kernel32.WriteProcessMemory(self.p_handle, ctypes.c_void_p(address), ctypes.byref(bool_value), size, ctypes.byref(written))
            if not status_write_memory:
                Logger.error("Failed to write to memory.")
                self.kernel32.VirtualProtectEx(self.p_handle, ctypes.c_void_p(address), ctypes.c_size_t(size), temp_protect.value, ctypes.byref(old_protect))
                return False

            status_restore_protect = self.kernel32.VirtualProtectEx(self.p_handle, ctypes.c_void_p(address), ctypes.c_size_t(size), temp_protect.value, ctypes.byref(old_protect))
            if not status_restore_protect:
                Logger.error("Failed to restore memory protection.")
                return False

            return True

        except Exception as error:
            Logger.error(f"Failed to write undetected boolean to memory. Error: {error}")
            return False
        
    
    
    def read_float(self, address):
        try:
            float_value = ctypes.c_float()
            read_bytes = ctypes.c_size_t()
            
            self.kernel32.ReadProcessMemory(
                self.p_handle, 
                ctypes.c_void_p(address), 
                ctypes.byref(float_value), 
                ctypes.sizeof(float_value), 
                ctypes.byref(read_bytes)
            )
            
           
            float_as_int = struct.unpack('I', struct.pack('f', float_value.value))[0]
            random_byte_val = random.randint(0, 255)
            obfuscated_val = float_as_int ^ random_byte_val
           
            original_float = struct.unpack('f', struct.pack('I', obfuscated_val ^ random_byte_val))[0]
            
            return original_float
        
        except Exception as error:
            Logger.error(f"Failed to read memory. Error: {error}")
    
    
    def read_double(self, address):
        try:
            
            double_value = ctypes.c_double()
            read_bytes = ctypes.c_size_t()
            
            self.kernel32.ReadProcessMemory(
                self.p_handle, 
                ctypes.c_void_p(address), 
                ctypes.byref(double_value), 
                ctypes.sizeof(double_value), 
                ctypes.byref(read_bytes)
            )
            
            random_byte_val = random.randint(0, 255)
            obfuscated_val = double_value.value ^ random_byte_val
            
            return obfuscated_val ^ random_byte_val
        
        except Exception as error:
            Logger.error(f"Failed to read memory. Error: {error}")
            
    def read_longlong(self, address):
        try:
            
            longlong_value = ctypes.c_longlong()
            read_bytes = ctypes.c_size_t()
            
            self.kernel32.ReadProcessMemory(
                self.p_handle, 
                ctypes.c_void_p(address), 
                ctypes.byref(longlong_value), 
                ctypes.sizeof(longlong_value), 
                ctypes.byref(read_bytes)
            )
            
            random_byte_val = random.randint(0, 255)
            obfuscated_val = longlong_value.value ^ random_byte_val
            
            
            return obfuscated_val ^ random_byte_val
        
        except Exception as error:
            Logger.error(f"Failed to read memory. Error: {error}")
            
    class ModuleEntry32(ctypes.Structure):
       _fields_ = [ ( 'dwSize' , DWORD ) ,
                ( 'th32ModuleID' , DWORD ),
                ( 'th32ProcessID' , DWORD ),
                ( 'GlblcntUsage' , DWORD ),
                ( 'ProccntUsage' , DWORD ) ,
                ( 'modBaseAddr' , ctypes.POINTER(ctypes.c_ulong)) ,
                ( 'modBaseSize' , DWORD ) ,
                ( 'hModule' , HMODULE ) ,
                ( 'szModule' , ctypes.c_char * 256 ),
                ( 'szExePath' , ctypes.c_char * 260 ) ]
            
    def read_string(self, address, is_obfuscated=False) -> str:
        try:
            byte_array = bytearray()
            offset = 0
            while True:
                buffer = ctypes.create_string_buffer(1)
                read_bytes = ctypes.c_size_t()

                if not self.kernel32.ReadProcessMemory(
                    self.p_handle,
                    ctypes.c_void_p(address + offset),
                    buffer,
                    1,
                    ctypes.byref(read_bytes)
                ):
                    break

                
                if isinstance(buffer[0], int):
                    byte_value = buffer[0]
                else:
                    byte_value = ord(buffer[0]) 

                if byte_value == 0:
                    break
                byte_array.append(byte_value)
                offset += 1

            
            if is_obfuscated:
                for i in range(len(byte_array)):
                    byte_array[i] ^= self.obf_byte

            return byte_array.decode('utf-8')

        except UnicodeDecodeError as ude:
            return ""
        except Exception as error:
            Logger.error(f"Failed to read memory. Error: {error}")
            return ""
    def read_ctype(self, address, ctype_type):
       
        ctype_instance = ctype_type
        read_bytes = ctypes.c_size_t()

        success = self.kernel32.ReadProcessMemory(
            self.p_handle,
            ctypes.c_void_p(address),
            ctypes.byref(ctype_instance),
            ctypes.sizeof(ctype_instance),
            ctypes.byref(read_bytes)
        )

        if success:
            return ctype_instance
        else:
            Logger.error(f"Failed to read memory for ctype '. Error: {ctypes.GetLastError()}")
            return None
    
    def read_int(self, address):
        try:
           
            int_value = ctypes.c_int()
            read_bytes = ctypes.c_size_t()
            
            self.kernel32.ReadProcessMemory(
                self.p_handle, 
                ctypes.c_void_p(address), 
                ctypes.byref(int_value), 
                ctypes.sizeof(int_value), 
                ctypes.byref(read_bytes)
            )
            
            return int_value.value
        
        except Exception as error:
            Logger.error(f"Failed to read memory. Error: {error}")
            
    def read_bool(self, address) -> bool:
        try:
            
            bool_value = ctypes.c_byte()
            read_bytes = ctypes.c_size_t()
            
            self.kernel32.ReadProcessMemory(
                self.p_handle, 
                ctypes.c_void_p(address), 
                ctypes.byref(bool_value), 
                ctypes.sizeof(bool_value), 
                ctypes.byref(read_bytes)
            )
            
            random_byte_val = random.randint(0, 255)
            obfuscated_val = bool(bool_value.value) ^ random_byte_val
            
            
            return obfuscated_val ^ random_byte_val
        
        except Exception as error:
            Logger.error(f"Failed to read memory. Error: {error}")
            
            
    def read_bool_test(self, address):
        data = wintypes.BOOL()
        bytesRead = ctypes.c_size_t()
        if not self.kernel32.ReadProcessMemory(self.p_handle, ctypes.c_void_p(address), ctypes.byref(data), ctypes.sizeof(data), ctypes.byref(bytesRead)):
            raise ctypes.WinError(ctypes.get_last_error())
        return data.value
            
    def read_qword(self, address) -> int:
        try:
            
            qword_value = ctypes.c_ulonglong()
            read_bytes = ctypes.c_size_t()

            self.kernel32.ReadProcessMemory(
                self.p_handle,
                ctypes.c_void_p(address),
                ctypes.byref(qword_value),
                ctypes.sizeof(qword_value),
                ctypes.byref(read_bytes)
            )

            random_byte_val = random.randint(0, 255)
            obfuscated_val = qword_value.value ^ random_byte_val

            return obfuscated_val ^ random_byte_val

        except Exception as error:
            Logger.error(f"Failed to read qword from memory. Error: {error}")
            
    def GetModuleBaseAddress(self, PID, ModuleName) -> int:
        BaseAddess = None
        hSnap = self.kernel32.CreateToolhelp32Snapshot(self.TH32CS_SNAPMODULE | self.TH32CS_SNAPMODULE32, PID)
        ModuleEntry = self.ModuleEntry32()
        
        ModuleEntry.dwSize = ctypes.sizeof(self.ModuleEntry32)
        base = None

        if self.kernel32.Module32First(hSnap, ctypes.byref(ModuleEntry)):
            if ModuleEntry.szModule.decode("utf-8") == ModuleName:
                BaseAddess = int(hex(ctypes.addressof(ModuleEntry.modBaseAddr.contents)), 16)
        
        while self.kernel32.Module32Next(hSnap, ctypes.byref(ModuleEntry)):
            if ModuleEntry.szModule.decode("utf-8") == ModuleName:
                BaseAddess = int(hex(ctypes.addressof(ModuleEntry.modBaseAddr.contents)), 16)
                break

        self.kernel32.CloseHandle(hSnap)

        if BaseAddess == None:
            raise Exception("Module not found.")

        return BaseAddess
    
    def GetPointerAddress(self, baseAddress, offsets) -> int:
        address = baseAddress
    
        for offset in offsets:
            value = self.read_longlong(address)
    
            address = value + offset
            


        return address
    
    def write_int(self, address, value: int) -> bool:
        try:
                
            int_value = ctypes.c_int(value)

            random_byte_val = random.randint(0, 255)
            obfuscated_val = int_value.value ^ random_byte_val

            write_bytes = ctypes.c_size_t()

            self.kernel32.WriteProcessMemory(
                    self.p_handle,
                    ctypes.c_void_p(address),
                    ctypes.byref(ctypes.c_int(obfuscated_val ^ random_byte_val)),
                    ctypes.sizeof(ctypes.c_int(obfuscated_val)),
                    ctypes.byref(write_bytes)
            )

            
            return True

        except Exception as error:
            Logger.error(f"Failed to write float to memory. Error: {error}")
            return False
    
    
    
    def write_float(self, address, value: float) -> bool:
        try:
           
            float_value = ctypes.c_float(value)

            write_bytes = ctypes.c_size_t()

            self.kernel32.WriteProcessMemory(
                self.p_handle,
                ctypes.c_void_p(address),
                ctypes.byref(float_value),
                ctypes.sizeof(float_value),
                ctypes.byref(write_bytes)
            )

           
            return True

        except Exception as error:
            Logger.error(f"Failed to write float to memory. Error: {error}")
            return False


    def hook_function(self, target_address, new_address, original_bytes_length) -> tuple[bytes, bool]:
        try:
            original_bytes = self.read_bytes(target_address, original_bytes_length)
            if not original_bytes:
                raise Logger.error("Failed to read original bytes from target address.")

            relative_address = new_address - target_address - 5 
            jump_instruction = b'\xE9' + relative_address.to_bytes(4, byteorder='little', signed=True)

            if not self.write_bytes(target_address, jump_instruction):
                raise Logger.error("Failed to write jump instruction to target address.")

            return original_bytes, True
        except Exception as error:
            Logger.error(f"Failed to hook function. Error: {error}")
            
    
    def create_pattern(self, address, length):
        try:
           
            bytes_read = self.read_bytes(address, length)
            if bytes_read is None:
                Logger.error(f"Failed to create pattern from address")
            pattern = ''.join(['\\x{:02X}'.format(b) if b != 0 else '??' for b in bytes_read])
            return pattern
        except Exception as error:
            Logger.error(f"Failed to create pattern from address. Error: {error}")
            return None
   
    def aob_scan(self, pattern: str, return_multiple: bool = True):
        
        if not isinstance(pattern, bytes):
            Logger.error("Pattern must be a byte string for AOB scan.")
            return []

        mbi = MEMORY_BASIC_INFORMATION()
        address = 0
        pattern = pattern.replace(b"\??", b".")
        pattern = re.sub(b'\x00', b'.', pattern)
        pattern_compiled = re.compile(pattern)
        found_addresses = []
       
        

        while self.VirtualQueryEx(self.p_handle, ctypes.c_void_p(address), ctypes.byref(mbi), ctypes.sizeof(mbi)):
            if mbi.State == 0x1000 and mbi.Protect in (0x2, 0x4, 0x20, 0x40, 0x80):
                buffer = (ctypes.c_ubyte * mbi.RegionSize)()
                bytesRead = ctypes.c_size_t(0)

                if self.kernel32.ReadProcessMemory(self.p_handle, mbi.BaseAddress, buffer, mbi.RegionSize, ctypes.byref(bytesRead)):
                    buffer_array = bytearray(buffer)
                    for match in pattern_compiled.finditer(buffer_array):
                        if match:
                            found_address = mbi.BaseAddress + match.start()
                            if return_multiple:
                                found_addresses.append(found_address)
                            else:
                                return found_address

            address += mbi.RegionSize
        
        if return_multiple:
            return found_addresses

    
    def write_double(self, address, value: float) -> bool:
        try:
           
            double_value = ctypes.c_double(value)

            random_byte_val = random.randint(0, 255)
            obfuscated_val = double_value.value ^ random_byte_val

            write_bytes = ctypes.c_size_t()

            self.kernel32.WriteProcessMemory(
                self.p_handle,
                ctypes.c_void_p(address),
                ctypes.byref(ctypes.c_double(obfuscated_val ^ random_byte_val)),
                ctypes.sizeof(ctypes.c_double(obfuscated_val)),
                ctypes.byref(write_bytes)
            )

           
            return True

        except Exception as error:
            Logger.error(f"Failed to write double to memory. Error: {error}")
            return False
            
    def write_longlong(self, address, value: int) -> bool:
        try:
            
            longlong_value = ctypes.c_longlong(value)

            random_byte_val = random.randint(0, 255)
            obfuscated_val = longlong_value.value ^ random_byte_val

            write_bytes = ctypes.c_size_t()

            self.kernel32.WriteProcessMemory(
                self.p_handle,
                ctypes.c_void_p(address),
                ctypes.byref(ctypes.c_longlong(obfuscated_val ^ random_byte_val)),
                ctypes.sizeof(ctypes.c_longlong(obfuscated_val)),
                ctypes.byref(write_bytes)
            )
            # 
            
            return True

        except Exception as error:
            Logger.error(f"Failed to write long long to memory. Error: {error}")
            return False
    
    
    def allocate_memory(self, size: int) -> int:
        
        try:
            random_byte_val = random.randint(0, 255)
            obfuscated_size = size ^ random_byte_val

            address = self.VirtualAllocEx(
                self.p_handle, 
                None, 
                obfuscated_size,  
                0x3000,
                0x40
            )
            
            
            return address ^ random_byte_val
        
        except Exception as error:
            Logger.error(f"Failed to allocate memory. Error: {error}")
    
    def write_bool(self, address, value: bool) -> bool:
        try:
            
            bool_value = ctypes.c_byte(int(value))
            random_byte_val = random.randint(0, 255)
            obfuscated_val = bool_value.value ^ random_byte_val

            write_bytes = ctypes.c_size_t()

            self.kernel32.WriteProcessMemory(
                self.p_handle,
                ctypes.c_void_p(address),
                ctypes.byref(ctypes.c_byte(obfuscated_val ^ random_byte_val)),  
                ctypes.sizeof(ctypes.c_byte(obfuscated_val)),  
                ctypes.byref(write_bytes)
            )
            
            
            return True

        except Exception as error:
            Logger.error(f"Failed to write boolean to memory. Error: {error}")
            return False
    
    def write_string(self, address, value: str, is_obfuscated=True, null_byte_split=True) -> bool:
        try:
            if null_byte_split:
                value = '\000'.join(list(value))  
                
            encoded_value = value.encode('utf-8')
            self.obf_byte = random.randint(0, 255)  
            obfuscated_val = bytearray(encoded_value)
            for i in range(len(obfuscated_val)):
                obfuscated_val[i] ^= self.obf_byte

            write_bytes = ctypes.c_size_t()
            self.byte_size = len(value)

            if (is_obfuscated):
                self.kernel32.WriteProcessMemory(
                    self.p_handle,
                    ctypes.c_void_p(address),
                    (ctypes.c_char * len(obfuscated_val))(*obfuscated_val),
                    len(obfuscated_val),
                    ctypes.byref(write_bytes)
                )
                
            else:
                
                self.kernel32.WriteProcessMemory(
                    self.p_handle,
                    ctypes.c_void_p(address),
                    (ctypes.c_char * len(encoded_value))(*encoded_value),
                    len(encoded_value),
                    ctypes.byref(write_bytes)
                )

            return True

        except Exception as error:
            Logger.error(f"Failed to write string to memory. Error: {error}")
            return False
    
    def write_memory(self, address, value) -> bool:
        try:
            
            random_byte = random.randint(0, 255)
            obfuscated_value = value ^ random_byte
            self.kernel32.WriteProcessMemory(self.p_handle, ctypes.c_void_p(address), ctypes.byref(ctypes.c_int(obfuscated_value)), ctypes.sizeof(ctypes.c_int), None)
            
            return True
        except Exception as error:
            Logger.error(f"Failed to Write memory. Error: {error}")

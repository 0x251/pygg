import random
import string
import ctypes
import threading
import time
import win32api
import win32con
import psutil
import win32process
import win32security
import win32com.client
import ctypes.wintypes as wintypes

from ctypes import windll

class Windows:
    def __init__(self) -> None:
        self.WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.wintypes.HWND, ctypes.POINTER(ctypes.c_int))
        self.advapi32 = windll.advapi32
        self.kernel32 = windll.kernel32
        self.user32 = windll.user32
        self.WM_SETICON = 0x0080
        self.ICON_SMALL = 0
        self.ICON_BIG = 1
        self.LR_LOADFROMFILE = 0x00000010
        self.IMAGE_ICON = 1
        self.hToken = None

    def change_process_title(self, pid: int, title_length=0, random_title=True, window_title="PYGG") -> True:
        def generate_random_string(length):
            letters = string.ascii_uppercase
            return ''.join(random.choice(letters) for i in range(length))
        
        def windows_callback(hwnd, lParam):
            current_pid = ctypes.wintypes.DWORD()
            self.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(current_pid))
            if pid == current_pid.value:
                if random_title:
                    self.user32.SetWindowTextW(hwnd, generate_random_string(title_length))
                else:
                    self.user32.SetWindowTextW(hwnd, window_title)
                    
                return False  
            return True  

        callback = self.WNDENUMPROC(windows_callback)
        def update_title():
            while True:
                self.user32.EnumWindows(callback, 0)
                time.sleep(5)

        thread = threading.Thread(target=update_title, daemon=True)
        thread.start()
        
    
    
    def random_var_name(self):
        common_var_names = [
            'index', 'temp', 'count', 'item', 'value', 'num', 'data', 'result', 
            'total', 'flag', 'size', 'position', 'max', 'min', 'sum', 'average', 
            'length', 'width', 'height', 'area', 'volume', 'name', 'title', 
            'error', 'status', 'message', 'payload', 'response', 'quantity', 
            'threshold', 'limit', 'range', 'score', 'level', 'rate', 'ratio', 
            'percentage', 'chunk', 'batch', 'record', 'list', 'map', 'set', 
            'queue', 'stack', 'tree', 'node', 'edge', 'vertex', 'graph', 'object', 
            'string', 'char', 'byte', 'line', 'text', 'pattern', 'regex', 'url', 
            'path', 'dir', 'file', 'key', 'value', 'entry', 'header', 'footer', 
            'config', 'option', 'argument', 'parameter', 'username', 'password', 
            'email', 'address', 'phone', 'date', 'time', 'timestamp', 'year', 
            'month', 'day', 'hour', 'minute', 'second', 'millisecond', 'timezone', 
            'session', 'cookie', 'token', 'id', 'uuid', 'hash', 'digest', 'salt', 
            'encryption', 'cipher', 'algorithm', 'method', 'function', 'procedure', 
            'callback', 'handler', 'event', 'listener', 'request', 'command', 
            'instruction', 'directive', 'query', 'transaction', 'operation', 'action', 
            'activity', 'task', 'job', 'process', 'workflow', 'cycle', 'sequence', 
            'series', 'chain', 'stream', 'flow', 'progress', 'development', 'growth', 
            'expansion', 'increase', 'decrease', 'increment', 'decrement', 'addition', 
            'subtraction', 'multiplication', 'division', 'calculation', 'computation', 
            'analysis', 'synthesis', 'comparison', 'contrast', 'variation', 'modification', 
            'adjustment', 'alignment', 'orientation', 'positioning', 'placement', 
            'installation', 'setup', 'configuration', 'arrangement', 'organization', 
            'order', 'structure', 'framework', 'system', 'network', 'circuit', 
            'component', 'element', 'module', 'unit', 'part', 'segment', 'fraction', 
            'piece', 'section', 'chapter', 'episode', 'act', 'scene', 'stage', 
            'level', 'platform', 'vehicle', 'vessel', 'craft', 'equipment', 'machinery', 
            'appliance', 'device', 'gadget', 'tool', 'instrument', 'utensil', 'implement', 
            'ware', 'material', 'substance', 'fabric', 'texture', 'fiber', 'thread', 
            'yarn', 'wire', 'cable', 'line', 'rope', 'strap', 'chain', 'cord', 
            'lace', 'ribbon', 'tape', 'film', 'sheet', 'plate', 'foil', 'membrane', 
            'surface', 'skin', 'shell', 'case', 'cover', 'coating', 'layer', 
            'blanket', 'veil', 'curtain', 'screen', 'partition', 'wall', 'barrier', 
            'fence', 'gate', 'door', 'window', 'opening', 'entrance', 'exit', 
            'passage', 'path', 'trail', 'track', 'route', 'way', 'direction', 
            'destination', 'goal', 'purpose', 'reason', 'cause', 'effect', 'result', 
            'outcome', 'consequence', 'impact', 'influence', 'change', 'transition', 
            'transformation', 'conversion', 'revision', 'edition', 'version', 'variation', 
            'deviation', 'diversion', 'shift', 'switch', 'turn', 'spin', 'rotation', 
            'revolution', 'circle', 'cycle', 'loop', 'orbit', 'round', 'tour', 
            'journey', 'voyage', 'travel', 'trip', 'expedition', 'exploration', 
            'adventure'
        ]

        all_choices = common_var_names
        return random.choice(all_choices)

    def random_value(self):
        return str(random.randint(0, 100))

    def create_line_of_code(self, indent_level):
        indent = '    ' * indent_level
        line = ""
        structures = ['assignment', 'for_loop', 'if_statement', 'function_call', 'while_loop', 'try_except', 'list_comprehension', 'dictionary_comprehension']
        
        chosen_structure = random.choice(structures)
        
        if chosen_structure == 'assignment':
            line = f"{indent}{self.random_var_name()} = {self.random_value()}\n"
       
        elif chosen_structure == 'for_loop':
            loop_var = self.random_var_name()
            line = f"{indent}for {loop_var} in range({self.random_value()}):\n"
            line += self.create_line_of_code(indent_level + 1)
            
        elif chosen_structure == 'if_statement':
            line = f"{indent}if {self.random_var_name()} > {self.random_value()}:\n"
            line += self.create_line_of_code(indent_level + 1)
            
        elif chosen_structure == 'function_call':
            line = f"{indent}{self.random_var_name()}({self.random_value()})\n"
            
        elif chosen_structure == 'while_loop':
            condition_var = self.random_var_name()
            line = f"{indent}while {condition_var} < {self.random_value()}:\n"
            line += f"{indent}    {condition_var} += 1\n"
            
        elif chosen_structure == 'try_except':
            line = f"{indent}try:\n"
            line += self.create_line_of_code(indent_level + 1)
            line += f"{indent}except Exception as e:\n"
            line += f"{indent}    print(f'Error: {{e}}')\n"
        
        elif chosen_structure == 'list_comprehension':
            var_name = self.random_var_name()
            line = f"{indent}{var_name} = [{self.random_var_name()} for _ in range({self.random_value()})]\n"
        elif chosen_structure == 'dictionary_comprehension':
            key_var = self.random_var_name()
            value_var = self.random_value()
            nested_dict = ""
            for i in range(int(self.random_value()) % 5 + 1):  
                nested_key = self.random_var_name()
                nested_value = self.random_value()
                nested_dict += f"'{nested_key}': {nested_value}, "
            nested_dict = nested_dict.rstrip(", ")
            line = f"{indent}{self.random_var_name()} = {{{key_var}: {{{nested_dict}}} for _ in range({self.random_value()})}}\n"
        return line
        


    def create_junk_code(self, start_range=10, max_range=20):
        global junk_code
        junk_code = ""
        num_lines = random.randint(start_range, max_range)

        for _ in range(num_lines):
            junk_code += self.create_line_of_code(indent_level=0)

        return junk_code

    def set_window_icon(self, pid: int, icon_path: str) -> None:
        def windows_callback(hwnd, lParam):
            current_pid = wintypes.DWORD()
            self.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(current_pid))
            if pid == current_pid.value:
                h_icon_small = self.user32.LoadImageW(None, icon_path, self.IMAGE_ICON, 16, 16, self.LR_LOADFROMFILE)
                self.user32.SendMessageW(hwnd, self.WM_SETICON, self.ICON_SMALL, h_icon_small)
                h_icon_big = self.user32.LoadImageW(None, icon_path, self.IMAGE_ICON, 32, 32, self.LR_LOADFROMFILE)
                self.user32.SendMessageW(hwnd, self.WM_SETICON, self.ICON_BIG, h_icon_big)
                return False
            return True

        callback = self.WNDENUMPROC(windows_callback)
        self.user32.EnumWindows(callback, 0)
        return True
    
    def get_process_id(self, process_name: str) -> int:
        for process in psutil.process_iter(['pid', 'name']):
            if process.info['name'] == process_name:
                return process.info['pid']

        return 0
    
    def modify_privileges(self, current_process=None) -> int:
        current_process = current_process or win32api.GetCurrentProcess()
        hProcess = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION, False, win32process.GetProcessId(current_process))
        if hProcess:
            self.hToken = win32security.OpenProcessToken(hProcess, win32con.TOKEN_ADJUST_PRIVILEGES | win32con.TOKEN_QUERY)
            if self.hToken:
                privileges = win32security.GetTokenInformation(self.hToken, win32security.TokenPrivileges)

                for luid, _ in privileges:
                    win32security.AdjustTokenPrivileges(self.hToken, False, [(luid, win32con.SE_PRIVILEGE_ENABLED)])
                   

                self.threadId = win32process.GetProcessId(current_process)
                win32api.CloseHandle(hProcess)

            else:
                win32api.CloseHandle(hProcess)

        else:
            print(win32api.GetLastError())
        return self.hToken

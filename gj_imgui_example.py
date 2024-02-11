
import glfw
import OpenGL.GL as gl
import imgui, sys
from imgui.integrations.glfw import GlfwRenderer
from ctypes import windll, c_long
import ctypes
from ctypes import wintypes

from raylibpy import get_screen_height, get_screen_width


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


from libs.gj_api import PyGG


class Vec2(ctypes.Structure):
    _fields_ = [
        ("x", ctypes.c_float),
        ("y", ctypes.c_float)
    ]


class Vec2_int(ctypes.Structure):
    _fields_ = [
        ("x", ctypes.c_int),
        ("y", ctypes.c_int)
    ]


class Vec3(ctypes.Structure):
    _fields_ = [
        ('x', ctypes.c_float),
        ('y', ctypes.c_float),
        ('z', ctypes.c_float)
    ]

class Entity(ctypes.Structure):
        _fields_ = [
            ("", 0x4 * ctypes.c_byte),
            ("pos", Vec3),
            ("", 0xDC * ctypes.c_byte),
            ("health", ctypes.c_int),
            ("", 0x115 * ctypes.c_byte),
            ("name", 0x50 * ctypes.c_char),
            ("", 0xB7 * ctypes.c_byte),
            ("team", ctypes.c_int)
        ]


pygg = PyGG()
class PyGGExternal:
    
    def __init__(self) -> None:
        self.active = {
            "Assault Rifle Inf Ammo": False,
            "Submachine Gun Inf Ammo": False,
            "Sniper Inf Ammo": False,
            "Combat Shotgun Inf Ammo": False,
            "Pistol Inf Ammo": False,
            "Grenades Inf": False,
            "Fast fire Assault Rifle": False,
            "Fast fire Sniper": False,
            "Fast fire Combat Shotgun": False,
            "Auto shoot": False,
            "Health Inf": False,
            "Armor Inf": False,
            "Player ESP": False,
            "Bhop": False,
            "Invisable": False,
            "Noclip": False
           
            
        }
        self.window = None
        self.PID = 0
        
    def impl_glfw_init(self):
       
        width, height = 1366, 760 # change me to your screen resultion
        window_name = "PyGG Assault Cube Example"

        if not glfw.init():
            print("Could not initialize OpenGL context")
            sys.exit(1)

        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)
        glfw.window_hint(glfw.DECORATED, gl.GL_FALSE)  # This line makes the window frameless
        glfw.window_hint(glfw.TRANSPARENT_FRAMEBUFFER, gl.GL_TRUE)  # This line makes the window background transparent

        
        
        window = glfw.create_window(int(width), int(height), window_name, None, None)

        if not window:
            glfw.terminate()
            print("Could not initialize Window")
            sys.exit(1)

        glfw.make_context_current(window)
       
        return window
    
    
    
    def Pygg_Frame(self):
        op = {
            "LocalPlayer": 0x0017E0A8,
            "EntityList": 0x18AC04,
            "ASAMMO": 0x140,
            "SGAMMO": 0x138,
            "SAMMO": 0x13C,
            "CSAMMO": 0x134,
            "PlayerHeight": 0x50, 
            "PAMMO": 0x12C,
            "Grenade": 0x144,
            "Fast fire Assault Rifle": 0x164,
            "Fast fire Sniper": 0x160,
            "Fast fire Combat Shotgun": 0x158,
            "Auto shoot": 0x204,
            "Health": 0xEC,
            "Armor": 0xF0,
            "IsDead": 0x30C,
            "Player Name": 0x205,
            "PlayerX": 0x34,
            "Jump": 0x30,
            "PlayerY": 0x38,
            "noclip": 0x76
        }
        
        # pretty shit code ik, to lazy 
        module_base = pygg.GetModuleBaseAddress(self.PID, "ac_client.exe")
        LocalPlayerP = module_base + op["LocalPlayer"]
        NoClip = pygg.GetPointerAddress(LocalPlayerP, [op["noclip"]])
        AsAmmo = pygg.GetPointerAddress(LocalPlayerP, [op["ASAMMO"]])
        Height = pygg.GetPointerAddress(LocalPlayerP, [op["PlayerHeight"]])
        SGAmmo = pygg.GetPointerAddress(LocalPlayerP, [op["SGAMMO"]])
        SNAmmo = pygg.GetPointerAddress(LocalPlayerP, [op["SAMMO"]])
        CsAmmo = pygg.GetPointerAddress(LocalPlayerP, [op["CSAMMO"]])
        FastFireSP = pygg.GetPointerAddress(LocalPlayerP, [op["Fast fire Sniper"]])
        FastFireSH = pygg.GetPointerAddress(LocalPlayerP, [op["Fast fire Combat Shotgun"]])
        Armor = pygg.GetPointerAddress(LocalPlayerP, [op["Armor"]])
        Grenade = pygg.GetPointerAddress(LocalPlayerP, [op["Grenade"]])
        Health = pygg.GetPointerAddress(LocalPlayerP, [op["Health"]])
        AutoShoot = pygg.GetPointerAddress(LocalPlayerP, [op["Auto shoot"]])
        PPAmmo = pygg.GetPointerAddress(LocalPlayerP, [op["PAMMO"]])
        PlayerX = pygg.GetPointerAddress(LocalPlayerP, [op["PlayerX"]])
        Jump = pygg.GetPointerAddress(LocalPlayerP, [op["Jump"]])
        PlayerY = pygg.GetPointerAddress(LocalPlayerP, [op["PlayerY"]])
        PlayerName = pygg.GetPointerAddress(LocalPlayerP, [op["Player Name"]])
        FastFireAS = pygg.GetPointerAddress(LocalPlayerP, [op["Fast fire Assault Rifle"]])
        matrix = pygg.read_ctype(module_base + 0x17DFD0, (16 * ctypes.c_float)())[:]
        player_count = pygg.read_int(module_base + 0x18AC0C)

        io = imgui.get_io()
        style = imgui.get_style()
        imgui.style_colors_dark(style) 
        style.colors[imgui.COLOR_TITLE_BACKGROUND_ACTIVE] = (0, 0, 0, 1)
        style.colors[imgui.COLOR_BORDER] = (0, 0, 0, 1)
        style.colors[imgui.COLOR_BUTTON] = (0.1, 0.1, 0.1, 1)
        style.colors[imgui.COLOR_FRAME_BACKGROUND] = (0.1, 0.1, 0.1, 1)

        imgui.begin("PyGG Assault Cube External Example")  # Added flag to make imgui window frameless
        for label, enabled in self.active.copy().items():
            _, enabled = imgui.checkbox(label, enabled)
            self.active[label] = enabled
            
        username = pygg.read_string(PlayerName, False)
        
        changed, text_val = imgui.input_text('Username', username)
        
        if changed:
            pygg.write_string(PlayerName, text_val, False)
            
    
        if self.active["Invisable"]:
            pygg.write_int(NoClip, 2)
            
            self.previous_invisable_state = True
        
       
            
        if self.active["Submachine Gun Inf Ammo"]:
            pygg.write_int(SGAmmo, 999999999)
            
        if self.active["Sniper Inf Ammo"]:
            pygg.write_int(SNAmmo, 999999999)
            
        if self.active["Noclip"]:
            
            pygg.write_int(NoClip, 4)
            
           
        
        imgui.spacing()
        current_height = pygg.read_float(Height)
       
        changed, float_val = imgui.slider_float("Height Selector", current_height, 0.0, 100.0)
        if changed:
            pygg.write_float(Height, float_val)
        
        if self.active["Combat Shotgun Inf Ammo"]:
            pygg.write_int(CsAmmo, 999999999)
            
        if self.active["Bhop"]:
            #00680F46
            pygg.write_int(Jump, 1066964608)
            

        if self.active["Grenades Inf"]:
            pygg.write_int(Grenade, 999999999)
            
        if self.active["Fast fire Sniper"]:
            pygg.write_bool(FastFireSP, True)
        
        if self.active["Armor Inf"]:
            pygg.write_int(Armor, 999999999)
        
        if self.active["Fast fire Combat Shotgun"]:
            pygg.write_bool(FastFireSH, True)
        
        if self.active["Fast fire Assault Rifle"]:
            pygg.write_bool(FastFireAS, True)
        
        if self.active["Assault Rifle Inf Ammo"]:
            pygg.write_int(AsAmmo, 9999999999)
            
        if self.active["Health Inf"]:
            pygg.write_int(Health, 9999999999)
            
        if self.active["Auto shoot"]:
            pygg.write_bool(AutoShoot, True)
       
            
        if self.active["Pistol Inf Ammo"]:
            pygg.write_int(PPAmmo, 9999999999)
            
        def world_to_screen(matrix, pos):
            clip = Vec3()
            ndc = Vec2()
            result = Vec3()

            clip.z = pos.x * matrix[3] + pos.y * matrix[7] + pos.z * matrix[11] + matrix[15]
            if clip.z < 0.2:
                pass
            clip.x = pos.x * matrix[0] + pos.y * matrix[4] + pos.z * matrix[8] + matrix[12]
            clip.y = pos.x * matrix[1] + pos.y * matrix[5] + pos.z * matrix[9] + matrix[13]
            ndc.x = clip.x / clip.z
            ndc.y = clip.y / clip.z
            try:
                io = imgui.get_io()
                result.x = (io.display_size.x / 2 * ndc.x) + (ndc.x + io.display_size.x / 2)
                result.y = -(io.display_size.y / 2 * ndc.y) + (ndc.y + io.display_size.y / 2)
                result.z = clip.z
            except Exception as e:
                pass

            return result
       
       
        def calculate_distance(local_player_pos, entity_player_pos):
            io = imgui.get_io()
            distance = (((local_player_pos.x - entity_player_pos.x) * io.display_size.x)**2 + ((local_player_pos.y - entity_player_pos.y) * io.display_size.y)**2 + (local_player_pos.z - entity_player_pos.z)**2)**0.5
            return distance

        if self.active["Player ESP"]:
            
            imgui.set_next_window_bg_alpha(0.8)  
            imgui.begin("Player ESP", False, imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_BACKGROUND | imgui.WINDOW_NO_INPUTS)
            
            io = imgui.get_io()
            
            if player_count > 1:
                entities = pygg.read_ctype(pygg.read_int(module_base + 0x18AC04), (player_count * ctypes.c_int)())[1:]
                
                for ent_addr in entities:
                    ent_obj = pygg.read_ctype(ent_addr, Entity())
                    try:
                        
                        if ent_obj.health > 0:
                        
                            try:
                                wts = world_to_screen(matrix, ent_obj.pos)
                                if wts.z >= 0.1:  #
                                    team_color = imgui.get_color_u32_rgba(0, 0, 1, 1) if ent_obj.team else imgui.get_color_u32_rgba(1, 0, 0, 1)
                                    text_color = imgui.get_color_u32_rgba(1, 1, 1, 1)if ent_obj.team else imgui.get_color_u32_rgba(1, 1, 1, 1)
                                    box_color = imgui.get_color_u32_rgba(1, 1, 0, 1)  
                                    
                                    if ent_obj.health > 75:
                                        health_color = imgui.get_color_u32_rgba(0, 1, 0, 1) if ent_obj.team else imgui.get_color_u32_rgba(0, 1, 0, 1)
                                    elif ent_obj.health > 50:
                                        health_color = imgui.get_color_u32_rgba(1, 1, 0, 1) if ent_obj.team else imgui.get_color_u32_rgba(1, 1, 0, 1)
                                    elif ent_obj.health > 25:
                                        health_color = imgui.get_color_u32_rgba(1, 0.5, 0, 1) if ent_obj.team else imgui.get_color_u32_rgba(1, 0.5, 0, 1)
                                    else:
                                        health_color = imgui.get_color_u32_rgba(1, 0, 0, 1)  if ent_obj.team else imgui.get_color_u32_rgba(1, 0, 0, 1)
                                        
                                   
                                    scale_factor = 1 / (wts.z * 0.1) if wts.z > 1 else 1
                                    box_height = 280 * scale_factor 
                                    box_width = 140 * scale_factor  
                                    box_min = (wts.x - box_width / 2, wts.y - box_height / 2)
                                    box_max = (wts.x + box_width / .9, wts.y + box_height / .9)
                                    health_line_min = (box_min[0] - 3 * scale_factor, box_min[1])
                                    health_line_max = (box_min[0] - 3 * scale_factor, box_min[1] + box_height * (ent_obj.health / 100))
                                    imgui.get_window_draw_list().add_line(io.display_size.x / 2, io.display_size.y / 2, wts.x, wts.y, team_color, 1.0)
                                    imgui.get_window_draw_list().add_rect(box_min[0], box_min[1], box_max[0], box_max[1], team_color, thickness=2.0)
                                    imgui.get_window_draw_list().add_line(health_line_min[0], health_line_min[1], health_line_max[0], health_line_max[1], health_color, 2.3)
                                    text_width, text_height = imgui.calc_text_size(ent_obj.name.decode('utf-8'))
                                    imgui.get_window_draw_list().add_text(wts.x - text_width / 3.5, box_min[1] - text_height / 3 - 10, text_color, ent_obj.name.decode('utf-8'))
                                   
                                    
                            except Exception as e:
                                print(f"An exception occurred: {str(e)}") 
                    except Exception as e:
                        pass
            imgui.end()
                   
        
        
           
        
       
        imgui.end()
        
        
    def set_window_click_through(self, hwnd, click_through):
        GWL_EXSTYLE = -20
        WS_EX_LAYERED = 0x00080000
        WS_EX_TRANSPARENT = 0x00000020
        LONG_PTR = c_long

        exStyle = LONG_PTR(windll.user32.GetWindowLongPtrW(hwnd, GWL_EXSTYLE))
        
        if click_through:
            new_style = exStyle.value | WS_EX_LAYERED | WS_EX_TRANSPARENT
        else:
            new_style = exStyle.value & ~(WS_EX_LAYERED | WS_EX_TRANSPARENT)

        windll.user32.SetWindowLongPtrW(hwnd, GWL_EXSTYLE, new_style)

    def render_frame(self, impl, window, font):
        glfw.poll_events()
        impl.process_inputs()
        imgui.new_frame()

        gl.glClearColor(0, 0, 0, 0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        if font is not None:
            imgui.push_font(font)
        self.Pygg_Frame()
        if font is not None:
            imgui.pop_font()

        
        self.window = window
        glfw.set_window_attrib(window, glfw.FLOATING, glfw.TRUE)
        
       
        hwnd = glfw.get_win32_window(window)
        is_interacting_with_imgui = (
            imgui.is_any_item_hovered() or
            imgui.is_any_item_active() or
            imgui.is_any_item_focused() or
            imgui.is_window_hovered()
        )

        self.set_window_click_through(hwnd, not is_interacting_with_imgui)

        imgui.render()
        impl.render(imgui.get_draw_data())
        glfw.swap_buffers(window)

        
    def main(self):
        PID = pygg.get_process_id("ac_client.exe")
        
        pygg.change_process_title(PID, 5, False, "Pygg - Nano")
        
        init = pygg.init_memory(PID)
        self.PID = PID
        
        imgui.create_context()
        window = self.impl_glfw_init()

        impl = GlfwRenderer(window)

        io = imgui.get_io()
        impl.refresh_font_texture()

        good_font = io.fonts.add_font_default()
        impl.refresh_font_texture()

        while not glfw.window_should_close(window):
            self.render_frame(impl, window, good_font)
            
            if glfw.get_key(window, glfw.KEY_RIGHT_SHIFT) == glfw.PRESS:
                glfw.focus_window(window)

        impl.shutdown()
        glfw.terminate()
        pygg.close_handle()


if __name__ == "__main__":
    PyGGExternal().main()
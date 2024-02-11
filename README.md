# 💀 PyGG
**PyGG** is a Python library for making externals that bypass **(AC / AT)**


## Features
**PyGG** provides a wide range of functions tailored for manipulating game processes and memory, all while maintaining a level of stealth to bypass anti-cheat systems. Below is a detailed list of the capabilities provided by the **PyGG** API, Using XOR for obfuscating the values to trick **AC / AT**

### Process Management
 - ``get_process_id(process_name: str)`` : Retrieve the process ID of an active window based on the process name.

 - ``change_process_title(pid: int, title_length=5, random_title=True, window_title="Pygg")`` : Alter the title of an active window process in a loop, defaulting to a 5-second interval.

 - ``modify_privileges(current_process=None)`` : Adjust the security descriptor's privileges of the target process.

 - ``set_window_icon(pid: int, icon_path: str)`` : Update a window's icon to the one specified by the icon path.

 - ``create_junk_code(start_range=10, max_range=20)`` : Generate junk code to obscure the operation from some anti-cheat detection mechanisms.

### Memory Manipulation
 - ``write_bool(address, value)`` : Write a boolean value to a specified memory address.

 - ``write_string(address, value)`` : Write a string value to a specified memory address.

 - ``write_memory(address, value)`` : Write a generic value to a specified memory address.

 - ``write_float(address, value)`` : Write a float value to a specified memory address.

 - ``write_double(address, value)`` : Write a double value to a specified memory address.

 - ``write_longlong(address, value)`` : Write a long long (int64) value to a specified memory address.

### Memory Reading
 - ``read_string(address, is_obfuscated=True)`` : Read a string value from a specified memory address, with optional obfuscation.

 - ``read_bool(address)`` : Read a boolean value from a specified memory address.

 - ``read_int(address)`` : Read an integer value from a specified memory address.

 - ``read_float(address)`` : Read a float value from a specified memory address.

 - ``read_qword(address)`` : Read a qword (int64) value from a specified memory address.

 - ``read_memory(address)`` : Read a generic value from a specified memory address.

 - ``read_double(address)`` : Read a double value from a specified memory address.

 - ``read_longlong(address)`` : Read a long long (int64) value from a specified memory address.
 
 - ``create_pattern(address, size)`` : Creates a byte pattern for the specified memory address.

 - ``aob_scan(pattern, multiple_address)`` Scan process memory for addresses matching byte patterns in memory.

### Lua VM
 - ``lua_version()``: Returns the lua Env version
 - ``lua_globals()``: Returns lua set globals example: lua_globals().b will return the value of the set global b 
 - ``lua_set_memory(max_memory: int)``: It Will set lua vm max memory to the env
 - ``lua_memory_used()``: Returns memory used by the lua env
 - ``lua_exec(str)``: Will execute lua, accepts multi line strings
 - ``lua_eval(str)``: Will execute lua, accepts multi line strings (same as exec kinda)

### Process Cleanup
 - ``close_handle()`` : Close the handle to the process, ensuring a clean detachment.

 - ``allocate_memory(size)`` : Allocate a specified amount of memory to the target process, with a default allocation size of 124 bytes.

 - ``refresh_handle(delay)`` : Reopens the open handle with a delay default (.5)

## Examples

**Assualt Cube ingame Imgui + Pygg Example**
<img src="https://cdn.discordapp.com/attachments/1160388470989135922/1199396061052141699/image.png?ex=65c263a0&is=65afeea0&hm=bcdc060a672d667f15fe505de9594eb6efcf799fe54c723221046f80078f7445&"></img>


**Pattern Creation & Aob scanning**
<img src="https://i.imgur.com/LKxCxdX.png"></img>

**Assualt Cube ingame Imgui ESP + Pygg Example**
<img src="https://media.discordapp.net/attachments/1160388470989135922/1199395904495550464/image.png?ex=65c2637b&is=65afee7b&hm=67da61cddeb7326a69de46d21724211acfbfb8ed521ea6b3cb7c9d9974b606f3&=&format=webp&quality=lossless&width=705&height=376"></img>



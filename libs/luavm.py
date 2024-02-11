import lupa.lua54
from lupa import LuaRuntime
from libs.logger import Logger

class Luavm:
    def __init__(self) -> None:
        self.lua_version = lupa.LUA_VERSION
        self.lupa_compiler = lupa.LuaRuntime().lua_implementation
        self.lua = LuaRuntime(unpack_returned_tuples=True, max_memory=0)
        

    def lua_exec(self, _lua: str):
        if isinstance(_lua, str):
            _lua = _lua.splitlines()
        for line in _lua:
            try:
                self.lua.execute(line)
            except (lupa.lua54.LuaError, lupa.LuaMemoryError) as _lua_error:
                exit(Logger.error(f"Pygg Luavm Error - {_lua_error}"))

    def lua_eval(self, _eval_lua: str):
        if isinstance(_eval_lua, str):
            _eval_lua = _eval_lua.splitlines()
        for lines in _eval_lua:
            try:
                self.lua.eval(lines)
            except (lupa.lua54.LuaError, lupa.LuaMemoryError) as _lua_error:
                exit(Logger.error(f"Pygg Luavm Error - {_lua_error}"))

    def lua_globals(self):
        return self.lua.globals()
    
    def lua_memory_used(self):
        return self.lua.get_memory_used()
    
    def lua_set_memory(self, _value: int):
        return self.lua.set_max_memory(_value)
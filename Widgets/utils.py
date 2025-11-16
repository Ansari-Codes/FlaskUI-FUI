from datetime import datetime as dt
from typing import Any, Literal
from colorama import init, Fore, Back, Style

class Logger:
    def __init__(self) -> None:
        self.colors = {
            "debug": lambda x: Back.LIGHTBLACK_EX + Fore.WHITE + x + Style.RESET_ALL,
            "error": lambda x: Back.RED + Fore.WHITE + x + Style.RESET_ALL,
            "success": lambda x: Back.GREEN + Fore.WHITE + x + Style.RESET_ALL,
            "info": lambda x: Back.BLUE + Fore.WHITE + x + Style.RESET_ALL,
            "warning": lambda x: Back.YELLOW + Fore.BLACK + x + Style.RESET_ALL,
        }
        init(True)
    
    def log(self, msg: str, type: Literal["debug", "error", "success", "info", "warning"] = "info"):
        t = self.colors.get(type, lambda x: x)(type.upper().center(7))
        d = " | " + dt.now().time().__str__()
        msg = " | " + msg
        line = t + d + msg
        print(line)
    
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        self.log(*args)

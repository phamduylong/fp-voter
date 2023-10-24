import threading
from enum import Enum
 
class AlertType(Enum):
    ERROR = "#f00"
    WARNING = "#ff0"
    SUCCESS = "#0f0"
    
def show_alert(type, msg, timeout, error_string_elem, error_msg_elem):
    error_string_elem.set(msg)
    match type:
        case AlertType.ERROR:
            error_msg_elem.config(fg=AlertType.ERROR.value)
        case AlertType.WARNING:
            error_msg_elem.config(fg=AlertType.WARNING.value)
        case AlertType.SUCCESS:
            error_msg_elem.config(fg=AlertType.SUCCESS.value)
    error_msg_elem.pack(pady=60)
    t = threading.Timer(timeout, pop_result, args=(error_msg_elem,))
    t.start()

def pop_result(element):
    hide(element)
            
def hide(element):
    element.pack_forget()
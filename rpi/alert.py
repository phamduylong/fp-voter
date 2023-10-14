import threading
from enum import Enum
 
class Alert_Type(Enum):
    ERROR = "#f00"
    WARNING = "#ff0"
    SUCCESS = "#0f0"
    
def show_alert(alert_type, msg, timeout, error_string_elem, error_msg_elem):
    error_string_elem.set(msg)
    match alert_type:
        case Alert_Type.ERROR:
            error_msg_elem.config(fg=Alert_Type.ERROR.value)
        case Alert_Type.WARNING:
            error_msg_elem.config(fg=Alert_Type.WARNING.value)
        case Alert_Type.SUCCESS:
            error_msg_elem.config(fg=Alert_Type.SUCCESS.value)
    error_msg_elem.pack(pady=30)
    t = threading.Timer(timeout, pop_result, args=(error_msg_elem,))
    t.start()

def pop_result(element):
    hide(element)
            
def hide(element):
    element.pack_forget()
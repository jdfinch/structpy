
from inspect import currentframe

def code_line_no():
    caller_frame = currentframe().f_back
    return caller_frame.f_lineno

print(code_line_no())
print(code_line_no())
print(code_line_no())
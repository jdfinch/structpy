
import time as std_time
import math

f = open('speed.txt', 'w')

recording = False
print_fn = print

session_module = None

def summary_string(item, n=10):
    string = str(item)
    if len(string) > n:
        return string[:n-3] + '...' + string[-3:]
    else:
        return string

def timed(func):
    def inner(*args, **kwargs):
        begin = std_time.time()
        func(*args, **kwargs)
        end = std_time.time()
        arg_strs = [summary_string(x) for x in args]
        kwarg_strs = [str(k) + '=' + summary_string(v) for k, v in kwargs.items()]
        if arg_strs and kwarg_strs:
            kwarg_str = ', '
        if kwarg_strs:
            kwarg_str += ', '.join(kwarg_strs)
        else:
            kwarg_str += ''
        return func.__name__ + '(' + ', '.join(arg_strs) \
            + kwarg_str + '): ' + '%0.5f' % (end-begin)
    return inner

def time(expression, globals=None):
    if globals is None:
        globals = vars(session_module)
    begin = std_time.time()
    error_msg = ''
    try:
        eval(expression, globals)
        end = std_time.time()
    except Exception as e:
        error_msg = str(e) + '\n'
        end = std_time.time()
    display = 'Timed test of expression:\n'
    display += expression + '\n'
    display += '==> ' + '%0.5f' % (end - begin) + 's\n'
    display += error_msg
    print_fn(display)
    return display

def header(text):
    print_fn()
    print_fn(text)
    return '\n' + text + '\n'

def footer(text):
    print_fn(text)
    print_fn()
    return text + '\n\n'

def record(*args, sep=' ', end='\n'):
    f.write(' '.join([str(a) for a in args]) + '\n')

def print_and_record(*args, sep=' ', end='\n'):
    print(*args, sep=sep, end=end)
    record(*args, sep=sep, end=end)

def toggle_record():
    global print_fn
    global recording
    recording = not recording
    if not recording:
        print_fn = print
    else:
        print_fn = print_and_record

def log_to(file_name):
    global f
    f.close()
    f = open(file_name, 'w')
    return f

def close_file():
    f.close()

def make_session(module, file_name=None):
    if file_name:
        log_to(file_name)
    global session_module
    session_module = module
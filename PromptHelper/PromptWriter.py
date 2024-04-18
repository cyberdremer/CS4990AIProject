
import time

def write_out_prompt(prompt):
    date = time.strftime("%Y%m%d -%H%M%S")
    file = open(date, 'x')
    file.write(prompt)

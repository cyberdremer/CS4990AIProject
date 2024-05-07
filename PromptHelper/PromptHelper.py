import json
import logging
from logging import *
import math

delimiter = "####"
item_delimter = "|"


def construct_system_message():
    system_message = f""" You are a customer service assistant at a computer store. Your job is to help the customer 
    pick out computer components for their new computer build. You will be given a part's list go off of. Ensure that 
    you do not go above the user's budget. Also ensure that each build has one video-card, one cpu, one compatible 
    motherboard(AMD 5000 series uses AM4 chipset and AMD 7000 series uses AM5 chipset, Intel uses LGA1700 chipset), one PSU, one computer case, at least one unit of memory, 
    one cpu-cooler, one SSD. Do not go over budget. Do not give a total cost.
        
        
        Output a python list of objects where each object has the following format and each object is delimited with {item_delimter}:
        {{Name of item : Price of item in dollars}}{item_delimter}
        
        The customer's query will be delimited using {delimiter}
        """
    return system_message


def construct_assistant_message(parts_list):
    assistant_message = f"""
        This is parts list that the user can choose, which is formatted as follows: PART_TYPE: PARTS
"""
    for component_type, component in parts_list.items():
        assistant_message += f"{component_type.upper()}:\n"
        for component_details in component:
            assistant_message += json.dumps(component_details) + "\n"
        assistant_message += "\n"
    return assistant_message


def construct_user_prompt(user_choices):
    user_message = f"""
    I would like to build a {user_choices['usage']} computer. 
    My budget is ${user_choices['budget']}. I would like a video-card from {user_choices['gpu_vendor']}.
    In addition, I would like a cpu from {user_choices['cpu_vendor']}. 
    I will also need a PC case, compatible motherboard, at minimum 8GB of RAM and at minimum 500GB of storage. 
"""

    return user_message


def construct_input_for_ai(ai_input):
    prompt = [{'role': 'system',
               'content': ai_input['system_message']},
              {'role': 'assistant',
               'content': ai_input['assistant_message']},
              {'role': 'user',
               'content': f"{delimiter} {ai_input['user_message']} {delimiter}"}]
    return prompt


def construct_prompt_dictionary(*args):
    prompt_dictionary = {}
    keys = ['user_message', 'system_message', 'assistant_message']
    loopCnt = 0

    for arg in args:
        prompt_dictionary[keys[loopCnt]] = arg
        loopCnt += 1

    return prompt_dictionary


def construct_user_prompt_dictionary(args_list):
    user_dictionary = {}
    keys = ['gpu_vendor', 'cpu_vendor', 'usage', 'budget']
    loopCnt = 0

    for arg in args_list:
        user_dictionary[keys[loopCnt]] = arg
        loopCnt += 1

    return user_dictionary


def format_output(ai_output) -> str:
    try:
        output = ai_output.replace("[", "").replace("]", "")
        tokens = output.split("|")
        final_output = ""
        total_price = 0
        for token in tokens:
            if len(token) > 2:
                temp = token.replace("{", "").replace("}", "")
                name, price = temp.split(":")
                total_price += float(price)
                price = "$" + price
                final_output += name + ": " + price + "\n"

        final_output += "\nTotal cost of build: $" + str(round(total_price, 2))
        return final_output
    except ValueError as valerr:
        logging.error(valerr)
        raise


def construct_final_prompt(user_choices, assistant_prompt) -> str:
    user_prompt_dictionary = construct_user_prompt_dictionary(user_choices)
    user_prompt = construct_user_prompt(user_prompt_dictionary)
    system_message = construct_system_message()

    prompt_dic = construct_prompt_dictionary(user_prompt, system_message, assistant_prompt)
    ai_prompt = construct_input_for_ai(prompt_dic)
    return ai_prompt

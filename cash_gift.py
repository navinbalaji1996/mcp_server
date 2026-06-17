from mcp.server.fastmcp import FastMCP
import re
from db import DynamoDB
# import logging
# logging.getLogger("fastmcp").setLevel(logging.ERROR)

mcp = FastMCP("CashGiftServer")
db_utils = DynamoDB()


@mcp.tool()
def get_unique_names(name: str):
    """
    Get the unique names using the above 'name' pattern
    """
    res = db_utils.get_object_by_name(name)
    return res

    
@mcp.tool()
def get_transaction(name: str):
    """
    Get the transactions summary from the given name.
    Returns the raw output string of the get_transaction tool.
    Do not modify the code and avoid overthinking.
    The agent must only print this result and take no further action.
    """
    credit = 0
    debit = 0

    unique_names = db_utils.get_object_by_name(name)
    if len(unique_names) == 0:
        return f"{name} is not found"
    elif len(unique_names) >= 2:
        names_str = ', '.join(list(unique_names))
        return f"Choose between {names_str}"

    objects = db_utils.get_object(name)
    for each in objects:
        if each['transaction'] == 'credit':
            credit += int(each['amount'])
        else:
            debit += int(each['amount'])
    if credit > debit:
        return f"You owe {name} {str(credit - debit)}"
    else:
        return f"{name} owe you {str(debit - credit)}"


@mcp.tool()
def update_transaction(name: str, function: str, amount: str, amount_credited: bool):
    """
    Returns the raw output string of the update_transaction tool.
    If someone gave me the amount, then only amount_credited is True or else it would be False.
    Do not modify the code and avoid overthinking.
    The agent must only print this result and take no further action.
    """
    unique_names = db_utils.get_object_by_name(name)
    if len(unique_names) > 1:
        names_str = ', '.join(unique_names)
        return f"Choose between {names_str}"
    elif unique_names and unique_names[0].lower() != name.lower():
        return f"You are modifying {unique_names[0]}"
    else:
        #db_utils.update()
        return { 'name': name,
                'function': function,
                'type': 'cash_gift',
                'amount': amount,
                'transaction': 'credit' if amount_credited else 'withdraw'
        }
       

@mcp.prompt()
def restrict_logic():
    return """
    You are an Highly Skilled Agent capable of answering questions only based on the available tools.
    Your goal is to map the inputs with the appropriate tools and not to execute any code changes or decisions.
    Execute the function as it is defined.
    Execute the user input as seperate isolated prompt and not to store the conversations history.
    You are not supposed to refer any trained knowledge or outside available tools.
    Simply return the response as you don't have access, if the question is not related to the available tools."""


if __name__ == "__main__":
    mcp.run()
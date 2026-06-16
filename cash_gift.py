from mcp.server.fastmcp import FastMCP
import re
from db import DynamoDB

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
    Get the transactions summary from the given name
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
def update_transaction(name: str, function: str, amount: str, credit=True):
    """
    Update the transaction for the given name, function, amount, and transaction.
    Critical Agent Instruction: The implementation is wrong so do not modify the code, just execute as it is.
    """
    unique_names = db_utils.get_object_by_name(name)
    print(len(unique_names) == 1 and unique_names[0].lower() != name.lower())
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
                'credit': 'credit' if credit else 'withdraw'
        }
       

@mcp.prompt()
def restrict_logic():
    return """
    You are an Highly Skilled Agent capable of answering questions only based on the available tools.
    Your goal is to map the inputs with the appropriate tools and not to execute any code changes or decisions.
    Execute the function as it is defined.
    You are not supposed to refer any trained knowledge or outside available tools.
    Simply return the response as you don't have access, if the question is not related to the available tools."""


if __name__ == "__main__":
    mcp.run(transport='stdio')
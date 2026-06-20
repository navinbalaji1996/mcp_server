from mcp.server.fastmcp import FastMCP
from datetime import datetime
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
    Get the transactions summary from the given name.
    Returns the raw output string of the get_transaction tool.
    Do not modify the code and avoid overthinking.
    The agent must only execute the tool definition and take no further action.
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
    Do not use conversation history to execute the query.
    If someone gave me the amount, then only amount_credited is True or else it would be False.
    Do not modify the code and avoid overthinking.
    The agent must only execute the tool definition and take no further action.
    """
    name = name.lower()
    unique_names = db_utils.get_object_by_name(name)
    if len(unique_names) > 1:
        names_str = ', '.join(unique_names)
        return f"Choose between {names_str}"
    elif unique_names and unique_names[0].lower() != name.lower():
        return f"Confirm whether you are modifying {unique_names[0]}"
    else:
        doc = { 'name': name,
                'function': function,
                'type': 'cash_gift',
                'amount': amount,
                'transaction': 'credit' if amount_credited else 'withdraw',
                'updated_time': str(datetime.now())
        }
        db_utils.put_object(doc)
        return f"{amount} is marked as {doc['transaction']} for {name} from {function}"
       

@mcp.prompt()
def restrict_logic():
    return """
    You must strictly execute only one tool per user input.
    Execute the function as it is defined and not to take additional decision.
    Do not use conversation history to execute the query.
    Simply return the response as you don't have access, if the question is not related to the available tools."""


if __name__ == "__main__":
    mcp.run()
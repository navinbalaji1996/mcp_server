from mcp.server.fastmcp import FastMCP
import re
from db import DynamoDB

mcp = FastMCP("CashGiftServer")
db_utils = DynamoDB()

@mcp.tool()
def get_transaction(name: str): 
    # Get the transactions from the name
    credit = 0
    debit = 0
    objects = db_utils.get_object()
    res = []
    for each in objects:
        if re.search(name, each['name'].lower()):
            res.append(each['name'])
            if each['transaction'] == 'credit':
                credit += int(each['amount'])
            else:
                debit += int(each['amount'])
    if credit > debit:
        return f"You owe {name} {str(credit - debit)}"
    else:
        return f"{name} owe you {str(debit - credit)}"


@mcp.tool()
def update_transaction(name: str, function: str, amount: str):
    # Update the transaction for the given name, function, amount, and transaction
    return {
        'name': name,
        'function': function,
        'amount': amount,
    }

@mcp.prompt()
def restrict_logic():
    return """
    You are an Highly Skilled Agent capable of answering questions only based on the available tools.
    You are not supposed to refer any trained knowledge or outside available tools.
    Simply return the response as you don't have access, if the question is not related to the available tools."""


if __name__ == "__main__":
    mcp.run(transport='stdio')
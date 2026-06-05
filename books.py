from mcp.server.fastmcp import FastMCP

# Create an MCP server instance
mcp = FastMCP("BooksServer")

AUTHOR_BOOKS = {
    'Navin': 'Ponniyan Selvan',
    'Kesharvi': 'Nayagan',
    'Vihana': 'Alaipauthey'
}

@mcp.tool()
def get_book_by_author(author: str):
    '''Returns the book by the specified author.'''
    return AUTHOR_BOOKS.get(author, "Book not found")


@mcp.tool()
def get_books():
    '''Returns a list of books.'''
    return list(AUTHOR_BOOKS.values())

@mcp.prompt()
def restrict_logic():
    return """
    You are an Highly Skilled Agent capable of answering questions only based on the available tools.
    You are not supposed to refer any trained knowledge or outside available tools.
    Simply return the response as you don't have access, if the question is not related to the available tools."""


if __name__ == "__main__":
    # Initialize the server using the Stdio transport
    mcp.run(transport='stdio')
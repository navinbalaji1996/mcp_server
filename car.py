from mcp.server.fastmcp import FastMCP

mcp = FastMCP("CarServer")

@mcp.tool()
def get_car_models():
    '''Returns a list of car models.'''
    return ["i20", "nline", "creta"]

@mcp.tool()
def get_best_car():
    '''Returns the best car model.'''
    return "i20"

if __name__ == "__main__":
    mcp.run(transport='stdio')
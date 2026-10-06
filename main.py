import random
from fastmcp import FastMCP

# create a FastMCP server instanace
mcp = FastMCP(name="Demo Server")

@mcp.tool
def rool_dice(n_dice: int=1) -> list[int]:
    """
    roll n_dice 6-sided dice and return the result
    """
    return [random.randint(1,6) for _ in range(n_dice)]

@mcp.tool
def add_numbers(a:float , b:float) ->float:
    """ Add two numbers together"""
    return a + b

if __name__ == "__main__":
    mcp.run()
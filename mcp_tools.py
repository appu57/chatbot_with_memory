from __future__ import annotations
from fastmcp import FastMCP

mcp = FastMCP("arithmethic")

def _as_number(x):
    """Accepts int/float or numeric strings; raise clean errors otherwise"""
    if isinstance(x, (int, float)):
        return float(x)
    if isinstance(x, str):
        return float(x.strip())
    
    raise TypeError("Expected a number (int/float or numeric string)")


@mcp.tool()
async def add(a:float, b:float)->float:
    """return a + b """
    return _as_number(a) + _as_number(b)

@mcp.tool()
async def subtract(a:float, b:float)->float:
    """Return a -b """
    return _as_number(a) - _as_number(b)

@mcp.tool()
async def multiple(a:float, b:float)->float:
    """Return a * b"""
    return _as_number(a) * _as_number(b)


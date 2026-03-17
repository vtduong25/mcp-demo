from fastmcp import FastMCP
import json
import os
from typing import Any, Optional

import httpx
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP("Rebrickable MCP")

REBRICKABLE_BASE = "https://rebrickable.com/api/v3"


def _api_key() -> str:
    key = os.environ.get("REBRICKABLE_API_KEY", "").strip()
    if not key:
        raise ValueError(
            "REBRICKABLE_API_KEY is not set. Get a key at https://rebrickable.com/api/v3/docs/"
        )
    return key


def _get(path: str, params: Optional[dict[str, Any]] = None) -> dict[str, Any]:
    """Call Rebrickable API GET; raises on error."""
    params = dict(params) if params else {}
    with httpx.Client(
        base_url=REBRICKABLE_BASE,
        headers={"Authorization": f"key {_api_key()}"},
        timeout=30.0,
    ) as client:
        r = client.get(path, params=params)
        r.raise_for_status()
        return r.json()


# ---------------------------
# Rebrickable API tools
# ---------------------------
@mcp.tool
def rebrickable_search_sets(
    search: Optional[str] = None,
    theme_id: Optional[str] = None,
    min_year: Optional[int] = None,
    max_year: Optional[int] = None,
    min_parts: Optional[int] = None,
    max_parts: Optional[int] = None,
    page: int = 1,
    page_size: int = 100,
    ordering: Optional[str] = None,
) -> str:
    """Search LEGO sets on Rebrickable. Optional filters: search (name/set_num), theme_id, year range, part count. Returns paginated results."""
    params: dict[str, Any] = {"page": page, "page_size": min(page_size, 1000)}
    if search:
        params["search"] = search
    if theme_id:
        params["theme_id"] = theme_id
    if min_year is not None:
        params["min_year"] = min_year
    if max_year is not None:
        params["max_year"] = max_year
    if min_parts is not None:
        params["min_parts"] = min_parts
    if max_parts is not None:
        params["max_parts"] = max_parts
    if ordering:
        params["ordering"] = ordering
    data = _get("/lego/sets/", params)
    return json.dumps(data, indent=2)


@mcp.tool
def rebrickable_get_set(set_num: str) -> str:
    """Get details for a specific LEGO set by set_num (e.g. '21348-1' or '8043-1')."""
    data = _get(f"/lego/sets/{set_num.strip()}/")
    return json.dumps(data, indent=2)


@mcp.tool
def rebrickable_get_set_parts(
    set_num: str,
    page: int = 1,
    page_size: int = 100,
    inc_part_details: bool = False,
) -> str:
    """Get the list of parts in a LEGO set. Use inc_part_details=True for full part info."""
    params: dict[str, Any] = {"page": page, "page_size": min(page_size, 1000)}
    if inc_part_details:
        params["inc_part_details"] = 1
    data = _get(f"/lego/sets/{set_num.strip()}/parts/", params)
    return json.dumps(data, indent=2)


@mcp.tool
def rebrickable_list_colors(
    page: int = 1,
    page_size: int = 100,
    ordering: Optional[str] = None,
) -> str:
    """List LEGO colors from Rebrickable catalog."""
    params: dict[str, Any] = {"page": page, "page_size": min(page_size, 1000)}
    if ordering:
        params["ordering"] = ordering
    data = _get("/lego/colors/", params)
    return json.dumps(data, indent=2)


@mcp.tool
def rebrickable_get_color(color_id: str) -> str:
    """Get details for a specific LEGO color by ID."""
    data = _get(f"/lego/colors/{color_id.strip()}/")
    return json.dumps(data, indent=2)


@mcp.tool
def rebrickable_search_parts(
    search: Optional[str] = None,
    part_cat_id: Optional[int] = None,
    color_id: Optional[int] = None,
    part_num: Optional[str] = None,
    part_nums: Optional[str] = None,
    page: int = 1,
    page_size: int = 100,
    ordering: Optional[str] = None,
    inc_part_details: bool = False,
) -> str:
    """Search LEGO parts. part_nums: comma-separated list for multiple (e.g. '3001,3002')."""
    params: dict[str, Any] = {"page": page, "page_size": min(page_size, 1000)}
    if search:
        params["search"] = search
    if part_cat_id is not None:
        params["part_cat_id"] = part_cat_id
    if color_id is not None:
        params["color_id"] = color_id
    if part_num:
        params["part_num"] = part_num
    if part_nums:
        params["part_nums"] = part_nums
    if ordering:
        params["ordering"] = ordering
    if inc_part_details:
        params["inc_part_details"] = 1
    data = _get("/lego/parts/", params)
    return json.dumps(data, indent=2)


@mcp.tool
def rebrickable_get_part(part_num: str) -> str:
    """Get details for a specific LEGO part by part number (e.g. '3001')."""
    data = _get(f"/lego/parts/{part_num.strip()}/")
    return json.dumps(data, indent=2)


@mcp.tool
def rebrickable_list_themes(
    page: int = 1,
    page_size: int = 100,
    ordering: Optional[str] = None,
) -> str:
    """List LEGO themes (e.g. Star Wars, City)."""
    params: dict[str, Any] = {"page": page, "page_size": min(page_size, 1000)}
    if ordering:
        params["ordering"] = ordering
    data = _get("/lego/themes/", params)
    return json.dumps(data, indent=2)


@mcp.tool
def rebrickable_get_theme(theme_id: int) -> str:
    """Get details for a specific LEGO theme by ID."""
    data = _get(f"/lego/themes/{theme_id}/")
    return json.dumps(data, indent=2)


@mcp.tool
def rebrickable_search_minifigs(
    search: Optional[str] = None,
    in_set_num: Optional[str] = None,
    in_theme_id: Optional[int] = None,
    min_parts: Optional[int] = None,
    max_parts: Optional[int] = None,
    page: int = 1,
    page_size: int = 100,
    ordering: Optional[str] = None,
) -> str:
    """Search LEGO minifigs. Filter by search, set, theme, or part count."""
    params: dict[str, Any] = {"page": page, "page_size": min(page_size, 1000)}
    if search:
        params["search"] = search
    if in_set_num:
        params["in_set_num"] = in_set_num
    if in_theme_id is not None:
        params["in_theme_id"] = in_theme_id
    if min_parts is not None:
        params["min_parts"] = min_parts
    if max_parts is not None:
        params["max_parts"] = max_parts
    if ordering:
        params["ordering"] = ordering
    data = _get("/lego/minifigs/", params)
    return json.dumps(data, indent=2)


@mcp.tool
def rebrickable_get_minifig(set_num: str) -> str:
    """Get details for a specific minifig by set_num."""
    data = _get(f"/lego/minifigs/{set_num.strip()}/")
    return json.dumps(data, indent=2)


@mcp.tool
def rebrickable_get_set_minifigs(set_num: str, page: int = 1, page_size: int = 100) -> str:
    """Get minifigs included in a LEGO set."""
    data = _get(
        f"/lego/sets/{set_num.strip()}/minifigs/",
        {"page": page, "page_size": min(page_size, 1000)},
    )
    return json.dumps(data, indent=2)

# --------------------------
# ASGI app initialization
# --------------------------
# stateless_http=True avoids "Session not found" when client reconnects or server restarts
app = mcp.http_app(stateless_http=True)

if __name__ == "__main__":
    import uvicorn
    # -- local STDIO v0
    #mcp.run()
    # local server running on port 8000 v1
    #mcp.run(transport="http", host="127.0.0.1", port=8000)
    # -- https ASGI Streamable v2
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=False)
    
    
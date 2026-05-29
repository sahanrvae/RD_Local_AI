from typing import List, Any

def paginate(items: List[Any], page: int, size: int) -> List[Any]:
    """Returns a paginated slice of a list.

    Args:
        items: The list of items to paginate.
        page: The desired page number (1-based index).
        size: The number of items per page.

    Returns:
        A list containing the items for the requested page.

    Raises:
        ValueError: If page or size are less than 1, or if the items list is empty.
    """
    if not items:
        raise ValueError("The items list cannot be empty.")
    if page < 1 or size < 1:
        raise ValueError("Page and size must be 1 or greater.")

    # Calculate start index (0-based) and end index (0-based)
    start_index = (page - 1) * size
    end_index = start_index + size

    return items[start_index:end_index]

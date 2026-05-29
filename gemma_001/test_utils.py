import pytest
from utils import paginate
from typing import List

# --- Test Cases ---

def test_normal_use():
    """Test pagination in the middle of a large list."""
    items = list(range(100))
    # Request page 3, size 10. Should get items 20 through 29.
    result = paginate(items, 3, 10)
    expected = list(range(20, 30))
    assert result == expected

def test_first_page():
    """Test pagination requesting the first page."""
    items = list(range(10))
    # Request page 1, size 3. Should get items 0, 1, 2.
    result = paginate(items, 1, 3)
    expected = [0, 1, 2]
    assert result == expected

def test_last_page():
    """Test pagination requesting the last page."""
    items = list(range(10))
    # Request page 3, size 4. Should get items 8, 9.
    result = paginate(items, 3, 4)
    expected = [8, 9]
    assert result == expected

def test_empty_list():
    """Test behavior when the input list is empty."""
    items: List[str] = []
    with pytest.raises(ValueError, match="The items list cannot be empty."): 
        paginate(items, 1, 10)

def test_out_of_range_page():
    """Test behavior when requesting a page number that results in an empty slice (too high)."""
    items = list(range(10))
    # Request page 11, size 3. Should return an empty list correctly.
    result = paginate(items, 11, 3)
    assert result == []

# Additional tests for required edge cases
def test_out_of_range_page_too_low():
    """Test behavior when requesting page 0 or negative page number."""
    items = list(range(10))
    with pytest.raises(ValueError, match="Page and size must be 1 or greater."): 
        paginate(items, 0, 3)

def test_invalid_size():
    """Test behavior when size is zero or negative."""
    items = list(range(10))
    with pytest.raises(ValueError, match="Page and size must be 1 or greater."): 
        paginate(items, 1, 0)

def test_large_size():
    """Test pagination where size is larger than the list itself (should return all items)."""
    items = list(range(5))
    result = paginate(items, 1, 10)
    assert result == [0, 1, 2, 3, 4]

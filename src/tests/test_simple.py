def test_simple():
    """Simple test to verify pytest setup"""
    print("Pytest is working!")
    assert True

def test_addition():
    """Testing basic arithmetic"""
    result = 2 + 2
    assert result == 4
    print(f"Addition test passed: 2 + 2 = {result}")
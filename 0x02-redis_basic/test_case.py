# Assuming the Cache class is already defined above

# Create an instance of the Cache class
cache = Cache()

# Define the test cases
TEST_CASES = {
    b"foo": None,  # Test storing a byte string with no conversion
    123: int,  # Test storing an integer and converting it back
    "bar": lambda d: d.decode("utf-8")  # Test storing a string and decoding it
}

# Loop through the test cases
for value, fn in TEST_CASES.items():
    # Store the value in Redis and get the key
    key = cache.store(value)
    
    # Retrieve the value using the key and the conversion function
    retrieved_value = cache.get(key, fn=fn)
    
    # Assert that the retrieved value matches the original value
    assert retrieved_value == value, f"Test failed for value: {value}. Expected {value}, got {retrieved_value}."
    
    print(f"Test passed for value: {value}")

# If all assertions pass, you'll see the message "Test passed for value: ..."


# ==================================================
# TESTS FOR ISSUE #14: USER REGISTRATION VALIDATION
# CONTRIBUTED BY: ELIZABETH
# ==================================================

def test_password_minimum_length_validation(client):
    # 1. ARRANGE: Set up registration details where the password is too short
    invalid_signup_data = {
        'email': 'elizabeth@ualr.edu', # A standard valid email address
        'password': '123'              # This password is only 3 characters long
    }
    
    # 2. ACT: Send a mock form submission (POST) to the registration URL route
    response = client.post('/auth/register', data=invalid_signup_data)
    
    # 3. ASSERT: Verify the exact validation message you read is returned on screen
    # The 'b' before the string converts it to bytes so Python can match the web data
    assert b'Password must be at least 8 characters long.' in response.data


def test_missing_email_validation(client):
    # 1. ARRANGE: Set up registration data leaving the email field completely blank
    blank_email_data = {
        'email': '',                   # Empty string error trigger
        'password': 'SecurePassword123!' # A perfectly valid password string
    }
    
    # 2. ACT: Submit the mock registration form to the backend server
    response = client.post('/auth/register', data=blank_email_data)
    
    # 3. ASSERT: Ensure the application flashes the required email error message
    assert b'Email is required.' in response.data


def test_missing_password_validation(client):
    # 1. ARRANGE: Set up registration data leaving the password field completely blank
    blank_password_data = {
        'email': 'elizabeth@ualr.edu', # A valid email address handle
        'password': ''                 # Empty password string error trigger
    }
    
    # 2. ACT: Submit the mock registration form to the server application
    response = client.post('/auth/register', data=blank_password_data)
    
    # 3. ASSERT: Verify that the backend code catches the empty password string
    assert b'Password is required.' in response.data


def test_duplicate_email_registration_fails(client, app):
    # 1. ARRANGE: Set up two identical registration form packets
    first_signup = {'email': 'duplicate@ualr.edu', 'password': 'SecurePassword123!'}
    second_signup = {'email': 'duplicate@ualr.edu', 'password': 'DifferentPassword456!'}
    
    # 2. ACT: Submit the first registration successfully to populate the database
    client.post('/auth/register', data=first_signup)
    
    # 3. ACT AGAIN: Attempt to register the exact same email a second time
    response = client.post('/auth/register', data=second_signup)
    
    # 4. ASSERT: This will FAIL right now because Daniel's code returns 'Registration failed.'
    # Once Daniel updates his code to be descriptive, this test will turn green!
    assert b'Email is already registered.' in response.data


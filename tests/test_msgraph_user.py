import pytest
import os
from msgraph_user import GraphUser
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
TENANT_ID = os.getenv('TENANT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

# @pytest.mark.asyncio
# async def test_get_user():
#     graph: GraphUser = GraphUser(CLIENT_ID, CLIENT_SECRET, TENANT_ID)
#     testUser = os.getenv('TEST_USER')
#     user = await graph.get_user(testUser)
#     print(f'  User: {user.surname} {user.given_name}')
#     print(f'  ID: {user.id}')
#     print(f'  Email: {user.mail}')
#     print(f'  User Principal Name: {user.user_principal_name}')
#     assert user is not None
#     assert user.mail.lower() == testUser

@pytest.mark.asyncio
async def test_get_user_by_id():
    graph: GraphUser = GraphUser(CLIENT_ID, CLIENT_SECRET, TENANT_ID)
    testUserId = os.getenv('TEST_USER_ID')
    user = await graph.get_user_by_id(testUserId)
    assert user is not None
    if user is not None:
        print(f'  User: {user.surname} {user.given_name}')
        print(f'  ID: {user.id}')
        print(f'  Email: {user.mail}')
        print(f'  User Principal Name: {user.user_principal_name}')
    assert user.id == testUserId
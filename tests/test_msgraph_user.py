import configparser
import pytest
from msgraph_user import GraphUser


# Load settings
config = configparser.ConfigParser()
config.read(['config.cfg', 'config.dev.cfg'])
azure_settings = config['azure']

# @pytest.mark.asyncio
# async def test_get_user():
#     graph: GraphUser = GraphUser(azure_settings)
#     testUser = config['azure']['email']
#     user = await graph.get_user(testUser)
#     print(f'  User: {user.surname} {user.given_name}')
#     print(f'  ID: {user.id}')
#     print(f'  Email: {user.mail}')
#     print(f'  User Principal Name: {user.user_principal_name}')
#     assert user is not None
#     assert user.mail.lower() == testUser

@pytest.mark.asyncio
async def test_get_user_by_id():
    graph: GraphUser = GraphUser(azure_settings)
    testUserId = config['azure']['userId']
    user = await graph.get_user_by_id(testUserId)
    assert user is not None
    if user is not None:
        print(f'  User: {user.surname} {user.given_name}')
        print(f'  ID: {user.id}')
        print(f'  Email: {user.mail}')
        print(f'  User Principal Name: {user.user_principal_name}')
    assert user.id == testUserId
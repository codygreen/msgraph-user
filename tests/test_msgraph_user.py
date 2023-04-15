import configparser
import pytest
from msgraph_user import GraphUser

# Load settings
config = configparser.ConfigParser()
config.read(['config.cfg', 'config.dev.cfg'])
azure_settings = config['azure']

graph: GraphUser = GraphUser(azure_settings)
testUser = config['azure']['email']

@pytest.mark.asyncio
async def test_get_user():
    user_page = await graph.get_user(testUser)
    user = None
    if user_page is not None and user_page.value is not None and len(user_page.value) > 0:
        user = user_page.value[0]
        print(f'  User: {user.surname} {user.given_name}')
        print(f'  ID: {user.id}')
        print(f'  Email: {user.mail}')
        print(f'  User Principal Name: {user.user_principal_name}')
    assert user is not None
    assert user.mail.lower() == testUser

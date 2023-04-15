"""Graph API client"""
from configparser import SectionProxy
from azure.identity.aio import ClientSecretCredential
from kiota_authentication_azure.azure_identity_authentication_provider import (
    AzureIdentityAuthenticationProvider
)
from msgraph import GraphRequestAdapter, GraphServiceClient
from msgraph.generated.users.users_request_builder import UsersRequestBuilder

class User:
    """User object"""
    id: str
    given_name: str
    mail: str
    surname: str
    user_principal_name: str

    def __init__(self):
        self.id = None
        self.given_name = None
        self.mail = None
        self.surname = None
        self.user_principal_name = None

    def __str__(self):
        return f'{self.surname} {self.given_name}'

    def __repr__(self):
        return f'{self.surname} {self.given_name}'

class GraphUser:
    """
    Microsoft Graph API client for the User endpoint
    """
    settings: SectionProxy
    client_credential: ClientSecretCredential
    adapter: GraphRequestAdapter
    app_client: GraphServiceClient

    def __init__(self, config: SectionProxy):
        self.settings = config
        client_id = self.settings['clientId']
        tenant_id = self.settings['tenantId']
        client_secret = self.settings['clientSecret']

        self.client_credential = ClientSecretCredential(tenant_id, client_id, client_secret)
        auth_provider = AzureIdentityAuthenticationProvider(self.client_credential) # type: ignore
        self.adapter = GraphRequestAdapter(auth_provider)
        self.app_client = GraphServiceClient(self.adapter)

    async def get_app_only_token(self):
        graph_scope = 'https://graph.microsoft.com/.default'
        access_token = await self.client_credential.get_token(graph_scope)
        return access_token.token
    
    async def get_user(self, email):
        query_params = UsersRequestBuilder.UsersRequestBuilderGetQueryParameters(
            # Only request specific properties
            select = ['id', 'givenName', 'surname', 'userPrincipalName', 'mail'],

            # set filter
            filter = f"mail eq '{email}'"
        )

        request_config = UsersRequestBuilder.UsersRequestBuilderGetRequestConfiguration(
            query_parameters=query_params
        )

        try:
            user_page = await self.app_client.users.get(request_configuration=request_config)
            if user_page is not None and user_page.value is not None and len(user_page.value) > 0:
                # return user_page.value[0]
                payload = User()
                payload.id = user_page.value[0].__dict__['_id']
                payload.given_name = user_page.value[0].__dict__['_given_name']
                payload.mail = user_page.value[0].__dict__['_mail']
                payload.surname = user_page.value[0].__dict__['_surname']
                payload.user_principal_name = user_page.value[0].__dict__['_user_principal_name']
                return payload
            else:
                return None
        except Exception as e:
            print(e.error.message)
            return None
    
    async def get_user_by_id(self, user_id):
        print(f'Getting user by ID: {user_id}')
        try:
            user = await self.app_client.users_by_id(user_id).get()
            if user is not None:
                payload = User()
                payload.id = user.__dict__['_id']
                payload.given_name = user.__dict__['_given_name']
                payload.mail = user.__dict__['_mail']
                payload.surname = user.__dict__['_surname']
                payload.user_principal_name = user.__dict__['_user_principal_name']
                return payload
            else:
                return None
        except Exception as e:
            # print(e.error.message)
            print(e)
            return None
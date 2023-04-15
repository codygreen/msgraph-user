"""Graph API client"""
from configparser import SectionProxy
from azure.identity.aio import ClientSecretCredential
from kiota_authentication_azure.azure_identity_authentication_provider import (
    AzureIdentityAuthenticationProvider
)
from msgraph import GraphRequestAdapter, GraphServiceClient
from msgraph.generated.users.users_request_builder import UsersRequestBuilder

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
            user = await self.app_client.users.get(request_configuration=request_config)
            return user
        except Exception as e:
            print(e.error.message)
            return None
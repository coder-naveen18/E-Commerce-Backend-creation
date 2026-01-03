from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
import pytest
# reusable fxture for the response 
@pytest.fixture
def create_collection(api_client):
    def do_create_collection(collection):
        return api_client.post('/store/collections', collection)
    return do_create_collection

@pytest.mark.django_db
class TestCreateCollection:
    # @pytest.mark.skip  --- > for skipping the test
    def test_if_user_is_annonymous_returns_401(self):
        # AAA(Arrange, Act, Assert)
        # Arrange

        #Act 
        client = APIClient() 
        response = client.post('/store/collections/', {'title': 'a'})

        #Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

# test for  authenticating user
    def test_if_user_is_not_admin_returns_403(self, api_client, create_collection):
        
        # client = APIClient() ---> in-place of this we can apply the fixture function as a parameter in the function 
        api_client.force_authenticate(user={})
        response = create_collection({'title': 'a'})
        # response = api_client.post('/store/collections/', {'title': 'a'}) ---> it is also repetative so we are now using fixture mentioned above.
        assert response.status_code == status.HTTP_403_FORBIDDEN

# test for invalid user
    def test_if_data_invalid_return_400(self):
        client = APIClient()
        client.force_authenticate(user=User(is_staff=True))
        response = client.post('/store/collections/', {'title': ''})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data ['title'] is not None

# test for valid user
    def test_if_data_valid_return_200(self):
        client = APIClient()
        client.force_authenticate(user=User(is_staff=True))
        response = client.post('/store/collections/', {'title': 'a'})

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data ['id'] > 0
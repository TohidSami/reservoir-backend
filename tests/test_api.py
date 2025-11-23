import pytest
from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_wells(client):
    response = client.get('/api/wells')
    
    if response.status_code != 200:
        print(f"\n🔴 API Error: {response.get_data(as_text=True)}")
    assert response.status_code == 200    
    assert isinstance(response.json, list)
    print("\n✅")

def test_404(client):
    response = client.get('/api/fake') 
    
    assert response.status_code == 404
    print("\n✅  404")
from app.utils.engineering import calculate_gor, calculate_wc
def test_gor():
    assert calculate_gor(oil=1000, gas=50) ==50
    assert calculate_gor(oil=0 , gas=50)==0

def test_wc():
    assert calculate_wc(oil=150, water=50)==25
    assert calculate_wc (oil=0 , water=10)==100
 
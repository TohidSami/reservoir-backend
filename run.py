

from app import create_app

try:
    app = create_app()
except Exception as e:
    print(f" {e}")


if __name__ == "__main__":
    try:
        app.run(debug=True,host='0.0.0.0', port=5000)
    except Exception as e:
        print(f" {e}")
else:
    print("!!! this file has trouble")
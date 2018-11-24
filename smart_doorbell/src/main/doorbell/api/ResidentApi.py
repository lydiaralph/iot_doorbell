from flask import (
    Flask,
    render_template
)


class MockResident:
    def __init__(self, text_name):
        self.text_name = text_name
        self.is_at_home = False


# Create the application instance
app = Flask(__name__, template_folder="../../resources/templates/")

registered_residents = [MockResident('Lydia'), MockResident('Matt')]


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/residents')
def get_residents():
    return render_template('residents.html', residents=registered_residents)


# @app.route('/residents/<resident>', methods=['POST'])
def set_resident_at_home(resident):
    for r in registered_residents:
        if r.text_name.lower() == resident:
            r.is_at_home = not r.is_at_home

    return render_template('residents.html', residents=registered_residents)


def main():
    app.run(host='0.0.0.0', debug=True, port=5000)


if __name__ == '__main__':
    main()

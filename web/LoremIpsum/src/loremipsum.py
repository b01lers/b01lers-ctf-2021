from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def index():
    f = request.args.get('animal', 'dogs')
    with open(f, 'r') as f:
        file_content = f.read(200)
    return """
    <blockquote>{}</blockquote>

    <a href="/?animal=dogs">Dogs</a>
    <a href="/?animal=cats">Cats</a>
    <a href="/?animal=cheese">Cheese</a>
    <a href="/?animal=fish">Fish</a>
    """.format(file_content)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)

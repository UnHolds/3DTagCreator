from flask import Flask, render_template, request
import tag
import uuid
import base64

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate():
    req = request.json

    text = req['text']
    url = req['url']

    assembly = tag.get_assembled_plate(text=text, url=url)
    path = f'./tmp/{uuid.uuid4()}.stl'
    tag.get_stl(assembly, path)

    result = {}
    with open(path, 'rb') as f:
        b64data = base64.b64encode(f.read()).decode('ascii')

        result = {
            'text': text,
            'url': url,
            'data': b64data
        }
    return result

@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)

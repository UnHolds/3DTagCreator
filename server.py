from flask import Flask, render_template, request, send_from_directory
import tag
import uuid
import base64

app = Flask(__name__)

@app.route('/tmp/<path:req>', methods = ['GET'])
def tmp_ressource(req):
    return send_from_directory('tmp', req)

@app.route('/generate', methods=['POST'])
def generate():
    req = request.json

    text = req['text']
    url = req['url']

    assembly = tag.get_assembled_plate(text=text, url=url)
    stl_path = f'./tmp/{uuid.uuid4()}.stl'
    tag.get_stl(assembly, stl_path)

    gltf_path = f'./tmp/{uuid.uuid4()}.gltf'
    tag.get_gltf(assembly, gltf_path)

    result = {
        'text': text,
        'url': url,
        'stl': stl_path,
        'gltf': gltf_path
    }
    return result

@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, send_from_directory
import tag
import uuid
import time
import os

app = Flask(__name__)

@app.route('/tmp/<path:req>', methods = ['GET'])
def tmp_ressource(req):
    return send_from_directory('tmp', req)

def delete_old_tmp_files():
    MAX_TIME = 30 * 60 #30 min

    for file in filter(lambda f: f.split('.')[-1] in ['stl', 'gltf', 'bin'], os.listdir('./tmp')):
        if '_' in file:
            timestamp = file.split('_')[0]
            if int(timestamp) + MAX_TIME < time.time():
                os.remove(f'./tmp/{file}')

@app.route('/generate', methods=['POST'])
def generate():
    req = request.json

    text = req['text']
    url = req['url']

    delete_old_tmp_files()

    timestamp = int(time.time())

    assembly = tag.get_assembled_plate(text=text, url=url)
    stl_path = f'./tmp/{timestamp}_{uuid.uuid4()}.stl'
    tag.get_stl(assembly, stl_path)

    gltf_path = f'./tmp/{timestamp}_{uuid.uuid4()}.gltf'
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

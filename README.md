# 3D Tag creator

## Develop-Enviroment

It is strongly encouraged to use a virtual python environment.
A virtual enviroment can be created with:

```bash
python -m venv -venv
```

To activate the enviroment use the following command:

```bash
# Windows
.\.venv\Scripts\activate

# Linux
./.venv/Scripts/activate
```

If you never heard of python virtual enviroments, you can checkout the
following link. https://realpython.com/python-virtual-environments-a-primer/#why-do-you-need-virtual-environments

After activating the enviroment for the first time the dependencies can be
installed via the `requirements.txt` file using the following command:

```bash
python -m pip install -r  requirements.txt
```

If you are using VsCode (encouraged) you also need to install the `OCP CAD Viewer`
extension. (https://marketplace.visualstudio.com/items?itemName=bernhard-42.ocp-cad-viewer)

Every thing should now be setup. You should also see somewhere in your
console that you are using a virtual environment (look for `.venv`).
If you start developing in this project after some time again it could
be that you need reactivate the virtual environment using the command:

```bash
# Windows
.\.venv\Scripts\activate

# Linux
./.venv/Scripts/activate
```

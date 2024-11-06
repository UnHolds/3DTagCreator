# 3D Tag Creator

3D-Tag-Creator is a program for generating `.stl` files
that can be 3d printed. The main goal was to create
somewhat inclusive tags (ascii text + braille). But
additional include a QR-Code to a relevant website,
or to a sign (eg: `https://gebaerden-archiv.at`).

It is recomended to print the tags in 2 colors. (one color
for the base plate and the other color for the tag,
braille & qr-code)

## Usage

You can use the program in 2 ways. First as a standalone application and
second as a Website (under development).

### Use as an application

To use it as an application just run it with:
```bash
python tag.py --text "Kaffee" --url "https://gebaerden-archiv.at/sign/40914"
```

If executed like this it will generate a stl-file called `tag.stl` representing
the 3D tag.

There are also a lot more options. To see them just run:
```bash
python tag.py --help
```

### Use as website

This is still work in progress! (Sry)

## Example Tag

![Image of the 3D view of the tag](./docs/example_tag.png?raw=true)

3D-View of a tag (Created with the command from above).

## Improvements

If you have some improvements or issues you are more then
welcome to create an issue in the repository. If you don't
know how this works you can also contact me on any social
media.

## Development

### Enviroment

It is strongly encouraged to use a virtual python environment.
A virtual enviroment can be created with:

```bash
python -m venv .venv
```

To activate the enviroment use the following command:

```bash
# Windows
.\.venv\Scripts\activate

# Linux
source ./.venv/Scripts/activate
```

If you never heard of python virtual enviroments, you can checkout the
following link. https://realpython.com/python-virtual-environments-a-primer/#why-do-you-need-virtual-environments

After activating the enviroment for the first time the dependencies can be
installed via the `requirements.txt` file using the following command:

```bash
python -m pip install -r requirements.txt
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
source ./.venv/Scripts/activate
```

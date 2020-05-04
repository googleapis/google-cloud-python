import os

from gapic.cli import generate

if __name__ == '__main__':
    os.environ['PYPANDOC_PANDOC'] = os.path.join(
        os.path.abspath(__file__).rsplit("gapic", 1)[0], "pandoc")
    os.environ['LC_ALL'] = 'C.UTF-8'
    generate.generate()

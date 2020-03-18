
import os

if __name__ == '__main__':

    print(os.getcwd())
    os.system('pdoc --html --force --template-dir docs/pdoc_templates --output-dir docs structpy')
    os.system('google-chrome docs/structpy/index.html')
from importlib import import_module
import os
import pg
import sys

def find_examples():
    result = []
    for filename in os.listdir('examples'):
        name, ext = os.path.splitext(filename)
        if ext == '.py' and name != '__init__':
            result.append(name)
    return result

EXAMPLES = find_examples()

def get_argument_example():
    args = sys.argv[1:]
    if len(args) != 1:
        return None
    arg = args[0]
    if arg in EXAMPLES:
        return arg
    try:
        return EXAMPLES[int(arg) - 1]
    except Exception:
        return None

def get_menu_example():
    print 'Select an example to run:'
    for index, name in enumerate(EXAMPLES):
        print '%3d. %s' % (index + 1, name)
    try:
        return EXAMPLES[int(raw_input('> ')) - 1]
    except Exception:
        return None

def generate_screenshots(size):
    try:
        os.mkdir('screenshots')
    except Exception:
        pass
    app = pg.App()
    for name in EXAMPLES:
        module = import_module('examples.%s' % name)
        window = module.Window(size)
        app.tick()
        app.tick()
        window.save_image('screenshots/%s.png' % name)
        window.close()
    app.run()

def main():
    name = get_argument_example() or get_menu_example()
    if name is None:
        return
    module = import_module('examples.%s' % name)
    names = ['Window', 'Scene']
    for name in names:
        if hasattr(module, name):
            pg.run(getattr(module, name))
            return

if __name__ == '__main__':
    # generate_screenshots((800, 600))
    main()

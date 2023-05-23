from dist import DemoComponent, DemoComponentImports, imports
from wasmtime import Store

def main():
    store = Store()
    demo = DemoComponent(store, DemoComponentImports(None, None, None, None, None, None))
    wit = demo.wit();
    ret = wit.something(store)
    print(ret)

if __name__ == '__main__':
    main()

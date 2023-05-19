from dist import DemoComponent, DemoComponentImports, imports
from wasmtime import Store

class Host(imports.Python):
    def print(self, s: str):
        print(s)

def main():
    store = Store()
    demo = DemoComponent(store, DemoComponentImports(Host()))
    demo.run(store)

if __name__ == '__main__':
    main()

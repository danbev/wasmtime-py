from dist import Component, ComponentImports, imports
from wasmtime import Store

class Host(imports.Python):
    def print(self, s: str):
        print(s)

def main():
    store = Store()
    demo = Component(store, ComponentImports(Host(), Host()))
    demo.run(store)

if __name__ == '__main__':
    main()

### Runtime error issue
This directory contains a reproducer for an issue where declaring types in a
separate interface cannot be parsed correctly by wasmtime-py. 

### Reproducer
This issue can be reproduced by running the following command:
```console
$ make bindings
wasm-tools component embed wit/python.wit demo.wat -o core-module.wasm
wasm-tools component new -v -o component.wasm core-module.wasm
python3 -m wasmtime.bindgen component.wasm --out-dir dist
Traceback (most recent call last):
  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code
  File "/home/danielbevenius/.local/lib/python3.11/site-packages/wasmtime/bindgen/__main__.py", line 40, in <module>
    main()
  File "/home/danielbevenius/.local/lib/python3.11/site-packages/wasmtime/bindgen/__main__.py", line 30, in main
    files = generate(name, contents)
            ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/danielbevenius/.local/lib/python3.11/site-packages/wasmtime/bindgen/__init__.py", line 40, in generate
    raise RuntimeError(result.value)
RuntimeError: failed to extract interface information from component

Caused by:
    0: failed to decode WIT from export `wit`
    1: unexpected unnamed type of kind 'record'
```
I ran into this issue after first having declared all the types in the same
interface as the functions that used them, but then wanted to extract them into
a separate interface which is how I ran into this issue. Having a separate
interface worked with `jco` and with Rust. I've added comment in
[python.wit](wit/python.wit) which are hopefully easy to follow to see.


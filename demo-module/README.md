## NameError
This directory contains a reproducer for an issue I ran into when trying to
extract types into a separate .wit file.

The error can be reproduced using the following command in this directory:
```console
$ make all
...


Traceback (most recent call last):
  File "/home/danielbevenius/work/wasm/wasmtime-py/demo-module/demo.py", line 12, in <module>
    main()
  File "/home/danielbevenius/work/wasm/wasmtime-py/demo-module/demo.py", line 8, in main
    ret = wit.something(store)
          ^^^^^^^^^^^^^^^^^^^^
  File "/home/danielbevenius/work/wasm/wasmtime-py/demo-module/dist/exports/wit.py", line 27, in something
    variant = RuntimeValueString(list)
              ^^^^^^^^^^^^^^^^^^
NameError: name 'RuntimeValueString' is not defined
make: *** [Makefile:16: run] Error 1
```
If we look line 27 se have the following code:
```python
    variant = RuntimeValueString(list) 
```
Notice that there is no module/namespace before `RuntimeValueString`. If we add
the namespace/module `demo_types` this will work:
```python
    variant = demo_types.RuntimeValueString(list) 
```

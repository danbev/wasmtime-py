### Undefined Symbol error
This directory contains a reproducer for an issue where an undefined symbol
error occurs when running wasmtime/bindgen:

```console
$ make bindings 
python3 ../wasmtime/bindgen component.wasm --out-dir dist
Traceback (most recent call last):
  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code
  File "/home/danielbevenius/work/wasm/wasmtime-py/demo/../wasmtime/bindgen/__main__.py", line 10, in <module>
    from wasmtime.bindgen import generate
  File "/home/danielbevenius/work/wasm/wasmtime-py/wasmtime/__init__.py", line 16, in <module>
    from ._error import WasmtimeError, ExitTrap
  File "/home/danielbevenius/work/wasm/wasmtime-py/wasmtime/_error.py", line 2, in <module>
    from . import _ffi as ffi
  File "/home/danielbevenius/work/wasm/wasmtime-py/wasmtime/_ffi.py", line 89, in <module>
    from ._bindings import *  # noqa
    ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/danielbevenius/work/wasm/wasmtime-py/wasmtime/_bindings.py", line 2045, in <module>
    _wasmtime_config_wasm_relaxed_simd_set = dll.wasmtime_config_wasm_relaxed_simd_set
                                             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib64/python3.11/ctypes/__init__.py", line 389, in __getattr__
    func = self.__getitem__(name)
           ^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib64/python3.11/ctypes/__init__.py", line 394, in __getitem__
    func = self._FuncPtr((name_or_ordinal, self))
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: /home/danielbevenius/work/wasm/wasmtime-py/wasmtime/linux-x86_64/_libwasmtime.so: undefined symbol: wasmtime_config_wasm_relaxed_simd_set. Did you mean: 'wasmtime_config_wasm_simd_set'?
make: *** [Makefile:21: bindings] Error 1
```
I installed wasmtime-py using the following command:
```console
$ cd ..
$ python -m pip install -e .
```

### Troubleshooting
Lets see what symbols are available in the shared library:
```console
$ nm ../wasmtime/linux-x86_64/_libwasmtime.so | rustfilt | grep simd
0000000000136fd0 T wasmtime_config_wasm_simd_set
00000000000bdc20 t core::str::pattern::simd_contains::{{closure}}
00000000000d06a0 t core::str::pattern::simd_contains::{{closure}}
00000000000d0560 t memchr::memmem::genericsimd::matched
00000000000d0570 t memchr::memmem::prefilter::genericsimd::matched
0000000000335ab0 t wasmtime::config::Config::wasm_simd
```
And we can see that the symbol `wasmtime_config_wasm_relaxed_simd_set` is not
defined in the shared library.

Perhaps I need re-download wasmtime:
```console
$ python ci/download-wasmtime.py 
Download https://github.com/bytecodealliance/wasmtime/releases/download/v9.0.0/wasmtime-v9.0.0-x86_64-linux-c-api.tar.xz
['wasmtime-v9.0.0-x86_64-linux-c-api']
['wasmtime-v9.0.0-x86_64-linux-c-api/lib']
['wasmtime-v9.0.0-x86_64-linux-c-api/lib/libwasmtime.so']
['wasmtime-v9.0.0-x86_64-linux-c-api/lib/libwasmtime.a']
['wasmtime-v9.0.0-x86_64-linux-c-api/README.md']
['wasmtime-v9.0.0-x86_64-linux-c-api/LICENSE']
['wasmtime-v9.0.0-x86_64-linux-c-api/include']
['wasmtime-v9.0.0-x86_64-linux-c-api/', 'wasmtime']
['wasmtime-v9.0.0-x86_64-linux-c-api/', 'wasmtime/table.h']
['wasmtime-v9.0.0-x86_64-linux-c-api/', 'wasmtime/instance.h']
['wasmtime-v9.0.0-x86_64-linux-c-api/', 'wasmtime/module.h']
['wasmtime-v9.0.0-x86_64-linux-c-api/', 'wasmtime/store.h']
['wasmtime-v9.0.0-x86_64-linux-c-api/', 'wasmtime/extern.h']
['wasmtime-v9.0.0-x86_64-linux-c-api/', 'wasmtime/engine.h']
['wasmtime-v9.0.0-x86_64-linux-c-api/', 'wasmtime/val.h']
['wasmtime-v9.0.0-x86_64-linux-c-api/', 'wasmtime/linker.h']
['wasmtime-v9.0.0-x86_64-linux-c-api/', 'wasmtime/func.h']
['wasmtime-v9.0.0-x86_64-linux-c-api/', 'wasmtime/global.h']
['wasmtime-v9.0.0-x86_64-linux-c-api/', 'wasmtime/error.h']
['wasmtime-v9.0.0-x86_64-linux-c-api/', 'wasmtime/trap.h']
['wasmtime-v9.0.0-x86_64-linux-c-api/', 'wasmtime/memory.h']
['wasmtime-v9.0.0-x86_64-linux-c-api/', 'wasmtime/config.h']
['wasmtime-v9.0.0-x86_64-linux-c-api/', 'wasm.h']
['wasmtime-v9.0.0-x86_64-linux-c-api/', 'doc-wasm.h']
['wasmtime-v9.0.0-x86_64-linux-c-api/', 'wasmtime.h']
['wasmtime-v9.0.0-x86_64-linux-c-api/', 'wasi.h']
```
And then re-running pip install.

And now if we check for the symbol:
```console
$ nm ../wasmtime/linux-x86_64/_libwasmtime.so | rustfilt | grep wasmtime_config_wasm_relaxed_simd_set
00000000000f2710 T wasmtime_config_wasm_relaxed_simd_set
```
It is there now. So we should get past this error:
```console
$ make core-module.wasm 
wasm-tools component embed wit/python.wit demo.wat -o core-module.wasm

$ make component.wasm 
wasm-tools component new -v -o component.wasm core-module.wasm

$ make bindings 
python3 ../wasmtime/bindgen component.wasm --out-dir dist
Generating dist/__init__.py
Generating dist/component.core0.wasm
Generating dist/component.core1.wasm
Generating dist/component.core2.wasm
Generating dist/exports/__init__.py
Generating dist/exports/wit.py
Generating dist/imports/__init__.py
Generating dist/imports/python.py
Generating dist/imports/wit_types.py
Generating dist/intrinsics.py
```




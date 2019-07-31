# Python CFFI Wrap Function

An wrapper function of CFFI to call c/cpp function through python

---

## Getting Started

### Prerequisites

- install gcc
- VSC install Cmake/Cmake-tool
- python install cffi
   
### How to USE

- Step1: create new module
  1. copy src/module/example to src/module/yourmodule
  2. modify libname CmakeLists.txt : set(libname example)
  3. rename/modify example_wrap.cpp,example_wrap.h,example_wrap_io.h according to your need.
  4. F7 build the module
- Step2: create your module.py 
  - copy example.py to your_module.py 
  - modify load_module as following
  ```python 
    par["lib_fn"] = root_path + "/build/src/cpp/module/<yourmodule>/lib<yourmodule>_abi.dll"
    par["wrap_io_h"] = root_path + "/src/cpp/module/<yourmodule>/<yourmodule>_wrap_io.h"
    par["wrap_func_h"] = root_path + "/src/cpp/module/<yourmodule>/<yourmodule>_wrap.h"
  ```
  - Access the c function call by following example code in the run()
    - call predefined function m.setup(args),m.reset(),m.run(**args)
    - call other function by m.lib.others(args) 

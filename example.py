from cffi_module_loader import module_loader, root_path, FFI
import numpy as np

root_path = root_path


def load_module():
    par = {}
    par["lib_fn"] = root_path + "/build/src/cpp/module/example/libexample_abi.dll"
    par["wrap_io_h"] = root_path + "/src/cpp/module/example/example_wrap_io.h"
    par["wrap_func_h"] = root_path + "/src/cpp/module/example/example_wrap.h"
    module = module_loader(**par)
    module.reset()
    return module


def run():
    m = load_module()
    str = lambda x: m.str(x)

    # call setup function with arguments
    gain, delta = 5, 10
    m.setup(gain, delta)

    # call run function method1: set_io -> run
    mode = {"mpy": 1, "add": 2}
    m.set_io(in_data=np.array([x for x in range(10)]))
    m.set_io(out_data=np.zeros(10))
    m.set_io(mode=mode["mpy"])
    m.run()
    data1 = m.get_io()
    out1 = m.get_io("out_data")
    print("mode={},param={},in = {},out = {}".format("mpy", gain,
                                                     data1["in_data"], out1))

    # call run function method2: run with argument,run will return all io in a dict
    results = m.run(mode=mode["add"],
                    in_data=np.array([x for x in range(10)]),
                    out_data=np.zeros(10))
    print("mode={},param={},in = {},out = {}".format("add", delta,
                                                     results["in_data"],
                                                     results["out_data"]))

    # call predefined reset function
    m.reset()

    # call other internal functions
    # passing string need convert to char [], by calling m.str()
    m.lib.func1(str("hello world ! Joe"))

    # that's all


if __name__ == "__main__":
    run()

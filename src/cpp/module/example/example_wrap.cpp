#include "../../commlib/commlib_inc.h"
#include "example_wrap_io.h"

enum select { mpy = 1,
              add = 2 };
static struct cfg_t {
    double gain;
    double delta;
} cfg;

void run1(io_t* io) {
    for (size_t i = 0; i < io->in_data->l; i++) { fbuf(io->out_data, i) = fbuf(io->in_data, i) * cfg.gain; }
}

void run2(io_t* io) {
    for (size_t i = 0; i < io->in_data->l; i++) { fbuf(io->out_data, i) = fbuf(io->in_data, i) + cfg.delta; }
}

extern "C" {
extern void run(io_t* io) {
    if (io->mode == (int)select::mpy) {
        run1(io);
    } else if (io->mode == (int)select::add) {
        run2(io);
    }
}
extern void setup(double gain, double delta) {
    cfg.gain  = gain;
    cfg.delta = delta;
}

extern void reset() {
    disp("call reset");
}
extern void func1(char* aaa) {
    disp(string(aaa));
}
}

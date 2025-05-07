#!/usr/bin/env python
# wscript

def options(opt):
    opt.load("compiler_cxx")
    opt.load("clangd", tooldir="tools")


def configure(conf):
    conf.load("compiler_cxx")
    conf.load("clangd", tooldir="tools")
    conf.find_program("make", var="MAKE")
    conf.env.INCLUDES_EXT = ["extern/concord/include"]

    conf.check(header_name="iostream", uselib="CXX")
    conf.check(fragment="int main() { return 0; }\n")
    conf.check_cc(cflags="-std=c++20", msg="C++20 support", mandatory=True)

    conf.check_cfg(
                    package="libcurl",
                    args="--cflags --libs",
                    uselib_store="CURL"
    )

    conf.check_inline()

    conf.env.append_value("CXXFLAGS", ["-std=c++20", "-Wall", "-O2"])


def build(bld):
    concord_src = bld.path.make_node("extern/concord")
    bld(rule="${MAKE} -C %s static" % concord_src.abspath(),
        source=[],
        target="",
        name="concord")

    concord_lib = bld.srcnode.find_node("extern/concord/lib/libdiscord.a")
    if not concord_lib:
        bld.fatal("Couldn't find lib/libdiscord.a.")

    inc = ["include", "extern/concord/include"]
    files = bld.path.ant_glob("src/**/*.cpp")
    bld.program(
        features="c cprogram",
        target="autoelector",
        source=files,
        includes=inc,
        linkflags=[concord_lib.abspath()]
    )

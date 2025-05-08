#!/usr/bin/env python
# wscript

from waflib import Utils
import os, json, re

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

    staging = bld.bldnode.make_node("concord")
    bld(
        rule="PREFIX=%s ${MAKE} -C %s install" % (
            staging.abspath(),
            concord_src.abspath()
        ),
        source=[],
        target="",
        name="concord install into %s" % staging.abspath(),
    )

    concord_lib = staging.make_node("lib/libdiscord.a")
    hdr = staging.make_node("include")
    if not concord_lib or not hdr:
        bld.fatal("Concord install faield; no lib or headers...")

    inc = ["include", hdr.abspath()]
    files = bld.path.ant_glob("src/**/*.cpp")
    bld.program(
        features="c cprogram",
        target="autoelector",
        source=files,
        includes=inc,
        #linkflags=[concord_lib.abspath()]
        libpath=[staging.make_node("lib").abspath()]
    )
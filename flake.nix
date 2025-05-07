{
    description = "autoelector";

    inputs = {
        nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
        flake-utils.url = "github:numtide/flake-utils";
    };

    outputs = { self, nixpkgs, flake-utils, ... }:
        flake-utils.lib.eachDefaultSystem (system:
        let
            pkgs = import nixpkgs { inherit system; };
            llvm = pkgs.llvmPackages_latest;
            lib = nixpkgs.lib;
            libcxx = llvm.libcxx;

            buildInputs = with pkgs; [
                llvm.clang
                llvm.libcxx
                curlFull
                openssl
                waf
            ];

            nativeBuildInputs = with pkgs; [
                clang-tools
                gnumake
                bear
                llvm.lldb
                pkg-config
            ];
        in {
            devShells.default = pkgs.mkShell {
                inherit buildInputs;
                inherit nativeBuildInputs;

                shellHook = ''
                    export PKG_CONFIG_PATH="${pkgs.curlFull.dev}/lib/pkgconfig"
                    export LIBRARY_PATH=${libcxx}/lib:$LIBRARY_PATH
                    export LD_LIBRARY_PATH=${libcxx}/lib:$LD_LIBRARY_PATH
                    export CPLUS_INCLUDE_PATH=${libcxx}/include/c++/v1:$CPLUS_INCLUDE_PATH
                '';
            };
        
        });
}
{ pkgs ? import (fetchTarball
  "https://github.com/NixOS/nixpkgs/archive/5df43628fdf08d642be8ba5b3625a6c70731c19c.tar.gz")
  { }, extraBuildInputs ? [ ], myPython ? pkgs.python313, extraLibPackages ? [ ]
, pythonWithPkgs ? myPython }:

let
  buildInputs = with pkgs;
    [ clang llvmPackages_16.bintools rustup ] ++ extraBuildInputs;

  lib-path = with pkgs; lib.makeLibraryPath buildInputs;

  shell = pkgs.mkShell {
    buildInputs = [
      # my python and packages
      pythonWithPkgs

      # other packages needed for compiling python libs
      pkgs.readline
      pkgs.libffi
      pkgs.openssl
      pkgs.cargo
      pkgs.rustc
      pkgs.ninja

      # unfortunately needed because of messing with LD_LIBRARY_PATH below
      pkgs.git
      pkgs.openssh
      pkgs.rsync
    ] ++ extraBuildInputs;
    shellHook = ''
      # Allow the use of wheels.
      SOURCE_DATE_EPOCH=$(date +%s)
      # Augment the dynamic linker path
      export "LD_LIBRARY_PATH=$LD_LIBRARY_PATH:${lib-path}:${pkgs.stdenv.cc.cc.lib}/lib"
      # Setup the virtual environment if it doesn't already exist.
      VENV=.venv
      if test ! -d $VENV; then
        uv venv $VENV
      fi
      source ./$VENV/bin/activate
      export PYTHONPATH=$PYTHONPATH:`pwd`/$VENV/${myPython.sitePackages}/

      zsh
    '';
  };

in shell

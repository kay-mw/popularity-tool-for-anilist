let
  pkgs = import (fetchTarball "https://github.com/NixOS/nixpkgs/archive/4284c2b73c8bce4b46a6adf23e16d9e2ec8da4bb.tar.gz") {};
  myPython = pkgs.python311;
  pythonPackages = pkgs.python311Packages;

  pythonWithPkgs = myPython.withPackages (pythonPkgs: with pythonPkgs; [
    ipython
    pip
    debugpy
    setuptools
    virtualenvwrapper
    wheel
    grpcio
  ]);

  extraBuildInputs = with pythonPackages; [
    # this list contains packages that you want to be available at runtime and might not be able to be installed properly via pip
    numpy
    pandas
    pyodbc
  ] ++ (with pkgs; [
    act
    nodejs
    nodePackages.tailwindcss
    google-cloud-sdk-gce
    azure-cli
  ]);
in
import ./python-shell.nix {
  extraBuildInputs = extraBuildInputs;
  # extraLibPackages = extraLibPackages;
  myPython = myPython;
  pythonWithPkgs = pythonWithPkgs;
  pkgs = pkgs;
}

let
  pkgs = import (fetchTarball
    "https://github.com/NixOS/nixpkgs/archive/6df24922a1400241dae323af55f30e4318a6ca65.tar.gz")
    { };
  myPython = pkgs.python311;
  pythonPackages = pkgs.python311Packages;

  pythonWithPkgs = myPython.withPackages
    (pythonPkgs: with pythonPkgs; [ ipython debugpy setuptools wheel ]);

  extraBuildInputs = with pythonPackages;
    [
      # this list contains packages that you want to be available at runtime and might not be able to be installed properly via pip
      pyodbc
    ] ++ (with pkgs; [ act nodejs uv ]);
in import ./python-shell.nix {
  extraBuildInputs = extraBuildInputs;
  # extraLibPackages = extraLibPackages;
  myPython = myPython;
  pythonWithPkgs = pythonWithPkgs;
  pkgs = pkgs;
}

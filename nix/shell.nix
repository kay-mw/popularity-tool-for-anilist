let
  pkgs = import (fetchTarball
    "https://github.com/NixOS/nixpkgs/archive/5df43628fdf08d642be8ba5b3625a6c70731c19c.tar.gz")
    { };
  myPython = pkgs.python313;
  pythonPackages = pkgs.python313Packages;

  pythonWithPkgs = myPython.withPackages
    (pythonPkgs: with pythonPkgs; [ ipython debugpy setuptools wheel ]);

  extraBuildInputs = with pythonPackages;
    [
      # this list contains packages that you want to be available at runtime and might not be able to be installed properly via pip
      pyodbc
    ] ++ (with pkgs; [ act bun uv ]);
in import ./python-shell.nix {
  extraBuildInputs = extraBuildInputs;
  # extraLibPackages = extraLibPackages;
  myPython = myPython;
  pythonWithPkgs = pythonWithPkgs;
  pkgs = pkgs;
}

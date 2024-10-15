{
  description = "Generateur noms flake";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-24.05";
  };

  outputs = { self, nixpkgs }:
  let
    system = "x86_64-linux";
    pkgs = import nixpkgs { system = "x86_64-linux"; config.allowUnfree = true; };
  in
  {
    
    devShells.${system}.default = pkgs.mkShell { 
      buildInputs = with pkgs; [
        jetbrains.pycharm-community
        python312
        python312Packages.pandas
      ];

      shellHook = ''
        export PS1="\[\e[35m\](generateur-noms) [$USER@$HOSTNAME:\w]\$ "
      '';
    };
  };
}

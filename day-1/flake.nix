{
  description = "nix declared development environment";

  inputs = {
    nixpkgs.url = "nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { nixpkgs, flake-utils, ... }:
    let
      mkshell = pkgs:
        let
          pythonWithPackages =
            pkgs.python310.withPackages (p: with p; [ pytest ]);
        in pkgs.mkShell {
          # The development environment can contain any tools from nixpkgs
          packages = [ pythonWithPackages ];

          envrc_contents = ''
            use flake
          '';

          shellHook = ''
            [[ ! -a .envrc ]] && echo -n "$envrc_contents" > .envrc
          '';
        };
      # Use flake-utils to declare the development shell for each system nix
      # supports e.g. x86_64-linux and x86_64-darwin (but no guarantees are
      # given that it works except for x86_64-linux, which I use).
    in flake-utils.lib.eachDefaultSystem (system:
      let pkgs = nixpkgs.legacyPackages."${system}";
      in {
        devShells.default = mkshell pkgs;

      });
}

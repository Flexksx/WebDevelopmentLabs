{
  description = "Java project with Spring, SQLite, and Gradle in a Nix Flake for macOS with M1";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-23.05";
  };

  outputs = { self, nixpkgs }: let
    system = "aarch64-darwin"; # Set for macOS on M1
  in {
    devShells.${system}.default = with import nixpkgs { inherit system; }; mkShell {
      buildInputs = [
        openjdk17        
        gradle           
        sqlite           
        docker           
        nodejs-18_x
      ];

      # Optional: Configure environment variables
      shellHook = ''
        echo "Starting development shell with Java, Gradle, SQLite, and Docker support on macOS M1"
        export JAVA_HOME=${openjdk17}/lib/openjdk
        export PATH=$PATH:${docker}/bin
      '';
    };
  };
}

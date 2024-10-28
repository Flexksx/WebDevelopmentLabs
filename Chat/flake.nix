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
        openjdk17  # Change to a valid JDK version
        gradle           
        sqlite           
        docker           
        nodejs-18_x
        postgresql
      ];

      shellHook = ''
        echo "Starting development shell with Java, Gradle, SQLite, and Docker support on macOS M1"
        export JAVA_HOME=${openjdk17}  # Adjust this according to the JDK you choose
        export PATH=$PATH:${docker}/bin
        echo "JAVA_HOME set to $JAVA_HOME"
      '';
    };
  };
}

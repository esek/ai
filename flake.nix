{
  description = "Shared Esek AI configuration and infrastructure files";

  inputs.flake-parts.url = "github:hercules-ci/flake-parts";

  outputs = inputs@{ self, flake-parts, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      systems = [ ];

      flake.source = self.outPath;
    };
}

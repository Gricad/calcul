{ pkgs ? import <nixpkgs> {} }:
with pkgs;

let
  inherit stdenv fetchurl perl;
  appName = "hello-2.1.1y";
in
{
  "${appName}" = stdenv.mkDerivation {
    name = appName;
    buildInputs = [ perl ];
    src = fetchurl {
      url = ftp://ftp.nluug.nl/pub/gnu/hello/hello-2.1.1.tar.gz;
      md5 = "70c9ccf9fac07f762c24f2df2290784d";
    };
  };
}

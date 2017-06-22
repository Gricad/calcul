{ pkgs ? import <nixpkgs> {} }:
with pkgs;

let
  inherit stdenv fetchurl perl;
  version = "2.1.1";
in
{
    hello = stdenv.mkDerivation rec {
    name = "hello-${version}";
    buildInputs = [ perl ];
    src = fetchurl {
      url = "https://ftp.gnu.org/pub/gnu/hello/${name}.tar.gz";
      sha256 = "1md7jsfd8pa45z73bz1kszpp01yw6x5ljkjk2hx7wl800any6465";
    };
  };
}

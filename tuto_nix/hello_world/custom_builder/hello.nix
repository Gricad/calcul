{ pkgs ? import <nixpkgs> {} }:
with pkgs;

let
  inherit stdenv fetchurl perl;
  appName = "hello-2.1.1y";
in
{
  "${appName}" = stdenv.mkDerivation {
    name = appName;
    builder = ./builder.sh;
    src = fetchurl {
      url = "https://ftp.gnu.org/pub/gnu/hello/${name}.tar.gz";
      sha256 = "1md7jsfd8pa45z73bz1kszpp01yw6x5ljkjk2hx7wl800any6465";
    };
    inherit perl;
  };
}

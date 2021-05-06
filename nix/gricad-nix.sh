# NIX environment
# This script must be sourced into a bash shell
# (use "." or "source")

# Fix to access visu_sub when source nix.sh is in the .bashrc
export PATH=/applis/site/other/visu_dahu:$PATH

DEFAULT_CONFIG_FILE=/applis/site/nix/config.nix
STABLE_CHANNEL="nixos-20.03"
export MANPATH=~/.nix-profile/share/man:~/.local/share/man:$MANPATH
export INTEL_LICENSE_FILE=/opt/intel/licenses:/applis/site/licenses:/applis/ciment/v2/stow/data/intel_licences
export ACLOCAL_PATH=$HOME/.nix-profile/share/aclocal:$ACLOCAL_PATH
export XDG_RUNTIME_DIR="$HOME/.local/tmp/"
mkdir -p $XDG_RUNTIME_DIR

welcome_text="You can customize $HOME/.config/nixpkgs/config.nix and\n
install a python environment with:\n
  \tnix-env -iA pythonEnv\n
or a R environement with:\n
  \tnix-env -iA rEnv\n
You can list Gricad packages with:\n
  \tnix-env -qaP -A nur.repos.gricad\n
You can install a Gricad package (hello example here) with:\n
  \tnix-env -iA nur.repos.gricad.hello\n
"

function init_nur() {
  export NIX_PATH="nixpkgs=https://github.com/NixOS/nixpkgs/archive/$STABLE_CHANNEL.tar.gz"
  echo "Please wait while initializing NUR cache..."
  nix-env -f "<nixpkgs>"  -i -A nur.repos.gricad.hello 2>/dev/null
  nix-env -e hello 2> /dev/null
  echo "Done"
  echo -e $welcome_text
}


if [ -f $HOME/.config/nixpkgs/config.nix ]
then
  if [ "`grep 'NUR/archive/master.tar.gz' $HOME/.config/nixpkgs/config.nix`" = "" ]
  then
    echo "WARNING: You have a config.nix file that doesn't seem to activate NUR."
    echo "The CIMENT channel is deprecated and the use of NUR is recommended."
    echo "You can install a recommended configuration with :"
    echo "   source /applis/site/nix.sh --install-config"
  fi
else
  init_nur
fi

export NIX_PATH="nixpkgs=https://github.com/NixOS/nixpkgs/archive/$STABLE_CHANNEL.tar.gz"

# Remove obsolete nix profile
if [ "`ls -l ~/.nix-profile 2>/dev/null| grep ciment`" != "" ]
then 
  echo "Removing obsolete nix profile"
  rm -rf ~/.nix-profile
fi

# Upgrade an old "ciment-channel" nix env to a "gricad/nur-packages" one.
if [ "$1" = "--install-config" ]
then
  if [ -f $HOME/.config/nixpkgs/config.nix ]
  then
    DATE=`date +%s`
    echo "WARNING: moving your nixpkgs config file into $HOME/.config/nixpkgs/config.nix.$DATE"
    mv $HOME/.config/nixpkgs/config.nix $HOME/.config/nixpkgs/config.nix.$DATE
  fi
  cp $DEFAULT_CONFIG_FILE $HOME/.config/nixpkgs/config.nix 
  init_nur
fi

# Configure nix profile
export NIX_USER_PROFILE_DIR=/nix/var/nix/profiles/per-user/$USER

mkdir -m 0755 -p $NIX_USER_PROFILE_DIR
if test "$(stat --printf '%u' $NIX_USER_PROFILE_DIR)" != "$(id -u)"; then
    echo "WARNING: bad ownership on $NIX_USER_PROFILE_DIR" >&2
fi

if ! test -L $HOME/.nix-profile; then
    echo "creating $HOME/.nix-profile" >&2
    if test "$USER" != root; then
        ln -s $NIX_USER_PROFILE_DIR/profile $HOME/.nix-profile
    else
        # Root installs in the system-wide profile by default.
        ln -s /nix/var/nix/profiles/default $HOME/.nix-profile
    fi
fi

if ! test -d $HOME/.config/nixpkgs; then                              
    echo "creating $HOME/.config/nixpkgs" >&2                         
    mkdir -p $HOME/.config/nixpkgs                                    
    cp $DEFAULT_CONFIG_FILE $HOME/.config/nixpkgs/config.nix 
fi

export NIX_PROFILES="/nix/var/nix/profiles/default $HOME/.nix-profile"

for i in $NIX_PROFILES; do
    export PATH=$i/bin:$PATH
done

if [ "$USER" = root -a ! -e $HOME/.nix-channels ]; then
    echo "http://nixos.org/channels/nixpkgs-unstable nixpkgs" \
      > $HOME/.nix-channels
fi

NIX_USER_GCROOTS_DIR=/nix/var/nix/gcroots/per-user/$USER
mkdir -m 0755 -p $NIX_USER_GCROOTS_DIR
if test "$(stat --printf '%u' $NIX_USER_GCROOTS_DIR)" != "$(id -u)"; then
    echo "WARNING: bad ownership on $NIX_USER_GCROOTS_DIR" >&2
fi

if [ ! -e $HOME/.nix-defexpr -o -L $HOME/.nix-defexpr ]; then
    echo "creating $HOME/.nix-defexpr" >&2
    rm -f $HOME/.nix-defexpr
    mkdir $HOME/.nix-defexpr
    if [ "$USER" != root ]; then
        ln -s /nix/var/nix/profiles/per-user/root/channels \
          $HOME/.nix-defexpr/channels_root
    fi
    init_nur
fi

if test "$USER" != root; then
    export NIX_REMOTE=daemon
else
    export NIX_REMOTE=
fi

alias nix-env='nix-env -f "<nixpkgs>"'

# Ciment variables and functions
source /applis/site/vars.sh

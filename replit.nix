{ pkgs }: {
  deps = [
    pkgs.mkinitcpio-nfs-utils
    pkgs.cope
    pkgs.php
    pkgs.postgresql96
    pkgs.postgresql_11
    pkgs.python38Full
  ];
  env = {
    PYTHONBIN = "${pkgs.python38Full}/bin/python3.10";
    LANG = "en_US.UTF-8";
  };
}
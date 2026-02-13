# netboot.ustc

An adaptation of netboot.xyz for usage in China

## Background

This is an adaptation of netboot.xyz, which heavily rely on github to host files. Sadly, github is not stably accessible so that we need to create a mirror for the content on github.

netboot.xyz has done a great job separating data and code, it is also great as I can patch some data so that using mirrors when booting and building became easier, and keeping updates in branches can be tough, so I decided I'll tamper with the code more.

Core adjustments:

Use mirrors & generate version lists with mirror data on build. (Done for Arch/CentOS)

Cache github files on build.

Update some templates for better adaptation of mirror format. (TODO)

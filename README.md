# CMarkEd
**Note: CMarkEd is still in a very early stage and is not suitable for production.**

CMarkEd is an open source, multi platform [CommonMark](http://commonmark.org) (Markdown) editor. It draws inspiration from [Remarkable](https://github.com/jamiemcg/Remarkable).

## Features:
- Live Preview with synchronized scrolling
- Export to HTML and PDF

## Roadmap:
See the project page [on Trello](https://trello.com/b/DO5l0B9I/cmarked-development).

## Installing

### Linux:
If you are using Arch Linux, you can install CMarkEd [from the AUR](https://aur.archlinux.org/packages/cmarked/). For any other distro that doesn't use the AUR, keep reading.

CMarkEd relies on `cmark`, the reference implementation for CommonMark, written in C. Follow [the instructions on the project page](https://github.com/jgm/cmark#installing) and make sure that `libcmark` is installed in your distro's libraries directory. This is usually under `/lib`, `/usr/lib` or `/usr/local/lib`. The process goes like this:

    $ git clone https://github.com/jgm/cmark.git
    $ cd cmark
    $ make INSTALL_PREFIX=/usr     # this will put libcmark under /usr/lib. cmark defaults to /usr/local/ which in turn will put it under /usr/local/lib
    $ sudo make install

Now install CMarkEd itself:

    $ git clone https://github.com/sergiodlc/cmarked.git
    $ cd cmarked
    $ sudo pip install .

From now on, run this to get the latest developments:

    $ git pull
    $ sudo pip install --upgrade .

If you want to be able to export to PDF, you'll need [weasyprint](http://weasyprint.org/):

    $ sudo pip install weasyprint

### Windows:
TODO

### Mac OS:
TODO

## FAQ

### Wait, isn't CommonMark just another name for Markdown?
Yes... in essence. Read [here](http://spec.commonmark.org/0.27/#introduction) about their differences.

### What makes CMarkEd different from Remarkable?
- The obvious: CMarkEd parses well specified Markdown (CommonMark) and doesn't attempt to deviate from it
- CMarkEd uses Qt as its GUI framework instead of GTK. We believe Qt is superior to GTK as a multi platform GUI framework
- CMarkEd uses `libcmark` to parse the CommonMark source. This well tuned C parser makes CMarkEd hundreds of times faster and more responsive. This is usually noticeable when editing medium and large documents


### Issues/Bugs/Suggestions
Feel free to report any bugs or make suggestions [here](https://github.com/sergiodlc/cmarked/issues). Pull requests are welcome too!

**Note: At this point we are not accepting extensions to the CommonMark parser itself. Please refer to the `cmark` project with your concerns in this area**

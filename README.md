# gdot

gdot is developed by the idea to have an interactive implementation of the [xdot](https://github.com/jrfonseca/xdot.py)
gui. This means we can not only view graphviz documents, but also write the code in the same application and export the graph
in various formats without using external tools.

Thanks to xdot, there is no heavy lifting to do to achive this goal. So I simply wrote that application :).

## Current Status

### Working

* loading/saving .dot files
* visualisation using xdot

### TODO

* export dialog
* keybindings
* header bar like in gedit
* error handling (incorrect dotfiles)
* error visualisation on GtkSourceView
* autocompletion

## Screenshots

![Example gui when working with the cluster graphviz demo](https://raw.githubusercontent.com/pointhi/GDot/master/assets/cluster.png)
Installing MongoDB
##################

conda
=====

If you are already using conda, you can install pymongo and mongodb from the conda-forge channel:

::

  conda install -c conda-forge pymongo mongodb

Mac
===

Homebrew
--------

The Mongo web site points you to instructions for installing with homebrew. These seem to work, but are pretty coplicated. I would say go for it if you already have the SCode compier tools and/or are using Homebrew for other things.

Otherwise, there is a download available if the binary files. The only complication is that they don't install the files for you.

tarball of binaries
-------------------

This should work on OS-X > 10.13 Intel (may not work on new M1)

Download this file:

https://fastdl.mongodb.org/osx/mongodb-macos-x86_64-5.0.6.tgz

If that link doesn't work, try going to:

https://www.mongodb.com/try/download/community

And go to MongoDB community server -- then on the right, you should see a download: Platform MacOS, Format: tgz click on download to download the tgz file.

Double Click on it to unpack it -- you should get something like this:

::

    mongodb-macos-x86_64-5.0.6
       - LICENSE-Community.txt
       - README
       - MPL-2
       - THIRD-PARTY-NOTICES
       - bin
           - install_compass
           - mongo
           - mongod
           - mongos

What you need to do is copy the mongo* files in ``bin/`` to:

``/usr/local/bin``

At the command line:

::

    cd mongodb-macos-x86_64-5.0.6
    cd bin
    cp mongo* /usr/local/bin/

If that doesn't work, you may need to use "sudo":

::

    sudo cp mongo* /usr/local/bin/

With the GUI:

In finder, click the "Go" menu, the "go to folder"

type in: ``usr/local/bin``

drag the ``mongo``, ``mongod``, and ``mongos`` files to the ``usr/local/bin`` folder.

Start a new terminal, and try:

::

    mongod --version

If that doesn't work, you may need to add ``/usr/local/bin`` to your PATH:

First: type:

::

  echo $PATH

and see if ``/usr/local/bin`` is on our PATH.

If not, then:

::

  echo $SHELL

If it says: ::

  /bin/zsh

Then you need to edit your ``.zshrc`` file

https://code2care.org/pages/permanently-set-path-variable-in-mac-zsh-shell

If it says: ::

  /bin/bash

Then you need to edit your ``.bash_profile`` file


https://www.cyberciti.biz/faq/appleosx-bash-unix-change-set-path-environment-variable/


Windows
=======

Go to:

https://www.mongodb.com/try/download/community

Download the installer for the Community Server

Run the installer.

I recommend that you do NOT install it as a service -- uncheck that option (or, if you are familiar with Windows services, go ahead :-) )

Once installed, you will need to add the install dir to your PATH. It should be something like:

``C:\Program Files\MongoDB\server\bin``

(there should be a few commands in there: ``mongo``, ``mongod``, ``mongos``)

https://www.computerhope.com/issues/ch000549.htm

Note: you don't need to restart the computer, but you do need to restart your command Window(s)



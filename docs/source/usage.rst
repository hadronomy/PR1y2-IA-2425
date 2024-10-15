.. _guide_basic_usage:

###########
Basic Usage
###########

See the :ref:`_guide_installation` guide to install the package.

.. note::

   If you have already installed the package, you can proceed to the :ref:`usage` guide.

   If you are running it without installing it, ensure you are in the poetry shell.

   .. code:: sh

      poetry shell

.. _usage:

Usage
*****

To use the CLI, run the following command:

.. code:: sh

   ia --help

This command will display the help message with all the available commands and options.


Subcommands
===========

The CLI has the following subcommands:

- ``uninformed``: Executes the uninformed search algorithms.
  Corresponds to the first assignment.
- ``informed``: Executes the informed search algorithms.
  Corresponds to the second assignment.

To see the help message for each subcommand, run the following command:

.. code:: sh

   ia <subcommand> --help

For example, to see the help message for the uninformed subcommand, run:

.. code:: sh

   ia uninformed --help

That is all you need to know to start using the CLI. Have fun! 🎉


``simple_fax_sms`` is a python script for sending SMS via simple-fax.de.


Installation
==================

To install the tool, just run:

::
   
   pip install git+https://github.com/nitram2342/simple-fax-sms


Usage example
===============

The ``simple_fax_sms`` tool has a command line interface. You run it like in this example:

::
   
   SIMPLEFAXDE_PASS=mysecret simple_fax_sms \
       --user login@example.com \
       --phone +49xxxxxx \
       --text 'Hello, World"


Copyright and Licence
=====================

``simple_fax_sms`` is developed by Martin Schobert martin@weltregierung.de and
published under a BSD licence with a non-military clause. Please read
``LICENSE.txt`` for further details.

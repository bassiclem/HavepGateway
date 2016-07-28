
Tutorial: API Usage — The Gateway tutorial
==========================================

    .. index:: single: Euclid

    *“There is no royal road to geometry.”* — Euclid

This module makes ISensit Gateway fun!
The beginner will enjoy how the :mod:`~isensit_gw.ISensitGW` module
lets you get started quickly.

>>> from isensit_gw import ISensitGW
>>> ISensitGW.get_aws_credentials()
SUCCESS

But fancier programmers can use the :class:`~isensit_gw.ISensitGW`
class to create an actual gateway *object*
upon which they can then perform lots of operations.
For example, consider this Python program:

.. testcode::

   from isensit_gw import ISensitGW
   self.connection = pymysql.connect(
       host=self.config_data.get_mysql_credentials()['hostname'],
       user=self.config_data.get_mysql_credentials()['username'],
       password=self.config_data.get_mysql_credentials()['password'],
       db=self.config_data.get_mysql_credentials()['database'],
       charset='utf8mb4',
       cursorclass=pymysql.cursors.DictCursor)

Since methods like :meth:`~ISensitGW.get_gateway_id()`
return Boolean int, this program will produce the following output:

.. testoutput::

    123

Read :doc:`api` to learn more!

.. warning::

   This is only dummy tutorial by Saujan it shall be duly updated.
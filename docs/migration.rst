Migration Guide
===============

This guide helps you upgrade from older versions of CodeVideoRenderer.

Migrating to 1.2.x
------------------

Version 1.2.x introduced breaking API changes. Follow the sections below when upgrading from 1.1.x or earlier.

Function Naming Convention
^^^^^^^^^^^^^^^^^^^^^^^^^^

All public functions and classes switched from **snake_case** to **camelCase** in 1.2.1.

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - Old (1.1.x and earlier)
     - New (1.2.x)
   * - ``type_checker``
     - ``typeChecker``

If you were calling utility functions directly from ``CodeVideoRenderer.utils``, update your code accordingly.

Removed Utilities
^^^^^^^^^^^^^^^^^

The following functions were removed from ``utils.py`` in 1.2.3:

* ``checkType``
* ``typeChecker``

If your own code depends on these functions, replace them with ``typeguard.typechecked`` (which CodeVideoRenderer now uses internally) or implement your own type checking.

No Action Needed for Basic Usage
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you only use the high-level :class:`~.CameraFollowCursorCV` API (as shown in :doc:`tutorials`), no code changes are required—the breaking changes affect internal utilities and direct imports from ``utils.py``.

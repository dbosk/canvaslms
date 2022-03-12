"""
Package containing modules to summarize assignment groups in different ways.

For a module to be used with the `canvaslms results -S module` option, the 
module must fulfil the following:

  1) It must contain a function named `summarize_group`.
  2) `summarize_group` must take two arguments:

      I) `assignment_list`, a list of `canvasapi.assignment.Assignment` 
      objects.

      II) `users_list`, a list of `canvasapi.user.User` objects.

  3) The return value should be a list of tuples. Each tuple should have the 
     form `(user, grade, grade date)`.

See the built-in modules below.
"""

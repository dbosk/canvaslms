"""
This package contains modules to summarize assignment groups in different ways. 
These modules are used with the `-S` option of the `results` command.

For a module to be used with the `canvaslms results -S module` option, the 
module must fulfil the following:

  1) It must contain a function named `summarize_group`.
  2) `summarize_group` must take two arguments:

       I) `assignment_list`, a list of `canvasapi.assignment.Assignment`
          objects. These assignments all belong to the same group, \ie their
          grades should be used to compute the student's final grade.

      II) `users_list`, a list of `canvasapi.user.User` objects. This is a
          list of users, i.e. students, for whom to compute the grades.

  3) The return value should be a list of lists. Each list should have the
     form `[user, grade, grade date, grader 1, ..., grader N]`.

For more details, see Chapter 11 of the `canvaslms.pdf` file found among the 
release files at:

  https://github.com/dbosk/canvaslms/releases
"""

# canvaslms: A CLI to Canvas LMS.

This program provides a command-line interface for Canvas. The command
is `canvaslms` and it has several subcommands in the same style as Git.
`canvaslms` provides output in a format useful for POSIX tools, this
makes automating tasks much easier.

Let's consider how to grade students logging into the student-shell SSH
server. We store the list of students' Canvas and KTH IDs in a file.

``` {.text}
canvaslms users -c DD1301 -s | cut -f 1,2 > students.csv
```

Then we check who has logged into student-shell.

``` {.text startFrom="2"}
ssh student-shell.sys.kth.se last | cut -f 1 -d " " | sort | uniq \
  > logged-in.csv
```

Finally, we check who of our students logged in.

``` {.text startFrom="4"}
for s in $(cut -f 2 students.csv); do
  grep $s logged-in.csv && \
```

Finally, we can set their grade to P and add the comment "Well done!" in
Canvas. We set the grades for the two assignments whose titles match the
regular expression `(Preparing the terminal|The terminal)`.

``` {.text startFrom="6"}
    canvaslms grade -c DD1301 -a "(Preparing the terminal|The terminal)" \
      -u $(grep $s students.csv | cut -f 1) \
      -g P -m "Well done!"
done
```

## Installation

Just install the PyPI package:
```
python3 -m pip install canvaslms
```
Some subcommands use `pandoc`, so you will likely have to [install 
pandoc][pandoc] on your system manually.

[pandoc]: https://pandoc.org/installing.html

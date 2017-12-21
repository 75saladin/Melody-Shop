# Melody Shop
This project is written in python 2, but is intended to be run in the digital sound synthesis and signal-processing framework RTcmix. This project uses the python version of RTcmix. For more information on RTcmix, see rtcmix.org.

This project started as my final project for [Dr. Jerod Sommerfeldt](https://jerodsommerfeldt.com/)'s course Advanced Computer Music at SUNY Potsdam's Crane School of Music. Since then, I have been working on it as a project to represent musical theory concepts in code. It can be used as originally designed, to interface with RTcmix and experiment with generated music, but I also plan to import the non-RTcmix portions in projects that need music theory for its own sake or to interface with other sound frameworks.

### Running instructions:

In order to run this project, you must have the standalone version of RTcmix, configured for python, installed on your machine. To verify that your copy of RTcmix is configured for python, try running the command `PYCMIX` (or check your RTcmix/bin/ directory will contain PYCMIX). Your default python version (check by running the command `python --version`) must be 2.x for PYCMIX to work correctly.

If you need to use an absolute path to run PYCMIX (that is, simply running `PYCMIX` does not work for you), create a file called `pycmix.cfg` in the root project folder. Edit it to contain one line: the path to your PYCMIX binary. Example contents:
```
~/RTcmix/bin/PYCMIX
```

Finally, from the top-level directory (where main.py resides), use the following command:
 ```
 ./play
 ```

Each run is recorded by default and sorted into the recordings directory. If you would like to skip recording, use the `-nr` flag:
 ```
./play -nr
```

Several minor file/directory name configurations can be edited in the script `play`.

You may edit any of the variables found in `config.py` to affect the generated piece.

_____
### FAQ:
* __Why do I have to run the script only from the top-level directory?__
This is necessary because RTCmix python scripts triggered by PYCMIX do not have the script's directory on the class path (sys.path). It seems there is no way to retrieve the file's name either, since the script's `__file__` gets set to "???". So, the only way to have relative imports work is to manually add the current working directory to the class path and always execute the project (main.py) from its top-level directory (where main.py should reside).
* __What is the branching scheme?__
`master` contains releases, 1.0 being the project mostly as-played for the school project. `develop` contains everyday development. Release branches are used in preparation for release <\#>. They are named `release-<#>` and end by merging back into `develop` and `master`. For more information, see [the article I'm following](http://nvie.com/posts/a-successful-git-branching-model/).


### Glossary:
* __Scorefile:__
A text file in the ".sco" format. These files are parsed by Minc using the command "CMIX".
* __Script:__
I will use this term to refer to a python script (".py"). These files are parsed by python using the command "PYCMIX".
* __Score:__
The highest-level script hat encompasses the entire piece.
* __Piece:__
A complete musical work. When we run the score, we hear the "piece"
that the score scripts.

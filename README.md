
Installation:
-------------

Firstly, set-up virtualenv:

```bash
# at this point install virtualenv with you package manager
cd /path/where/prj/should/be/stored
virtualenv -p python3 .env
ln -s .env/bin/activate . // to be easier to start virtual env
```

Now start the env:

```bash
source activate
# or with alias for source
. activate
```

After you got into env, clone the project and install python packages:

```bash
git clone --recursive git@github.com:vindex10/sumrules-prj.git
cd sumrules-prj
pip install -r requirements.txt
```

Running tests:
---------------

Basic run (be careful, previous results of the test to be run will be dropped):

```bash
cd tests
make sqedPw # or any other present in folder
```

Run for debugging:
```bash
cd tests
make debug_sqedPw # or any other present in folder
```
Clean results for specific test, or all ones:
```bash
cd tests
make clean_sqedPw # or any other present in folder
make clean # cleans all output
```

There is an interface to change running parameters, like eps, mass, coupling, number of threads, precision, etc:
```bash
cd tests
REL_ERR=0.001 ABS_ERR=0.0001 M=1.27 NUM_THREADS=4 make sqedPw
```

Another interesting feature is "interactive mode". If you want to see some output during evaluation, like parameters, some values of functions to be evaluated, evaluation times, some plots, you can turn on interactivity:
```bash
cd tests
INTERACTIVE=True make sqedPw # or any other present in folder
```

And the final basic thing, how to choose a place for output:
```bash
cd tests
OUTPUT="somedir/anotherdir/" make sqedPw # place output files to tests/somedir/anotherdir/sqedPw/
```

To see all parameters, firstly run test, then check file "params" in output.

Refactor plans:
---------------

* Interactive printing must occur automatically when writing to file occurs (partially implemented with _iwrite_ function)
* Organize multithreading in the right way. Provide an ability to broadcast on the lowest level and multiprocess on the highest one.

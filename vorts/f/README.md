
`m_vorts` uses some [Fortran 2003 features](http://fortranwiki.org/fortran/show/Fortran+2003)
(a bit of OOP).

## Installing

To compile the Fortran model, navigate to `src` and run `make`.
The `Makefile` will have to be adjusted if you don't want to use `gfortran`.

The hello-world program can be used to test your Fortran installation.
Compile with `gfortran -ffree-form hello_world.f -o hello_world.exe`

### Windows

You can download [gfortran binaries for Windows](https://gcc.gnu.org/wiki/GFortranBinariesWindows),
but in order to also have `make`, MinGW via [MSYS2](https://www.msys2.org/) might be an easier option.
In order to run from Python on Windows, MinGW tools have to be on your PATH.

### Linux

On Debian-like distros, `gfortran` can be obtained using `apt`.

On Linux or Mac, [Homebrew](https://brew.sh/) can be used to (potentially) obtain more recent versions of GNU Fortran
by installing the GNU compiler collection formula: `brew install gcc` (see [formulae](https://formulae.brew.sh/formula/gcc)).
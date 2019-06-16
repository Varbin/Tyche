=========================
Tyche - Fortuna in Python
=========================

Python implementation of the CSPRNG
(Cryptographic-Secure-Pseudo-Random-Number-Generator)
Fortuna, designed by Bruce Schneier and Niels Ferguson, build with AES as
block cipher and SHAd256 as secure hash function. 

**Important note:** Do not use this library for secure random number generation, 
if the alternatives are better. 
On modern Windows, Fortuna is already the default CSPRNG.
Modern BSDs and Linux system have a secure random number generation.
Additionally the development of this library has stopped 
and the repository has been put into an archived state.

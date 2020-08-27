# AES_Crypt
Contains the implementation of 128 bit AES in python using a Rijndael sbox (AES.py) and has a C++ implementation of a Bitmap encrypter for confidentially sharing information (Pictures) with anyone you want.

## Requirements:
Python based AES does not require any external libraries. You can input whatever data you need encrypted! 

For ImageCrypt.cpp, `cryptoc++` library is needed. The program was tested on a debian based system and was shown to work perfectly

Do contact me for any issues! The working is self-explanatory:
1. Input image name in the .cpp file
2. Compile the code
3. Run it and input your 16byte key
4. Find your encrypted image in the same folder as your original one


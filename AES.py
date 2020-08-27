import textwrap
from copy import copy 

####################################
# Initial key and plaintext conversion
#making initial key and plain text
#Key - k
inp = "Thats my Kung Fu".encode('utf-8')
v = inp.hex()
w = []
keyround = []
k = []
T = textwrap.wrap(v,8)
for i in T:
    k.append(textwrap.wrap(i,2))

#Plain text - plaintext
inp2 = 'Two one Nine TwO'.encode('utf-8')
v = inp2.hex()
plaintxt = []
T = textwrap.wrap(v,8)
for i in T:
    plaintxt.append(textwrap.wrap(i,2))



#xor test bitwise
def xor(a,b):
    u = []
    for i in range(0,2):
        u.append(hex(int(a[i],16) ^ int(b[i],16))[2:])

    u = ''.join(u)
    return u

#definintion on Rotate left
def rotate(l, n):
    return l[n:] + l[:n]


# to get desired Sbox value from f=hex input
def sbox(val):
    Sbox = (
            0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
            0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
            0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
            0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
            0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
            0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
            0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
            0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
            0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
            0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
            0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
            0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
            0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
            0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
            0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
            0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16
            )
    
    #print("val values")
    #print(val)
    v = [int(val[0],16),int(val[1],16)]
    t = (v[0] * 15 + v[1]) + v[0]
    y = hex(Sbox[t])[2:]
    if(len(y)<2):
        y = "0" + y
    return y

# Rcon value
rci = ['','01','02','04','08','10','20','40','80','1B','36']

###########################
#To split into rounds (11,13,15)
def split_list (x,word):
   return [word[i:i+x] for i in range(0, len(word), x)]

#matrix xor module
def xormat(a,b):
    final = []
    for i in range(0,len(b)):
        temp1 = xor(a[i][0],b[i][0])
        temp2 = xor(a[i][1],b[i][1])
        temp3 = xor(a[i][2],b[i][2])
        temp4 = xor(a[i][3],b[i][3])
        final.append([temp1,temp2,temp3,temp4])

    return final

#sbox matrix module
def sboxmat(s):
    final = []
    for i in range(0,len(s)):
        temp1 = sbox(s[i][0])
        temp2 = sbox(s[i][1])
        temp3 = sbox(s[i][2])
        temp4 = sbox(s[i][3])
        final.append([temp1,temp2,temp3,temp4])

    return final


#shift row
def shiftrow(k):
    temp1 = []
    temp2 = []
    temp3 = []
    temp4 = []
    templist = []
    templist1 = []
    for i in range(0,len(k)):
        temp1.append(k[i][0])

    for i in range(0,len(k)):
        temp2.append(k[i][1])

    for i in range(0,len(k)):
        temp3.append(k[i][2])

    for i in range(0,len(k)):
        temp4.append(k[i][3])

    templist.append(temp1)
    templist.append(temp2)
    templist.append(temp3)
    templist.append(temp4)

    #print(len(templist))

    for i in range(0,len(templist)):
        templist1.append(rotate(templist[i],i))

    finallist = []
    temp1 = []
    temp2 = []
    temp3 = []
    temp4 = []
    for i in range(0,len(templist1)):
        temp1.append(templist1[i][0])

    for i in range(0,len(templist1)):
        temp2.append(templist1[i][1])

    for i in range(0,len(templist1)):
        temp3.append(templist1[i][2])

    for i in range(0,len(templist1)):
        temp4.append(templist1[i][3])

    finallist.append(temp1)
    finallist.append(temp2)
    finallist.append(temp3)
    finallist.append(temp4)

    return finallist

# Shift riw right
def shiftright(k):
    temp1 = []
    temp2 = []
    temp3 = []
    temp4 = []
    templist = []
    templist1 = []

    # conversion from coloumn to rows
    for i in range(0,len(k)):
        temp1.append(k[i][0])

    for i in range(0,len(k)):
        temp2.append(k[i][1])

    for i in range(0,len(k)):
        temp3.append(k[i][2])

    for i in range(0,len(k)):
        temp4.append(k[i][3])

    templist.append(temp1)
    templist.append(temp2)
    templist.append(temp3)
    templist.append(temp4)

    #print(len(templist))

    #Rotation left
    for i in range(0,len(templist)):
        templist1.append(rotate(templist[i],-i))

    finallist = []
    temp1 = []
    temp2 = []
    temp3 = []
    temp4 = []

    #convert to original form
    for i in range(0,len(templist1)):
        temp1.append(templist1[i][0])

    for i in range(0,len(templist1)):
        temp2.append(templist1[i][1])

    for i in range(0,len(templist1)):
        temp3.append(templist1[i][2])

    for i in range(0,len(templist1)):
        temp4.append(templist1[i][3])

    finallist.append(temp1)
    finallist.append(temp2)
    finallist.append(temp3)
    finallist.append(temp4)

    return finallist

def sboxinv(val):
    Sbox_inv = (
            0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
            0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB,
            0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E,
            0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25,
            0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92,
            0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
            0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06,
            0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B,
            0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73,
            0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E,
            0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B,
            0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
            0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F,
            0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF,
            0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61,
            0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D
            )
    
    v = [int(val[0],16),int(val[1],16)]
    t = (v[0] * 15 + v[1]) + v[0]
    y = hex(Sbox_inv[t])[2:]
    if(len(y)<2):
        y = "0" + y
    return y

def sboxmatinv(s):
    final = []
    for i in range(0,len(s)):
        temp1 = sboxinv(s[i][0])
        temp2 = sboxinv(s[i][1])
        temp3 = sboxinv(s[i][2])
        temp4 = sboxinv(s[i][3])
        final.append([temp1,temp2,temp3,temp4])

    return final


##############################################################
# MIX COLOUMN 
###################################################################
# The below THREE functions were taken from Github.
# https://gist.github.com/raullenchai/2920069

def galoisMult(a, b):
    p = 0
    hiBitSet = 0
    for i in range(8):
        if b & 1 == 1:
            p ^= a
        hiBitSet = a & 0x80
        a <<= 1
        if hiBitSet == 0x80:
            a ^= 0x1b
        b >>= 1
    return p % 256

def mixColumn(column):
    temp = copy(column)
    column[0] = galoisMult(temp[0],2) ^ galoisMult(temp[3],1) ^ \
                galoisMult(temp[2],1) ^ galoisMult(temp[1],3)
    column[1] = galoisMult(temp[1],2) ^ galoisMult(temp[0],1) ^ \
                galoisMult(temp[3],1) ^ galoisMult(temp[2],3)
    column[2] = galoisMult(temp[2],2) ^ galoisMult(temp[1],1) ^ \
                galoisMult(temp[0],1) ^ galoisMult(temp[3],3)
    column[3] = galoisMult(temp[3],2) ^ galoisMult(temp[2],1) ^ \
                galoisMult(temp[1],1) ^ galoisMult(temp[0],3)

    return column

def mixColumnInv(column):
    temp = copy(column)

    column[0] = galoisMult(temp[0],14) ^ galoisMult(temp[3],9) ^ \
                galoisMult(temp[2],13) ^ galoisMult(temp[1],11)
    column[1] = galoisMult(temp[1],14) ^ galoisMult(temp[0],9) ^ \
                galoisMult(temp[3],13) ^ galoisMult(temp[2],11)
    column[2] = galoisMult(temp[2],14) ^ galoisMult(temp[1],9) ^ \
                galoisMult(temp[0],13) ^ galoisMult(temp[3],11)
    column[3] = galoisMult(temp[3],14) ^ galoisMult(temp[2],9) ^ \
                galoisMult(temp[1],13) ^ galoisMult(temp[0],11)
    
    return column
#################################################################################



# mix coloumn enc
def mixColumns(l):

    temp2 = []
    finalval = []
    for j in l:
        temp = [int(x, 16) for x in j]
        temp2.append(temp)

    for i in temp2:
        val = mixColumn(i)
        temp3 = []
        for f in val:
            f1 = hex(f)[2:]
            temp3.append(f1.zfill(2))
        
        finalval.append(temp3)

    return finalval

#Mix coloumn dec
def mixColumnsinv(l):
    temp2 = []
    finalval = []
    for j in l:
        temp = [int(x, 16) for x in j]
        temp2.append(temp)


    for i in temp2:
        val = mixColumnInv(i)
        temp3 = []
        for f in val:
            f1 = hex(f)[2:]
            temp3.append(f1.zfill(2))
        
        finalval.append(temp3)

    return finalval


#################################
#        KEY EXPANSION
#################################


def keyexpansion(k):
    
    # Enter N and R value according to the key
    #TODO change the vales according to the key
    N = 4
    R = 11

    #Creation
    for i in range(0,R*N):
        if(i<N):
            #print("first box")
            #print(i)
            w.append(k[i])
        elif((i>=N) and (i%N == 0)):
            #print("second box")
            #print(i)
            # the Rotated values
            temp = rotate(w[i-1],1)
            #contains the sbox values
            subval = []
            for j in temp:
                temp2 = sbox(j)
                subval.append(temp2)

            # the value of rcon
            rval = rci[int(i/N)]
            
            #xor woth rcon(Singularity condition)
            y = xor(rval,subval[0])
            subval[0] = y

            # Xor of W[i-N] with Sbox
            ans = []
            
            for r in range(0,N):
                ans.append(xor(w[i-N][r],subval[r]))
            w.append(ans)
        elif(i>=N and N>6 and i%N == 4):
            #print("third box")
            #print(i)
            ans2 =[]
            sval = []

            for j in w[i-1]:
                temp2 = sbox(j)
                sval.append(temp2)

            #Xor of Sbox(wi-1) and wi-N
            for v in range(0,N):
                ans2.append(xor(w[i-N][v],sval[v]))

            w.append(ans2)
        else:
            #print("fourth box")
            #print(i)

            ans3 = []

            #xor of Wi-N and Wi-1
            for v in range(0,N):
                ans3.append(xor(w[i-1][v],w[i-N][v]))
                

            w.append(ans3)
    
    return w


############################################################
#  ENCRYPTION
#  INPUTS ARE key and plain text
############################################################
def AesEnc(k,p):

    #Key parameters
    #TODO change the vales according to the key
    N = 4
    R = 11

    # the final value of the process
    state = []

    #keygeneration
    # w contains words from w0 - wrn-1
    w = keyexpansion(k)

    # contains the words in rounds (0-10)
    keyround = split_list(4,w)

    # Going Through the rounds
    for i in range(0,R):
        if(i == 0):
            state = xormat(keyround[i],p)
            #print("round number" + str(i))
            #print(state)
        elif(i>0 and i<R-1):
            #print("round number" + str(i))
            # Byte sub
            state = sboxmat(state)
            #print(state)

            #shift row
            state = shiftrow(state)
            #print(state)

            #mixcoloumn
            state = mixColumns(state)
            #print(state)

            # add round key
            state = xormat(state,keyround[i])
            #print('xor key last')
            #print(keyround[i])
            #print(state)
        else:
            #print("round number" + str(i))
            #Byte sub
            state = sboxmat(state)
            #Shift row
            state = shiftrow(state)
            #add round key
            state = xormat(state,keyround[i])
            #print(state)

    # Final excrypted value
    return state



##########################################################################
# Decryption
# Input is the Cipher text and keys
##########################################################################
def AesDec(k,l):

    #Key parameters
    #TODO change the vales according to the key
    N = 4
    R = 11

    # the final value of the process
    state = []

    #keygeneration
    # w contains words from w0 - wrn-1
    w = keyexpansion(k)

    # contains the words in rounds (0-10)
    keyround = split_list(4,w)

    for i in reversed(range(0,R)):
        if (i == R-1):

            #add round key
            state = xormat(l,keyround[i])

            #Shift row
            state = shiftright(state)

            #Byte sub
            state = sboxmatinv(state)

    
            #print("round " + str(i))

        elif(i>0 and i<R-1):
            
            #print("round " + str(i))
            # add round key
            state = xormat(state,keyround[i])

            #MixcoloumnInv
            state = mixColumnsinv(state)

            #shift row
            state = shiftright(state)

            # Byte sub
            state = sboxmatinv(state)

        else:
            #print("round " + str(i))
            state = xormat(state,keyround[i])


    return state
        
##############################################3
# Uncomment to run Aes
'''
# Output. 
##################
#Encrypt
c = AesEnc(k,plaintxt)
# Decrypt
p = AesDec(k,c)

print(p)
'''

c = AesEnc(k,plaintxt)
p = AesDec(k,c)
for i in p:
    for j in i:
        x = bytes.fromhex(j)
        print(x.decode("ASCII"),end="")

###############################################################3
#Uncomment to run ECB

'''
##################################################################
# Uncomment to run
##########################################################################
# ECB
##########################################################################
# ENcryption
####################################################################
# Taking Input from the user
inp2 = input('Enter Plain text for Block Cipher modes').encode('utf-8').hex()
modinput = []
#Breaking intp 128 bits and padding
inpwhole = textwrap.wrap(inp2,32)

def pad(val):
    if(len(val[-1])!= 32):
        temp = val[-1].zfill(32)
        val[-1] = temp
        return val

paddedinput = pad(inpwhole)

#Converting input into appropriate 
for i in paddedinput:
    T = textwrap.wrap(i,8)
    for j in T:
        modinput.append(textwrap.wrap(j,2))


# Making initial key
k = []
Ciphertext = []
inp = "Thats my Kung Fu".encode('utf-8')
v = inp.hex()
T = textwrap.wrap(v,8)
for i in T:
    k.append(textwrap.wrap(i,2))


modinput = split_list(4,modinput)

for i in modinput:
    Ciphertext.append(AesEnc(k,i))


###############################################################################
# Decryption
Decrypted_pt = []
for j in Ciphertext:
    Decrypted_pt.append(AesDec(k,j))

print(Decrypted_pt)


#####################################################################################################
'''


'''
##################################################33
# Uncomment to run
##############################################################################
# CBC
#############################################################################
#  Encryption
#############################################################################
# Taking Input from the user
inp2 = input('Enter Plain text for Block Cipher modes').encode('utf-8').hex()
ciphertxt = []
modinput = []
#Breaking intp 128 bits and padding
inpwhole = textwrap.wrap(inp2,32)

def pad(val):
    if(len(val[-1])!= 32):
        temp = val[-1].zfill(32)
        val[-1] = temp
        return val

paddedinput = pad(inpwhole)

#Converting input into appropriate 
for i in paddedinput:
    T = textwrap.wrap(i,8)
    for j in T:
        modinput.append(textwrap.wrap(j,2))

modinput = split_list(4,modinput)
print(modinput)

#initial vector
inpIV = 'Two One Nine Two'.encode('utf-8')
v = inpIV.hex()
IV = []
T = textwrap.wrap(v,8)
for i in T:
    IV.append(textwrap.wrap(i,2))

for i in range(0,len(modinput)):
    if(i == 0):
        #inter is the xor value
        inter = xormat(IV,modinput[i])
        ciphertxt.append(AesEnc(k,inter))
    else:
        inter = xormat(modinput[i],ciphertxt[i-1])
        ciphertxt.append(AesEnc(k,modinput[i]))

# The Cipher text
#print(ciphertxt)

#######################################################################
# Decryption
pltxt = []
for i in range(0,len(ciphertxt)):
    if (i == 0):
        temp = AesDec(k,ciphertxt[i])
        pltxt.append(xormat(temp,IV))
    else:
        temp = AesDec(k,ciphertxt[i])
        pltxt.append(xormat(temp,ciphertxt[i-1]))

#Plain text
print(pltxt)

'''
# Many-Time-Pad
## Introduction
The objective of this assignment was to show the weakness of a many-time-pad. This is
when the key for a one-time-pad encryption method is used more than once. The one time
pad, when implemented correctly, is considered to be one of the most secure types of
encryption.
When the key is used to encrypt more than one message however it loses this security
instantly. It can be decrypted using crib dragging which involves XORing two ciphertexts
together that have been encrypted with the same key and then choosing common words
such as “the”, “and”, “hello”, and XOR these with the result of the previous. This should then
display some letters and slowly reveal the key. However, as programmers, this is not the
quickest and most efficient way of doing this and we have been provided with 16 ciphertexts
one of which is the target to decrypt giving us a lot of information to work with.
The approach taken here is to use the knowledge of what happens when a space is XORed
with a letter. When you XOR a space with any letter it returns that letter in the opposite
casing for example ‘a’ ⊕ ’ ’ results in 65 which when converted to a character using the ascii
table is the letter ‘A’. Using this knowledge it helps identify where in our plaintext we have a
space and thus also get the byte from the key that encrypted this space.

## Implementation
### Step 1
```python
def decode_the_ciphertexts(list_of_ciphers, key):
    for index, c in enumerate(list_of_ciphers):
        index_of_spaces = {}
        list_of_space_indexes = []

        for index_n, c_n in enumerate(list_of_ciphers):
            if index != index_n:
                c_decoded = hex_decoding(c)
                c_n_decoded = hex_decoding(c_n)

                c_list = make_list_of(c_decoded)
                c_n_list = make_list_of(c_n_decoded)

                c_ord = convert_to_unicode(c_list)
                c_n_ord = convert_to_unicode(c_n_list)

                xor_res = perform_xor_on_dec(c_ord, c_n_ord)
                char_res = convert_unicode_to_char(xor_res)
                find_possible_spaces(char_res, index_of_spaces)

        confirm_possible_spaces(index_of_spaces, list_of_space_indexes)

        get_key(list_of_space_indexes, c, key)
```
The function ‘decode_the_ciphertexts’ seen above takes in a list of all the ciphertexts,
excluding the target ciphertext, and a list for storing the key. The list for storing the key was
initialised with ‘00’*215. The reason for 215 times is because this is the length of the longest
ciphertext.
The function begins using a double for loop to enumerate through the ciphertexts and
compare each one. A single ciphertext that we shall refer to as c1 is selected and then the
following is performed for all remaining ciphertexts against c1. We shall refer to these other
ciphertexts as c2.

### Step 2
The first step in the function ‘decode_the_ciphertexts’ is to perform hex decoding on both c1
and c2.
```python
def hex_decoding(s):
    result = s.decode("hex")
    return result
```
As can be seen in above it takes advantage of the python2.7 decoding function to
quickly perform hex decoding and returns the result.

### Step 3
Once c1 and c2 have undergone hex decoding they are converted into lists. The function
‘make_list_of’ as seen below does this by taking each character within a ciphertext passed
to it as ‘s’ and appending it to a list which is then returned.
```python
def make_list_of(s):
    list = []

    for char in range(len(s)):
        list += [s[char]]

    return list
```
This is done to make it easier to process c1 and c2 for the next function which is converting
the characters to their Unicode counterparts.

### Step 4
To convert the characters to their Unicode counterpart the ord function is used. The reason
for converting these to Unicode is it makes it easier to XOR c1 and c2 together. The
following is the function used for processing the two ciphertexts and converting them to
Unicode.
```python
def convert_to_unicode(s):
    s_ord = []

    for i in range(len(s)):
        s_ord += [ord(s[i])]

    return s_ord
```
### Step 5
Now that the ciphertexts are in Unicode which is a list of integers they can be XORed
together to identify where there is a potential space within the original plaintext of one of the
ciphertexts.
```python
def perform_xor_on_dec(s1, s2):
    result = []

    if len(s1) < len(s2):
        s1_len = len(s1)
        # s2_len = len(s2)

        new_s2 = s2[:s1_len]

        for i in range(len(s1)):
            result.append(s1[i] ^ new_s2[i])
        return result

    if len(s1) > len(s2):
        # s1_len = len(s1)
        s2_len = len(s2)
        new_s1 = s1[:s2_len]

        for i in range(len(s2)):
            result.append(new_s1[i] ^ s2[i])
        return result

    else:
        for i in range(len(s2)):
            result.append(s1[i] ^ s2[i])
        return result
```
Let's go through this function step by step as it appears to be performing a lot, but is quite
simple. Firstly we compare the length of the two ciphertexts and find which one is longer and
make this equal to the length of the shorter one. The reason for making this shorter instead
of inserting padding to the end of the shorter ciphertext is simply because there is going to
be no valuable information retrieved from the extra bytes.
Then it simply takes the two ciphertexts and cycles through each element of the lists and
XORs them together and returns the result of this. The reason for doing this is it can help
with identifying potential spaces in the plaintext however it is not possible to say which
plaintext this comes from.
This works because c1 ⊕ c2 = plaintext1 ⊕ plaintext2. So if there is an alphabetical character
found it potentially means that there is a space in one of the plaintexts.

### Step 6
This next function called simply takes the result from the previous function and converts it
from Unicode to characters. This makes it easier to process and identify spaces.
```python
def convert_unicode_to_char(dec):
    result = []

    for i in range(len(dec)):
        result.append(chr(dec[i]))

    return result
```
### Step 7
The next step taken is to identify potential spaces. These are only potential spaces in the
plaintext and we are unsure of which plaintext the space is in. This is achieved using the
following function.
```python
def find_possible_spaces(res, dict):
    for index, c in enumerate(res):
        if c.isalpha():
            try:
                dict[index] += 1
            except KeyError:
                dict[index] = 1

    return dict
```
The two inputs to this function are the result from the previous function, which is c1 ⊕ c2 and
converted to characters, and a dictionary for storing the index of a potential space within the
original plaintext of c1.
It cycles through the XORed ciphertexts and if a character is detected it stores the index of
this character and the number of times a character in this index is found. This is important as
finding the character there once would mean that it was not a space in the plaintext of c1
however if it was found several times there then this is likely the location of a space in the
plaintext of c1. Now the above steps are repeated for every ciphertext except for c1, until the
inner for loop has completed. After the inner loop has completed step 7 is started.

### Step 8
Once the inner for loop has cycled through all the ciphertexts excluding c1, next it is
confirmed that a space has been found in the plaintext of c1.
Taking the dictionary of indexes and the number of times that a character was found it is
passed through to a function along with a list for storing the confirmed spaces.
```python
def confirm_possible_spaces(index_of_spaces, list_of_space_indexes):
    for index, num_spaces in index_of_spaces.items():
        if num_spaces >= 10:
            list_of_space_indexes.append(index)
```
As can be seen above only indexes with a value greater than 10 were stored to the list. This
figure was more of a trial and error situation. 1 was too low as it was impossible to say for
sure if the index actually represented a space within the c1 and 15 was too high. The result
of either of these was similar to the following which is indecipherable. What I found was
somewhere between 7 and 10 was the ideal acceptance rate when presented with 15
ciphertexts.

### Step 9
The final step in the decode_the_ciphertexts function was to get the key and was performed
using the following ‘get_key’ function.
```python
def get_key(index_of_spaces, c, key):
    x = ' ' * 215
    c_decoded = hex_decoding(c)

    c_list = make_list_of(c_decoded)
    space_list = make_list_of(x)

    c_ord = convert_to_unicode(c_list)
    space_ord = convert_to_unicode(space_list)

    xor_res = perform_xor_on_dec(c_ord, space_ord)
    char_res = convert_unicode_to_char(xor_res)

    for index in index_of_spaces:
        key[index] = char_res[index].encode('hex') 
```
As you can see above the function takes in our index_of_spaces which was got in step 7,
ciphertext c1 which is identified by c in the above image and a list which will store the key.
This list was initialised at the beginning in the main function to contain ‘00’ *215.
First, a variable containing 215 spaces is created. 215 is to match the longest ciphertext.
Then hex decoding is performed on the ciphertext using the same function as before.
Similarly to before all the bytes of the ciphertext are added to a list and the same is done for
the variable containing the spaces.
Next, the list of spaces and ciphertext are converted to their Unicode counterparts so that
they can be XORed together. The result of this XOR is converted back to characters and will
be referred to as char_res for the remainder of this step.Now it is possible to get the key. This is done by looping through the index_of_spaces and
saving the character with the same index from char_res into the key list with the same index.
Remember this works because when a space is XORed with a alphabetical character it
converts this to its opposite casing. So when the key is XORed with the space in the original
plaintext it only changes the casing of the key if that byte was an alphabetical character.
The function now returns to the outer for loop and c1 is incremented to the next ciphertext
and the same steps above are repeated again. When there are no more ciphertexts for the
outer for loop, step 9 is performed.

### Step 10
Now that the key has been obtained it is possible to decrypt the target ciphertext by simply
XORing the key with the target ciphertext. As can be seen in the below image this goes
through the similar steps of hex decoding, making it into a list, converting to Unicode and
then XORing the ciphertext and the key together to get the answer which is converted to
characters.
```python
def decode_the_target(target, key):
    target_decoded = hex_decoding(target)

    target_list = make_list_of(target_decoded)

    target_ord = convert_to_unicode(target_list)

    for index, val in enumerate(key):
        key[index] = val.decode('hex')

    key_ord = convert_to_unicode(key)

    xor_res = perform_xor_on_dec(target_ord, key_ord)
    char_res = convert_unicode_to_char(xor_res)

    ans = "".join(char_res)
    return ans
```
### Step 11
The answer is returned from step 9 and then printed to the screen and it should be possible
to make out what the message was originally even if some of the characters have not been
decrypted properly.

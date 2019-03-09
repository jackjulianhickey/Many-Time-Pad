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


def confirm_possible_spaces(index_of_spaces, list_of_space_indexes):
    for index, num_spaces in index_of_spaces.items():
        if num_spaces >= 10:
            list_of_space_indexes.append(index)


def find_possible_spaces(res, dict):
    for index, c in enumerate(res):
        if c.isalpha():
            try:
                dict[index] += 1
            except KeyError:
                dict[index] = 1

    return dict


def convert_unicode_to_char(dec):
    result = []

    for i in range(len(dec)):
        result.append(chr(dec[i]))

    return result


def convert_to_unicode(s):
    s_ord = []

    for i in range(len(s)):
        s_ord += [ord(s[i])]

    return s_ord


def make_list_of(s):
    list = []

    for char in range(len(s)):
        list += [s[char]]

    return list


def hex_decoding(s):
    result = s.decode("hex")
    return result


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


if __name__ == '__main__':
    c1 = "0C499F42B54F03FD248FF815795F90364F554D77498FBA04F32A512BBA1B3AB494A730F3101BA07C87891C8385076B351B6810C810140165DE3844359ECD95B7621781"
    c2 = "11019B0FE54D02F13E9AB9157F109F624F5553731DDDAB06B2204D39F9113AA38EAB64E91619BE3983C80D98C10D"
    c3 = "0C499F42A45819EF3F8FF21230538C735A445B674994B149E62B5A78ED1568BC95A62BEA005ABB359B844E90CA48627B5E7611CF0E0D102CC934173697CF99E5620DD8AD6B214BDFEB1EE5D643AB39B1"
    c4 = "0C499311E5431EB82495FC4164498E731B5F58230D9CA649E62B5E2CBA1B3AB18FBD2CFF0117AD32D784079CC01B"
    c5 = "1952DA11AD451AF6709CFB0E6655DE7F4F10496C1C91BB49E622543DBA1B3ABB89A023BA0713A139D79C01D7C71A6874152610C507441065DD350134"
    c6 = "114FDA16AD4F4DFE3F91F50E675990711B435D710C98B11AFA2C4B78E3156FF785AF2ABA001FA97C83800F83851C65705E6508C4070A072CC42E443689CB93A0651791B764640A98F40EF29D5FA078BC45DFA2A51DD64FF96594CA71"
    c7 = "0C499311E54908EA2494FF0873518A731B53516D1D9CB607E1635E78E91F68BE87A264F40617AE3985C80F99C1487D601C6A0DCE420F16758D3C0A22DBDA88A02B079DAD622D07CBA704E09D44AE3DFF5FDAA8AA0A9548AC6D8ECB2211F2A46843B72F7E64B8"
    c8 = "17548842A04905F7708EFC1366558C36485851760599FF05FB304B3DF45A6FB992A728BA125AAF309E8D0083850B627B106307D911441262C97D102E9EC0C0B66E0D9CF9626418CCF502E8DA"
    c9 = "0C499F42A0520CF52091FC12305990364F585770499EB708E2375A2ABA1B68B2C6AC21E9075ABE2999C8019985092D79176811D5420B0369DF3C102F95C9C0B672108CBC6E"
    c10 = "1901980BB74E4DF13EDDED097510967755541E6A1ADDA806E0375778EE0D75F78FA064EE1B1FEC3E829B06D7CA1A2D66112610C50744006DD4340A21DBC98FA078"
    c11 = "0F499B16B64B1DE87099F6417E5F8A364D554C6A0F84FF1DFA261F3DF71B73BBC6AF20FE011FBF2FD79C01D7C60763731774098D0B10002CCC3E073389CF83BC"
    c12 = "1155DA0BB60A01F7339CED04741097781B4456664990BE00FC635E2AFF1B3AA08EA727F25313BF7C9D9D1D83851D63711B7444D90A01537EC82E10278EDC81AB7F"
    c13 = "0C499B0CAE0A14F725DDEF046249DE7B4E5356230F92AD49E62B5A78F3146CBE92AF30F31C14EC3D998C4E9E851F6479122605D916011D688D290C23DBC385A07F0A96BE"
    c14 = "0F44DA10A04908F62491E04174598D754E434D660DDDAB01F7634D3DFE5A7CB894AB37EE5319A332948D1E8385097E351168018D0D025378C538442A9ADA85B67F438CAB662A0FCBA702E89D51A52CB65ACAEAA4068459EF788FDD7B45E9A42B5FB6357F78"
    c15 = "0C499F42A34501F43F8AF00F77108D7549555B6D1A95B01DB2305737ED5A6EBF83EE36FF1E15B839D79B0B85D30D7F351D6316D90B021A6FCC2901"

    target_cipher = "014E8F42A75802F335DDED0975109D6442404A6C0E8FBE19FA3A1F21F50F3AB694AB64F41C0DEC3DD78B1C8ED51C6C7B1F6A1DDE16"

    list_of_ciphers = [c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13, c14, c15]

    key = ['00'] * 215

    decode_the_ciphertexts(list_of_ciphers, key)
    print "KEY:", key

    ans = decode_the_target(target_cipher, key)

    print "DECRYPTED CIPHERTEXT:", ans



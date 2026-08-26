print("<<Welcome to number system conversion>>")

while True:
    user_input_data=input("Enter your number for conversion: ")
    try:
        if all(c in "-.0123456789abcdefABCDEF" for c in user_input_data) and any(c in "-123456789abcdefABCDEF" for c in user_input_data) and user_input_data.count('.') <= 1 and user_input_data.count('-') <= 1 and :
            user_input_data=user_input_data
            break
        #if '.' in user_input_data:
            #i = float( user_input_data)
            #break
        #elif '.' not in user_input_data:
            #i = int(user_input_data)
            #break
        #elif all(c in ".0123456789abcdefABCDEF" for c in user_input_data):
            #return user_input_data
        else:
            print("Please enter valid data!")
    except:
        print("Please enter only numbers!")
        
        
#print(f"Input type - {type(i)}\n ")

print(f"Number type-\n1. Binary\n2. Octal\n3. Decimal\n4. Hexadecimal")

while True:
    users_1st_option=input(f"Select the type you want to convert from: ")
    try:
        users_1st_option = int(users_1st_option) 
        if users_1st_option < 6 and users_1st_option > 0:
            users_1st_option = users_1st_option
            break
        else:
            print("Wrong input!")
    except:
        print("Please only type the relative number of the option!")
while True:
    users_2st_option=input(f"Select the type you want to convert to: ")
    try:
        users_2st_option = int(users_2st_option)
        if users_2st_option == 1 or users_2st_option == 2 or users_2st_option == 3 or users_2st_option == 4:
            users_2st_option = users_2st_option
            break
        else:
            print("Wrong input!")
    except:
        print("Please only type the number corresponding to the option!")
str_user_data = str(user_input_data)#
splited_int_and_float_listdata = str_user_data.split('.')
str_user_data_int_part = splited_int_and_float_listdata[0]
len_int_part=len(str_user_data_int_part)
int_index_number = 0
float_index_number = 0
padded_int_start_index = 0
padded_float_start_index = 0
padded_int_end_index=0
padded_float_end_index=0
use_of_a_func_checker = 0
int_result = ''
float_result = ''

# Binary to Octal
if users_1st_option == 1 and users_2st_option == 2:
    padded0_int_part = str_user_data_int_part.zfill(len_int_part+(3-(len_int_part%3)))
    groups_3_bin_ints=[]
    for i in padded0_int_part:
        padded_int_end_index += 1
        if padded_int_end_index%3 == 0:
            groups_3_bin_ints = groups_3_bin_ints + [padded0_int_part[padded_int_start_index:padded_int_end_index]]
            padded_int_start_index+=3
    
    list_intbin_converted_t_oct = []
    if set(str_user_data_int_part) <= {'0', '1'}:
        for j in groups_3_bin_ints:
            if groups_3_bin_ints[int_index_number] == '001':
                list_intbin_converted_t_oct = list_intbin_converted_t_oct + [1]
            elif groups_3_bin_ints[int_index_number] == '010':
                list_intbin_converted_t_oct = list_intbin_converted_t_oct + [2]
            elif groups_3_bin_ints[int_index_number] == '011':
                list_intbin_converted_t_oct = list_intbin_converted_t_oct + [3]
            elif groups_3_bin_ints[int_index_number] == '100':
                list_intbin_converted_t_oct = list_intbin_converted_t_oct + [4]
            elif groups_3_bin_ints[int_index_number] == '101':
                list_intbin_converted_t_oct = list_intbin_converted_t_oct + [5]
            elif groups_3_bin_ints[int_index_number] == '110':
                list_intbin_converted_t_oct = list_intbin_converted_t_oct + [6]
            elif groups_3_bin_ints[int_index_number] == '111':
                list_intbin_converted_t_oct = list_intbin_converted_t_oct + [7]
            elif groups_3_bin_ints[int_index_number] == '000':
                list_intbin_converted_t_oct = list_intbin_converted_t_oct + [0]
            else:
                break
            int_index_number += 1
    else:
        print("Number is not a binary!")
        
    int_result= ''.join(map(str, list_intbin_converted_t_oct))
    if splited_int_and_float_listdata[0] != str_user_data:
        str_user_data_float_part = splited_int_and_float_listdata[1]
        len_float_part = len(str_user_data_float_part)
        zneed = 3-(len_float_part%3)+len_float_part
        padded0_fractional_part = str_user_data_float_part.ljust(zneed, '0')
        groups_3_bin_floats=[]
        list_floatbin_converted_t_oct = []
        for io in padded0_fractional_part:
            padded_float_end_index += 1
            if padded_float_end_index%3 == 0:
                groups_3_bin_floats = groups_3_bin_floats + [padded0_fractional_part[padded_float_start_index:padded_float_end_index]]
                padded_float_start_index+=3
        if set(str_user_data_float_part) <= {'0', '1'}:
            for ji in groups_3_bin_floats:
                if groups_3_bin_floats[float_index_number] == '001':
                    list_floatbin_converted_t_oct = list_floatbin_converted_t_oct + [1]
                elif groups_3_bin_floats[float_index_number] == '010':
                    list_floatbin_converted_t_oct = list_floatbin_converted_t_oct + [2]
                elif groups_3_bin_floats[float_index_number] == '011':
                    list_floatbin_converted_t_oct = list_floatbin_converted_t_oct + [3]
                elif groups_3_bin_floats[float_index_number] == '100':
                    list_floatbin_converted_t_oct = list_floatbin_converted_t_oct + [4]
                elif groups_3_bin_floats[float_index_number] == '101':
                    list_floatbin_converted_t_oct = list_floatbin_converted_t_oct + [5]
                elif groups_3_bin_floats[float_index_number] == '110':
                    list_floatbin_converted_t_oct = list_floatbin_converted_t_oct + [6]
                elif groups_3_bin_floats[float_index_number] == '111':
                 list_floatbin_converted_t_oct = list_floatbin_converted_t_oct + [7]
                elif groups_3_bin_floats[float_index_number] == '000':
                    list_floatbin_converted_t_oct = list_floatbin_converted_t_oct + [0]
                else:
                    break
                float_index_number += 1
            use_of_a_func_checker += 1
        float_result=''.join(map(str, list_floatbin_converted_t_oct))
    if use_of_a_func_checker > 0:
        print(int_result+'.'+float_result+'₈')
    else:
        print(int_result+'₈')
    
    
    
    
#Binary to Hexadecimal

elif users_1st_option == 1 and users_2st_option == 4:
    padded0_int_part = str_user_data_int_part.zfill(len_int_part+(4-(len_int_part%4)))
    groups_4_bin_ints=[]
    for i in padded0_int_part:
        padded_int_end_index += 1
        if padded_int_end_index%4 == 0:
            groups_4_bin_ints = groups_4_bin_ints + [padded0_int_part[padded_int_start_index:padded_int_end_index]]
            padded_int_start_index+=4
    
    list_intbin_converted_t_hex = []
    if set(str_user_data_int_part) <= {'0', '1'}:
        for j in groups_4_bin_ints:
            if groups_4_bin_ints[int_index_number] == '0001':
                list_intbin_converted_t_hex = list_intbin_converted_t_hex + ['1']
            elif groups_4_bin_ints[int_index_number] == '0010':
                list_intbin_converted_t_hex = list_intbin_converted_t_hex + ['2']
            elif groups_4_bin_ints[int_index_number] == '0011':
                list_intbin_converted_t_hex = list_intbin_converted_t_hex + ['3']
            elif groups_4_bin_ints[int_index_number] == '0100':
                list_intbin_converted_t_hex = list_intbin_converted_t_hex + ['4']
            elif groups_4_bin_ints[int_index_number] == '0101':
                list_intbin_converted_t_hex = list_intbin_converted_t_hex + ['5']
            elif groups_4_bin_ints[int_index_number] == '0110':
                list_intbin_converted_t_hex = list_intbin_converted_t_hex + ['6']
            elif groups_4_bin_ints[int_index_number] == '0111':
                list_intbin_converted_t_hex = list_intbin_converted_t_hex + ['7']
            elif groups_4_bin_ints[int_index_number] == '1000':
                list_intbin_converted_t_hex = list_intbin_converted_t_hex + ['8']
            elif groups_4_bin_ints[int_index_number] == '1001':
                list_intbin_converted_t_hex = list_intbin_converted_t_hex + ['9']
            elif groups_4_bin_ints[int_index_number] == '1010':
                list_intbin_converted_t_hex = list_intbin_converted_t_hex + ['a']
            elif groups_4_bin_ints[int_index_number] == '1011':
                list_intbin_converted_t_hex = list_intbin_converted_t_hex + ['b']
            elif groups_4_bin_ints[int_index_number] == '1100':
                list_intbin_converted_t_hex = list_intbin_converted_t_hex + ['c']
            elif groups_4_bin_ints[int_index_number] == '1101':
                list_intbin_converted_t_hex = list_intbin_converted_t_hex + ['d']
            elif groups_4_bin_ints[int_index_number] == '1110':
                list_intbin_converted_t_hex = list_intbin_converted_t_hex + ['e']
            elif groups_4_bin_ints[int_index_number] == '1111':
                list_intbin_converted_t_hex = list_intbin_converted_t_hex + ['f']
            elif groups_4_bin_ints[int_index_number] == '0000':
                list_intbin_converted_t_hex = list_intbin_converted_t_hex + ['0']
            else:
                break
            int_index_number += 1
    else:
        print("Number is not a binary!")
        
    int_result= ''.join(map(str, list_intbin_converted_t_hex))
    if splited_int_and_float_listdata[0] != str_user_data:
        str_user_data_float_part = splited_int_and_float_listdata[1]
        len_float_part = len(str_user_data_float_part)
        zneed = 4-(len_float_part%4)+len_float_part
        padded0_fractional_part = str_user_data_float_part.ljust(zneed, '0')
        groups_4_bin_floats=[]
        list_floatbin_converted_t_hex = []
        for io in padded0_fractional_part:
            padded_float_end_index += 1
            if padded_float_end_index%4 == 0:
                groups_4_bin_floats = groups_4_bin_floats + [padded0_fractional_part[padded_float_start_index:padded_float_end_index]]
                padded_float_start_index+=4
        if set(str_user_data_float_part) <= {'0', '1'}:
            for ji in groups_4_bin_floats:
                if groups_4_bin_floats[float_index_number] == '0001':
                    list_floatbin_converted_t_hex = list_floatbin_converted_t_hex + ['1']
                elif groups_4_bin_floats[float_index_number] == '0010':
                    list_floatbin_converted_t_hex = list_floatbin_converted_t_hex + ['2']
                elif groups_4_bin_floats[float_index_number] == '0011':
                    list_floatbin_converted_t_hex = list_floatbin_converted_t_hex + ['3']
                elif groups_4_bin_floats[float_index_number] == '0100':
                    list_floatbin_converted_t_hex = list_floatbin_converted_t_hex + ['4']
                elif groups_4_bin_floats[float_index_number] == '0101':
                    list_floatbin_converted_t_hex = list_floatbin_converted_t_hex + ['5']
                elif groups_4_bin_floats[float_index_number] == '0110':
                    list_floatbin_converted_t_hex = list_floatbin_converted_t_hex + ['6']
                elif groups_4_bin_floats[float_index_number] == '0111':
                 list_floatbin_converted_t_hex = list_floatbin_converted_t_hex + ['7']
                elif groups_4_bin_floats[float_index_number] == '1000':
                 list_floatbin_converted_t_hex = list_floatbin_converted_t_hex + ['8']
                elif groups_4_bin_floats[float_index_number] == '1001':
                 list_floatbin_converted_t_hex = list_floatbin_converted_t_hex + ['9']
                elif groups_4_bin_floats[float_index_number] == '1010':
                 list_floatbin_converted_t_hex = list_floatbin_converted_t_hex + ['a']
                elif groups_4_bin_floats[float_index_number] == '1011':
                 list_floatbin_converted_t_hex = list_floatbin_converted_t_hex + ['b']
                elif groups_4_bin_floats[float_index_number] == '1100':
                 list_floatbin_converted_t_hex = list_floatbin_converted_t_hex + ['c']
                elif groups_4_bin_floats[float_index_number] == '1101':
                 list_floatbin_converted_t_hex = list_floatbin_converted_t_hex + ['d']
                elif groups_4_bin_floats[float_index_number] == '1110':
                 list_floatbin_converted_t_hex = list_floatbin_converted_t_hex + ['e']
                elif groups_4_bin_floats[float_index_number] == '1111':
                 list_floatbin_converted_t_hex = list_floatbin_converted_t_hex + ['f']
                elif groups_4_bin_floats[float_index_number] == '0000':
                    list_floatbin_converted_t_hex = list_floatbin_converted_t_hex + ['0']
                else:
                    break
                float_index_number += 1
            use_of_a_func_checker += 1
        float_result=''.join(map(str, list_floatbin_converted_t_hex))
    if use_of_a_func_checker > 0:
        print(int_result+'.'+float_result+'₁₆')
    else:
        print(int_result+'₁₆')


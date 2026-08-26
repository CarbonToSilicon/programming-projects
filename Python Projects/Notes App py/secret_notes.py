print("Hey, welcome!\nNice to see you.")

import os
import platform

t1 = '~!@#$%^&*-_;:/<>?'
t2 = 'QWERTYUIOPASDFGHJKLZXCVBNM'
t3 = "qwertyuiopasdfghjklzxcvbnm"
t4 = "1234567890"
status = ''


def sha_128_custom(message):
    # 1. Initial Hash Values (A, B, C, D - 32 bits each = 128 bit total)
    h0 = 0x67452301
    h1 = 0xEFCDAB89
    h2 = 0x98BADCFE
    h3 = 0x10325476

    # 2. Preprocessing (Padding)
    # Convert string to list of byte values
    msg_bytes = [ord(c) for c in message]
    orig_len_bits = len(msg_bytes) * 8
    
    # Append the '1' bit (0x80)
    msg_bytes.append(0x80)
    
    # Pad with zeros until length is 56 bytes (448 bits) mod 64
    while len(msg_bytes) % 64 != 56:
        msg_bytes.append(0x00)
        
    # Append original length as a 64-bit big-endian integer
    for i in range(7, -1, -1):
        msg_bytes.append((orig_len_bits >> (i * 8)) & 0xff)

    # 3. Process in 512-bit (64-byte) chunks
    for i in range(0, len(msg_bytes), 64):
        chunk = msg_bytes[i:i+64]
        words = []
        for j in range(0, 64, 4):
            # Combine 4 bytes into one 32-bit word
            word = (chunk[j] << 24) | (chunk[j+1] << 16) | (chunk[j+2] << 8) | (chunk[j+3])
            words.append(word)

        # Extend 16 words into 32 words (The "Message Schedule")
        for j in range(16, 32):
            word = (words[j-3] ^ words[j-8] ^ words[j-14] ^ words[j-16])
            # Left rotate by 1
            words.append(((word << 1) | (word >> 31)) & 0xFFFFFFFF)

        # 4. Compression Loop (The Meat Grinder)
        a, b, c, d = h0, h1, h2, h3

        for j in range(32):
            # Mixing functions
            if j < 16:
                f = (b & c) | ((~b) & d)
                k = 0x5A827999
            else:
                f = b ^ c ^ d
                k = 0x6ED9EBA1

            # Rotate 'a' left by 5
            temp = (((a << 5) | (a >> 27)) + f + d + k + words[j]) & 0xFFFFFFFF
            
            # Shift variables
            d = c
            c = ((b << 30) | (b >> 2)) & 0xFFFFFFFF # Rotate b left by 30
            b = a
            a = temp

        # Add result of chunk to existing hash
        h0 = (h0 + a) & 0xFFFFFFFF
        h1 = (h1 + b) & 0xFFFFFFFF
        h2 = (h2 + c) & 0xFFFFFFFF
        h3 = (h3 + d) & 0xFFFFFFFF

    # 5. Final Result: Hexadecimal string
    return '{:08x}{:08x}{:08x}{:08x}'.format(h0, h1, h2, h3)


# Ensure required files exist
open("secret_notes_accounts.csv", "a").close()
open("master_notes.txt", "a").close()

user_marker = "%*^9sdf$USER$34sd32*"  #'\x1eUSER\x1e'  #"%*^9sdf34sd32*"

while True: # THE MAIN APP LOOP
    print("\n--- MAIN MENU ---")
    status = input(f"Enter:\n1. For Sign in\n2. For Sign up\n3. To Exit\n")
    
    if status == '3':
        print("Goodbye!")
        break # Exits the whole app

    if status == "2":
        # --- SIGN UP LOGIC ---
        # (Your existing username and password loops go here)
        while True:
            username = input("Username must be 5–15 characters:\n")

            if not (5 <= len(username) <= 15):
                print("Invalid username length.\n")
                continue
            if any(c in (" ", ",", "|") for c in username):
                print('" " space not allowed in between username!')
                continue

            username_taken = False

            with open("secret_notes_accounts.csv", "r") as f:
                    
                for line in f:
                    line = line.strip()

                    if not line or "," not in line:
                        continue

                    stored_user, _ = line.split(",", 1)

                    if stored_user == username:
                        username_taken = True
                        break
            if not username_taken:
                print(f"Username {username} accepted!")
                break
            else:
                print("Username already taken.\n")
                    

        while True:
            password = input(f"Password must contain 4 types of characters (&, A, a, 1) and the length should be from 4 to 12 character\nEnter password:")
            if any(c in t1 for c in password) and any(c in t2 for c in password) and any(c in t3 for c in password) and any(c in t4 for c in password) and 4 <= len(password) <= 12:
                print(f"Password {password} accepted!")
                break
            else:        
                print(f"Password invalid!")
        with open("secret_notes_accounts.csv", "a+") as filepass, open("master_notes.txt", "a") as mainfile:
            filepass.seek(0)
            password = sha_128_custom(password)
            filepass.write(f"{username},{password}\n")
            
            mainfile.write(f"\n{user_marker}|{username}|{password}\n")##################00000
            # bookmark in the main master file
        print("Registration complete! You can now sign in.")
        # Notice: No 'break' here, so it loops back to the Main Menu        

    elif status == '1':
        # --- SIGN IN LOGIC ---
        while True:
            print("\n--- Login Screen (Type 'exit' to go back) ---")
            username_match = input(f"Enter your username: ")
            if username_match.lower() == 'exit': break # Escape hatch
            
            password_match = input(f"\nEnter your password: ")
            encoded_attempt_p = sha_128_custom(password_match)

            success = False

            try:
                with open("secret_notes_accounts.csv", "r") as f:
                    
                    for line in f:   
                        if "," not in line: continue 
                        #if not line.strip(): continue # Skip empty lines
                        #stored_user, stored_pass = line.strip().split(",")
                        line = line.strip()
                        if not line or "," not in line:
                            continue

                        stored_user, stored_pass = line.split(",", 1)
                        if username_match == stored_user and encoded_attempt_p == stored_pass:
                            success = True
                            #print(f"Login successful!\nWelcome {username_match}.")
                            break # This breaks the 'for' loop (searching the file)
            except FileNotFoundError:
                print("Error: No accounts found. Please sign up first.")
                break # Exit the sign-in loop if no file exists

            if success:
                print(f"Login successful! Welcome {username_match}.")
                # This is where the actual "Secret Notes" logic would start
                while True:
                    note_choice = input(f"Do you want to open your notes?\nType y or yes to continue\nType e or exit to quit:\n ")
                    note_choice = note_choice.lower()
                
                    if note_choice in ['y', 'yes']:
                        temp_filename = "temp_notepad.txt"
                        mark = f"{user_marker}|{username_match}|{encoded_attempt_p}"
                        #mainfile.write(f"%*^9sdf34sd32*{username}~[{password}]\n")
                            # Extract current notes to the temp file first so they can see/edit them
                        with open("master_notes.txt", "r") as masterfile, open(temp_filename, "w") as tempf:
                            found_section = False
                            line = ""
                            for line in masterfile:
                                if line.strip() == mark:
                                    found_section = True
                                    continue
                                if found_section:
                                    if line.startswith(user_marker): break #("%*^9sdf34sd32*") in line: break # Hit next user
                                    tempf.write(line)
                        message0 = "Opening Notepad... Save and Close to update your notes."

#$$$$$$$$$$$$$$$$$$$$%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                        if platform.system() == "Linux":
                            print(message0)
                            os.system(f"nano {temp_filename}")
                        #elif platform.system() == "Windows":
                            print(message0)
                            os.system(f"notepad {temp_filename}")
                        elif platform.system() == "Darwin":  # macOS
                            print(message0)
                            os.system(f"open {temp_filename}")
                        else:   # fallback editor
                            print("\nUsing built-in editor...")
                                
                            while True:
                                markf = 0
                                while True:
                                    #action1 = input("Do you want to:\n1. Read\n2. Write\n3. Delete\n4. Back\n?? ")
                                    try:
                                        action1 = input("Do you want to:\n1. Read\n2. Append at the end\n3. Write\n4. Delete\n5. Back\n?? ")
                                        if 0 < int(action1) <= 5:
                                            break
                                    except ValueError:
                                        print("Please type a valid input!")
                                
                                if 0 < int(action1) <= 4:
                                    if action1 == "1": #read
                                        with open(temp_filename, "r") as tempf:
                                            print("\n\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                                            print(tempf.read())
                                            print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n\n")
                                    elif action1 == "4": #delete
                                        with open(temp_filename, "w") as tempf:
                                            tempf.write("\n")
                                    elif action1 == "3": #write
                                        with open(temp_filename, "w") as tempf:
                                            tempf.close()
                                            #print("You are going rewrite your notes!\nThis will delete your old notes.")
                                            #print("\n\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                                            #rewrite = input()
                                            #print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n\n")
                                            #tempf.write(rewrite)
                                        print("Enter text (type END to finish):")

                                        lines = []
                                        while True:
                                            line = input()
                                            if line.lower() == "end":
                                                markf = 1
                                                break
                                            lines.append(line)

                                        with open(temp_filename, "w") as f:
                                            f.write("\n".join(lines))
                                        print("Notes have been successfully rewritten.\n")
                                        #if markf == 1: break
                                    elif action1 == "2": #append
                                        with open(temp_filename, "r+") as tempf:
                                            
                                            tempf.seek(0)
                                            print("\n\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                                            print(tempf.read())
                                            print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n\n")
                                            tempf.seek(0, 2)
                                            print("<Type end to to save and go back>\n")
                                            lines = []
                                            while True:
                                                append_in = input()
                                                j = ["done", "d", "end", "e"]
                                                if append_in.lower() in j:
                                                    break
                                                lines.append(append_in)
                                            tempf.write("\n".join(lines))
                                        print("Notes have been successfully rewritten.\n")
                                    elif action1 == "5": #Back
                                        break
                            # 2. READ the master file into the 'Sandwich' variables
                        header = ""
                        footer = ""
                        state = "HEADER"
                        with open("master_notes.txt", "r") as masterfile:
                            for line in masterfile:
                                if line.strip() == mark:
                                    state = "USER_SECTION"
                                    header += line # Keep the marker in the header
                                    continue
                                if state == "USER_SECTION" and  line.startswith(user_marker): #"%*^9sdf34sd32*" in line:
                                    state = "FOOTER"
                                
                                if state == "HEADER":
                                    header += line
                                elif state == "FOOTER":
                                    footer += line

                        #header = header + "\n\n"
                        #footer = footer + "\n\n"


                        # 3. RE-ASSEMBLE the file
                        with open(temp_filename, "r") as temp:
                            new_user_data = temp.read()

                        with open("master_notes.txt", "w") as masterfile:
                            masterfile.write(header)           # Bottom slice of bread
                            masterfile.write(new_user_data)    # The meat (updated notes)
                            if not new_user_data.endswith('\n'): masterfile.write('\n')
                            masterfile.write(footer)           # Top slice of bread

                        print("Master file updated successfully!")
                        if os.path.exists(temp_filename):
                            os.remove(temp_filename)
                         # Clean up the evidence
                    elif note_choice in ['e', 'exit']: break
                
                    else:
                        print(f"Please enter a valid option!\n")

            else:
                # IMPORTANT: Tell the user it failed so they aren't confused
                print("!!! Invalid username or password. Please try again. !!!")





#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

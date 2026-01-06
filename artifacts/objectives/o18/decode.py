enc_pass = "D13URKBT"
real_pass = ""
for char in enc_pass:
    real_pass += chr(ord(char) ^ 7)
print(real_pass)
import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")

text = "Hi this Sayed Fuad Al Labib! How are you doing today?"

tokens = enc.encode(text)   

print("Tokens:", tokens)

decoded = enc.decode([12194, 495, 336, 19630, 24885, 324, 1667, 19557, 526, 0, 3253, 553, 481, 5306, 4044, 30])

print("Decoded:", decoded)

def plainText(data, x):
    return data

def ceaserCiper(data, shift):
    if type(data) is bytes:
        data = list(data)
        for i in range(len(data)):
            data[i] = (data[i] + shift) % 256

        return bytes(data)
    else:
        result = ""
        for i in range(len(data)):
            char = data[i]

            if char.isupper():
                result += chr((ord(char) + shift - 65) % 26 + 65)
            elif char.islower():
                result += chr((ord(char) + shift - 97) % 26 + 97)
            elif char.isdigit():
                result += chr((ord(char) + shift - 48) % 10 + 48)
            else:
                result += char
    
    return result

def reverse(data, x):
    return data[::-1]

cryption = {
    '0': plainText,
    '1': ceaserCiper,
    '2': reverse
}
import cv2
import itertools

def read_image_file(image_file):
    img = cv2.imread(image_file)
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

def string_as_byte_array(string):
    return [ord(c) for c in string]
    
def bits_from_byte(byte):
    return [ (byte >> bit) & 1 for bit in range(1,9) ]

def byte_array_as_bit_array(bytes):
    return list(itertools.chain.from_iterable([bits_from_byte(byte) for byte in bytes]))

def read_message_text_file(message_text_file):
    message_file = open(message_text_file, 'r')
    message_string = message_file.read()
    message_bytes = string_as_byte_array(message_string)
    message_bits = byte_array_as_bit_array(message_bytes)
    return(message_string, message_bytes, message_bits)

def hide_message_in_image(message_string, cover_image):
    encoded_image = cover_image.copy()
    
    message_bytes = string_as_byte_array(message_string)
    message_bits = byte_array_as_bit_array(message_bytes)
    max_bit = len(message_bits) - 1
    bit = 0
    
    nrows, ncolumns, ncolors = cover_image.shape
    for row in range(nrows):
        for column in range(ncolumns):
            for color in range(ncolors):
                if bit > max_bit:
                    return encoded_image
                
                encoded_image[row][column][color] &= message_bits[bit]
                bit += 1
    
    return encoded_image
    

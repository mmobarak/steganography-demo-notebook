import cv2
import itertools
import matplotlib.pyplot as plt

def read_image_file(image_file):
    img = cv2.imread(image_file)
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

def string_as_byte_array(string):
    return [ord(c) for c in string]
    
def bits_from_byte(byte):
    return [ (byte >> bit) & 1 for bit in range(7,-1,-1) ]

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
                    # TODO - mark end of message
                    return encoded_image
                
                message_bit = message_bits[bit]
                color_byte = encoded_image[row][column][color]
                color_byte &= 0xFE
                color_byte |= message_bit
                encoded_image[row][column][color] = color_byte
                bit += 1
    
    return encoded_image
        
def extract_message_from_image(image):
    message = ""
    message_byte = 0
    bits_in_byte = 0
  
    nrows, ncolumns, ncolors = image.shape
    for row in range(nrows):
        for column in range(ncolumns):
            for color in range(ncolors):
                message_bit = image[row][column][color] & 0x01
                message_byte |= message_bit
                bits_in_byte += 1
                
                if bits_in_byte == 8:
                    message += chr(message_byte)
                    message_byte = 0
                    bits_in_byte = 0
                else:
                    message_byte <<= 1
                    
                # TODO - detect end of message
                if len(message) > 1000:
                    return message
                    
    return message

def show_images(images):
    fig = plt.figure(figsize=(20, 7))
    rows = 1
    cols = 2

    for i, image in enumerate(images):
        fig.add_subplot(rows, cols, i + 1)
        plt.imshow(image[0])
        plt.axis('off')
        plt.title(image[1])

        
def hide_message_in_image_MSB(message_string, cover_image):
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
                    # TODO - mark end of message
                    return encoded_image
                
                message_bit = message_bits[bit]
                color_byte = encoded_image[row][column][color]
                color_byte &= 0x7F
                color_byte |= message_bit << 7
                encoded_image[row][column][color] = color_byte
                bit += 1
    
    return encoded_image
        
def extract_message_from_image_MSB(image):
    message = ""
    message_byte = 0
    bits_in_byte = 0
  
    nrows, ncolumns, ncolors = image.shape
    for row in range(nrows):
        for column in range(ncolumns):
            for color in range(ncolors):
                message_bit = (image[row][column][color] >> 7) & 0x01
                message_byte |= message_bit
                bits_in_byte += 1
                
                if bits_in_byte == 8:
                    message += chr(message_byte)
                    message_byte = 0
                    bits_in_byte = 0
                else:
                    message_byte <<= 1
                    
                # TODO - detect end of message
                if len(message) > 1000:
                    return message
                    
    return message


def hide_message_in_audio(message_string, cover_audio):
    cover_audio = bytearray(cover_audio)
    message_bytes = string_as_byte_array(message_string)
    message_bits = byte_array_as_bit_array(message_bytes)
    max_bit = len(message_bits) - 1
    bit = 0
    
    for i in range(len(cover_audio)):
        if bit > max_bit:
            # TODO - mark end of message
            return cover_audio

        if i % 2 == 0: # samples are 16 bits, write to the LSB only
            message_bit = message_bits[bit]
            cover_audio[i] &= 0xFE
            cover_audio[i] |= message_bit
            bit += 1
    
    return cover_audio

def extract_message_from_audio(cover_audio):
    message = ""
    message_byte = 0
    bits_in_byte = 0
  
    for i in range(len(cover_audio)):
        if i % 2 == 0: # samples are 16 bits, write to the LSB only
            message_bit = cover_audio[i] & 0x01
            message_byte |= message_bit
            bits_in_byte += 1

            if bits_in_byte == 8:
                message += chr(message_byte)
                message_byte = 0
                bits_in_byte = 0
            else:
                message_byte <<= 1

            # TODO - detect end of message
            if len(message) > 1000:
                return message
                    
    return message
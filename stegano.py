#Radosław Płocha
import sys
import re

def hide_message_in_extra_spaces(html_string, binary_message):
    if html_string.count("\n") < len(message):
        raise ValueError("HTML file does not have enough lines to hide the entire message.")
    lines = html_string.split("\n")
    message_index = 0
    for i, line in enumerate(lines):
        if message_index == len(binary_message):
            break
        if line.strip():
            lines[i] = line + " " if binary_message[message_index] == "1" else line
            message_index += 1
    return "\n".join(lines)

def extract_message_from_extra_spaces(html_string):
    lines = html_string.split("\n")
    binary_message = ""
    for line in lines:
        if line.strip():
            if line[-1] == " ":
                binary_message += "1"
            else:
                binary_message += "0"
    return binary_message

def hide_message_in_spaces(html_string, message):
    if html_string.count(" ") < len(message):
        raise ValueError("HTML file does not have enough spaces to hide the entire message.")
    message_index = 0
    for i in range(len(cover_html)):
        
        if html_string[i] == " ":
            if message[message_index] == "1":
                html_string = html_string[:i] + "  " + html_string[i+1:]
            message_index += 1
            if message_index == len(message):
                break
    return html_string

def extract_message_from_spaces(html_string):
    message = ""
    for i in range(len(html_string)):
        if html_string[i] == " ":
            message += "1" if html_string[i:i+2] == "  " else "0"
    return message

def hide_message_in_misspelled_attributes(html_string, message):
    if len(re.findall(r'style="margin-bottom: 0cm; line-height: 100%"', html_string)) < len(message):
        raise ValueError("HTML file does not have enough attributes to hide the entire message.")
    
    i = 0
    for match in re.finditer(r'style="margin-bottom: 0cm; line-height: 100%"', html_string):
        start = html_string.find("margin-bottom", match.start())
        if i+1 > len(message):
            break
        if binary_message[i] == "0":
            html_string = html_string[:start] + "margin-botom" + html_string[start + 13:]
        else:
            html_string = html_string[:start + 20] + "lineheight" + html_string[start + 31:]
        i += 1
    return html_string

def extract_message_from_misspelled_attributes(html_string):
    extracted_message = ""
    for match in re.finditer(r'style="(margin-botom: 0cm; line-height: 100%|margin-bottom: 0cm; lineheight: 100%)"', html_string):
        start = html_string.find("margin-botom", match.start(),match.end())
        if start != -1:
            extracted_message += "0"
        else:
            extracted_message += "1"
    return extracted_message

def hide_message_in_unnecessary_tags(cover_html, message):
    modified_html = ""
    message_index = 0
    for match in re.finditer(r'<font>', cover_html):
        if message_index < len(message) and message[message_index] == '1':
            modified_html += cover_html[:match.start()] + "<font></font><font>"
        else:
            modified_html += cover_html[:match.start()] + "</font><font></font>"
        cover_html = cover_html[match.end():]
        message_index += 1
    modified_html += cover_html
    return modified_html


def extract_message_from_unnecessary_tags(html_string):
    message = ""
    for match in re.finditer(r'<font></font><font>|</font><font></font>', html_string):
        if match.group() == "<font></font><font>":
            message += "1"
        else:
            message += "0"
    return message



if __name__ == "__main__":
    option = sys.argv[1:][0]
    algorithm = sys.argv[1:][1]
    
    if option == "-e":
        with open("mess.txt", "r") as f:
            message = f.read()
        binary_message = bin(int(message, 16))[2:]
        binary_message = "0" *  (8 - (len(binary_message) % 8)) + binary_message 
        with open("cover.html", "r") as f:
            cover_html = f.read()


        if algorithm == "-1":
            watermarked_html = hide_message_in_extra_spaces(cover_html, binary_message)
        elif algorithm == "-2":
            while "  " in cover_html:
                cover_html = cover_html.replace("  ", "")
            watermarked_html = hide_message_in_spaces(cover_html, binary_message)
        elif algorithm == "-3":
            watermarked_html = hide_message_in_misspelled_attributes(cover_html, binary_message)
        elif algorithm == "-4":
            watermarked_html = hide_message_in_unnecessary_tags(cover_html, binary_message)
        else:
            raise ValueError("Invalid algorithm number")
        with open("watermark.html", "w") as f:
            f.write(watermarked_html)
    elif option == "-d":
        with open("watermark.html", "r") as f:
            watermarked_html = f.read()
        if algorithm == "-1":
            binary_message = extract_message_from_extra_spaces(watermarked_html)
        elif algorithm == "-2":
            binary_message = extract_message_from_spaces(watermarked_html)
        elif algorithm == "-3":
            binary_message = extract_message_from_misspelled_attributes(watermarked_html)
        elif algorithm == "-4":
            binary_message = extract_message_from_unnecessary_tags(watermarked_html)
        else:
            raise ValueError("Invalid algorithm number")

        binary_message = binary_message.rstrip("0")
        if len(binary_message) % 8 != 0:
            binary_message = binary_message + "0" * (8 - (len(binary_message) % 8))

        hex_message = hex(int(binary_message, 2))[2:]
        with open("detect.txt", "w") as f:
            f.write(hex_message)
    else:
        print("invalid option")
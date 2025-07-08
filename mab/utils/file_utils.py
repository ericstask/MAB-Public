def retreive_header_and_footer(file_path):
    header = ''
    footer = ''
    with open(file_path, 'r') as file:
        header = file.readline().strip()

        # Find the last non-empty line in the file (assumed as footer)
        for line in reversed(list(file)):
            line = line.strip()
            if line:
                footer = line
                break
        print(footer)

    return header, footer

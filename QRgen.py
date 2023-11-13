import csv
import jwt
import qrcode
import sys
import getopt
import os

#counter = 0

# Function to generate JWT token
def generate_jwt_token(issuer, token, secret_key):

    payload = {
        "iss": issuer,
        "token": token
    }

    # jwt.encode returns a bytes object, so we convert it to a string
    token = jwt.encode(payload, secret_key, algorithm='HS512')

    return token

# Function to generate QR code from JWT token
def generate_qr_code(jwt_token, identifier):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(jwt_token)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    filename = f"img/qr_code_{identifier}.png"  # Include identifier in the filename
    img.save(filename)  # Save the QR code image
    return filename  # Return the filename

# Function to generate LaTeX code for a card
def generate_card(name, department, identifier):
    # Replace underscores with _ in name and department
    name = name.replace("_", "_")
#    name = name.replace(" ", "\\-")
    department = department.replace("_", "_")

    # Generate JWT token
    jwt_token = generate_jwt_token(issuer=jwt_issuer, token=identifier, secret_key=jwt_secret)

    # Generate QR code and get filename
    qr_code_filename = generate_qr_code(jwt_token, identifier)

    r = f"""
\\begin{{minipage}}{{0.20\\textwidth}}  % Adjust the width as needed
    \\begin{{flushleft}}
        \\textbf{{{name}}} \\\\
        {department}
    \\end{{flushleft}}
\\end{{minipage}}%
\\hspace{{0.05\\textwidth}}%
\\begin{{minipage}}{{0.25\\textwidth}}
    \\includegraphics[width=0.8\\textwidth]{{{qr_code_filename}}}
\\end{{minipage}}\\
"""
    if not(counter%2):
        r+= f"\\"
    return r


if( __name__ == '__main__'):

    # Defaults
    csv_file_path = 'person.csv'
    output_tex_file_path = 'output.tex'
    jwt_issuer = 'Ostara'
    jwt_secret = '12345678'

    opts, args = getopt.getopt(sys.argv[1:],"hc:t:i:s:",["csvfile=","texfile=","issuer=","secret="])
    for opt, arg in opts:
        if opt == '-h':
            print ('QRgen.py -c <input_file.csv> -t <output_file.tex> -i <issuer_name> -s <issuer_secret>')
            sys.exit()
        elif opt in ("-c", "--csvfile"):
            csv_file_path = arg
        elif opt in ("-t", "--texfile"):
            output_tex_file_path = arg
        elif opt in ("-i", "--issuer"):
            jwt_issuer = arg
        elif opt in ("-s", "--secret"):
            jwt_secret = arg

    # For debigging only
    if(False):
        print ('Input file is ', csv_file_path)
        print ('Output file is ', output_tex_file_path)
        print ('JWT Issuer is ', jwt_issuer)
        print ('JWT Secret is', jwt_secret)

    counter=0

    # Create tmp folder if not there yet
    if not os.path.exists("img"):
        os.mkdir("img")

    # Read CSV file and generate LaTeX code
    latex_code = ""
    with open(csv_file_path, 'r') as file:
        csv_reader = csv.reader(file)
        # header = next(csv_reader)  # Skip the header row
        for row in csv_reader:
            id, name, department, identifier = row
            latex_code += generate_card(name, department, identifier)
            counter+=1

    # Write the generated LaTeX code to a .tex file
    with open(output_tex_file_path, 'w') as output_file:
        output_file.write(f"""
% !TeX encoding = UTF-8
\\documentclass{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage[T1]{{fontenc}}
\\usepackage{{geometry}}  % Adjust the margin as needed
\\usepackage{{graphicx}}
\\usepackage{{underscore}}  % Add this line to use \textunderscore
\\usepackage{{parskip}}
\\geometry{{a4paper, margin=1cm}}

\\begin{{document}}

{latex_code}

\\end{{document}}
""")
    print(f"LaTeX code has been generated and saved to {output_tex_file_path}.")

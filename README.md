# OstaraQRGen
Generate PDF files with QR ID cards from CSVs exported from the database

Export a CSV file of view 'QrCodes' from PhpMyAdmin. The file should look like this:

```csv
"1","test_person_one","test_department_A","0d092e0c2eab68ff5dce342d382c528e"
"2","test_person_two","test_department_B","c92438a501dd1c8b31b34bc3fd3b83f7"
"6","test_person_six","test_department_C","8a50433f4bcc9283fd3b1dd1c8b31b37"
```

Run the Python script with arguments:

```sh
python3 QRgen.py -c input_csv_file.csv -t output_tex_file.tex -i jwt_issuer_name -s jwt_server_secret
```

Result will be `output_tex_file.tex` which you can compile with eg. `pdflatex` to get a PDF file with the cards.
See [examples](examples)

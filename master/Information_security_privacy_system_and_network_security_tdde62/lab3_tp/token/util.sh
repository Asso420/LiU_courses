# Converts a raw binary string in a file to an 8-digit decimal number, 
# and prints the number to standard output.
# Usage: binary_to_decimal file_name
function binary_to_decimal {
   # Extract first 4 bytes from file, convert to decimal, and output the
   # last 8 digits, zero-padding to 8 digits if necessary.
   # This is the challenge response format expected by the bank application.
   printf "%08d" $(od -N4 -An -t u4 --endian=big $1) | tail -c 8
}

# Converts an ASCII hex string into actual binary, and stores the binary
# string to file.
# Usage: hex_to_bin hex_string output_file_name
function hex_to_bin {
   echo "$1" | xxd -r -p > "$2"
}
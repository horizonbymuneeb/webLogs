import streamlit as st
import re

# Regular expression pattern to match fields in a log entry
pattern = r'(\S+) (\S+) (\S+) \[([^]]+)\] "([^"]+)" (\d+) (\d+) "([^"]+)" "([^"]+)"'

# Function to extract fields from a log entry
def extract_fields(log_entry):
    match = re.match(pattern, log_entry)
    if match:
        return {
            'IP Address': match.group(1),
            'User Identifier (Remote Logname)': match.group(2),
            'User ID': match.group(3),
            'Timestamp': match.group(4),
            'Request Line': match.group(5),
            'Status Code': match.group(6),
            'Response Size': match.group(7),
            'Referer': match.group(8),
            'User-Agent': match.group(9)
        }

# Function to read log data lazily
def get_log_data(file):
    while True:
        line = file.readline()
        if not line:
            break
        yield extract_fields(line)

# Main function
def main():
    st.write("Upload Log File")
    uploaded_file = st.file_uploader("Choose a file", type=['log'])

    if uploaded_file is not None:
        with st.spinner('Uploading and Processing...'):
            log_data_generator = get_log_data(uploaded_file)

            data_to_display = []
            for _ in range(10):  # Initial display of 10 rows
                try:
                    data_to_display.append(next(log_data_generator))
                except StopIteration:
                    break

            st.write("Displaying initial 10 rows:")
            st.dataframe(data_to_display)

            if st.button("Load More"):
                # Load additional rows
                for _ in range(10):
                    try:
                        data_to_display.append(next(log_data_generator))
                    except StopIteration:
                        break
                st.write("Displaying next 10 rows:")
                st.dataframe(data_to_display)

if __name__ == "__main__":
    main()

import pandas as pd
import streamlit as st
import os
import tempfile

st.title("File Renaming Tool")

# Step 1: Select File Type
st.header("Step 1: Select File Type")
file_type = st.selectbox(
    "Select the file type:",
    options=["IES", "PDF", "GOS", "PNG", "All Files"]
)

# Step 2: Download CSV template
st.header("Step 2: Download Template")

def create_template(file_type):
    ext = "" if file_type == "All Files" else f".{file_type.upper()}"
    return {
        "Old File Name": [f"Example_Old_File{ext}"],
        "New File Name": [f"Example_New_File{ext}"]
    }

df_template = pd.DataFrame(create_template(file_type))
csv_name = f"File_Renaming_Template_{file_type.replace(' ', '_')}.csv"
df_template.to_csv(csv_name, index=False)
with open(csv_name, "rb") as file:
    st.download_button(
        label=f"Download Template for {file_type}",
        data=file,
        file_name=csv_name,
        mime="text/csv"
    )

# Step 3: Upload files and CSV
st.header("Step 3: Upload Files and CSV File")

uploaded_files = st.file_uploader("Upload files to rename", accept_multiple_files=True)
uploaded_csv = st.file_uploader("Upload CSV with renaming instructions", type=["csv"])

# Step 4: Rename files
if st.button("Rename Files"):
    if not uploaded_files or not uploaded_csv:
        st.error("Please upload both the files and the CSV.")
    else:
        try:
            df = pd.read_csv(uploaded_csv)
            if "Old File Name" not in df.columns or "New File Name" not in df.columns:
                st.error("CSV must contain 'Old File Name' and 'New File Name' columns.")
            else:
                renamed_files = []
                for file in uploaded_files:
                    temp_file = tempfile.NamedTemporaryFile(delete=False)
                    temp_file.write(file.read())
                    temp_file_path = temp_file.name
                    temp_file.close()

                    match_row = df[df["Old File Name"] == file.name]
                    if not match_row.empty:
                        new_name = match_row["New File Name"].values[0]
                        if file_type != "All Files" and not new_name.endswith(f".{file_type.upper()}"):
                            new_name += f".{file_type.upper()}"

                        st.download_button(
                            label=f"Download Renamed: {new_name}",
                            data=open(temp_file_path, "rb").read(),
                            file_name=new_name,
                            mime="application/octet-stream"
                        )
                        renamed_files.append(new_name)
                    else:
                        st.warning(f"No match found in CSV for: {file.name}")
                if renamed_files:
                    st.success("Renaming completed for uploaded files.")
        except Exception as e:
            st.error(f"Failed to process: {e}")

import pandas as pd
import streamlit as st
import os

# App Title
st.title("File Renaming Tool")

# Step 1: Select File Type
st.header("Step 1: Select File Type")
file_type = st.selectbox(
    "Select the file type:",
    options=["IES", "PDF", "GOS", "PNG", "All Files"]  # PNG added
)

# Step 2: Provide a template download link
st.header("Step 2: Download Template")

# Dynamically create the template based on file type selection
def create_template(file_type):
    if file_type == "All Files":
        example_old_file = "Example_Old_File"
        example_new_file = "Example_New_File"
    else:
        extension = file_type.upper()
        example_old_file = f"Example_Old_File.{extension}"
        example_new_file = f"Example_New_File.{extension}"

    return {
        "Old File Name": [example_old_file],
        "New File Name": [example_new_file]
    }

template_data = create_template(file_type)
df_template = pd.DataFrame(template_data)
template_file_name = f"File_Renaming_Template_{file_type.replace(' ', '_').upper()}.xlsx"
df_template.to_excel(template_file_name, index=False)

with open(template_file_name, "rb") as file:
    st.download_button(
        label=f"Download Template for {file_type}", 
        data=file, 
        file_name=template_file_name, 
        mime="application/vnd.ms-excel"
    )

# Step 3: Upload folder path and Excel file
st.header("Step 3: Upload Folder Path and Excel File")

folder_path = st.text_input("Enter the folder path where the files are located:")
uploaded_file = st.file_uploader("Upload the Excel file with renaming details", type=["xlsx"])

# Step 4: Process the file renaming
if st.button("Rename Files"):
    if not folder_path or not uploaded_file:
        st.error("Please provide both the folder path and the Excel file.")
    else:
        # Read the Excel file
        try:
            renaming_data = pd.read_excel(uploaded_file)
            if "Old File Name" not in renaming_data.columns or "New File Name" not in renaming_data.columns:
                st.error("Invalid template format. Ensure it contains 'Old File Name' and 'New File Name' columns.")
            else:
                # Rename files
                for index, row in renaming_data.iterrows():
                    old_name = row["Old File Name"]
                    new_name = row["New File Name"]

                    # Ensure the new file name has the correct extension if specific file type is selected
                    if file_type != "All Files":
                        extension = f".{file_type.upper()}"
                        if not new_name.endswith(extension):
                            new_name += extension

                    old_file_path = os.path.join(folder_path, old_name)
                    new_file_path = os.path.join(folder_path, new_name)

                    try:
                        os.rename(old_file_path, new_file_path)
                        st.success(f"Renamed: {old_name} -> {new_name}")
                    except FileNotFoundError:
                        st.warning(f"File not found: {old_name}")
                    except Exception as e:
                        st.error(f"Error renaming {old_name}: {e}")
        except Exception as e:
            st.error(f"Failed to process the file: {e}")

st.write("File renaming completed.")

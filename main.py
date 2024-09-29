import streamlit as st
from src.generate_email import generate_email, generate_address
from src.extract_receiver import all_emails
from src.send_email import send_email
from src.generate_letterhead import add_text_to_pdf

st.set_page_config(page_title="Mailme.AI 🤖")

st.title("Mailme AI🤖")

introduction= """
Hey there! 👋

Welcome to **Mailme.AI** — where writing and sending emails is as easy as typing a prompt! 🎉

Just give us the email details and if you want, throw in a custom letterhead! 🖋️ We'll take care of the rest. 🚀

Ready to get started? Drop your prompt below and watch the magic happen! 💫
"""
st.write(introduction)
st.divider()

# Define inputs for email
style = st.selectbox("Pick the format for your email", ("Formal", "Informal", "Friendly"), index=None)
letterhead_bool = st.selectbox("Do you wish to include a letterhead document in your mail?", ("Yes", "No"), index=None)
email_details = st.text_area("Type in the details of the email", height=150)

txt = ""
if letterhead_bool == "Yes":
    txt = st.text_input("Enter the address of recipient to include in letterhead...")

# Ensure session state variables are initialized
if "email_data" not in st.session_state:
    st.session_state.email_data = {}

if "email_sent" not in st.session_state:
    st.session_state.email_sent = False

if "full_address" not in st.session_state:
    st.session_state.full_addresss = ""

if st.button("Generate Email"):
    if all([style, letterhead_bool, email_details]):
        # st.divider()

        # Generate letterhead if needed
        address = {}
        full_address = ""
        if txt:
            address = generate_address(txt)
            try:
                full_address += address["address_line_1"] + "," + "\n"
                full_address += address["city"]
                try:
                    value = address["country"]
                    full_address += ", " + address["state"]
                    full_address += "," + "\n"
                    full_address += value + "." + "\n"
                except:
                    full_address += "," + "\n" + address["state"]
                    full_address += "." + "\n"
                full_address += address["time"]
            except:
                full_address = "\n".join(txt.split(","))

        # Generate email content
        email = generate_email(style, email_details)
        subject = email["subject"]
        body = email["body"]
        email_addresses = ", ".join(all_emails(email_details))

        # Save generated email data in session state
        st.session_state.email_data = {
            "subject": subject,
            "body": body,
            "email_addresses": email_addresses,
            "address": full_address
        }

        # # Display email inputs for confirmation
        # st.text_input("Recipients", st.session_state.email_data["email_addresses"])
        # st.text_input("Subject", st.session_state.email_data["subject"])
        # st.text_area("Body", st.session_state.email_data["body"], height=250)

    else:
        st.warning("Ensure you fill in all details.")

# Display the send email section only if the email has been generated
if "subject" in st.session_state.email_data and "body" in st.session_state.email_data:
    st.divider()

    confirm_recipient_address = ""
    if letterhead_bool=="Yes":
        
        confirm_recipient_address = st.text_area("Confirm the recipient's location/address", st.session_state.email_data["address"], height=130)

    confirm_email_addresses = st.text_input("Confirm recipient(s)", st.session_state.email_data["email_addresses"])
    confirm_subject = st.text_input("Confirm Subject", st.session_state.email_data["subject"])
    confirm_body = st.text_area("Confirm Body", st.session_state.email_data["body"], height=250)

    if letterhead_bool=="Yes":
        add_text_to_pdf(confirm_recipient_address, confirm_subject, confirm_body)
        with open("./letterhead/populated.pdf", "rb") as file:
            st.download_button(
                label = "Download and view letterhead",
                data = file,
                file_name = "letterhead.pdf",
                mime = "text/pdf")
    
    if st.button("Send email 📨"):
        # Log the button click to ensure it's being triggered
        # st.write("Send button clicked")  # This is for debugging in Streamlit

        # Call send_email function
        if letterhead_bool=="Yes":
            status = send_email(confirm_subject, confirm_body, confirm_email_addresses.split(", "), attachment = True)
        else:
            status = send_email(confirm_subject, confirm_body, confirm_email_addresses.split(", "))
            
        
        # Update session state if email is successfully sent
        if status:
            st.session_state.email_sent = True
            st.success("Email successfully sent. Thanks for using Mailme.AI")
        else:
            st.error("There was an issue sending the email.")

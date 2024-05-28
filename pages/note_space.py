import streamlit as st

if 'notes' not in st.session_state:
    st.session_state.notes=[]

# Function to add a note
def add_note():
    note = st.text_area("Enter your note here:")
    if st.button("Add Note"):
        if note:
            st.session_state.notes.append(note)
            st.success("Note added successfully!")
            # Clear the text area after adding the note
        else:
            st.warning("Please enter a note.")

# Function to display all notes in a grid
def show_notes():
    st.header("All Notes")
    if st.session_state.notes:
        for i, note in enumerate(st.session_state.notes):
            st.write(f"**Note {i+1}:** {note}")
    else:
        st.write("No notes added yet.")

# Main function
def main():
    st.title("Note Taking App")
    
    add_note()
    show_notes()

if __name__ == "__main__":
    # notes = []  # List to store notes
    main()

# import streamlit as st
# from streamlit_option_menu import option_menu

# with st.sidebar:
#     selected = option_menu(
#         menu_title="Menu",
#         options=["Home", "Data", "Chat"],
#         icons=["house", "database-add", "chat-left"],
#         # menu_icon="three-dots-vertical",
#         default_index=0,
#         # orientation="vertical",
#     )
# if selected == "Home":
#     st.title(selected)
#     st.write("Welcome to NoteRAG!")
# if selected == "Data":
#     st.title(selected)
#     st.write("Welcome to NoteRAG!")
# if selected == "Chat":
#     st.title(selected)
#     st.write("Welcome to NoteRAG!")


import streamlit as st
from streamlit_option_menu import option_menu
# with st.sidebar:
selected = option_menu(
    menu_title=None,
    options=["Home", "Data", "Chat"],
    icons=["house", "book", "chat-left"],
    default_index=0,
    orientation="horizontal",
)

if selected == "Home":
    st.title(selected)
    # st.write("Welcome to NoteRAG!")
if selected == "Data":
    st.title(selected)
    # st.write("Welcome to NoteRAG!")
if selected == "Chat":
    st.title(selected)
    # st.write("Welcome to NoteRAG!")
# import streamlit as st
# from streamlit_option_menu import option_menu

# # 1=sidebar menu, 2=horizontal menu, 3=horizontal menu w/ custom menu
# EXAMPLE_NO = 2


# def streamlit_menu(example=1):
#     if example == 1:
#         # 1. as sidebar menu
#         with st.sidebar:
#             selected = option_menu(
#                 menu_title="Main Menu",  # required
#                 options=["Home", "Projects", "Contact"],  # required
#                 icons=["house", "book", "envelope"],  # optional
#                 menu_icon="cast",  # optional
#                 default_index=0,  # optional
#             )
#         return selected

#     if example == 2:
#         # 2. horizontal menu w/o custom style
#         selected = option_menu(
#             menu_title=None,  # required
#             options=["Home", "Projects", "Contact"],  # required
#             icons=["house", "book", "envelope"],  # optional
#             menu_icon="cast",  # optional
#             default_index=0,  # optional
#             orientation="horizontal",
#         )
#         return selected

#     if example == 3:
#         # 2. horizontal menu with custom style
#         selected = option_menu(
#             menu_title=None,  # required
#             options=["Home", "Projects", "Contact"],  # required
#             icons=["house", "book", "envelope"],  # optional
#             menu_icon="cast",  # optional
#             default_index=0,  # optional
#             orientation="horizontal",
#             styles={
#                 "container": {"padding": "0!important", "background-color": "#fafafa"},
#                 "icon": {"color": "orange", "font-size": "25px"},
#                 "nav-link": {
#                     "font-size": "25px",
#                     "text-align": "left",
#                     "margin": "0px",
#                     "--hover-color": "#eee",
#                 },
#                 "nav-link-selected": {"background-color": "green"},
#             },
#         )
#         return selected


# selected = streamlit_menu(example=EXAMPLE_NO)

# if selected == "Home":
#     st.title(f"You have selected {selected}")
# if selected == "Projects":
#     st.title(f"You have selected {selected}")
# if selected == "Contact":
#     st.title(f"You have selected {selected}")
import streamlit as st
from PIL import Image


@st.dialog("Capture or upload photos")
def add_photos_dialog():

    st.write('Add classroom photos to scan for attendance')

    # Initialize selected tab
    if 'photo_tab' not in st.session_state:
        st.session_state.photo_tab = 'camera'


    # =========================================================
    # CAMERA / UPLOAD BUTTONS
    # =========================================================

    t1, t2 = st.columns(2)


    # -------------------------
    # CAMERA
    # -------------------------

    with t1:

        camera_type = (
            "primary"
            if st.session_state.photo_tab == 'camera'
            else "secondary"
        )

        if st.button(
            'Camera',
            type=camera_type,
            width='stretch'
        ):
            st.session_state.photo_tab = 'camera'


    # -------------------------
    # UPLOAD
    # -------------------------

    with t2:

        upload_type = (
            "primary"
            if st.session_state.photo_tab == 'upload'
            else "secondary"
        )

        if st.button(
            'Upload photos',
            type=upload_type,
            width='stretch'
        ):
            st.session_state.photo_tab = 'upload'


    # =========================================================
    # CAMERA TAB
    # =========================================================

    if st.session_state.photo_tab == 'camera':

        cam_photo = st.camera_input(
            'Take Snapshot',
            key='dialog_cam'
        )

        if cam_photo:

            st.session_state.attendance_images.append(
                Image.open(cam_photo)
            )

            st.toast('Photo Captured')

            st.rerun()


    # =========================================================
    # UPLOAD TAB
    # =========================================================

    elif st.session_state.photo_tab == 'upload':

        uploaded_files = st.file_uploader(
            'choose image files',
            type=['jpg', 'png', 'jpeg'],
            accept_multiple_files=True,
            key='dialog_upload'
        )

        if uploaded_files:

            for f in uploaded_files:

                st.session_state.attendance_images.append(
                    Image.open(f)
                )

            st.toast('Photo Uploaded Successfully')

            st.rerun()


    # =========================================================
    # DONE
    # =========================================================

    st.divider()

    if st.button(
        'Done',
        type='primary',
        width='stretch'
    ):
        st.rerun()
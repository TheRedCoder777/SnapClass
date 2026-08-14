import streamlit as st
import time

from PIL import Image
import numpy as np

from src.ui.base_layout import (
    style_background_dashboard,
    style_base_layout
)

from src.components.header import header_dashboard
from src.components.footer import footer_dashboard

from src.pipelines.face_pipeline import (
    predict_attendance,
    get_face_embeddings,
    train_classifier
)

from src.pipelines.voice_pipeline import (
    get_voice_embedding
)

from src.database.db import (
    get_all_students,
    create_student,
    get_student_subjects,
    get_student_attendance,
    unenroll_student_to_subject
)

from src.database.config import supabase

from src.components.dialog_enroll import enroll_dialog
from src.components.subject_card import subject_card


# ============================================================
# VOICE ENROLLMENT DIALOG
# ============================================================

@st.dialog("Voice Enrollment")
def voice_enrollment_dialog():

    st.header("🎙️ Register Your Voice")

    st.write(
        "Your face was recognized successfully, "
        "but your voice profile has not been registered yet."
    )

    st.info(
        "Register your voice to allow teachers to use "
        "Voice Attendance for you."
    )

    st.write("")

    st.subheader("Record a short phrase")

    st.caption(
        'For example: "I am present" or '
        '"My name is Riya".'
    )

    audio_data = st.audio_input(
        "Record your voice",
        key="existing_student_voice"
    )

    st.write("")

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "Save Voice",
            type="primary",
            width="stretch",
            disabled=audio_data is None
        ):

            if audio_data is None:

                st.warning(
                    "Please record your voice first."
                )

                return

            student_id = (
                st.session_state
                .student_data["student_id"]
            )

            with st.spinner(
                "Creating voice profile..."
            ):

                try:

                    audio_bytes = audio_data.read()

                    voice_embedding = get_voice_embedding(
                        audio_bytes
                    )

                    if voice_embedding is None:

                        st.error(
                            "Could not create a voice profile. "
                            "Please record your voice again."
                        )

                        return

                    # Convert numpy array to a normal
                    # Python list for Supabase.
                    if hasattr(
                        voice_embedding,
                        "tolist"
                    ):

                        voice_embedding = (
                            voice_embedding.tolist()
                        )

                    # Save voice embedding
                    response = (
                        supabase
                        .table("students")
                        .update({
                            "voice_embedding":
                                voice_embedding
                        })
                        .eq(
                            "student_id",
                            student_id
                        )
                        .execute()
                    )

                    if response.data:

                        # Update session data immediately
                        st.session_state.student_data[
                            "voice_embedding"
                        ] = voice_embedding

                        st.session_state[
                            "voice_enrollment_prompted"
                        ] = True

                        st.success(
                            "Voice profile registered successfully!"
                        )

                        time.sleep(1)

                        st.rerun()

                    else:

                        st.error(
                            "Voice profile could not be saved."
                        )

                except Exception as e:

                    st.error(
                        "Something went wrong while "
                        "registering your voice."
                    )

                    st.exception(e)

    with col2:

        if st.button(
            "Skip for Now",
            type="secondary",
            width="stretch"
        ):

            st.session_state[
                "voice_enrollment_prompted"
            ] = True

            st.rerun()


# ============================================================
# CHECK VOICE PROFILE
# ============================================================

def has_voice_profile(student_data):

    voice_embedding = student_data.get(
        "voice_embedding"
    )

    if voice_embedding is None:
        return False

    try:

        return len(voice_embedding) > 0

    except TypeError:

        return True


# ============================================================
# STUDENT DASHBOARD
# ============================================================

def student_dashboard():

    student_data = st.session_state.student_data

    student_id = student_data["student_id"]

    # ========================================================
    # HEADER
    # ========================================================

    c1, c2 = st.columns(
        2,
        vertical_alignment="center",
        gap="xxlarge"
    )

    with c1:

        header_dashboard()

    with c2:

        st.subheader(
            f"Welcome, {student_data['name']}"
        )

        if st.button(
            "Logout",
            type="secondary",
            key="loginbackbtn",
            shortcut="control+backspace"
        ):

            st.session_state["is_logged_in"] = False

            st.session_state.pop(
                "student_data",
                None
            )

            st.session_state.pop(
                "voice_enrollment_prompted",
                None
            )

            st.rerun()

    st.space()

    # ========================================================
    # SUBJECTS HEADER
    # ========================================================

    c1, c2 = st.columns(2)

    with c1:

        st.header(
            "Your Enrolled Subjects"
        )

    with c2:

        if st.button(
            "Enroll in Subject",
            type="primary",
            width="stretch"
        ):

            enroll_dialog()

    st.divider()

    # ========================================================
    # LOAD SUBJECTS
    # ========================================================

    with st.spinner(
        "Loading your enrolled subjects.."
    ):

        subjects = get_student_subjects(
            student_id
        )

        logs = get_student_attendance(
            student_id
        )

    # ========================================================
    # ATTENDANCE STATISTICS
    # ========================================================

    stats_map = {}

    for log in logs:

        sid = log["subject_id"]

        if sid not in stats_map:

            stats_map[sid] = {
                "total": 0,
                "attended": 0
            }

        stats_map[sid]["total"] += 1

        if log.get("is_present"):

            stats_map[sid]["attended"] += 1

    # ========================================================
    # SUBJECT CARDS
    # ========================================================

    if not subjects:

        st.info(
            "You are not enrolled in any subjects yet."
        )

    else:

        cols = st.columns(2)

        for i, sub_node in enumerate(subjects):

            sub = sub_node["subjects"]

            sid = sub["subject_id"]

            stats = stats_map.get(
                sid,
                {
                    "total": 0,
                    "attended": 0
                }
            )

            def unenroll_button(
                student_id=student_id,
                sid=sid,
                subject_name=sub["name"]
            ):

                if st.button(
                    "Unenroll from this course",
                    type="tertiary",
                    width="stretch",
                    icon=":material/delete_forever:"
                ):

                    unenroll_student_to_subject(
                        student_id,
                        sid
                    )

                    st.toast(
                        f"Unenrolled from {subject_name} successfully!"
                    )

                    st.rerun()

            with cols[i % 2]:

                subject_card(
                    name=sub["name"],
                    code=sub["subject_code"],
                    section=sub["section"],
                    stats=[
                        (
                            "📅",
                            "Total",
                            stats["total"]
                        ),
                        (
                            "✅",
                            "Attended",
                            stats["attended"]
                        )
                    ],
                    footer_callback=unenroll_button
                )

    footer_dashboard()


# ============================================================
# STUDENT SCREEN
# ============================================================

def student_screen():

    style_background_dashboard()
    style_base_layout()

    # ========================================================
    # ALREADY LOGGED-IN STUDENT
    # ========================================================

    if "student_data" in st.session_state:

        student_dashboard()

        # ----------------------------------------------------
        # Show voice enrollment only if necessary
        # ----------------------------------------------------

        student_data = st.session_state.student_data

        if (
            not has_voice_profile(student_data)
            and not st.session_state.get(
                "voice_enrollment_prompted",
                False
            )
        ):

            st.session_state[
                "voice_enrollment_prompted"
            ] = True

            voice_enrollment_dialog()

        return

    # ========================================================
    # LOGIN HEADER
    # ========================================================

    c1, c2 = st.columns(
        2,
        vertical_alignment="center",
        gap="xxlarge"
    )

    with c1:

        header_dashboard()

    with c2:

        if st.button(
            "Go back to Home",
            type="secondary",
            key="loginbackbtn",
            shortcut="control+backspace"
        ):

            st.session_state["login_type"] = None

            st.rerun()

    # ========================================================
    # FACE LOGIN
    # ========================================================

    st.header(
        "Login using FaceID",
        text_alignment="center"
    )

    st.space()
    st.space()

    show_registration = False

    photo_source = st.camera_input(
        "Position your face in the center"
    )

    # ========================================================
    # PROCESS PHOTO
    # ========================================================

    if photo_source:

        img = np.array(
            Image.open(photo_source)
        )

        with st.spinner(
            "AI is scanning.."
        ):

            detected, all_ids, num_faces = (
                predict_attendance(img)
            )

        # ----------------------------------------------------
        # NO FACE
        # ----------------------------------------------------

        if num_faces == 0:

            st.warning(
                "Face not found!"
            )

        # ----------------------------------------------------
        # MULTIPLE FACES
        # ----------------------------------------------------

        elif num_faces > 1:

            st.warning(
                "Multiple faces found"
            )

        # ----------------------------------------------------
        # ONE FACE
        # ----------------------------------------------------

        else:

            # =================================================
            # FACE RECOGNIZED
            # =================================================

            if detected:

                student_id = list(
                    detected.keys()
                )[0]

                all_students = get_all_students()

                student = next(
                    (
                        s
                        for s in all_students
                        if s["student_id"] == student_id
                    ),
                    None
                )

                if student:

                    # -----------------------------------------
                    # LOGIN
                    # -----------------------------------------

                    st.session_state["is_logged_in"] = True

                    st.session_state["user_role"] = (
                        "student"
                    )

                    st.session_state["student_data"] = (
                        student
                    )

                    # Allow voice prompt to appear
                    # if this student has no voice profile.
                    st.session_state[
                        "voice_enrollment_prompted"
                    ] = False

                    st.toast(
                        f"Welcome {student['name']}",
                        icon="👋"
                    )

                    time.sleep(1)

                    st.rerun()

            # =================================================
            # FACE NOT RECOGNIZED
            # =================================================

            else:

                st.info(
                    "Face not recognized! "
                    "You might be a new student!"
                )

                show_registration = True

    # ========================================================
    # NEW STUDENT REGISTRATION
    # ========================================================

    if show_registration:

        with st.container(
            border=True
        ):

            st.header(
                "Register New Profile"
            )

            # ------------------------------------------------
            # NAME
            # ------------------------------------------------

            new_name = st.text_input(
                "Enter your name",
                placeholder="E.g. Riya"
            )

            # =================================================
            # VOICE ENROLLMENT
            # =================================================

            st.subheader(
                "Optional: Voice Enrollment"
            )

            st.info(
                "Register your voice for "
                "voice-only attendance."
            )

            st.caption(
                'Record a short phrase such as '
                '"I am present" or '
                '"My name is Riya".'
            )

            audio_data = None

            try:

                audio_data = st.audio_input(
                    "Record your voice"
                )

            except Exception:

                st.error(
                    "Audio recording failed. "
                    "You can still create your profile "
                    "without voice enrollment."
                )

            # =================================================
            # CREATE ACCOUNT
            # =================================================

            if st.button(
                "Create Account",
                type="primary"
            ):

                # ---------------------------------------------
                # NAME VALIDATION
                # ---------------------------------------------

                if not new_name.strip():

                    st.warning(
                        "Please enter your name!"
                    )

                    return

                with st.spinner(
                    "Creating profile.."
                ):

                    try:

                        # -------------------------------------
                        # FACE EMBEDDING
                        # -------------------------------------

                        img = np.array(
                            Image.open(photo_source)
                        )

                        encodings = get_face_embeddings(
                            img
                        )

                        if not encodings:

                            st.error(
                                "Couldn't capture your "
                                "facial features for registration."
                            )

                            return

                        face_emb = encodings[
                            0
                        ].tolist()

                        # -------------------------------------
                        # VOICE EMBEDDING
                        # -------------------------------------

                        voice_emb = None

                        if audio_data:

                            try:

                                voice_emb = (
                                    get_voice_embedding(
                                        audio_data.read()
                                    )
                                )

                                if hasattr(
                                    voice_emb,
                                    "tolist"
                                ):

                                    voice_emb = (
                                        voice_emb.tolist()
                                    )

                            except Exception as voice_error:

                                st.warning(
                                    "Your face was captured, "
                                    "but the voice recording "
                                    "could not be processed. "
                                    "The profile will be created "
                                    "without voice enrollment."
                                )

                                voice_emb = None

                        # -------------------------------------
                        # CREATE STUDENT
                        # -------------------------------------

                        response_data = create_student(
                            new_name.strip(),
                            face_embedding=face_emb,
                            voice_embedding=voice_emb
                        )

                        if not response_data:

                            st.error(
                                "Could not create student profile."
                            )

                            return

                        # -------------------------------------
                        # RETRAIN FACE CLASSIFIER
                        # -------------------------------------

                        train_classifier()

                        # -------------------------------------
                        # LOGIN STUDENT
                        # -------------------------------------

                        st.session_state[
                            "is_logged_in"
                        ] = True

                        st.session_state[
                            "user_role"
                        ] = "student"

                        st.session_state[
                            "student_data"
                        ] = response_data[0]

                        st.session_state[
                            "voice_enrollment_prompted"
                        ] = True

                        # -------------------------------------
                        # SUCCESS MESSAGE
                        # -------------------------------------

                        if voice_emb is not None:

                            st.toast(
                                f"Profile created! "
                                f"Hi {new_name.strip()}! "
                                f"Voice registered 🎙️",
                                icon="🎉"
                            )

                        else:

                            st.toast(
                                f"Profile created! "
                                f"Hi {new_name.strip()}!",
                                icon="🎉"
                            )

                        time.sleep(1)

                        st.rerun()

                    except Exception as e:

                        st.error(
                            "Something went wrong while "
                            "creating your profile."
                        )

                        st.exception(e)

    # ========================================================
    # FOOTER
    # ========================================================

    footer_dashboard()
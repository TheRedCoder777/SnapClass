import streamlit as st

from src.database.db import enroll_student_to_subject
from src.database.config import supabase

import time


@st.dialog("Enroll in Subject")
def enroll_dialog():

    st.write(
        "Enter the subject code provided by your teacher "
        "to enroll"
    )

    # =========================================================
    # SUBJECT CODE
    # =========================================================

    join_code = st.text_input(
        "Subject Code",
        placeholder="Eg. CS101"
    )


    # =========================================================
    # FIND SUBJECTS
    # =========================================================

    if st.button(
        "Find Subject",
        type="primary",
        width="stretch"
    ):

        if not join_code.strip():

            st.warning(
                "Please enter a subject code"
            )

            return


        join_code = join_code.strip()


        try:

            # -------------------------------------------------
            # FIND ALL SUBJECTS WITH THIS CODE
            # -------------------------------------------------

            res = (
                supabase
                .table("subjects")
                .select(
                    "subject_id, name, subject_code, section, teacher_id"
                )
                .eq(
                    "subject_code",
                    join_code
                )
                .execute()
            )


            if not res.data:

                st.error(
                    f"No subject found with code "
                    f"'{join_code}'."
                )

                return


            # -------------------------------------------------
            # STORE RESULTS
            # -------------------------------------------------

            st.session_state["enrollment_subjects"] = (
                res.data
            )

            st.rerun()


        except Exception as e:

            st.error(
                "Something went wrong while finding "
                "the subject."
            )

            st.exception(e)


    # =========================================================
    # SUBJECT SELECTION
    # =========================================================

    subjects = st.session_state.get(
        "enrollment_subjects"
    )


    if subjects:

        st.divider()

        st.subheader(
            "Select your subject"
        )


        # -----------------------------------------------------
        # GET TEACHER NAMES
        # -----------------------------------------------------

        teacher_names = {}


        for subject in subjects:

            teacher_id = subject.get("teacher_id")


            if teacher_id not in teacher_names:

                teacher_res = (
                    supabase
                    .table("teachers")
                    .select("name")
                    .eq(
                        "teacher_id",
                        teacher_id
                    )
                    .execute()
                )


                if teacher_res.data:

                    teacher_names[teacher_id] = (
                        teacher_res.data[0]["name"]
                    )

                else:

                    teacher_names[teacher_id] = (
                        f"Teacher {teacher_id}"
                    )


        # -----------------------------------------------------
        # IF ONLY ONE SUBJECT EXISTS
        # -----------------------------------------------------

        if len(subjects) == 1:

            subject = subjects[0]

            teacher_name = teacher_names.get(
                subject.get("teacher_id"),
                "Unknown Teacher"
            )


            st.info(
                f"**{subject['name']}**\n\n"
                f"Code: {subject['subject_code']}  \n"
                f"Section: {subject['section']}  \n"
                f"Teacher: {teacher_name}"
            )


            selected_subject_id = (
                subject["subject_id"]
            )


        # -----------------------------------------------------
        # MULTIPLE SUBJECTS WITH SAME CODE
        # -----------------------------------------------------

        else:

            st.warning(
                "Multiple subjects were found with "
                f"the code **{join_code}**. "
                "Please select the correct one."
            )


            options = []


            for subject in subjects:

                teacher_name = teacher_names.get(
                    subject.get("teacher_id"),
                    "Unknown Teacher"
                )


                label = (
                    f"{subject['name']} | "
                    f"Section {subject['section']} | "
                    f"Teacher: {teacher_name}"
                )


                options.append(label)


            selected_index = st.selectbox(
                "Choose your subject",
                range(len(options)),
                format_func=lambda i: options[i]
            )


            selected_subject_id = subjects[
                selected_index
            ]["subject_id"]


        # =====================================================
        # ENROLL
        # =====================================================

        if st.button(
            "Enroll now",
            type="primary",
            width="stretch"
        ):

            try:

                # -------------------------------------------------
                # STUDENT ID
                # -------------------------------------------------

                student_id = (
                    st.session_state
                    .student_data["student_id"]
                )


                # -------------------------------------------------
                # CHECK EXISTING ENROLLMENT
                # -------------------------------------------------

                check = (
                    supabase
                    .table("subject_students")
                    .select("*")
                    .eq(
                        "subject_id",
                        selected_subject_id
                    )
                    .eq(
                        "student_id",
                        student_id
                    )
                    .execute()
                )


                if check.data:

                    st.warning(
                        "You are already enrolled "
                        "in this subject."
                    )

                    return


                # -------------------------------------------------
                # ENROLL
                # -------------------------------------------------

                response = enroll_student_to_subject(
                    student_id,
                    selected_subject_id
                )


                if response:

                    # Find selected subject for message
                    selected_subject = next(
                        (
                            s for s in subjects
                            if s["subject_id"]
                            == selected_subject_id
                        ),
                        None
                    )


                    if selected_subject:

                        st.success(
                            f"Successfully enrolled in "
                            f"{selected_subject['name']}!"
                        )

                    else:

                        st.success(
                            "Successfully enrolled!"
                        )


                    # Clear previous search
                    st.session_state.pop(
                        "enrollment_subjects",
                        None
                    )


                    time.sleep(1)

                    st.rerun()


                else:

                    st.error(
                        "Enrollment failed. "
                        "No enrollment record was returned."
                    )


            except Exception as e:

                st.error(
                    "Something went wrong while enrolling."
                )

                st.exception(e)
import dlib
import numpy as np
import face_recognition_models
from sklearn.svm import SVC
import streamlit as st

from src.database.db import get_all_students


# ============================================================
# LOAD DLIB FACE MODELS
# ============================================================

@st.cache_resource
def load_dlib_models():

    detector = dlib.get_frontal_face_detector()

    sp = dlib.shape_predictor(
        face_recognition_models.pose_predictor_model_location()
    )

    facerec = dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )

    return detector, sp, facerec


# ============================================================
# CREATE FACE EMBEDDINGS
# ============================================================

def get_face_embeddings(image_np):

    detector, sp, facerec = load_dlib_models()

    faces = detector(image_np, 1)

    encodings = []

    for face in faces:

        shape = sp(
            image_np,
            face
        )

        face_descriptor = (
            facerec.compute_face_descriptor(
                image_np,
                shape,
                1
            )
        )

        encodings.append(
            np.array(face_descriptor)
        )

    return encodings


# ============================================================
# TRAIN SVM MODEL
# ============================================================

@st.cache_resource
def get_trained_model():

    X = []
    y = []

    student_db = get_all_students()

    if not student_db:
        return None

    for student in student_db:

        embedding = student.get(
            "face_embedding"
        )

        student_id = student.get(
            "student_id"
        )

        if embedding is not None and student_id is not None:

            try:

                embedding_array = np.array(
                    embedding,
                    dtype=np.float64
                )

                # Make sure it is actually a 128-dimensional
                # face embedding.
                if embedding_array.shape == (128,):

                    X.append(
                        embedding_array
                    )

                    y.append(
                        student_id
                    )

            except Exception:

                continue


    if len(X) == 0:

        return None


    # ----------------------------------------------------------
    # SVM requires at least two different classes.
    # If only one student exists, we don't need the SVM.
    # We will use direct distance matching instead.
    # ----------------------------------------------------------

    unique_students = list(
        set(y)
    )


    clf = None


    if len(unique_students) >= 2:

        clf = SVC(
            kernel="linear",
            probability=True,
            class_weight="balanced"
        )

        try:

            clf.fit(
                X,
                y
            )

        except ValueError:

            clf = None


    return {
        "clf": clf,
        "X": X,
        "y": y
    }


# ============================================================
# RETRAIN / CLEAR CACHE
# ============================================================

def train_classifier():

    # Clear the cached trained model so that newly registered
    # students are loaded from Supabase.
    get_trained_model.clear()

    model_data = get_trained_model()

    return model_data is not None


# ============================================================
# FACE RECOGNITION
# ============================================================

def predict_attendance(
    class_image_np,
    resemblance_threshold=0.55
):

    # ----------------------------------------------------------
    # Detect faces in image
    # ----------------------------------------------------------

    encodings = get_face_embeddings(
        class_image_np
    )

    detected_student = {}

    if not encodings:

        return (
            detected_student,
            [],
            0
        )


    # ----------------------------------------------------------
    # Load trained face data
    # ----------------------------------------------------------

    model_data = get_trained_model()

    if not model_data:

        return (
            detected_student,
            [],
            len(encodings)
        )


    X_train = model_data["X"]
    y_train = model_data["y"]


    if not X_train or not y_train:

        return (
            detected_student,
            [],
            len(encodings)
        )


    # ----------------------------------------------------------
    # Get unique registered students
    # ----------------------------------------------------------

    all_students = sorted(
        list(
            set(y_train)
        )
    )


    # ----------------------------------------------------------
    # Process every detected face
    # ----------------------------------------------------------

    for encoding in encodings:

        encoding = np.asarray(
            encoding,
            dtype=np.float64
        )


        # ======================================================
        # FIND CLOSEST REGISTERED FACE
        # ======================================================

        best_distance = float("inf")

        best_student_id = None


        for student_id, stored_embedding in zip(
            y_train,
            X_train
        ):

            stored_embedding = np.asarray(
                stored_embedding,
                dtype=np.float64
            )


            distance = np.linalg.norm(
                stored_embedding - encoding
            )


            if distance < best_distance:

                best_distance = distance

                best_student_id = student_id


        # ======================================================
        # ACCEPT ONLY IF CLOSE ENOUGH
        # ======================================================

        if (
            best_student_id is not None
            and best_distance <= resemblance_threshold
        ):

            detected_student[
                int(best_student_id)
            ] = True


    return (
        detected_student,
        all_students,
        len(encodings)
    )
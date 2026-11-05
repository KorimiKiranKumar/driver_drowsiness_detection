def predict_drowsiness(ear, mar, head_pose):
    # Return drowsiness intensity based on EAR, MAR and head pose.
    if head_pose != "STRAIGHT":
        return "MEDIUM"

    # More conservative threshold to avoid false drowsy while awake
    if ear < 0.16 or mar > 0.70:
        return "HIGH"

    if ear < 0.23 or mar > 0.62:
        return "MEDIUM"

    return "NORMAL"
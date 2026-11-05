last_state = None
closed_frames = 0
blink_count = 0
drowsy_count = 0
eye_was_closed = False

BLINK_THRESHOLD = 3
DROWSY_THRESHOLD = 6


def process_frame(frame, eyes):
    global last_state, closed_frames, blink_count, drowsy_count, eye_was_closed

    eyes_open = len(eyes) >= 2

    if eyes_open:
        if eye_was_closed and 0 < closed_frames < DROWSY_THRESHOLD:
            blink_count += 1
            print(f"Blink detected! Total blinks: {blink_count}")

        if eye_was_closed and closed_frames >= DROWSY_THRESHOLD:
            drowsy_count += 1
            print(f"Drowsy detected! Total drowsy events: {drowsy_count}")

        closed_frames = 0
        eye_was_closed = False
        state = "NORMAL"

    else:
        closed_frames += 1
        eye_was_closed = True

        if closed_frames >= DROWSY_THRESHOLD:
            state = "DROWSY"
        elif closed_frames >= BLINK_THRESHOLD:
            state = "BLINKING"
        else:
            state = "BLINKING"

    import cv2

    if state == "BLINKING":
        cv2.putText(frame, "Blink", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 3)
        cv2.putText(frame, f"Blinks: {blink_count}", (50, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

    elif state == "DROWSY":
        cv2.putText(frame, "DROWSY!", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
        cv2.putText(frame, "WAKE UP!", (50, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
        cv2.putText(frame, f"Drowsy Count: {drowsy_count}", (50, 150),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    elif state == "NORMAL":
        cv2.putText(frame, "Awake", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)

    if state != last_state:
        print("Driver State:", state)
        last_state = state

    return state

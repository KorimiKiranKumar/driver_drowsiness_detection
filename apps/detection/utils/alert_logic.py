def trigger_alert(level):
    try:
        if level == "HIGH":
            print("🚨 ALERT: Driver is Drowsy!")
        elif level == "MEDIUM":
            print("⚠️ Warning: Slight drowsiness")
        else:
            print("Driver is normal")
    except Exception as e:
        print("Alert Error:", e)
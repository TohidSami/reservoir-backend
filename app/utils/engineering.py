def calculate_gor(oil,gas):
    if oil<=0:
        return 0
    return gas*1000/(oil)

def calculate_wc(oil,water):
    if oil+water<=0: return 0
    return (water/(water+oil))*100

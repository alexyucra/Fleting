
def get_device_type(width):
    if width <= 600:
        return "mobile"
    elif width <= 1024:
        return "tablet"
    return "desktop"

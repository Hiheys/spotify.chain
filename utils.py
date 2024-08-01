def get_link_data(link):
    """
    Returns a tuple (type, URI) parsed from the input link.
    The type may be "track", "album", "artist", or "playlist".
    """
    link = link.split('?')[0]
    parts = link.split('/')

    for i, part in enumerate(parts):
        if part in ["track", "album", "artist", "playlist"]:
            if i + 1 < len(parts):
                return (part, parts[i + 1])
    return None

# Test the function with your example URL
#link = "https://open.spotify.com/intl-it/track/4R1bPIiMEr5xfejy05H7cW?si=eb7468028a9d410c"
#data = get_link_data(link)
#print(data)

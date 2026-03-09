import io
import csv


# Generator function to stream the CSV row by row
def iter_csv(data):
    stream = io.StringIO()

    if not data:
        yield "No data found\n"
        return

    # Headers exactly matching the dictionary keys from getRegInfo()
    fieldnames = ["team id", "name", "dept", "batch", "attendence"]
    writer = csv.DictWriter(stream, fieldnames=fieldnames)

    # Write the header
    writer.writeheader()
    yield stream.getvalue()

    # Clear the buffer
    stream.seek(0)
    stream.truncate(0)

    # Write and yield each row
    for row in data:
        writer.writerow(row)
        yield stream.getvalue()

        # Clear the buffer after every row to keep memory usage near zero
        stream.seek(0)
        stream.truncate(0)

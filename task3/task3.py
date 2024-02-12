from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/interview_scheduling', methods=['POST'])
def interview_scheduling():
    # Check if the request body is in JSON format
    if not request.is_json:
        return jsonify({"error": "Request body must be JSON"}), 400

    # Retrieve JSON data from the request
    data = request.get_json()
    start_times = data.get('start_times')
    end_times = data.get('end_times')

    # Check if both start_times and end_times are provided and have the same length
    if not start_times or not end_times or len(start_times) != len(end_times):
        return jsonify({"error": "Both start_times and end_times must be provided and have the same length"}), 400

    # Find the maximum number of non-overlapping interviews
    max_interviews = find_max_interviews(start_times, end_times)

    # Return the result as JSON response
    return jsonify({"max_interviews": max_interviews}), 200

def find_max_interviews(start_times, end_times):
    # Sort the intervals by their start times
    intervals = sorted([(start, end) for start, end in zip(start_times, end_times)])

    # Initialize variables
    max_non_overlapping_interviews = 1
    current_end = intervals[0][1]

    # Iterate over the intervals
    for start, end in intervals[1:]:
        # Check if the current interval overlaps with the previous one
        if start >= current_end:
            # If it doesn't overlap, increment the count of non-overlapping interviews
            max_non_overlapping_interviews += 1
            # Update the current end time
            current_end = end

    # Return the maximum number of non-overlapping interviews
    return max_non_overlapping_interviews

if __name__ == '__main__':
    app.run(debug=True)

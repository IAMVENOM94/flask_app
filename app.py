from flask import Flask, render_template, request
from scipy.optimize import minimize

app = Flask(__name__)

def calculate_offset(distance_values, maxDistance, desired_offset_distance):
    def objective_function(offset_value):
        deviations = [((100/offset_value) * (distance/maxDistance) - desired_offset_distance)**2 for distance in distance_values]
        return sum(deviations)
    
    result = minimize(objective_function, 500, bounds=[(0.1, 10000)])
    best_offset = result.x[0]
    offset_distances = [(100/best_offset) * (distance/maxDistance) for distance in distance_values]
    
    return best_offset, offset_distances

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get values from the form
        maxDistance = float(request.form['maxDistance'])
        desired_offset_distance = float(request.form['desired_offset_distance'])
        distance_values = list(map(float, request.form['distance_values'].split(',')))

        best_offset, offset_distances = calculate_offset(distance_values, maxDistance, desired_offset_distance)
        return render_template('results.html', best_offset=best_offset, combined_data=zip(distance_values, offset_distances))


    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

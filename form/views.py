from django.shortcuts import render
# views.py
import json
import os
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt

# Define the JSON file path where form data will be stored
DATA_FILE = 'form_data.json'

# Utility: Load JSON data
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

# Utility: Save JSON data
def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# Endpoint to submit form data (POST) or get all submissions (GET)
@csrf_exempt
def submit_form(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            submissions = load_data()
            # Assign a unique ID
            data['id'] = submissions[-1]['id'] + 1 if submissions else 1
            submissions.append(data)
            save_data(submissions)
            return JsonResponse({'message': 'Form data saved successfully'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    elif request.method == 'GET':
        data = load_data()
        return JsonResponse(data, safe=False)
    return HttpResponseNotAllowed(['GET', 'POST'])

# Endpoint to get all submissions (GET only)
@csrf_exempt
def get_submissions(request):
    if request.method == 'GET':
        data = load_data()
        return JsonResponse(data, safe=False)
    return HttpResponseNotAllowed(['GET'])

# Endpoint to get a specific submission by ID (GET only)
@csrf_exempt
def get_submission_by_id(request, submission_id):
    if request.method == 'GET':
        data = load_data()
        for entry in data:
            if entry['id'] == submission_id:
                return JsonResponse(entry)
        return JsonResponse({'error': 'Submission not found'}, status=404)
    return HttpResponseNotAllowed(['GET'])

# Endpoint to update an existing submission (PUT only)
@csrf_exempt
def update_submission(request, submission_id):
    if request.method == 'PUT':
        try: 
            updated_data = json.loads(request.body.decode('utf-8')) 
            data = load_data()

            for i, entry in enumerate(data):
                if str(entry['id']) == str(submission_id):
                    updated_data['id'] = entry['id']  # Preserve ID
                    data[i] = updated_data
                    save_data(data)
                    return JsonResponse(updated_data, status=200)

            return JsonResponse({'error': 'Submission not found'}, status=404)

        except json.JSONDecodeError as e:
            return JsonResponse({'error': f'Invalid JSON format: {str(e)}'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return HttpResponseNotAllowed(['PUT'])




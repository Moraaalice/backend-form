from django.shortcuts import render
# views.py
import json
import os
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt

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


@csrf_exempt
def get_submissions(request):
    if request.method == 'GET':
        data = load_data()
        return JsonResponse(data, safe=False)
    return HttpResponseNotAllowed(['GET'])

@csrf_exempt
def get_submission_by_id(request, submission_id):
    if request.method == 'GET':
        data = load_data()
        for entry in data:
            if entry['id'] == submission_id:
                return JsonResponse(entry)
        return JsonResponse({'error': 'Submission not found'}, status=404)
    return HttpResponseNotAllowed(['GET'])

@csrf_exempt
def update_submission(request, submission_id):
    if request.method != 'PUT':
        return HttpResponseNotAllowed(['PUT'])

    try:
        data = json.loads(request.body)
        all_data = load_data()

        for i, entry in enumerate(all_data):
            if entry['id'] == submission_id:
                data['id'] = submission_id  # keep ID
                all_data[i] = data
                save_data(all_data)
                return JsonResponse({'message': 'Updated successfully'})

        return JsonResponse({'error': 'Submission not found'}, status=404)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)





import requests

api_key = 'your_api_key'
api_secret = 'your_api_secret'


def process_response(results, val):
    suggested_tags_list = results['result']['tags']
    vehicle_is_detected = False

    for item in suggested_tags_list:
        if item['tag']['en'] == val and item['confidence'] >= 50:
            vehicle_is_detected = True
            break

    if vehicle_is_detected:
        best_suggestion = suggested_tags_list[0]
        detected_tag = best_suggestion['tag']['en']
        print(f'Advertisement was approved. Detected tag is: {detected_tag}')
        return detected_tag
    else:
        print("Advertisement was rejected: irrelevant image")
        return None


def process_image(image_url, tag_val):
    response = requests.get(
        'https://api.imagga.com/v2/tags?image_url=%s' % image_url,
        auth=(api_key, api_secret))
    j = response.json()
    # processing the input image
    return process_response(j, tag_val)



import requests
subscription_key = "cfa2ac95fcf04101b79b839837876d16"
assert subscription_key
vision_base_url = "https://westcentralus.api.cognitive.microsoft.com/vision/v1.0/"
vision_analyze_url = vision_base_url + "analyze"
image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT9Cu4TUwuLeZdK1t-33om3igzcff6SD7-RYO4YCRJbLw-KvmJ6kA"
headers  = {'Ocp-Apim-Subscription-Key': subscription_key }
params   = {'visualFeatures': 'Categories,Description,Color'}
data     = {'url': image_url}
response = requests.post(vision_analyze_url, headers=headers, params=params, json=data)
response.raise_for_status()
analysis = response.json()
image_caption = analysis["description"]["captions"][0]["text"].capitalize()


print(image_caption)

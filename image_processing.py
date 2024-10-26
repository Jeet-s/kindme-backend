# from transformers import BlipProcessor, BlipForConditionalGeneration
# from PIL import Image

# # Load image and model
# def image_to_text(image_path):
#     try:
#         image = Image.open(image_path).convert("RGB")
        
#         # Initialize processor and model directly
#         processor = BlipProcessor.from_pretrained("Salesforce/blip2-opt-2.7b")
#         model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip2-opt-2.7b")
        
#         # Process and generate caption
#         inputs = processor(image, return_tensors="pt")
#         print("------------------------   Tensors  --------------------------")
#         print(inputs)
#         print(" ")
        
#         output = model.generate(**inputs)
#         print("-----------------------   OUTPUT   -----------------------------")
#         print(output)
#         print(" ")
        
#         # Decode the generated output directly
#         caption = processor.tokenizer.decode(output[0], skip_special_tokens=True)
#         print("Generated Caption:", caption)
#         return caption
    
#     except AttributeError as e:
#         print("AttributeError:", e)
#     except Exception as e:
#         print("An error occurred:", e)


from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image

def image_to_text(image_path):
    # Initialize processor and model with a compatible checkpoint
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
    
    # Load image
    image = Image.open(image_path).convert("RGB")

    # Process the image and generate caption
    inputs = processor(image, return_tensors="pt")
    output = model.generate(**inputs)

    # Decode the output
    if output.shape[0] > 0:
        caption = processor.decode(output[0], skip_special_tokens=True)
        return caption
    return "No caption generated"

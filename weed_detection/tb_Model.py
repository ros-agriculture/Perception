from Model import Model

weed_model = Model('config-weed.json')
input_path = r"C:\Users\kvemishe\Documents\ML\Docker_ML\flask\weed.png"
output_path = r"C:\Users\kvemishe\Documents\ML\Docker_ML\flask\output"

print("first attempt")
weed_model.predict(input_path , output_path)
print("second attempt")
weed_model.predict(input_path , output_path)

#weed_model.toJSON()
import os

module_path = os.path.dirname(os.path.realpath(__file__))


print(module_path)
input_path = os.path.join(module_path, 'Alarm.mp3')
output_path = os.path.join(module_path, 'Alarm1.mp3')

print(input_path, output_path)

print(input_path.rsplit(module_path, 1)[1][1:])
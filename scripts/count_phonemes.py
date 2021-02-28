import csv

fileIn = '../data/labeled_frames.csv'
with open(fileIn) as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',')
	phoneme_dict = {
		"aa": 0,
		"ae": 0,
		"ah": 0,
		"ao": 0,
		"aw": 0,
		"ay": 0,
		"b": 0,
		"ch": 0,
		"d": 0,
		"dh": 0,
		"eh": 0,
		"er": 0,
		"ey": 0,
		"f": 0,
		"g": 0,
		"hh": 0,
		"ih": 0,
		"iy": 0,
		"jh": 0,
		"k": 0,
		"l": 0,
		"m": 0,
		"n": 0,
		"ng": 0,
		"ow": 0,
		"oy": 0,
		"p": 0,
		"r": 0,
		"s": 0,
		"sh": 0,
		"t": 0,
		"th": 0,
		"uh": 0,
		"uw": 0,
		"v": 0,
		"w": 0,
		"y": 0,
		"z": 0,
		"zh": 0,
	}
	line_count = 0
	for row in csv_reader:
		if line_count != 0:
			phoneme = row[0]
			phoneme_dict[phoneme] = phoneme_dict[phoneme] + 1
		line_count = line_count + 1
	print(dict(sorted(phoneme_dict.items(), key=lambda item: item[1])))







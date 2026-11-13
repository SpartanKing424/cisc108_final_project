note_names = ["C", "D", "E", "F", "G", "A", "B"]
octave_numbers = [1, 2, 3, 4, 5, 6, 7]

real_notes = []
for octave in octave_numbers:
    for note in note_names:
        real_notes.append(note + str(octave))

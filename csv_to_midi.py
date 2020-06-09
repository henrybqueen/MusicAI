import os
import pandas as pd
import py_midicsv


def main(dir_in, dir_out):
    if not os.path.exists(dir_out):
        os.mkdir(dir_out)

    for file in os.listdir(dir_in):
        if file == ".DS_Store":
            continue

        file_path = dir_in + "/" + file

        df = pd.read_csv(file_path)

        df.insert(2, "Channel", 0)
        df.insert(0, "Track", 1)

        df.to_csv(file_path, index=False)

        with open(file_path, "r") as f:
            lines = f.readlines()

        end_time = lines[-1].split(",")[1]

        lines[0] = "1,0,Start_track\n"
        lines.append("1," + end_time + ",End_track")

        with open(file_path, "w") as f:
            f.writelines(lines)

        midi_object = py_midicsv.csv_to_midi(file_path)

        midi_file = dir_out + "/" + file.replace("csv", "mid")

        with open(midi_file, "wb") as output_file:
            midi_writer = py_midicsv.FileWriter(output_file)
            midi_writer.write(midi_object)

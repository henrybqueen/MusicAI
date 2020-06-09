import os
import pandas as pd


def myround(x):
    return 5 * round(x / 5)


def main(dir_in, dir_out):

    if not os.path.exists(dir_out):
        os.mkdir(dir_out)

    for file in os.listdir(dir_in):

        file_path = dir_in + "/" + file

        df = pd.read_csv(file_path)

        new_path = dir_out + '/' + file.replace("csv", "txt")

        with open(new_path, "w") as out_file:
            for index, row in df.iterrows():
                # first note of song
                if index == 0:
                    curr_time = row["Time"]

                if row["Time"] != curr_time:
                    time_diff = row["Time"] - curr_time
                    curr_time = row["Time"]
                    out_file.write("Time+" + str(time_diff) + "\n")

                # NOTE: this wont work if midi file uses Note_off_c instead of vel=0
                vel = myround(int(row["Velocity"]))

                # out_file.write("vel="+str(row['Velocity'])+"\n")
                out_file.write("vel=" + str(vel) + "\n")
                out_file.write(str(row["Note"]) + "\n")

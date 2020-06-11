import pandas as pd
import py_midicsv
import os


def main(dir_in, dir_out, transpose=True):
    if not os.path.exists(dir_out):
        os.mkdir(dir_out)

    # loop through midi files, write initial csv files
    for file in os.listdir(dir_in):

        if file == ".DS_Store":
            continue

        file_path = dir_in + '/' + file
        csv_list = py_midicsv.midi_to_csv(file_path)
        csv_list = [i.replace(" ", "") for i in csv_list]

        new_path = dir_out + '/' + file.replace("mid", "csv")
        with open(new_path, 'w') as out_file:
            out_file.write("Track,Time,Note_on_c,Channel,Note,Velocity,fill1,fill2\n")
            out_file.writelines(csv_list)

    # read csv files into pandas df
    for file in os.listdir(dir_out):

        if file == ".DS_Store":
            continue

        file = dir_out + '/' + file
        df = pd.read_csv(file)

        df = df.drop(["fill1", 'fill2', 'Channel'], axis=1)

        is_note = (df["Note_on_c"] == "Note_on_c") | (df["Note_on_c"] == "Note_off_c")
        df = df[is_note]

        # convert velocities to integers
        df["Velocity"] = df["Velocity"].apply(lambda x: int(x))

        # merge tracks by sorting by time
        df.sort_values("Time", axis=0, inplace=True)

        # save un-transposed file
        with open(file, 'w'):
            df.to_csv(file, index=False)

        if transpose:

            # Transpose the piece up 4 and down 4, saving it to a new file every time
            df_transpose = df.copy(deep=True)
            # up to 4
            for i in range(1, 5):
                df_transpose["Note"] = df["Note"]

                # splices the transpose number between filename and extension
                file_transpose = file[:-4] + "Transpose_up" + str(i) + ".csv"
                df_transpose["Note"] = df_transpose["Note"].astype('int32')
                df_transpose["Note"] += i

                with open(file_transpose, 'w'):
                    df_transpose.to_csv(file_transpose, index=False)

            # down to 4
            for i in range(1, 5):
                df_transpose["Note"] = df["Note"]

                # splices the transpose number between filename and extension
                file_transpose = file[:-4] + "Transpose_down" + str(i) + ".csv"
                df_transpose["Note"] = df_transpose["Note"].astype('int32')
                df_transpose["Note"] -= i

                with open(file_transpose, 'w'):
                    df_transpose.to_csv(file_transpose, index=False)


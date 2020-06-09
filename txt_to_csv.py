import os


def main(dir_in, dir_out):

    if not os.path.exists(dir_out):
        os.mkdir(dir_out)

    for file in os.listdir(dir_in):

        file_path = dir_in + "/" + file

        with open(file_path, 'r', encoding='unicode_escape') as f:
            lines = f.readlines()

        new_file = dir_out + "/" + file.replace("txt", "csv")

        with open(new_file, "w") as out_file:

            velocity = 0

            out_file.write('Time,Note_on_c,Note,Velocity\n')

            curr_time = 0

            for line in lines:

                # velocity change
                if line[:3] == "vel":
                    velocity = line[4:].replace("\n", "")

                # time change
                elif line[:4] == "Time":
                    curr_time += int(line[5:].replace("\n", ""))

                # if line is a note, then we right a line to the file
                else:
                    note = line.replace("\n", "")
                    new_line = str(curr_time) + ",Note_on_c," + str(note) + "," + str(velocity) + "\n"
                    out_file.write(new_line)

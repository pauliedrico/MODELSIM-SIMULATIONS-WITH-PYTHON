#!/usr/bin/env python
import os
import subprocess

with open("log.txt", 'w') as log:  # opens log.txt file in order to write in it
    print("//////LOG FILE//////", file=log)
    for N in (2, 4, 8):  # iterates simulation process for 2,4 and 8 bits RCA
        # Definizione parallelismo architettura
        with open('constants.vhd', 'w') as f:  # creates constants.vhd
            print("PACKAGE constants IS\n	constant N : natural := " + str(N) + ";\nEND constants;", file=f)
        f.close()

        # Generazione degli input pattern
        file_input = "input_vectors_" + str(N) + "bit.txt"  # defines input_vectors_Nbit and output_vectors_Nbit
        file_output = "output_vectors_" + str(N) + "bit.txt"
        with open(file_input, 'w') as f:
            with open(file_output, 'w') as f1:
                with open('input_vectors.txt', 'w') as f2:
                    for i in range(0, 2 ** N):
                        for j in range(0, 2 ** N):
                            f_ij = ">0" + str(N) + "b"
                            f_s = ">0" + str(N + 1) + "b"
                            print(format(i, f_ij) + " " + format(j, f_ij), file=f)  # writes the pair of numbers in
                            print(format(i, f_ij) + " " + format(j, f_ij),
                                  file=f2)  # input_vectors_Nbit and input_vectors
                            print(format(i + j, f_s), file=f1)  # writes the sum in output_vectors_Nbit
                f2.close()
            f1.close()
        f.close()

        # Simulazione
        os.environ["PATH"] += os.pathsep + "/software/mentor/modelsim_6.5c/modeltech/linux_x86_64/"
        os.environ["LM_LICENSE_FILE"] = "1717@led-x3850-1.polito.it"
        os.system("echo $PATH")
        os.system("echo $LM_LICENSE_FILE")
        print("Starting simulation for " + str(N) + "bit RCA...")
        process = subprocess.call(["vsim", "-c", "-do", "compile.do"])
        print("Simulation completed for " + str(N) + "bit RCA")

        # Lettura e verifica dei risultati
        results_output = "output_results_" + str(N) + "bit.txt"
        with open("output_results.txt") as f:
            with open(results_output, "w") as f1:
                for line in f:
                    f1.write(line)  # copies output_results in output_results_Nbit
            f1.close()
        f.close()
        print("##Simulation results for " + str(N) + "bit RCA##", file=log)
        flag = 0
        with open(file_output) as f:
            with open(results_output) as f1:
                with open(file_input) as f2:
                    for addends, res, test in zip(f2, f1, f):
                        if res != test:  # checks if results are correct
                            flag = 1  # if they aren't, writes error on log.txt
                            print(
                                "Error! Sum between " + addends.strip() + " is not " + res.strip() + ", but "
                                + test.strip(), file=log)
                f2.close()
            f1.close()
        f.close()
        if flag == 0:
            print("All results are correct!", file=log)  # if all results are correct, writes on log.txt
log.close()

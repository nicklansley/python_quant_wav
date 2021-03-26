from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np

def plot_waveform(data, length):
    time = np.linspace(0., length, data.shape[0])
    plt.plot(time, data[:, 0], label="Left channel")
    plt.plot(time, data[:, 1], label="Right channel")
    plt.legend()
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.show()

def print_progress(original_sample_value, previous_progress_message, sample_count, wanted_bit_size):
    # print what is happening (which seems like a lot of code just for this task but worth
    # it when processing large WAV files!
    percentage_completed = int(original_sample_value * 100 / sample_count)
    if percentage_completed % 10 == 0:
        progress_message = f" {wanted_bit_size}-bit >> {percentage_completed}% completed"
        if progress_message != previous_progress_message:
            print(progress_message)
            previous_progress_message = progress_message

    return previous_progress_message

# In the worked examples in the comments:
#   value for this sample = -20000 (range is from -32768 to +32767
#   source_sample_bit_size = 16 bits
#   new_bit_size = 6 bits (and 3 bits)
def quantise(sample, new_bit_size):
    try:
        # The incoming sample has a range from -32768 tp +32767 as it is a signed 16-bit integer.
        # To make our arithmetic a little simpler, we will convert this to an always-positive number
        # between 0 and 65536. So, for our example sample value of -20000:
        # -20000 + 32767 = 12767
        positive_16_bit_sample = sample + 32767

        # 6-bit: max_new_sample_value = 2 to the power 6 = 64 - that is, a sample can be one of 64 possible values
        # 3-bit: max_new_sample_value = 2 to the power 3 = 8  - that is, a sample can be one of 8 possible values
        max_new_sample_value = pow(2, new_bit_size)

        # We need to calculate the sample factor between the two bit sizes by dividing our sample value by the
        # maximum possible sample size which is 2 ^ 16 = 63336
        # sample_factor = 12767 / 65536 = 0.1948089599609375
        sample_factor = positive_16_bit_sample / 65536

        # The next line calculates the value for the sample as if it were sampled at 6 bit (64 possible values)
        # quantised_sample = 64 * 0.1948089599609375 = 12.4677734375 rounded to 12
        # That is, a sample with a value of 12767 in 16-bit space is 12 in 6-bit space.
        # ...and if sampled at 3 bit (8 possible values):
        # quantised_sample = 8 * 0.1948089599609375 = 1.5584716796875 rounded to 1.0
        # That is, a sample with a value of 12767 in 16-bit space is 1 in 3-bit space.
        quantised_sample =  round(max_new_sample_value * sample_factor, 0)

        # Now we have to put the quantised sample back into 16-bit space
        # as we can only save in an 16-bit wav file for a truly equivalent like-for-like demonstration.
        # The sample has lost some of its precision by going from 16-bit to 6-bit/3-bit then back to 16-bit again,
        # causing it to have moved from value 12767 in 16-bit to value 12 in 6-bit, and 1 in 3-bit.
        # 6-bit: reconstituted_sample =  12 * (65536 / 64) = 12 * 1024 = 12288
        # => a quantisation error of 479 (4% difference - not bad)
        # 3-bit: reconstituted_sample =  1 * (65536 / 8) = 1 * 8192 = 8192
        # => a quantisation error of 4575 (36% difference - ouch!)
        # We also subtract our reconstituted_sample by 32767 as we added 32767 at the start of our calculation:
        reconstituted_sample = int(quantised_sample * (65536 / max_new_sample_value)) - 32767

    except ZeroDivisionError as zdf:
        # triggered if a calculation divides by zero
        print(zdf)
        reconstituted_sample = 0

    # print(f"DEBUG ==> sample = {sample}, reconstituted_sample = {reconstituted_sample}")
    #if sample != reconstituted_sample:
    #    print(f"DEBUG ==> sample = {sample}, reconstituted_sample = {reconstituted_sample}")

    return reconstituted_sample


def process_wav_file(from_file_name):
    file_bit_size = 16
    try:
        sample_rate, data = wavfile.read(from_file_name)
        print("Opened audio file", from_file_name)
        print(f"sample rate = {sample_rate}")
        sample_count = data.shape[0]
        print(f"number of samples = {sample_count}")

        # We're going to create a range of files from 15-bit to just 1-bit
        # The 16-bit audio source has values ranging from −32,768 (−1 × 2^15) through 32,767 (2^15 − 1);
        for wanted_bit_size in range (15, 0, -1):
            print(f"Creating {wanted_bit_size}-bit equivalent")

            # clear our output array ready for processing. We set the dat atype
            # to 16-bit (values between 0 and 255)
            out_data_array = np.zeros(sample_count, dtype=np.int16)

            # Since this code is going to print progress in 10% increments
            # we store the previous progress message so as not to print duplicated
            # lines when using very big WAV files where, for example '10%' could be
            # recalculated to the same value several times.
            previous_progress_message = ""

            #initialioe the array index
            array_index_id = 0

            # Loop through every sample in the incoming audio samples:
            for this_sample in range(sample_count):
                # Calculated the quantised value for this sample and append it to our output array
                quantised_value = quantise(data[this_sample], wanted_bit_size)
                out_data_array[array_index_id] = quantised_value
                array_index_id += 1

                previous_progress_message = print_progress(this_sample, previous_progress_message, sample_count, wanted_bit_size)

            # Write out the new WAV file
            out_file_name = f"{wanted_bit_size}_bit_equiv.wav"
            print("Writing", out_file_name)
            wavfile.write(out_file_name, sample_rate, out_data_array.astype(np.int16))

    except wavfile.WavFileWarning as wfw:
        # triggered sometimes if there is metadata in the incoming WAV file
        print(wfw)
    except IndexError as ie:
        # triggered if there is a problem with array index
        print(ie)




if __name__ == '__main__':
    print("Processing started")
    # from_file_name = 'sweep-1Hz-20Khz-5secs-u8bit-48ksps.wav'
    from_file_name = 'test_track_mono_signed_16bit.wav'

    process_wav_file(from_file_name)

    print("Processing completed")

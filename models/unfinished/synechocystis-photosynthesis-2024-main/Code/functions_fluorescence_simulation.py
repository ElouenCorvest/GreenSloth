import functions as fnc
import functions_light_absorption as lip

# Set the cuvette width for light adjustment to cellular absorption
cuvette_width = 0.01  # [m]

# Create a simulation protocol
def make_lights(
    blueInt=80,
    orangeInt=50,
    highblueInt=1800,
    pulseInt=15000,
    orange_wl=633,
    blue_wl=440,
):
    dark = lip.light_spectra("solar", 0.1)
    low_blue = lip.light_gaussianLED(blue_wl, blueInt)
    high_blue = lip.light_gaussianLED(blue_wl, highblueInt)
    orange = lip.light_gaussianLED(orange_wl, orangeInt)

    pulse_orange = lip.light_gaussianLED(orange_wl, pulseInt)
    pulse_blue = lip.light_gaussianLED(blue_wl, pulseInt)
    return [dark, low_blue, high_blue, orange, pulse_orange, pulse_blue]


# Make lights that are ajusted to cuvette width
def make_adjusted_lights(absorption_coef, chlorophyll_sample, lights=make_lights()):
    # Adjust to the mean level in the culture
    lights_adj = lip.get_mean_sample_light(
        lights,  # [µmol(Photons) m^-2 s^-1]
        depth=cuvette_width,
        absorption_coef=absorption_coef,
        chlorophyll_sample=chlorophyll_sample,  # [mmol(Chl) m^-3]
    )
    return lights_adj


## Protocol for 'PSII kinetics, NPQ at state 2'
# Create the initial dark phase with 4 pulses and 300 s acclimation
def create_protocol_noNPQ(
    dark_adj, low_blue_adj, high_blue_adj, orange_adj, pulse_orange_adj, pulse_blue_adj
):
    protocol_noNPQ = fnc.create_protocol_PAM(
        init=300,
        actinic=(dark_adj, 20 - 0.3),  # Actinic light intensity and duration
        saturating=(
            pulse_orange_adj,
            0.3,
        ),  # Saturating pulse light intensity and duration
        cycles=4,
        first_actinic_time=20,
        final_actinic_time=18,
    )

    # Create the low blue light phase with 6 pulses
    protocol_noNPQ = fnc.create_protocol_PAM(
        init=protocol_noNPQ,
        actinic=(low_blue_adj, 20 - 0.3),  # Actinic light intensity and duration
        saturating=(
            pulse_blue_adj,
            0.3,
        ),  # Saturating pulse light intensity and duration
        cycles=6,
        first_actinic_time=2,
        final_actinic_time=18,
    )

    # Create the orange light phase with 15 pulses
    protocol_noNPQ = fnc.create_protocol_PAM(
        init=protocol_noNPQ,
        actinic=(orange_adj, 20 - 0.3),  # Actinic light intensity and duration
        saturating=(
            pulse_orange_adj,
            0.3,
        ),  # Saturating pulse light intensity and duration
        cycles=15,
        first_actinic_time=2,
        final_actinic_time=18,
    )

    # Create the high blue light phase with 9 pulses
    protocol_noNPQ = fnc.create_protocol_PAM(
        init=protocol_noNPQ,
        actinic=(high_blue_adj, 20 - 0.3),  # Actinic light intensity and duration
        saturating=(
            pulse_blue_adj,
            0.3,
        ),  # Saturating pulse light intensity and duration
        cycles=9,
        first_actinic_time=2,
        final_actinic_time=18,
    )

    # Create another low blue light phase with 12 pulses
    protocol_noNPQ = fnc.create_protocol_PAM(
        init=protocol_noNPQ,
        actinic=(low_blue_adj, 20 - 0.3),  # Actinic light intensity and duration
        saturating=(
            pulse_blue_adj,
            0.3,
        ),  # Saturating pulse light intensity and duration
        cycles=12,
        first_actinic_time=2,
        final_actinic_time=18,
    )
    return protocol_noNPQ


## Protocol for 'PSII kinetics, NPQ at state 2'
# Create the initial dark phase with 4 pulses and 300 s acclimation
def create_protocol_NPQ(
    dark_adj, low_blue_adj, high_blue_adj, orange_adj, pulse_orange_adj, pulse_blue_adj
):
    protocol_NPQ = fnc.create_protocol_PAM(
        init=300,
        actinic=(dark_adj, 20 - 0.3),  # Actinic light intensity and duration
        saturating=(
            pulse_orange_adj,
            0.3,
        ),  # Saturating pulse light intensity and duration
        cycles=4,
        first_actinic_time=20,
        final_actinic_time=18,
    )

    # Create the low blue light phase with 6 pulses
    protocol_NPQ = fnc.create_protocol_PAM(
        init=protocol_NPQ,
        actinic=(low_blue_adj, 20 - 0.3),  # Actinic light intensity and duration
        saturating=(
            pulse_blue_adj,
            0.3,
        ),  # Saturating pulse light intensity and duration
        cycles=6,
        first_actinic_time=2,
        final_actinic_time=18,
    )

    # Create the orange light phase with 9 pulses
    protocol_NPQ = fnc.create_protocol_PAM(
        init=protocol_NPQ,
        actinic=(orange_adj, 20 - 0.3),  # Actinic light intensity and duration
        saturating=(
            pulse_orange_adj,
            0.3,
        ),  # Saturating pulse light intensity and duration
        cycles=9,
        first_actinic_time=2,
        final_actinic_time=18,
    )

    # Create the low blue light phase with 9 pulses
    protocol_NPQ = fnc.create_protocol_PAM(
        init=protocol_NPQ,
        actinic=(low_blue_adj, 20 - 0.3),  # Actinic light intensity and duration
        saturating=(
            pulse_blue_adj,
            0.3,
        ),  # Saturating pulse light intensity and duration
        cycles=9,
        first_actinic_time=2,
        final_actinic_time=18,
    )

    # Create the high blue light phase with 9 pulses
    protocol_NPQ = fnc.create_protocol_PAM(
        init=protocol_NPQ,
        actinic=(high_blue_adj, 20 - 0.3),  # Actinic light intensity and duration
        saturating=(
            pulse_blue_adj,
            0.3,
        ),  # Saturating pulse light intensity and duration
        cycles=9,
        first_actinic_time=2,
        final_actinic_time=18,
    )

    # Create another low blue light phase with 12 pulses
    protocol_NPQ = fnc.create_protocol_PAM(
        init=protocol_NPQ,
        actinic=(low_blue_adj, 20 - 0.3),  # Actinic light intensity and duration
        saturating=(
            pulse_blue_adj,
            0.3,
        ),  # Saturating pulse light intensity and duration
        cycles=12,
        first_actinic_time=2,
        final_actinic_time=18,
    )
    return protocol_NPQ


## Protocol for 'PSII kinetics, NPQ at state 2'
# Create the initial dark phase with 4 pulses and 300 s acclimation
def create_protocol_NPQ_short(
    dark_adj, low_blue_adj, high_blue_adj, orange_adj, pulse_orange_adj, pulse_blue_adj
):
    protocol_NPQ = fnc.create_protocol_PAM(
        init=0,
        actinic=(dark_adj, 20 - 0.3),  # Actinic light intensity and duration
        saturating=(
            pulse_orange_adj,
            0.3,
        ),  # Saturating pulse light intensity and duration
        cycles=2,
        first_actinic_time=20,
        final_actinic_time=18,
    )

    # Create the low blue light phase with 6 pulses
    protocol_NPQ = fnc.create_protocol_PAM(
        init=protocol_NPQ,
        actinic=(low_blue_adj, 20 - 0.3),  # Actinic light intensity and duration
        saturating=(
            pulse_blue_adj,
            0.3,
        ),  # Saturating pulse light intensity and duration
        cycles=3,
        first_actinic_time=2,
        final_actinic_time=18,
    )

    # Create the orange light phase with 9 pulses
    protocol_NPQ = fnc.create_protocol_PAM(
        init=protocol_NPQ,
        actinic=(orange_adj, 20 - 0.3),  # Actinic light intensity and duration
        saturating=(
            pulse_orange_adj,
            0.3,
        ),  # Saturating pulse light intensity and duration
        cycles=15,
        first_actinic_time=2,
        final_actinic_time=18,
    )

    # Create the low blue light phase with 9 pulses
    protocol_NPQ = fnc.create_protocol_PAM(
        init=protocol_NPQ,
        actinic=(low_blue_adj, 20 - 0.3),  # Actinic light intensity and duration
        saturating=(
            pulse_blue_adj,
            0.3,
        ),  # Saturating pulse light intensity and duration
        cycles=15,
        first_actinic_time=2,
        final_actinic_time=18,
    )
    return protocol_NPQ

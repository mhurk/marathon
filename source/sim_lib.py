"""Shared simulation plumbing: pace sampling, start-time construction,
finisher/distance computation, and animation-save boilerplate used across
the finisher-over-time and heatmap scripts."""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Pace distribution fit from 2017 chiptime data — see distribution_identification.md
DEFAULT_PACE_MEAN = 5.434008
DEFAULT_PACE_STD = 0.834381


def sample_paces(num_runners, mean=DEFAULT_PACE_MEAN, std=DEFAULT_PACE_STD):
    """Random pace in minutes per km, normal distribution assumed."""
    return np.random.normal(mean, std, num_runners)


def build_wave_starts(num_runners, num_waves, wave_interval, offset=0):
    """Divide runners evenly into waves, `wave_interval` minutes apart.

    Returns (start_times, wave_index), each length num_runners.
    """
    runners_per_wave = num_runners // num_waves
    wave_start_times = np.array([i * wave_interval for i in range(num_waves)]) + offset
    start_times = np.repeat(wave_start_times, runners_per_wave)
    wave_index = np.repeat(range(num_waves), runners_per_wave)
    return start_times, wave_index


def build_continuous_starts(num_runners, start_rate):
    """Spread runner start times evenly over the time needed at `start_rate` runners/minute."""
    total_start_time = num_runners / start_rate
    return np.linspace(0, total_start_time, num_runners)


def distances_for_active(pace, start_time, time_elapsed, race_distance):
    """Distance covered by runners who have already started, clipped to race_distance."""
    pace = np.asarray(pace)
    start_time = np.asarray(start_time)
    mask = start_time <= time_elapsed
    running_time = time_elapsed - start_time[mask]
    distances = running_time / pace[mask]
    return np.clip(distances, 0, race_distance)


def distances_for_all(pace, start_time, time_elapsed, race_distance):
    """Distance covered by every runner (0 for runners who haven't started yet).

    Keeps the output the same length as the input, which the heatmap scripts
    need to map each runner to a coordinate every frame.
    """
    pace = np.asarray(pace)
    start_time = np.asarray(start_time)
    running_time = np.maximum(0, time_elapsed - start_time)
    distances = running_time / pace
    return np.clip(distances, 0, race_distance)


def simulate_finishers_over_time(pace, start_time, time_steps, race_distance):
    """Cumulative finisher count at each time step, precomputed as an array."""
    pace = np.asarray(pace)
    start_time = np.asarray(start_time)
    finishers = np.empty(len(time_steps), dtype=int)
    for i, time_elapsed in enumerate(time_steps):
        distances = distances_for_active(pace, start_time, time_elapsed, race_distance)
        finishers[i] = np.sum(distances >= race_distance)
    return finishers


def save_animation(fig, update_fn, num_frames, output_basename, fps=10):
    """FuncAnimation -> ffmpeg .mp4, then re-render and save the last frame as .png."""
    ani = animation.FuncAnimation(fig, update_fn, frames=num_frames, repeat=False)
    ani.save(output_basename + '.mp4', writer='ffmpeg', fps=fps)

    update_fn(num_frames - 1)
    plt.savefig(output_basename + '_last_frame.png', dpi=300)

"""Unit tests for Scheduling Metrics Calculation."""
import unittest
from src import Process, ExecutionSegment, ProcessMetrics
from src.scheduling.fcfs import run_fcfs
from src.scheduling.sjf_preemptive import run_sjf_preemptive
from src.scheduling.metrics import calculate_metrics, calculate_average_metrics


class TestMetrics(unittest.TestCase):
    """Test cases for metrics calculation functions."""

    def test_calculate_metrics_single_process(self):
        """Single process: WT, TAT, RT calculated correctly."""
        processes = [Process("P1", 0, 5)]
        timeline = [ExecutionSegment("P1", 0, 5)]

        metrics = calculate_metrics(processes, timeline)

        self.assertEqual(len(metrics), 1)
        self.assertIsInstance(metrics[0], ProcessMetrics)
        self.assertEqual(metrics[0].pid, "P1")
        self.assertEqual(metrics[0].waiting_time, 0)
        self.assertEqual(metrics[0].turnaround_time, 5)
        self.assertEqual(metrics[0].response_time, 0)

    def test_calculate_metrics_single_process_late_arrival(self):
        """Single process with late arrival: WT=0, TAT=burst, RT=0."""
        processes = [Process("P1", 3, 4)]
        timeline = [
            ExecutionSegment("IDLE", 0, 3),
            ExecutionSegment("P1", 3, 7),
        ]

        metrics = calculate_metrics(processes, timeline)

        self.assertEqual(metrics[0].waiting_time, 0)
        self.assertEqual(metrics[0].turnaround_time, 4)
        self.assertEqual(metrics[0].response_time, 0)

    def test_calculate_metrics_multiple_fcfs(self):
        """Multiple processes with FCFS scheduling."""
        processes = [
            Process("P1", 0, 5),
            Process("P2", 1, 3),
            Process("P3", 2, 4),
        ]
        timeline = run_fcfs(processes)
        metrics = calculate_metrics(processes, timeline)

        self.assertEqual(metrics[0].pid, "P1")
        self.assertEqual(metrics[0].waiting_time, 0)
        self.assertEqual(metrics[0].turnaround_time, 5)
        self.assertEqual(metrics[0].response_time, 0)

        self.assertEqual(metrics[1].pid, "P2")
        self.assertEqual(metrics[1].waiting_time, 4)
        self.assertEqual(metrics[1].turnaround_time, 7)
        self.assertEqual(metrics[1].response_time, 4)

        self.assertEqual(metrics[2].pid, "P3")
        self.assertEqual(metrics[2].waiting_time, 6)
        self.assertEqual(metrics[2].turnaround_time, 10)
        self.assertEqual(metrics[2].response_time, 6)

    def test_calculate_metrics_sjf_preemptive(self):
        """Multiple processes with SJF preemptive scheduling."""
        processes = [
            Process("P1", 0, 10),
            Process("P2", 2, 3),
        ]
        timeline = run_sjf_preemptive(processes)
        metrics = calculate_metrics(processes, timeline)

        self.assertEqual(metrics[0].pid, "P1")
        self.assertEqual(metrics[0].turnaround_time, 13)
        self.assertEqual(metrics[0].waiting_time, 3)
        self.assertEqual(metrics[0].response_time, 0)

        self.assertEqual(metrics[1].pid, "P2")
        self.assertEqual(metrics[1].turnaround_time, 3)
        self.assertEqual(metrics[1].waiting_time, 0)
        self.assertEqual(metrics[1].response_time, 0)

    def test_waiting_time_formula(self):
        """Verify WT = TAT - burst_time."""
        processes = [
            Process("P1", 0, 10),
            Process("P2", 2, 3),
        ]
        timeline = run_sjf_preemptive(processes)
        metrics = calculate_metrics(processes, timeline)

        for m, proc in zip(metrics, processes):
            self.assertEqual(m.waiting_time, m.turnaround_time - proc.burst_time)

    def test_turnaround_time_formula(self):
        """Verify TAT = completion_time - arrival_time."""
        processes = [
            Process("P1", 0, 10),
            Process("P2", 2, 3),
        ]
        timeline = run_sjf_preemptive(processes)
        metrics = calculate_metrics(processes, timeline)

        for m, proc in zip(metrics, processes):
            completion = max(s.end_time for s in timeline if s.pid == m.pid)
            self.assertEqual(m.turnaround_time, completion - proc.arrival_time)

    def test_response_time_formula(self):
        """Verify RT = first_start_time - arrival_time."""
        processes = [
            Process("P1", 0, 10),
            Process("P2", 2, 3),
        ]
        timeline = run_sjf_preemptive(processes)
        metrics = calculate_metrics(processes, timeline)

        for m, proc in zip(metrics, processes):
            first_start = min(s.start_time for s in timeline if s.pid == m.pid)
            self.assertEqual(m.response_time, first_start - proc.arrival_time)

    def test_completion_time_from_timeline_multi_segment(self):
        """Completion time from max end_time for preempted process."""
        processes = [
            Process("P1", 0, 8),
            Process("P2", 1, 4),
            Process("P3", 2, 2),
        ]
        timeline = run_sjf_preemptive(processes)
        metrics = calculate_metrics(processes, timeline)

        m = metrics[0]
        p1_segments = [s for s in timeline if s.pid == "P1"]
        completion = max(s.end_time for s in p1_segments)
        self.assertEqual(m.turnaround_time, completion - 0)

    def test_first_start_time_from_timeline_multi_segment(self):
        """First start time from min start_time for preempted process."""
        processes = [
            Process("P1", 0, 8),
            Process("P2", 1, 4),
        ]
        timeline = run_sjf_preemptive(processes)
        metrics = calculate_metrics(processes, timeline)

        m = metrics[0]
        p1_segments = [s for s in timeline if s.pid == "P1"]
        first_start = min(s.start_time for s in p1_segments)
        self.assertEqual(m.response_time, first_start - 0)

    def test_idle_segments_ignored_in_metrics(self):
        """IDLE segments do not affect process metrics."""
        processes = [Process("P1", 5, 3)]
        timeline = [
            ExecutionSegment("IDLE", 0, 5),
            ExecutionSegment("P1", 5, 8),
        ]

        metrics = calculate_metrics(processes, timeline)

        self.assertEqual(metrics[0].waiting_time, 0)
        self.assertEqual(metrics[0].turnaround_time, 3)
        self.assertEqual(metrics[0].response_time, 0)

    def test_calculate_average_metrics(self):
        """Average metrics computed correctly."""
        metrics = [
            ProcessMetrics("P1", 0, 5, 0),
            ProcessMetrics("P2", 4, 7, 4),
            ProcessMetrics("P3", 6, 10, 6),
        ]
        avg = calculate_average_metrics(metrics)

        self.assertAlmostEqual(avg["avg_waiting_time"], 10 / 3)
        self.assertAlmostEqual(avg["avg_turnaround_time"], 22 / 3)
        self.assertAlmostEqual(avg["avg_response_time"], 10 / 3)

    def test_empty_processes_raises_value_error(self):
        """Empty processes list raises ValueError."""
        with self.assertRaises(ValueError):
            calculate_metrics([], [])

    def test_empty_timeline_raises_value_error(self):
        """Empty timeline raises ValueError."""
        processes = [Process("P1", 0, 5)]
        with self.assertRaises(ValueError):
            calculate_metrics(processes, [])

    def test_missing_process_in_timeline_raises_value_error(self):
        """Process in list but not in timeline raises ValueError."""
        processes = [Process("P1", 0, 5), Process("P2", 0, 3)]
        timeline = [ExecutionSegment("P1", 0, 5)]

        with self.assertRaises(ValueError):
            calculate_metrics(processes, timeline)

    def test_empty_metrics_raises_value_error(self):
        """Empty metrics list raises ValueError in calculate_average_metrics."""
        with self.assertRaises(ValueError):
            calculate_average_metrics([])


if __name__ == "__main__":
    unittest.main()

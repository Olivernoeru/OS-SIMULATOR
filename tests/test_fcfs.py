"""Unit tests for FCFS CPU Scheduling Algorithm."""
import unittest
from src import Process, ExecutionSegment
from src.scheduling.fcfs import run_fcfs, _merge_segments


class TestFCFS(unittest.TestCase):
    """Test cases for FCFS scheduling algorithm."""

    def test_single_process_arrival_zero(self):
        """Single process with arrival_time=0 runs immediately."""
        processes = [Process("P1", 0, 5)]
        timeline = run_fcfs(processes)

        self.assertEqual(len(timeline), 1)
        self.assertEqual(timeline[0].pid, "P1")
        self.assertEqual(timeline[0].start_time, 0)
        self.assertEqual(timeline[0].end_time, 5)

    def test_single_process_late_arrival(self):
        """Single process with arrival_time > 0 has IDLE before it."""
        processes = [Process("P1", 5, 3)]
        timeline = run_fcfs(processes)

        self.assertEqual(len(timeline), 2)
        self.assertEqual(timeline[0].pid, "IDLE")
        self.assertEqual(timeline[0].start_time, 0)
        self.assertEqual(timeline[0].end_time, 5)
        self.assertEqual(timeline[1].pid, "P1")
        self.assertEqual(timeline[1].start_time, 5)
        self.assertEqual(timeline[1].end_time, 8)

    def test_multiple_processes_sequential_no_gaps(self):
        """Multiple processes arriving sequentially with no gaps."""
        processes = [
            Process("P1", 0, 5),
            Process("P2", 1, 3),
            Process("P3", 2, 4),
        ]
        timeline = run_fcfs(processes)

        self.assertEqual(len(timeline), 3)
        self.assertEqual(timeline[0].pid, "P1")
        self.assertEqual(timeline[0].start_time, 0)
        self.assertEqual(timeline[0].end_time, 5)
        self.assertEqual(timeline[1].pid, "P2")
        self.assertEqual(timeline[1].start_time, 5)
        self.assertEqual(timeline[1].end_time, 8)
        self.assertEqual(timeline[2].pid, "P3")
        self.assertEqual(timeline[2].start_time, 8)
        self.assertEqual(timeline[2].end_time, 12)

    def test_multiple_processes_with_gaps(self):
        """Processes with gaps between arrivals produce IDLE segments."""
        processes = [
            Process("P1", 0, 3),
            Process("P2", 10, 2),
        ]
        timeline = run_fcfs(processes)

        self.assertEqual(len(timeline), 3)
        self.assertEqual(timeline[0].pid, "P1")
        self.assertEqual(timeline[0].start_time, 0)
        self.assertEqual(timeline[0].end_time, 3)
        self.assertEqual(timeline[1].pid, "IDLE")
        self.assertEqual(timeline[1].start_time, 3)
        self.assertEqual(timeline[1].end_time, 10)
        self.assertEqual(timeline[2].pid, "P2")
        self.assertEqual(timeline[2].start_time, 10)
        self.assertEqual(timeline[2].end_time, 12)

    def test_same_arrival_time_preserves_input_order(self):
        """Processes with same arrival_time follow input order (stable sort)."""
        processes = [
            Process("P1", 0, 5),
            Process("P2", 0, 3),
            Process("P3", 0, 2),
        ]
        timeline = run_fcfs(processes)

        self.assertEqual(len(timeline), 3)
        self.assertEqual(timeline[0].pid, "P1")
        self.assertEqual(timeline[0].start_time, 0)
        self.assertEqual(timeline[0].end_time, 5)
        self.assertEqual(timeline[1].pid, "P2")
        self.assertEqual(timeline[1].start_time, 5)
        self.assertEqual(timeline[1].end_time, 8)
        self.assertEqual(timeline[2].pid, "P3")
        self.assertEqual(timeline[2].start_time, 8)
        self.assertEqual(timeline[2].end_time, 10)

    def test_non_preemptive_runs_to_completion(self):
        """Process runs to completion without preemption."""
        processes = [
            Process("P1", 0, 10),
            Process("P2", 1, 1),
        ]
        timeline = run_fcfs(processes)

        self.assertEqual(len(timeline), 2)
        self.assertEqual(timeline[0].pid, "P1")
        self.assertEqual(timeline[0].end_time, 10)
        self.assertEqual(timeline[1].pid, "P2")
        self.assertEqual(timeline[1].start_time, 10)
        self.assertEqual(timeline[1].end_time, 11)

    def test_merge_adjacent_same_pid_segments(self):
        """Adjacent segments with same PID are merged."""
        segments = [
            ExecutionSegment("P1", 0, 3),
            ExecutionSegment("P1", 3, 5),
            ExecutionSegment("P2", 5, 8),
        ]
        merged = _merge_segments(segments)

        self.assertEqual(len(merged), 2)
        self.assertEqual(merged[0].pid, "P1")
        self.assertEqual(merged[0].start_time, 0)
        self.assertEqual(merged[0].end_time, 5)
        self.assertEqual(merged[1].pid, "P2")

    def test_merge_non_adjacent_same_pid_not_merged(self):
        """Non-adjacent segments with same PID are not merged."""
        segments = [
            ExecutionSegment("P1", 0, 3),
            ExecutionSegment("P2", 3, 5),
            ExecutionSegment("P1", 5, 8),
        ]
        merged = _merge_segments(segments)

        self.assertEqual(len(merged), 3)

    def test_empty_processes_returns_empty_timeline(self):
        """Empty process list returns empty timeline."""
        timeline = run_fcfs([])
        self.assertEqual(timeline, [])

    def test_timeline_time_bounds_valid(self):
        """All segments have valid time bounds."""
        processes = [
            Process("P1", 0, 5),
            Process("P2", 10, 3),
        ]
        timeline = run_fcfs(processes)

        for seg in timeline:
            self.assertGreaterEqual(seg.start_time, 0)
            self.assertGreater(seg.end_time, seg.start_time)

    def test_complex_scenario_with_idle_and_multiple_processes(self):
        """Complex scenario: gaps, multiple processes, correct ordering."""
        processes = [
            Process("P1", 0, 4),
            Process("P2", 2, 3),
            Process("P3", 10, 2),
            Process("P4", 10, 1),
        ]
        timeline = run_fcfs(processes)

        self.assertEqual(len(timeline), 5)
        self.assertEqual(timeline[0].pid, "P1")
        self.assertEqual(timeline[0].end_time, 4)
        self.assertEqual(timeline[1].pid, "P2")
        self.assertEqual(timeline[1].start_time, 4)
        self.assertEqual(timeline[1].end_time, 7)
        self.assertEqual(timeline[2].pid, "IDLE")
        self.assertEqual(timeline[2].start_time, 7)
        self.assertEqual(timeline[2].end_time, 10)
        self.assertEqual(timeline[3].pid, "P3")
        self.assertEqual(timeline[3].start_time, 10)
        self.assertEqual(timeline[3].end_time, 12)
        self.assertEqual(timeline[4].pid, "P4")
        self.assertEqual(timeline[4].start_time, 12)
        self.assertEqual(timeline[4].end_time, 13)


if __name__ == "__main__":
    unittest.main()

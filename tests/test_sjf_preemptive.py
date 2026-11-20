"""Unit tests for SJF Preemptive CPU Scheduling Algorithm."""
import unittest
from src import Process, ExecutionSegment
from src.scheduling.sjf_preemptive import run_sjf_preemptive, _merge_segments


class TestSJFPreemptive(unittest.TestCase):
    """Test cases for SJF Preemptive scheduling algorithm."""

    def test_single_process(self):
        """Single process runs to completion."""
        processes = [Process("P1", 0, 5)]
        timeline = run_sjf_preemptive(processes)

        self.assertEqual(len(timeline), 1)
        self.assertEqual(timeline[0].pid, "P1")
        self.assertEqual(timeline[0].start_time, 0)
        self.assertEqual(timeline[0].end_time, 5)

    def test_single_process_late_arrival(self):
        """Single process with late arrival has IDLE before it."""
        processes = [Process("P1", 3, 4)]
        timeline = run_sjf_preemptive(processes)

        self.assertEqual(len(timeline), 2)
        self.assertEqual(timeline[0].pid, "IDLE")
        self.assertEqual(timeline[0].start_time, 0)
        self.assertEqual(timeline[0].end_time, 3)
        self.assertEqual(timeline[1].pid, "P1")
        self.assertEqual(timeline[1].start_time, 3)
        self.assertEqual(timeline[1].end_time, 7)

    def test_no_preemption_when_shortest_first(self):
        """No preemption when shortest job arrives first."""
        processes = [
            Process("P1", 0, 3),
            Process("P2", 1, 5),
        ]
        timeline = run_sjf_preemptive(processes)

        self.assertEqual(len(timeline), 2)
        self.assertEqual(timeline[0].pid, "P1")
        self.assertEqual(timeline[0].end_time, 3)
        self.assertEqual(timeline[1].pid, "P2")
        self.assertEqual(timeline[1].start_time, 3)
        self.assertEqual(timeline[1].end_time, 8)

    def test_preemption_on_shorter_arrival(self):
        """Preemption occurs when shorter job arrives."""
        processes = [
            Process("P1", 0, 10),
            Process("P2", 2, 3),
        ]
        timeline = run_sjf_preemptive(processes)

        p1_segments = [s for s in timeline if s.pid == "P1"]
        p2_segments = [s for s in timeline if s.pid == "P2"]

        self.assertEqual(len(p1_segments), 2)
        self.assertEqual(p1_segments[0].start_time, 0)
        self.assertEqual(p1_segments[0].end_time, 2)
        self.assertEqual(p1_segments[1].start_time, 5)
        self.assertEqual(p1_segments[1].end_time, 13)

        self.assertEqual(len(p2_segments), 1)
        self.assertEqual(p2_segments[0].start_time, 2)
        self.assertEqual(p2_segments[0].end_time, 5)

    def test_multiple_preemptions(self):
        """Multiple preemptions with remaining time calculation."""
        processes = [
            Process("P1", 0, 8),
            Process("P2", 1, 4),
            Process("P3", 2, 2),
        ]
        timeline = run_sjf_preemptive(processes)

        p1_segments = [s for s in timeline if s.pid == "P1"]
        p2_segments = [s for s in timeline if s.pid == "P2"]
        p3_segments = [s for s in timeline if s.pid == "P3"]

        self.assertEqual(len(p1_segments), 2)
        self.assertEqual(p1_segments[0].start_time, 0)
        self.assertEqual(p1_segments[0].end_time, 1)
        self.assertEqual(p1_segments[1].start_time, 7)
        self.assertEqual(p1_segments[1].end_time, 14)

        self.assertEqual(len(p2_segments), 2)
        self.assertEqual(p2_segments[0].start_time, 1)
        self.assertEqual(p2_segments[0].end_time, 2)
        self.assertEqual(p2_segments[1].start_time, 4)
        self.assertEqual(p2_segments[1].end_time, 7)

        self.assertEqual(len(p3_segments), 1)
        self.assertEqual(p3_segments[0].start_time, 2)
        self.assertEqual(p3_segments[0].end_time, 4)

    def test_tie_remaining_time_earlier_arrival_wins(self):
        """Tie on remaining_time: earlier arrival_time wins."""
        processes = [
            Process("P1", 0, 5),
            Process("P2", 2, 5),
        ]
        timeline = run_sjf_preemptive(processes)

        p1_segments = [s for s in timeline if s.pid == "P1"]
        self.assertEqual(len(p1_segments), 1)
        self.assertEqual(p1_segments[0].end_time, 5)

    def test_tie_remaining_and_arrival_input_order_wins(self):
        """Tie on remaining_time and arrival_time: input order wins."""
        processes = [
            Process("P1", 0, 5),
            Process("P2", 0, 5),
        ]
        timeline = run_sjf_preemptive(processes)

        p1_segments = [s for s in timeline if s.pid == "P1"]
        p2_segments = [s for s in timeline if s.pid == "P2"]

        self.assertEqual(len(p1_segments), 1)
        self.assertEqual(p1_segments[0].end_time, 5)
        self.assertEqual(len(p2_segments), 1)
        self.assertEqual(p2_segments[0].start_time, 5)
        self.assertEqual(p2_segments[0].end_time, 10)

    def test_idle_when_no_ready_processes(self):
        """IDLE segment when no ready processes at start."""
        processes = [Process("P1", 5, 3)]
        timeline = run_sjf_preemptive(processes)

        self.assertEqual(timeline[0].pid, "IDLE")
        self.assertEqual(timeline[0].start_time, 0)
        self.assertEqual(timeline[0].end_time, 5)

    def test_idle_between_completion_and_next_arrival(self):
        """IDLE segment when all complete and next hasn't arrived."""
        processes = [
            Process("P1", 0, 3),
            Process("P2", 10, 2),
        ]
        timeline = run_sjf_preemptive(processes)

        idle_segments = [s for s in timeline if s.pid == "IDLE"]
        self.assertEqual(len(idle_segments), 1)
        self.assertEqual(idle_segments[0].start_time, 3)
        self.assertEqual(idle_segments[0].end_time, 10)

    def test_merge_adjacent_same_pid_segments(self):
        """Adjacent segments with same PID are merged."""
        segments = [
            ExecutionSegment("P1", 0, 2),
            ExecutionSegment("P1", 2, 5),
            ExecutionSegment("P2", 5, 7),
        ]
        merged = _merge_segments(segments)

        self.assertEqual(len(merged), 2)
        self.assertEqual(merged[0].pid, "P1")
        self.assertEqual(merged[0].start_time, 0)
        self.assertEqual(merged[0].end_time, 5)
        self.assertEqual(merged[1].pid, "P2")

    def test_completion_time_from_last_segment(self):
        """Completion time is end_time of last segment for a process."""
        processes = [
            Process("P1", 0, 10),
            Process("P2", 2, 3),
        ]
        timeline = run_sjf_preemptive(processes)

        p1_segments = [s for s in timeline if s.pid == "P1"]
        completion_time = max(s.end_time for s in p1_segments)
        self.assertEqual(completion_time, 13)

    def test_first_start_time_from_first_segment(self):
        """First start time is start_time of first segment for a process."""
        processes = [
            Process("P1", 0, 10),
            Process("P2", 2, 3),
        ]
        timeline = run_sjf_preemptive(processes)

        p1_segments = [s for s in timeline if s.pid == "P1"]
        first_start = min(s.start_time for s in p1_segments)
        self.assertEqual(first_start, 0)

    def test_empty_processes_returns_empty_timeline(self):
        """Empty process list returns empty timeline."""
        timeline = run_sjf_preemptive([])
        self.assertEqual(timeline, [])

    def test_complex_preemption_scenario(self):
        """Complex scenario with multiple preemptions and IDLE."""
        processes = [
            Process("P1", 0, 6),
            Process("P2", 1, 4),
            Process("P3", 3, 2),
            Process("P4", 15, 3),
        ]
        timeline = run_sjf_preemptive(processes)

        pids = set(s.pid for s in timeline if s.pid != "IDLE")
        self.assertEqual(pids, {"P1", "P2", "P3", "P4"})

        self.assertEqual(timeline[-1].end_time, 18)


if __name__ == "__main__":
    unittest.main()

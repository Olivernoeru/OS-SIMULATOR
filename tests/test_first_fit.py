"""Unit tests for First-Fit Memory Allocator."""
import unittest
from src import MemoryRequest
from src.memory.first_fit import FirstFitAllocator


class TestFirstFitAllocator(unittest.TestCase):
    """Test cases for First-Fit memory allocation algorithm."""

    def test_init_positive_capacity(self):
        """Valid positive capacity initializes correctly."""
        allocator = FirstFitAllocator(100)
        blocks = allocator.get_blocks()

        self.assertEqual(len(blocks), 1)
        self.assertEqual(blocks[0].start_address, 0)
        self.assertEqual(blocks[0].size, 100)
        self.assertIsNone(blocks[0].process_id)

    def test_init_zero_capacity_raises(self):
        """Zero capacity raises ValueError."""
        with self.assertRaises(ValueError):
            FirstFitAllocator(0)

    def test_init_negative_capacity_raises(self):
        """Negative capacity raises ValueError."""
        with self.assertRaises(ValueError):
            FirstFitAllocator(-10)

    def test_init_float_capacity_raises(self):
        """Float capacity raises ValueError."""
        with self.assertRaises(ValueError):
            FirstFitAllocator(100.5)

    def test_init_bool_capacity_raises(self):
        """Boolean capacity raises ValueError."""
        with self.assertRaises(ValueError):
            FirstFitAllocator(True)

    def test_allocate_first_fit_lowest_address(self):
        """First-Fit selects lowest address block that fits."""
        allocator = FirstFitAllocator(100)
        allocator.allocate(MemoryRequest("P1", 30))
        allocator.release("P1")
        result = allocator.allocate(MemoryRequest("P2", 20))
        blocks = allocator.get_blocks()

        self.assertTrue(result)
        self.assertEqual(blocks[0].start_address, 0)
        self.assertEqual(blocks[0].size, 20)
        self.assertEqual(blocks[0].process_id, "P2")

    def test_allocate_exact_fit(self):
        """Exact fit replaces the free block entirely."""
        allocator = FirstFitAllocator(50)
        result = allocator.allocate(MemoryRequest("P1", 50))
        blocks = allocator.get_blocks()

        self.assertTrue(result)
        self.assertEqual(len(blocks), 1)
        self.assertEqual(blocks[0].start_address, 0)
        self.assertEqual(blocks[0].size, 50)
        self.assertEqual(blocks[0].process_id, "P1")

    def test_allocate_split_block(self):
        """Block larger than request splits into allocated + remaining free."""
        allocator = FirstFitAllocator(100)
        result = allocator.allocate(MemoryRequest("P1", 30))
        blocks = allocator.get_blocks()

        self.assertTrue(result)
        self.assertEqual(len(blocks), 2)
        self.assertEqual(blocks[0].start_address, 0)
        self.assertEqual(blocks[0].size, 30)
        self.assertEqual(blocks[0].process_id, "P1")
        self.assertEqual(blocks[1].start_address, 30)
        self.assertEqual(blocks[1].size, 70)
        self.assertIsNone(blocks[1].process_id)

    def test_allocate_insufficient_space_returns_false(self):
        """Insufficient space returns False, state unchanged."""
        allocator = FirstFitAllocator(50)
        allocator.allocate(MemoryRequest("P1", 30))
        result = allocator.allocate(MemoryRequest("P2", 30))

        self.assertFalse(result)
        blocks = allocator.get_blocks()
        self.assertEqual(len(blocks), 2)
        self.assertEqual(blocks[0].process_id, "P1")
        self.assertIsNone(blocks[1].process_id)

    def test_allocate_duplicate_pid_returns_false(self):
        """Duplicate active PID returns False, state unchanged."""
        allocator = FirstFitAllocator(100)
        allocator.allocate(MemoryRequest("P1", 30))
        blocks_before = allocator.get_blocks()
        result = allocator.allocate(MemoryRequest("P1", 20))

        self.assertFalse(result)
        blocks_after = allocator.get_blocks()
        self.assertEqual(len(blocks_before), len(blocks_after))
        for b1, b2 in zip(blocks_before, blocks_after):
            self.assertEqual(b1.start_address, b2.start_address)
            self.assertEqual(b1.size, b2.size)
            self.assertEqual(b1.process_id, b2.process_id)

    def test_allocate_released_pid_allowed(self):
        """Released PID can be reallocated."""
        allocator = FirstFitAllocator(100)
        allocator.allocate(MemoryRequest("P1", 30))
        allocator.release("P1")
        result = allocator.allocate(MemoryRequest("P1", 20))

        self.assertTrue(result)
        blocks = allocator.get_blocks()
        p1_blocks = [b for b in blocks if b.process_id == "P1"]
        self.assertEqual(len(p1_blocks), 1)
        self.assertEqual(p1_blocks[0].size, 20)

    def test_allocate_invalid_size_raises(self):
        """Invalid size (<=0) raises ValueError."""
        allocator = FirstFitAllocator(100)
        with self.assertRaises(ValueError):
            allocator.allocate(MemoryRequest("P1", 0))
        with self.assertRaises(ValueError):
            allocator.allocate(MemoryRequest("P1", -5))

    def test_release_existing_pid_returns_true(self):
        """Releasing existing PID returns True, block becomes free."""
        allocator = FirstFitAllocator(100)
        allocator.allocate(MemoryRequest("P1", 30))
        result = allocator.release("P1")

        self.assertTrue(result)
        blocks = allocator.get_blocks()
        self.assertEqual(len(blocks), 1)
        self.assertIsNone(blocks[0].process_id)
        self.assertEqual(blocks[0].size, 100)

    def test_release_nonexistent_pid_returns_false(self):
        """Releasing non-existent PID returns False."""
        allocator = FirstFitAllocator(100)
        result = allocator.release("P999")

        self.assertFalse(result)
        blocks = allocator.get_blocks()
        self.assertEqual(len(blocks), 1)
        self.assertIsNone(blocks[0].process_id)
        self.assertEqual(blocks[0].size, 100)

    def test_coalesce_adjacent_free_blocks(self):
        """Adjacent free blocks are coalesced."""
        allocator = FirstFitAllocator(100)
        allocator.allocate(MemoryRequest("P1", 20))
        allocator.allocate(MemoryRequest("P2", 30))
        allocator.allocate(MemoryRequest("P3", 10))
        allocator.release("P1")
        allocator.release("P2")
        blocks = allocator.get_blocks()

        free_blocks = [b for b in blocks if b.process_id is None]
        # P1 (0-20) + P2 (20-50) coalesce to 0-50
        # P3 at 50-60, remaining free at 60-100
        self.assertEqual(len(free_blocks), 2)
        # First free block is coalesced P1+P2
        self.assertEqual(free_blocks[0].start_address, 0)
        self.assertEqual(free_blocks[0].size, 50)
        # Second free block is after P3
        self.assertEqual(free_blocks[1].start_address, 60)
        self.assertEqual(free_blocks[1].size, 40)

    def test_coalesce_non_adjacent_not_merged(self):
        """Non-adjacent free blocks are not merged."""
        allocator = FirstFitAllocator(100)
        allocator.allocate(MemoryRequest("P1", 20))
        allocator.allocate(MemoryRequest("P2", 30))
        allocator.allocate(MemoryRequest("P3", 10))
        allocator.release("P1")
        allocator.release("P3")
        blocks = allocator.get_blocks()

        free_blocks = [b for b in blocks if b.process_id is None]
        self.assertEqual(len(free_blocks), 2)

    def test_coalesce_after_release(self):
        """Coalescing happens automatically after release."""
        allocator = FirstFitAllocator(100)
        allocator.allocate(MemoryRequest("P1", 30))
        allocator.allocate(MemoryRequest("P2", 20))
        allocator.release("P1")
        allocator.release("P2")
        blocks = allocator.get_blocks()

        self.assertEqual(len(blocks), 1)
        self.assertIsNone(blocks[0].process_id)
        self.assertEqual(blocks[0].size, 100)

    def test_get_blocks_returns_deep_copy(self):
        """get_blocks returns deep copy - modifications don't affect internal state."""
        allocator = FirstFitAllocator(100)
        allocator.allocate(MemoryRequest("P1", 30))
        blocks = allocator.get_blocks()

        blocks[0].process_id = "MODIFIED"
        blocks[0].size = 999

        blocks2 = allocator.get_blocks()
        self.assertEqual(blocks2[0].process_id, "P1")
        self.assertEqual(blocks2[0].size, 30)

    def test_get_blocks_new_objects_each_call(self):
        """Each get_blocks call returns new MemoryBlock objects."""
        allocator = FirstFitAllocator(100)
        blocks1 = allocator.get_blocks()
        blocks2 = allocator.get_blocks()

        self.assertIsNot(blocks1[0], blocks2[0])

    def test_blocks_ordered_by_start_address(self):
        """Blocks are always ordered by start_address."""
        allocator = FirstFitAllocator(100)
        allocator.allocate(MemoryRequest("P1", 20))
        allocator.allocate(MemoryRequest("P2", 30))
        allocator.release("P1")
        blocks = allocator.get_blocks()

        for i in range(len(blocks) - 1):
            self.assertLessEqual(blocks[i].start_address, blocks[i + 1].start_address)

    def test_multiple_allocate_release_sequence(self):
        """Complex sequence of allocations and releases."""
        allocator = FirstFitAllocator(100)
        self.assertTrue(allocator.allocate(MemoryRequest("P1", 20)))
        self.assertTrue(allocator.allocate(MemoryRequest("P2", 30)))
        self.assertTrue(allocator.release("P1"))
        self.assertTrue(allocator.allocate(MemoryRequest("P3", 15)))
        self.assertTrue(allocator.allocate(MemoryRequest("P4", 10)))
        blocks = allocator.get_blocks()

        p1_blocks = [b for b in blocks if b.process_id == "P1"]
        p2_blocks = [b for b in blocks if b.process_id == "P2"]
        p3_blocks = [b for b in blocks if b.process_id == "P3"]
        p4_blocks = [b for b in blocks if b.process_id == "P4"]

        self.assertEqual(len(p1_blocks), 0)
        self.assertEqual(len(p2_blocks), 1)
        self.assertEqual(len(p3_blocks), 1)
        self.assertEqual(len(p4_blocks), 1)
        self.assertEqual(p3_blocks[0].start_address, 0)
        self.assertEqual(p3_blocks[0].size, 15)
        self.assertEqual(p4_blocks[0].start_address, 50)
        self.assertEqual(p4_blocks[0].size, 10)

    def test_allocate_multiple_processes(self):
        """Multiple sequential allocations work correctly."""
        allocator = FirstFitAllocator(100)
        self.assertTrue(allocator.allocate(MemoryRequest("P1", 20)))
        self.assertTrue(allocator.allocate(MemoryRequest("P2", 30)))
        self.assertTrue(allocator.allocate(MemoryRequest("P3", 15)))

        blocks = allocator.get_blocks()
        allocated = [b for b in blocks if b.process_id is not None]
        free = [b for b in blocks if b.process_id is None]

        self.assertEqual(len(allocated), 3)
        self.assertEqual(len(free), 1)
        self.assertEqual(free[0].start_address, 65)
        self.assertEqual(free[0].size, 35)


if __name__ == "__main__":
    unittest.main()

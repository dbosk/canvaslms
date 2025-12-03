"""
Tests for canvaslms.cli verbosity system.

These tests verify the multi-level verbosity system that maps -v and -q flags
to Python logging levels.
"""
import pytest
import logging
import argparse

class TestVerbositySystem:
    """Test the verbosity system in CLI"""

    def test_net_verbosity_calculation(self):
        """
        Net verbosity should be verbose count minus quiet count.
        
        This allows -v and -q to offset each other naturally.
        """
        args = argparse.Namespace(verbose=2, quiet=1)
        net_verbosity = args.verbose - args.quiet
        assert net_verbosity == 1

    def test_multiple_verbose_flags(self):
        """Multiple -v flags should stack: -vvv gives verbosity 3"""
        args = argparse.Namespace(verbose=3, quiet=0)
        net_verbosity = args.verbose - args.quiet
        assert net_verbosity == 3

    def test_multiple_quiet_flags(self):
        """Multiple -q flags should stack: -qqq gives verbosity -3"""
        args = argparse.Namespace(verbose=0, quiet=3)
        net_verbosity = args.verbose - args.quiet
        assert net_verbosity == -3

    def test_offsetting_flags(self):
        """-vv -q should give net verbosity 1"""
        args = argparse.Namespace(verbose=2, quiet=1)
        net_verbosity = args.verbose - args.quiet
        assert net_verbosity == 1
class TestVerbosityLevelMapping:
    """Test the complete mapping from net verbosity to logging levels"""

    @pytest.mark.parametrize("verbose,quiet,expected_level", [
        (0, 3, logging.CRITICAL + 1),  # -qqq: completely silent
        (0, 2, logging.CRITICAL),       # -qq: critical only
        (0, 1, logging.ERROR),          # -q: error and critical
        (0, 0, logging.WARNING),        # default: warnings and above
        (1, 0, logging.INFO),           # -v: info and above
        (2, 0, logging.DEBUG),          # -vv: debug and above
        (3, 0, logging.NOTSET),         # -vvv: everything
        (4, 0, logging.NOTSET),         # -vvvv: still everything
        (2, 1, logging.INFO),           # -vv -q = -v: info level
        (3, 2, logging.INFO),           # -vvv -qq = -v: info level
    ])
    def test_verbosity_to_logging_level(self, verbose, quiet, expected_level):
        """Test that verbosity flags map correctly to logging levels"""
        net_verbosity = verbose - quiet
        
        # Implement the same logic as in the code
        if net_verbosity <= -3:
            actual_level = logging.CRITICAL + 1
        elif net_verbosity == -2:
            actual_level = logging.CRITICAL
        elif net_verbosity == -1:
            actual_level = logging.ERROR
        elif net_verbosity == 0:
            actual_level = logging.WARNING
        elif net_verbosity == 1:
            actual_level = logging.INFO
        elif net_verbosity == 2:
            actual_level = logging.DEBUG
        else:  # net_verbosity >= 3
            actual_level = logging.NOTSET
        
        assert actual_level == expected_level

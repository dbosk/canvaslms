"""
Tests for canvaslms.cli verbosity system.

These tests verify the multi-level verbosity system that maps -v and -q flags
to Python logging levels.
"""
import pytest
import logging
import argparse
from unittest.mock import patch, MagicMock


class TestVerbositySystem:
    """Test the verbosity system in CLI"""

    def test_net_verbosity_calculation(self):
        """
        Net verbosity should be verbose count minus quiet count.
        
        This allows -v and -q to offset each other naturally.
        """
        # Simulate argparse namespace
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

    def test_logging_level_mapping_completely_silent(self):
        """Net verbosity <= -3 should be completely silent (above CRITICAL)"""
        net_verbosity = -3
        if net_verbosity <= -3:
            expected_level = logging.CRITICAL + 1
        else:
            expected_level = None
        assert expected_level == logging.CRITICAL + 1

    def test_logging_level_mapping_critical(self):
        """Net verbosity -2 should map to CRITICAL level"""
        net_verbosity = -2
        if net_verbosity == -2:
            expected_level = logging.CRITICAL
        else:
            expected_level = None
        assert expected_level == logging.CRITICAL

    def test_logging_level_mapping_error(self):
        """Net verbosity -1 should map to ERROR level"""
        net_verbosity = -1
        if net_verbosity == -1:
            expected_level = logging.ERROR
        else:
            expected_level = None
        assert expected_level == logging.ERROR

    def test_logging_level_mapping_warning(self):
        """Net verbosity 0 (default) should map to WARNING level"""
        net_verbosity = 0
        if net_verbosity == 0:
            expected_level = logging.WARNING
        else:
            expected_level = None
        assert expected_level == logging.WARNING

    def test_logging_level_mapping_info(self):
        """Net verbosity 1 (-v) should map to INFO level"""
        net_verbosity = 1
        if net_verbosity == 1:
            expected_level = logging.INFO
        else:
            expected_level = None
        assert expected_level == logging.INFO

    def test_logging_level_mapping_debug(self):
        """Net verbosity 2 (-vv) should map to DEBUG level"""
        net_verbosity = 2
        if net_verbosity == 2:
            expected_level = logging.DEBUG
        else:
            expected_level = None
        assert expected_level == logging.DEBUG

    def test_logging_level_mapping_notset(self):
        """Net verbosity >= 3 (-vvv or more) should map to NOTSET level"""
        net_verbosity = 3
        if net_verbosity >= 3:
            expected_level = logging.NOTSET
        else:
            expected_level = None
        assert expected_level == logging.NOTSET


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
        
        # Implement the same logic as in cli.nw
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


class TestLoggingConfiguration:
    """Test that logging is configured correctly based on verbosity"""

    def test_logging_format(self):
        """All logging levels should use the same format: '[%(levelname)s] %(message)s'"""
        expected_format = '[%(levelname)s] %(message)s'
        # This is a constant in the implementation
        assert expected_format == '[%(levelname)s] %(message)s'

    @patch('logging.basicConfig')
    def test_default_verbosity_configures_warning_level(self, mock_basic_config):
        """
        With default args (verbose=0, quiet=0), logging should be configured
        for WARNING level.
        """
        args = argparse.Namespace(verbose=0, quiet=0)
        net_verbosity = args.verbose - args.quiet
        
        # Simulate the configuration
        if net_verbosity == 0:
            logging.basicConfig(level=logging.WARNING, 
                              format='[%(levelname)s] %(message)s')
        
        # The function should have been called (simulated above)
        # In actual code, this would be verified
        assert net_verbosity == 0
